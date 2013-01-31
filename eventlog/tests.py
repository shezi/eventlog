from django.test import TestCase
from django.contrib.auth.models import User

from testfixtures import LogCapture

from .models import Event
from .models import create_event
from .models import log_debug, log_info, log_event, log_warning, log_error, log_fatal
from .models import log_exception

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class EventLogAvailabilityTesting(TestCase):
    """Check that all of our functions are available at the module level."""

    def test_imports(self):
        import eventlog
        from eventlog import create_event
        from eventlog import log_debug, log_info, log_event, log_warning, log_error, log_fatal
        from eventlog import log_exception


class EventLogTesting(TestCase):
    
    extra = {'key': 'value', 'key2': 'value2'}
    
    def setUp(self):
        self.user = User.objects.create(username='johndoe', email='johndoe')  # email same as username because some systems use email as username
    
    
    def test_basic_creation(self):
        """Test that the basic event creation works."""
        
        event = create_event("test label")
        self.assertTrue(event.id)
        self.assertEqual(event.label, "test label")
        self.assertIsNone(event.message)
        self.assertIsNone(event.user)
        self.assertIsNone(event.extra)
        self.assertEqual(event.level, logging.INFO)
        
    def test_create_event_full(self):
        """Test creating an event with all options on."""
        
        event = create_event("test label", message="message", user=self.user,
            extra={'key': 'value'},
            level=logging.WARNING
        )
        self.assertTrue(event.id)
        self.assertEqual(event.label, "test label")
        self.assertEqual(event.message, "message")
        self.assertEqual(event.user, self.user)
        self.assertEqual(event.extra, {'key': 'value'})
        self.assertEqual(event.level, logging.WARNING)
        
    def test_create_event_full_userid(self):
        """Test creating an event with all options on and the user given as a number instead of an object."""
        
        event = create_event("test label", message="message", user=1,
            extra={'key': 'value'},
            level=logging.WARNING
        )
        self.assertTrue(event.id)
        self.assertEqual(event.label, "test label")
        self.assertEqual(event.message, "message")
        self.assertEqual(event.user, self.user)
        self.assertEqual(event.extra, {'key': 'value'})
        self.assertEqual(event.level, logging.WARNING)

    def test_create_event_bad_userid(self):
        """Test creating an event with a bad user ID."""
        
        with LogCapture() as l:
            event = create_event("label", message="message", user=999,
                django_log=False)
            self.assertTrue(event.id)
            self.assertEqual(event.label, "label")
            self.assertEqual(event.message, "message")
            self.assertIsNone(event.user)
            
            # check to see if an exception was logged (nice: recursive!)
            l.check(
                ('eventlog', 'WARNING',
                '0000000000000001 EVENTLOG_COULD_NOT_FIND_USER - Could not resolve user_id to actual user {\'exception\': \'Traceback (most recent call last):\\n  File "/Users/spielmann/prog/bitchest/server/env/lib/python2.7/site-packages/eventlog-0.7.0-py2.7.egg/eventlog/models.py", line 55, in create_event\\n    user = User.objects.get(id=user)\\n  File "/Users/spielmann/prog/bitchest/server/env/lib/python2.7/site-packages/django/db/models/manager.py", line 131, in get\\n    return self.get_query_set().get(*args, **kwargs)\\n  File "/Users/spielmann/prog/bitchest/server/env/lib/python2.7/site-packages/django/db/models/query.py", line 366, in get\\n    % self.model._meta.object_name)\\nDoesNotExist: User matching query does not exist.\\n\', \'user_id\': 999}'
                ), 
                )
            # yes, I copied that from the output
            # and yes, it is quite brittle


    def test_convenience_log_debug(self):
        """Test the log_debug convenience function."""
        
        event = log_debug("label", "message", self.user, extra=self.extra)
        self.assertTrue(event.id)
        self.assertEqual(event.label, "label")
        self.assertEqual(event.message, "message")
        self.assertEqual(event.user, self.user)
        self.assertEqual(event.extra, self.extra)
        self.assertEqual(event.level, logging.DEBUG)
        
    def test_convenience_log_info(self):
        """Test the log_info convenience function."""
        
        event = log_info("label", "message", self.user, extra=self.extra)
        self.assertTrue(event.id)
        self.assertEqual(event.label, "label")
        self.assertEqual(event.message, "message")
        self.assertEqual(event.user, self.user)
        self.assertEqual(event.extra, self.extra)
        self.assertEqual(event.level, logging.INFO)

    def test_convenience_log_event(self):
        """Test the log_event convenience function."""
        
        event = log_event("label", "message", self.user, extra=self.extra)
        self.assertTrue(event.id)
        self.assertEqual(event.label, "label")
        self.assertEqual(event.message, "message")
        self.assertEqual(event.user, self.user)
        self.assertEqual(event.extra, self.extra)
        self.assertEqual(event.level, logging.INFO)

    def test_convenience_log_warn(self):
        """Test the log_warn convenience function."""
        
        event = log_warning("label", "message", self.user, extra=self.extra)
        self.assertTrue(event.id)
        self.assertEqual(event.label, "label")
        self.assertEqual(event.message, "message")
        self.assertEqual(event.user, self.user)
        self.assertEqual(event.extra, self.extra)
        self.assertEqual(event.level, logging.WARN)

    def test_convenience_log_error(self):
        """Test the log_error convenience function."""
        
        event = log_error("label", "message", self.user, extra=self.extra)
        self.assertTrue(event.id)
        self.assertEqual(event.label, "label")
        self.assertEqual(event.message, "message")
        self.assertEqual(event.user, self.user)
        self.assertEqual(event.extra, self.extra)
        self.assertEqual(event.level, logging.ERROR)

    def test_convenience_log_fatal(self):
        """Test the log_fatal convenience function."""
        
        event = log_fatal("label", "message", self.user, extra=self.extra)
        self.assertTrue(event.id)
        self.assertEqual(event.label, "label")
        self.assertEqual(event.message, "message")
        self.assertEqual(event.user, self.user)
        self.assertEqual(event.extra, self.extra)
        self.assertEqual(event.level, logging.CRITICAL)


        
    def test_log_messages_bare(self):
        """Test that log messages are generated if and only if the are enabled."""

        with LogCapture() as l:
            event = create_event("label")
            m = ('eventlog', 'INFO', '0000000000000001 label')
            l.check(m)
            
            event = create_event("label", django_log=False)
            l.check(m)

    def test_log_messages_idcount(self):
        """Test that log messages are generated if and only if the are enabled."""
        
        # yes, it is a silly test!
        
        with LogCapture() as l:
            event = create_event("label") # 1
            event = create_event("label") # 2
            event = create_event("label") # 3
            event = create_event("label") # 4
            event = create_event("label") # 5
            event = create_event("label") # 6
            event = create_event("label") # 7
            event = create_event("label") # 8
            event = create_event("label") # 9
            event = create_event("label") # 10
            event = create_event("label") # 11
            l.check(
                ('eventlog', 'INFO', '0000000000000001 label'),
                ('eventlog', 'INFO', '0000000000000002 label'),
                ('eventlog', 'INFO', '0000000000000003 label'),
                ('eventlog', 'INFO', '0000000000000004 label'),
                ('eventlog', 'INFO', '0000000000000005 label'),
                ('eventlog', 'INFO', '0000000000000006 label'),
                ('eventlog', 'INFO', '0000000000000007 label'),
                ('eventlog', 'INFO', '0000000000000008 label'),
                ('eventlog', 'INFO', '0000000000000009 label'),
                ('eventlog', 'INFO', '0000000000000010 label'),
                ('eventlog', 'INFO', '0000000000000011 label'),
            )

    def test_log_messages_user(self):
        """Test that log messages are generated with the user name if a user is given."""

        with LogCapture() as l:
            user = User.objects.create(username="hello", email="hello") # email attached because some people use emails as user name
            event = create_event("label", user=user)
            m = ('eventlog', 'INFO', '0000000000000001 label (user: hello)')
            l.check(m)
            event = create_event("label", user=user, django_log=False)
            l.check(m)

    def test_log_messages_message(self):
        """Test that log messages are generated with the message if given."""

        with LogCapture() as l:
            event = create_event("label", message="message")
            m = ('eventlog', 'INFO', '0000000000000001 label - message')
            l.check(m)
            event = create_event("label", message="message", django_log=False)
            l.check(m)

    def test_log_messages_extra(self):
        """Test that log messages are generated with the extra info if given."""

        with LogCapture() as l:
            event = create_event("label", extra={'key': 'value', 'key2': 'value2'})
            m = ('eventlog', 'INFO', "0000000000000001 label - {'key2': 'value2', 'key': 'value'}") # order is different, NICE!
            l.check(m)
            event = create_event("label", extra={'key': 'value', 'key2': 'value2'}, django_log=False)
            l.check(m)
    
    def test_log_messages_everything(self):
        """Test that log messages are generated with the extra info if given."""

        user = User.objects.create(username="hello", email="hello") # email attached because some people use emails as user name
        with LogCapture() as l:
            event = create_event("label", message="message", user=user, extra={'key': 'value', 'key2': 'value2'})
            m = ('eventlog', 'INFO', "0000000000000001 label (user: hello) - message {'key2': 'value2', 'key': 'value'}") # order is different, NICE!
            l.check(m)
            event = create_event("label", extra={'key': 'value', 'key2': 'value2'}, django_log=False)
            l.check(m)

    def test_log_messages_everything_with_levels(self):
        """Test that log messages are generated with the extra info if given."""

        user = User.objects.create(username="hello", email="hello") # email attached because some people use emails as user name
        with LogCapture() as l:
            event = create_event(level=logging.DEBUG, label="label", message="message", user=user, extra={'key': 'value', 'key2': 'value2'})
            event = create_event(level=logging.INFO, label="label", message="message", user=user, extra={'key': 'value', 'key2': 'value2'})
            event = create_event(level=logging.WARN, label="label", message="message", user=user, extra={'key': 'value', 'key2': 'value2'})
            event = create_event(level=logging.ERROR, label="label", message="message", user=user, extra={'key': 'value', 'key2': 'value2'})
            event = create_event(level=logging.FATAL, label="label", message="message", user=user, extra={'key': 'value', 'key2': 'value2'})
            m1 = ('eventlog', 'DEBUG', "0000000000000001 label (user: hello) - message {'key2': 'value2', 'key': 'value'}") # order is different, NICE!
            m2 = ('eventlog', 'INFO', "0000000000000002 label (user: hello) - message {'key2': 'value2', 'key': 'value'}") # order is different, NICE!
            m3 = ('eventlog', 'WARNING', "0000000000000003 label (user: hello) - message {'key2': 'value2', 'key': 'value'}") # order is different, NICE!
            m4 = ('eventlog', 'ERROR', "0000000000000004 label (user: hello) - message {'key2': 'value2', 'key': 'value'}") # order is different, NICE!
            m5 = ('eventlog', 'CRITICAL', "0000000000000005 label (user: hello) - message {'key2': 'value2', 'key': 'value'}") # order is different, NICE!
            l.check(m2, m3, m4, m5) # debug logging is disabled
            event = create_event(level=logging.DEBUG, django_log=False, label="label", message="message", user=user, extra={'key': 'value', 'key2': 'value2'})
            event = create_event(level=logging.INFO, django_log=False, label="label", message="message", user=user, extra={'key': 'value', 'key2': 'value2'})
            event = create_event(level=logging.WARN, django_log=False, label="label", message="message", user=user, extra={'key': 'value', 'key2': 'value2'})
            event = create_event(level=logging.ERROR, django_log=False, label="label", message="message", user=user, extra={'key': 'value', 'key2': 'value2'})
            event = create_event(level=logging.FATAL, django_log=False, label="label", message="message", user=user, extra={'key': 'value', 'key2': 'value2'})
            l.check(m2, m3, m4, m5)

    def test_log_log_debug(self):
        """Test that log_debug convenience function logs if enabled."""
        
        with LogCapture() as l:
            event = log_debug("label", "message", self.user, extra=self.extra)
            l.check() # debug logging is disabled, HAHA!


    def test_log_log_info(self):
        """Test that log_info convenience function logs if enabled."""
        
        with LogCapture() as l:
            event = log_info("label", "message", self.user, extra=self.extra)
            m = ('eventlog', 'INFO', "0000000000000001 label (user: johndoe) - message {'key2': 'value2', 'key': 'value'}")
            l.check(m)
            event = log_info("label", "message", self.user, extra=self.extra, django_log=False)
            l.check(m)


    def test_log_log_event(self):
        """Test that log_event convenience function logs if enabled."""
        
        with LogCapture() as l:
            event = log_event("label", "message", self.user, extra=self.extra)
            m = ('eventlog', 'INFO', "0000000000000001 label (user: johndoe) - message {'key2': 'value2', 'key': 'value'}")
            l.check(m)
            event = log_event("label", "message", self.user, extra=self.extra, django_log=False)
            l.check(m)


    def test_log_log_warning(self):
        """Test that log_warning convenience function logs if enabled."""
        
        with LogCapture() as l:
            event = log_warning("label", "message", self.user, extra=self.extra)
            m = ('eventlog', 'WARNING', "0000000000000001 label (user: johndoe) - message {'key2': 'value2', 'key': 'value'}")
            l.check(m)
            event = log_warning("label", "message", self.user, extra=self.extra, django_log=False)
            l.check(m)


    def test_log_log_error(self):
        """Test that log_error convenience function logs if enabled."""
        
        with LogCapture() as l:
            event = log_error("label", "message", self.user, extra=self.extra)
            m = ('eventlog', 'ERROR', "0000000000000001 label (user: johndoe) - message {'key2': 'value2', 'key': 'value'}")
            l.check(m)
            event = log_error("label", "message", self.user, extra=self.extra, django_log=False)
            l.check(m)


    def test_log_log_critical(self):
        """Test that log_fatal convenience function logs if enabled."""
        
        with LogCapture() as l:
            event = log_fatal("label", "message", self.user, extra=self.extra)
            m = ('eventlog', 'CRITICAL', "label (user: johndoe) - message {'key2': 'value2', 'key': 'value'}")
            l.check(m)
            event = log_fatal("label", "message", self.user, extra=self.extra, django_log=False)
            l.check(m)


    def test_log_exception(self):
        """Test that the log_exception function captures the exception trace."""
        
        event = None
        try:
            raise Exception()
        except:
            event = log_exception("EXCEPTION", message="message")
        self.assertIsNotNone(event)
        self.assertEqual(event.label, "EXCEPTION")
        self.assertEqual(event.message, "message")
        self.assertIsNone(event.user)
        self.assertIsNotNone(event.extra)
        self.assertIn('exception', event.extra)




