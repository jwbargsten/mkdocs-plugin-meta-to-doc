
import pytest

from mkdocs_plugin_meta_to_doc import plugin

def test_format_meta():
    res = plugin.format_meta({'vorg': 'abc.md', 'sw': 'a, b, c'})
    ref = ['**[Vorgänger](/abc)**', '**Schlüsselwörter:** a, b, c']
    assert res == ref

class Page():
    meta = {'vorg': 'abc.md', 'sw': 'a, b, c'}

def test_meta_to_doc():
    mtd = plugin.MetaToDoc()
    res = mtd.on_page_markdown("nix\n# titel\nxin", Page(), None, None)
    assert res == "a"

