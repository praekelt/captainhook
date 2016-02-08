import subprocess

from django.db import models
import django.dispatch


on_hook_received = django.dispatch.Signal(providing_args=["payload"])


class Hook(models.Model):
    name = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    repo = models.CharField(max_length=255)
    path = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Script to execute"
    )
    site_root = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Eg. http://my.site.com/today/"
    )
    fieldnames = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Log file column headings represented as a comma separated string"
    )
    number_to_replay = models.PositiveIntegerField(default=1000, blank=True)
    speedup_factor = models.PositiveIntegerField(default=1, blank=True)
    replay_log = models.FileField(upload_to="replay_logs", null=True, blank=True)

    def execute(self, payload):
        if self.path:
            subprocess.call([self.path])
        on_hook_received.send(self, payload=payload)

    def __unicode__(self):
        return "%s (%s/%s)" % (self.name, self.user, self.repo)
