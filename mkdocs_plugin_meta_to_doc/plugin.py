import os
import sys
from timeit import default_timer as timer
from datetime import datetime, timedelta

from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin
from pathlib import Path

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

def realise_includes(lines, base_path):
    for line in lines:
        match = re.search(r"^\{%\s+include\s+(\S.*\S)\s+%\}$", line)
        if match:
            p = Path(match.group(1))
            if not p.is_absolute():
                p = base_path / p
            if not p.exists():
                continue
            for inc_line in p.read_text(encoding="utf-8").splitlines():
                yield inc_line
        else:
            yield line

class MetaToDoc(BasePlugin):
    def __init__(self):
        self.enabled = True
        self.total_time = 0

    def on_page_markdown(self, markdown, page, config, files):
        base_path = Path(page.file.abs_src_path).parent
        mdneu = []
        found = False
        for l in realise_includes(markdown.split("\n"), base_path):
            mdneu.append(l)
            if found:
                continue
            src_uri = re.sub(r"\.md$", "", page.file.src_uri)
            meta_fmt = [
                f'<a href="zettel://zk/{src_uri}">Bearbeiten</a><br /><br />'
            ] + [f"{x}<br />" for x in format_meta(page.meta)]

            if re.match(r"\s*#\s", l):
                mdneu.append('<div id="sidebar-extra" class="md-nav">')
                mdneu.extend(meta_fmt)
                mdneu.append("<br />")
                mdneu.append("<br />")
                mdneu.append("</div>")
                found = True
        return "\n".join(mdneu)
