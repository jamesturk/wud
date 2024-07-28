import importlib
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import (
    Static,
    Header,
    ListView,
    ListItem,
    Label,
    MarkdownViewer,
    Markdown,
)
from .parse_mod import parse_module

TEXT = """\
Docking a widget removes it from the layout and fixes its position, aligned to either the top, right, bottom, or left edges of a container.

Docked widgets will not scroll out of view, making them ideal for sticky headers, footers, and sidebars.

"""


class MemberListView(ListView):
    def __init__(self, mod_list):
        super().__init__(id="sidebar")
        self.mod_list = mod_list

    def compose(self):
        for f in self.mod_list:
            yield ListItem(Label(f"{f.name:<16}{f.icon}"))


def func2md(func):
    return f"""## {func.name}{func.signature}
    {func.desc}
    """


def mod2md(mod):
    func_md = "\n\n".join(func2md(f) for f in mod.functions)
    return f"""# {mod.name}
    {mod.desc}

    {func_md}
    """


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
        self.mod_list = [self.mod] + self.mod.functions + self.mod.data

    def compose(self) -> ComposeResult:
        yield Header()
        yield MemberListView(self.mod_list)
        yield Markdown(mod2md(self.mod), id="docview")

    def on_mount(self):
        self.title = "wud"
        self.sub_title = self.mod.name

    def on_list_view_highlighted(self, _):
        lv = self.query_one("#sidebar", MemberListView)
        md = self.query_one("#docview", Markdown)
        md.update(markdown=f"{self.mod_list[lv.index]}")


if __name__ == "__main__":
    import sys

    app = WudTui(sys.argv[1])
    app.run()
