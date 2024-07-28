import importlib
from textual.app import App, ComposeResult
from textual.widgets import (
    Header,
    ListView,
    ListItem,
    Label,
    Markdown,
)
from .parse_mod import parse_module


class MemberListView(ListView):
    def __init__(self, mod_list):
        super().__init__(id="sidebar")
        self.mod_list = mod_list

    def compose(self):
        for f in self.mod_list:
            yield ListItem(Label(f"{f.name:<16}{f.icon}"))


# class DocView(MarkdownViewer):
#
#     def __init__(self, mod):
#         super().__init__(markdown=mod)
#
#     def watch_md(self):
#         self.markdown = self.md
#


class WudTui(App):
    CSS_PATH = "sidebar.tcss"

    def __init__(self, modname):
        super().__init__()
        _mod = importlib.import_module(modname)
        self.mod = parse_module(_mod)
        self.mod_list = (
            [self.mod] + self.mod.functions + self.mod.classes + self.mod.data
        )

    def compose(self) -> ComposeResult:
        yield Header()
        yield MemberListView(self.mod_list)
        yield Markdown(self.mod_list[0].as_markdown(), id="docview")

    def on_mount(self):
        self.title = "wud"
        self.sub_title = self.mod.name

    def on_list_view_highlighted(self, _):
        lv = self.query_one("#sidebar", MemberListView)
        md = self.query_one("#docview", Markdown)
        md.update(markdown=f"{self.mod_list[lv.index].as_markdown()}")


if __name__ == "__main__":
    import sys

    app = WudTui(sys.argv[1])
    app.run()
