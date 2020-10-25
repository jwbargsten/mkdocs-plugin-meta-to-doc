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
    fixed = ["datum", "themen", "sw"]
    content = []
    val = meta.get("vorg", None)
    if val is not None:
        val = re.sub(r"\.md$", "", val)
        content.append(f'**[{mapping["vorg"]}](/{val})**')
        content.append("")
    for key in fixed:
        val = meta.get(key, None)
        if val is not None:
            val2 = ", ".join(val.split(","))
            content.append(f"**{mapping[key]}:** {val2}")
    for key, val in meta.items():
        if key in fixed or key == "vorg":
            continue
        if val is not None:
            content.append(f"**{key.title()}:** {val}")
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
            meta_fmt = [f"{x}<br />" for x in format_meta(page.meta)]
            if re.match(r"\s*#\s", l):
                mdneu.append('<div markdown=1 id="sidebar-extra" class="md-nav">')
                mdneu.extend(meta_fmt)
                mdneu.append("<br />")
                mdneu.append("<br />")
                mdneu.append("</div>")
                found = True
        return "\n".join(mdneu)
