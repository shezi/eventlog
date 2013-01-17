from datetime import datetime

from django.db import models

from django.contrib.auth.models import User

import jsonfield

import logging
logger = logging.getLogger('eventlog')


class Log(models.Model):
    """A simple event logging model."""
    
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=50)
    extra = jsonfield.JSONField()
    
    class Meta:
        ordering = ["-timestamp"]


def log_event(action, user=None, extra=None, loglevel=None):
    """Log an event that has happened and attach extra information to it.
    
    If a loglevel is giving, the event will additionally be logged through the standard
    Django logging system at that level.
    """
    if user is not None and not user.is_authenticated():
        user = None
    if extra is None:
        extra = {}
    
    if loglevel is not None:
        if user:
            logger.log(loglevel, "%s (user %s) - %s" % (action, user.username, str(extra)))
        else:
            logger.log(loglevel, "%s - %s" % (action, str(extra)))
    
    return Log.objects.create(user=user, action=action, extra=extra)
