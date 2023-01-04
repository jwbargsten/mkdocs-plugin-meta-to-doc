import os
import sys
from timeit import default_timer as timer
from datetime import datetime, timedelta

from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin

import json

import re

mapping = {"datum": "Datum", "themen": "Themen", "sw": "Schlüsselwörter", "vorg": "Vorgänger"}


def format_meta(meta):
    fixed = ["datum", "vorg", "themen", "sw"]
    content = []
    for key in fixed:
        val = meta.get(key, None)
        if val is not None and key == "vorg":
            val = re.sub(r"\.md$", "", val)
            content.append(f'<strong><a href="/{val}">{mapping["vorg"]}</a></strong>')
            content.append("")
        elif val is not None:
            val2 = ", ".join(val.split(","))
            content.append(f"<strong>{mapping[key]}:</strong> {val2}")
    for key, val in meta.items():
        if key in fixed:
            continue
        if val is not None:
            content.append(f"<strong>{key.title()}:</strong> {val}")
    return content


class MetaToDoc(BasePlugin):
    def __init__(self):
        self.enabled = True
        self.total_time = 0

    def on_page_markdown(self, markdown, page, config, files):
        mdneu = []
        found = False
        for l in markdown.split("\n"):
            mdneu.append(l)
            if found:
                continue
            meta_fmt = [
                f'<a href="zettel://zk/{page.file.src_uri}">Bearbeiten</a><br /><br />'
            ] + [f"{x}<br />" for x in format_meta(page.meta)]

            if re.match(r"\s*#\s", l):
                mdneu.append('<div id="sidebar-extra" class="md-nav">')
                mdneu.extend(meta_fmt)
                mdneu.append("<br />")
                mdneu.append("<br />")
                mdneu.append("</div>")
                found = True
        return "\n".join(mdneu)
