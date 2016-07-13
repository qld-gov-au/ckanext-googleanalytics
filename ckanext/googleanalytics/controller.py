import logging
from ckan.lib.base import BaseController, c, render, request

import urllib
import urllib2

import logging
import ckan.logic as logic
import hashlib
import plugin
from pylons import config
import paste.deploy.converters as converters

from webob.multidict import UnicodeMultiDict
from paste.util.multidict import MultiDict

from ckan.controllers.api import ApiController
from ckan.controllers.package import PackageController

log = logging.getLogger('ckanext.googleanalytics')

class GAApiController(ApiController):
    # intercept API calls to record via google analytics
    def _post_analytics(
            self, user, request_obj_type, request_function, request_event_label, request_dict={}):
        if config.get('googleanalytics.id') and converters.asbool(config.get('googleanalytics.track_backend_events','False')):
            data_dict = {
                "v": 1,
                "tid": config.get('googleanalytics.id'),
                "cid": hashlib.md5(user).hexdigest(),
                # customer id should be obfuscated
                "t": "event",
                "dh": c.environ['HTTP_HOST'],
                "dp": c.environ['PATH_INFO'],
                "dr": c.environ.get('HTTP_REFERER', ''),
                "ec": "CKAN API Request",
                "ea": request_obj_type+request_function,
                "el": request_event_label
            }
            #Rename keys in request_dict to not conflict with GA
            request_dict_keys = request_dict.keys()
            if len(request_dict_keys) > 0:
                for request_key in request_dict_keys:
                    prefix = 'ckan_'
                    request_dict[prefix + request_key] = request_dict.pop(request_key)
            data_dict.update(request_dict)
                
            plugin.GoogleAnalyticsPlugin.analytics_queue.put(data_dict)

    def action(self, logic_function, ver=None):
        try:
            function = logic.get_action(logic_function)
            side_effect_free = getattr(function, 'side_effect_free', False)
            request_data = self._get_request_data(
                try_url_params=side_effect_free)
            if isinstance(request_data, dict):
                event_label = request_data.get('id', '')
                if event_label == '':
                    event_label = request_data.get('resource_id', '')
                if event_label == '' and 'q' in request_data:
                    event_label = 'Query'
                if event_label == '' and 'query' in request_data:
                    event_label = 'Query'
                if event_label == '' and 'sql' in request_data:
                    event_label = 'SQL Query'
                if event_label == '':
                    event_label = logic_function
                self._post_analytics(c.user, logic_function, '', event_label, request_data)
        except Exception, e:
            log.debug(e)
            pass

        return ApiController.action(self, logic_function, ver)

    def list(self, ver=None, register=None,
             subregister=None, id=None):
        self._post_analytics(c.user,
                             register +
                             ("_"+str(subregister) if subregister else ""),
                             "list",
                             id)
        return ApiController.list(self, ver, register, subregister, id)

    def show(self, ver=None, register=None,
             subregister=None, id=None, id2=None):
        self._post_analytics(c.user,
                             register +
                             ("_"+str(subregister) if subregister else ""),
                             "show",
                             id)
        return ApiController.show(self, ver, register, subregister, id, id2)

    def update(self, ver=None, register=None,
               subregister=None, id=None, id2=None):
        self._post_analytics(c.user,
                             register +
                             ("_"+str(subregister) if subregister else ""),
                             "update",
                             id)
        return ApiController.update(self, ver, register, subregister, id, id2)

    def delete(self, ver=None, register=None,
               subregister=None, id=None, id2=None):
        self._post_analytics(c.user,
                             register +
                             ("_"+str(subregister) if subregister else ""),
                             "delete",
                             id)
        return ApiController.delete(self, ver, register, subregister, id, id2)

    def search(self, ver=None, register=None):
        id = None
        try:
            params = MultiDict(self._get_search_params(request.params))
            if 'q' in params.keys():
                id = params['q']
            if 'query' in params.keys():
                id = params['query']
        except ValueError, e:
            log.debug(str(e))
            pass
        self._post_analytics(c.user, register, "search", id)

        return ApiController.search(self, ver, register)


class GAResourceController(PackageController):
    # intercept API calls to record via google analytics
    def _post_analytics(
            self, user, request_obj_type, request_function, request_id):
        if config.get('googleanalytics.id') and converters.asbool(config.get('googleanalytics.track_backend_events','False')):
            data_dict = {
                "v": 1,
                "tid": config.get('googleanalytics.id'),
                "cid": hashlib.md5(user).hexdigest(),
                # customer id should be obfuscated
                "t": "event",
                "dh": c.environ['HTTP_HOST'],
                "dp": c.environ['PATH_INFO'],
                "dr": c.environ.get('HTTP_REFERER', ''),
                "ec": "CKAN Resource Download Request",
                "ea": request_obj_type+request_function,
                "el": request_id,
            }
            plugin.GoogleAnalyticsPlugin.analytics_queue.put(data_dict)

    def resource_download(self, id, resource_id, filename=None):
        self._post_analytics(c.user, "Resource", "Download", resource_id)
        return PackageController.resource_download(self, id, resource_id,
                                                   filename)
