'''
Tests for the ckanext.googleanalytics extension.
'''
import paste.fixture
import pylons.test
import pylons.config as config
import webtest

import ckan.model as model
import ckan.tests.legacy as tests
import ckan.plugins
#import ckan.tests.factories as factories
import uuid
import urllib
import urllib2

class TestGAValidHit(object):
    def test_has_ga_id(self):
        ga_tid = config.get('googleanalytics.id',"")
        assert ga_tid != "" 

'''
Test will fail under CKAN testing environment cannot resolve HTTP/S
    def test_hit(self):
        ga_version = 1
        ga_tid = config.get('googleanalytics.id',""),
        customer_id = str(uuid.uuid4())
        ga_type = "event"
        document_host = "foo.com"
        document_path = "/foo"
        document_referrer = "http://foo.com"
        event_category = "CKAN API Request"
        event_action = "datastore_search"
        event_label = "An Event Occured"

        data_dict = {
            "v": ga_version,
            "tid": ga_tid,
            "cid": customer_id,
            "t": ga_type,
            "dh": document_host,
            "dp": document_path,
            "dr": document_referrer,
            "ec": event_category,
            "ea": event_action,
            "el": event_label
        }

        data = urllib.urlencode(data_dict)
        headers= {
            'Content-Type':'application/x-www-form-urlencoded',
            'User-Agent':'Analytics Pros - Universal Analytics (Python)'
        }

        ga_collection_url = config.get('googleanalytics.collection_url')
        request = urllib2.Request(
            ga_collection_url,
            data=data,
            headers=headers
        )
        response = urllib2.urlopen(request,timeout=10)

        ga_debug_collection_url = config.get('googleanalytics.debug_collection_url')
        request = urllib2.Request(
            ga_debug_collection_url,
            data=data,
            headers=headers
        )
        response = urllib2.urlopen(request,timeout=10)

        assert 1 == 1
'''
