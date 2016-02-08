import sys
import csv

import requests
import dateutil
from celery.task import task

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from captainhook.models import Hook


@task(max_retries=0, ignore_result=True)
def get_url(url, user_agent):
    headers = {"User-Agent": user_agent}
    try:
        r = requests.get(url, headers=headers)
    except requests.ConnectionError:
        print "Couldn't fetch %s" % url



@task(max_retries=0, ignore_result=True)
def replay(hook_id):
    hook = Hook.objects.get(id=hook_id)
    now = timezone.now()
    pth = sys.argv[-1]
    fp = open(hook.replay_log, "r")
    # todo: softcode
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
    reader = csv.DictReader(fp, fieldnames=fieldnames, delimiter=" ", quotechar='"')
    reader = list(reader)[-hook.number_to_replay:]
    fp.close()
    processed = []
    first_diff = None
    for row in reader:
        method, url, b = row["path_raw"].split()
        if method.lower() not in ("get", "head"):
            continue
        sent_raw = "%s %s:%s:%s" % tuple(row["datetime_a"].lstrip("[").split(":"))\
            + " " + row["datetime_b"].rstrip("]")
        sent = dateutil.parser.parse(sent_raw)
        if first_diff is None:
            first_diff = (now - sent).seconds + 1
        get_url.apply_async(
            (hook.site_root.rstrip("/") + url, row["user_agent"] + " #pk1"),
            countdown=(first_diff - (now - sent).seconds) / hook.speedup_factor
        )
