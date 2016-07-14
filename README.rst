CKAN Google Analytics Extension
===============================

**Status:** Production

**CKAN Version:** >= 1.5.*

A CKAN extension that sends tracking data to Google Analytics 

Features
--------

* Puts the Google Analytics asynchronous tracking code into your page headers
  for basic Google Analytics page tracking.

* Adds Google Analytics Event Tracking to resource download links, so that
  resource downloads will be displayed as Events in the Google Analytics
  reporting interface.

* Adds Google Analytics Event Tracking to some API calls so that usage of the
  API can be reported on via Google Analytics.

* Adds Google Analytics Event Tracking to group links on the home page,
  user profile links, editing and saving user profiles, etc.

  *CKAN 1.x only*.

* Puts download stats into dataset pages, e.g. "[downloaded 4 times]".

  *CKAN 1.x only.*

CKAN 1.x Support
----------------

To use ckanext-googleanalytics with CKAN 1.x, make sure you have
``ckan.legacy_templates = true`` in your CKAN ini file.

Installation
------------

1. Install the extension as usual, e.g. (from an activated virtualenv):

    ::

    $ pip install -e  git+https://github.com/ckan/ckanext-googleanalytics.git#egg=ckanext-googleanalytics

2. Edit your development.ini (or similar) to provide these necessary parameters:

    ::

      googleanalytics.id = UA-1010101-1
      googleanalytics.track_frontend_events = true
      googleanalytics.track_backend_events = true
      googleanalytics.collection_url = https://www.google-analytics.com/collect

3. Edit again your configuration ini file to activate the plugin
   with:

   ::

      ckan.plugins = googleanalytics

   (If there are other plugins activated, add this to the list.  Each
   plugin should be separated with a space).

4. If you are using this plugin with a version of CKAN < 2.0 then you should
   also put the following in your ini file::

       ckan.legacy_templates = true

5. Finally, there are some optional configuration settings (shown here
   with their default settings)::

      googleanalytics_resource_prefix = /downloads/
      googleanalytics.domain = auto

   ``resource_prefix`` is an arbitrary identifier so that we can query
   for downloads in Google Analytics.  It can theoretically be any
   string, but should ideally resemble a URL path segment, to make
   filtering for all resources easier in the Google Analytics web
   interface.

   ``domain`` allows you to specify a domain against which Analytics
   will track users.  You will usually want to leave this as ``auto``;
   if you are tracking users from multiple subdomains, you might want
   to specify something like ``.mydomain.com``.
   See `Google's documentation
   <http://code.google.com/apis/analytics/docs/gaJS/gaJSApiDomainDirectory.html#_gat.GA_Tracker_._setDomainName>`_
   for more info.

   The track_frontend_events and track_backend_events can be toggled to provide tracking.

Testing
-------

Very unuseful at this stage!

Checks test.ini for googleanalytics.id being set. (Working)
Example POST HTTPS Request of hit google-analytics/collect. (Not working)

Future
------

The 1.x support has been left in for Frontend integration but all 
authentication for getting data from GA has been removed.

1.x support will likely be entirely removed.

Dashboards/Visualisation
-----

For creating detailed reports of CKAN analytics use `CKAN GA Report <https://github.com/datagovuk/ckanext-ga-report>`_
