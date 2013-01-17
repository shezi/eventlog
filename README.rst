========
eventlog
========

``eventlog`` is a simple app that provides an easy and clean
interface for logging diagnostic as well as business intelligence
data about activity that occurs in your site.

Each event you log gets added to the your database. You can use the Django
admin interface to review your events.

=====
Usage
=====

For each event you want to log in your code, simply put a call to the ``log_event`` function.

::

  from eventlog import log_event
  log_event("EVENTNAME")

You can attach a user to the event and also add extra information to it, by adding them to the ``log_event`` call::

  from eventlog import log_event
  log_event("EVENTNAME", user, extra={'info': 'this is a JSON field'})

The extra information gets stored in a JSON field and must therefor be JSON serializable.

If you want to add the event in the regular Django logging, you can simply add a loglevel to the call. This will make
a call to the logger called ``eventlog``, so you can capture your events in the regular logs, too.

::

  # in settings:
  LOGGING = {
      'version': 1,
      'disable_existing_loggers': False,
      'formatters': {
          'simple': {
              'format': '%(levelname)s %(message)s'
          },
      },
      'handlers': {
          'console':{
              'level':'DEBUG',
              'class':'logging.StreamHandler',
              'formatter': 'simple'
          },
      },
      'loggers': {
          'eventlog': {
              'handlers': ['console', ],
              'level': 'INFO',
              'propagate': True,
          },
      }
  }

  # in your code:
  import logging
  from eventlog import log_event
  log_event("EVENTNAME", user, extra={'info': 'an event happened',}, loglevel=logging.INFO)

  # output:
  INFO EVENTNAME (user user) - {'info': 'an event happened'}



============
Installation
============

The simplest way to install eventlog is using pip, directly from this git repository::

  pip install -e git://github.com/shezi/eventlog.git#egg=eventlog


=======
Credits
=======

 - eventlog was first developed by eldarion, http://github.com/eldarion/eventlog
 - Additions were developed by Johannes Spielmann, http://github.com/shezi/eventlog
