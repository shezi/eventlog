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

It can be very useful to attach an event log to some Django signals. For example, if you want to track user logins and logouts, you could do it like this::

  import logging
  from django.dispatch import receiver
  from django.contrib.auth import signals
  from eventlog import log_event

  @receiver(signals.user_logged_in)
  def handle_user_logged_in(sender, **kwargs):
      log_event("USER_LOGIN", kwargs.get("user"), loglevel=logging.INFO)
        
  @receiver(signals.user_logged_out)
  def handle_user_logged_out(sender, **kwargs):
      log_event("USER_LOGIN", kwargs.get("user"), extra={'logout': True}, loglevel=logging.INFO)

The reason we use the same event name ``USER_LOGIN`` is so that we can filter more easily in the admin area and see all login and logout events in the same list.


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


License
=======

Copyright 2011, 2012, 2013, Patrick Altman (https://github.com/paltman)

Copyright 2013, Johannes Spielmann (https://github.com/shezi)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
