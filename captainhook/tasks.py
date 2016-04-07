import os
import sys
import csv
from tempfile import mkdtemp
from shutil import rmtree
import subprocess
import json

import requests
from requests.auth import HTTPBasicAuth
from dateutil import parser
from celery.task import task
from celery import shared_task
from celery.result import ResultSet
from celery import group
from slacker import Slacker

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings


@shared_task()
def get_url(url, user_agent, auth=None):
    headers = {"User-Agent": user_agent}
    try:
        r = requests.get(url, headers=headers, auth=auth)
        del r
    except requests.ConnectionError:
        print "Couldn't fetch %s" % url


@shared_task()
def replay_complete_callback(results, hook_id, payload):

    # Prevent circular import
    from captainhook.models import Hook, Log

    hook = Hook.objects.get(id=hook_id)

    if hook.script_after:
        pth = mkdtemp()
        try:
            script = os.path.join(pth, "after.sh")
            fp = open(script, "w")
            fp.write(hook.script_after)
            fp.close()
            os.chmod(script, 0755)
            subprocess.call(["/bin/bash", script])
            out = subprocess.check_output(["/bin/bash", script])
        finally:
            if pth:
                rmtree(pth)

        if out:
            slack_token = getattr(settings, "SLACK_TOKEN", None)
            if hook.slack_channel and slack_token:
                message = "%s:\n%s" % (hook.site_root.split('//')[-1], out)
                slack = Slacker(slack_token)
                slack.chat.post_message("#" + hook.slack_channel.lstrip("#"), message, as_user=True)

    if hook.script_log:
        pth = mkdtemp()
        try:
            script = os.path.join(pth, "log.sh")
            fp = open(script, "w")
            fp.write(hook.script_log)
            fp.close()
            os.chmod(script, 0755)
            subprocess.call(["/bin/bash", script])
            out = subprocess.check_output(["/bin/bash", script])
            if out:
                try:
                    pretty_json = json.dumps(json.loads(out), indent=4)
                except ValueError:
                    pass
                else:
                    Log.objects.create(
                        hook=hook,
                        number_to_replay=hook.number_to_replay,
                        speedup_factor=hook.speedup_factor,
                        raw_json=pretty_json
                    )
        finally:
            if pth:
                rmtree(pth)


@shared_task(ignore_result=True)
def replay(hook_id, payload):

    # Prevent circular import
    from captainhook.models import Hook

    hook = Hook.objects.get(id=hook_id)

    pth = mkdtemp()
    if hook.script_before:
        try:
            script = os.path.join(pth, "before.sh")
            fp = open(script, "w")
            fp.write(hook.script_before)
            fp.close()
            os.chmod(script, 0755)
            subprocess.call(["/bin/bash", script])
        finally:
            if pth:
                rmtree(pth)

    now = timezone.now()

    # todo: softcode properly. This is hacky.
    if "router" in hook.replay_log.name:
        # Our router format
        fieldnames=[
            "ip",
            "dc1",
            "cache_result",
            "datetime_a",
            "datetime_b",
            "request_time",
            "upstream_time",
            "dc2",
            "path_raw",
            "status_code",
            "size_bytes",
            "header_url",
            "user_agent"
        ]
    else:
        # Normal nginx format
        fieldnames=[
            "ip",
            "dc1",
            "dc2",
            "datetime_a",
            "datetime_b",
            "path_raw",
            "status_code",
            "size_bytes",
            "header_url",
            "user_agent"
        ]

    reader = csv.DictReader(hook.replay_log, fieldnames=fieldnames, delimiter=" ", quotechar='"')
    reader = list(reader)[-hook.number_to_replay:]
    first_diff = None
    todo = []
    for row in reader:
        method, url, b = row["path_raw"].split()
        if method.lower() not in ("get", "head"):
            continue
        sent_raw = "%s %s:%s:%s" % tuple(row["datetime_a"].lstrip("[").split(":"))\
            + " " + row["datetime_b"].rstrip("]")
        sent = parser.parse(sent_raw)
        if first_diff is None:
            first_diff = (now - sent).seconds + 1
        todo.append((
            hook.site_root.rstrip("/") + url,
            row["user_agent"] + " #pk1",
            (first_diff - (now - sent).seconds) / hook.speedup_factor
        ))

    auth = None
    if hook.basic_auth_username and hook.basic_auth_password:
        auth=HTTPBasicAuth(hook.basic_auth_username, hook.basic_auth_password)

    gr = group(
        get_url.s(a, b, auth=auth).set(countdown=c) for a, b, c in todo
    )
    gr = gr| replay_complete_callback.s(hook_id, payload)
    gr()
