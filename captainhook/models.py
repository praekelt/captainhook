import subprocess

from django.db import models
import django.dispatch


on_hook_received = django.dispatch.Signal(providing_args=["payload"])


class Hook(models.Model):
    name = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    repo = models.CharField(max_length=255)
    path = models.CharField(max_length=255, blank=True, null=True)

    def execute(self, payload):
        if self.path:
            subprocess.call([self.path])
        on_hook_received.send(self, payload=payload)

    def __unicode__(self):
        return "%s (%s/%s)" % (self.name, self.user, self.repo)
