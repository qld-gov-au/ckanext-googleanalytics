import logging
import hashlib
from ckan.lib.base import BaseController, c, render, request
import ckan.logic as logic
import plugin
from pylons import config
import paste.deploy.converters as converters

from webob.multidict import UnicodeMultiDict
from paste.util.multidict import MultiDict

from ckan.controllers.api import ApiController
from ckan.controllers.package import PackageController

log = logging.getLogger('ckanext.googleanalytics')

class GAApiController(ApiController):

    def _alter_sql(self,sql_query):
        '''Quick and dirty altering of sql to prevent injection'''
        sql_query = sql_query.lower()
        sql_query = sql_query.replace('select','CK_SEL')
        sql_query = sql_query.replace('insert','CK_INS')
        sql_query = sql_query.replace('update','CK_UPD')
        sql_query = sql_query.replace('upsert','CK_UPS')
        sql_query = sql_query.replace('declare','CK_DEC')
        return sql_query

    # intercept API calls to record via google analytics
    def _post_analytics(
            self, user, request_obj_type, request_function, request_event_label, request_dict={}):
        if config.get('googleanalytics.id') and converters.asbool(config.get('googleanalytics.track_backend_events', 'False')):
            data_dict = {
                "v": 1,
                "tid": config.get('googleanalytics.id'),
                "cid": hashlib.md5(user).hexdigest(),
                # customer id should be obfuscated
                "t": "event",
                "dh": c.environ['HTTP_HOST'],
                "dp": c.environ['PATH_INFO'],
                "dr": c.environ.get('HTTP_REFERER', ''),
                "ec": c.environ['HTTP_HOST'] + " CKAN API Request",
                "ea": request_obj_type+request_function,
                "el": request_event_label
            }
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
                    if request_data.get('resource_id', '') != '':
                        event_label = 'Resource Id: ' + request_data.get('resource_id', '')
                if event_label == '' and 'q' in request_data:
                    event_label = 'Query: ' + request_data['q']
                if event_label == '' and 'query' in request_data:
                    event_label = 'Query: ' + request_data['query']
                if event_label == '' and 'sql' in request_data:
                    altered_sql = self._alter_sql(request_data['sql'])
                    event_label = 'SQL Query: ' + altered_sql
                if event_label == '':
                    event_label = logic_function
                request_obj_type = logic_function + ' - ' + c.environ['PATH_INFO']
                self._post_analytics(c.user, request_obj_type, '', event_label, request_data)
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
        if config.get('googleanalytics.id') and converters.asbool(config.get('googleanalytics.track_backend_events', 'False')):
            data_dict = {
                "v": 1,
                "tid": config.get('googleanalytics.id'),
                "cid": hashlib.md5(user).hexdigest(),
                # customer id should be obfuscated
                "t": "event",
                "dh": c.environ['HTTP_HOST'],
                "dp": c.environ['PATH_INFO'],
                "dr": c.environ.get('HTTP_REFERER', ''),
                "ec": c.environ['HTTP_HOST'] + " CKAN Resource Download Request",
                "ea": request_obj_type+request_function,
                "el": request_id,
            }
            plugin.GoogleAnalyticsPlugin.analytics_queue.put(data_dict)

    def resource_download(self, id, resource_id, filename=None):
        self._post_analytics(c.user, "Resource", "Download", resource_id)
        return PackageController.resource_download(self, id, resource_id,
                                                   filename)
