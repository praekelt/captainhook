import subprocess

from django.db import models
import django.dispatch

from captainhook.tasks import replay


on_hook_received = django.dispatch.Signal(providing_args=["payload"])


class Hook(models.Model):
    name = models.CharField(max_length=255)
    site_root = models.CharField(
        max_length=255,
        help_text="Eg. http://my.site.com/today/"
    )
    basic_auth_username = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    basic_auth_password = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    fieldnames = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Log file column headings represented as a comma separated string - unused at the moment"
    )
    number_to_replay = models.PositiveIntegerField(default=1000)
    speedup_factor = models.PositiveIntegerField(default=1)
    replay_log = models.FileField(upload_to="replay_logs")
    script_before = models.TextField(
        null=True,
        blank=True,
        help_text="Bash to execute before the replay starts. This typically contains commands that run within SSH."
    )
    script_after = models.TextField(
        null=True,
        blank=True,
        help_text="Bash to execute after the replay has ended. This typically contains commands that run within SSH."
    )
    slack_channel = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Notifications are published to this channel."
    )

    def execute(self, payload):
        on_hook_received.send(self, payload=payload)
        replay.delay(self.id, payload)

    def __unicode__(self):
        return self.name
