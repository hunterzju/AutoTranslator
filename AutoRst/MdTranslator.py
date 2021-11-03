import sys
import os
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(ROOT_PATH)

from marko import Markdown
from marko.renderer import Renderer
from contextlib import contextmanager
import time
from Translator.TxyTranslator import TencentTranslate

translator = TencentTranslate()

class TranslatorRender(Renderer):
    def __init__(self):
        self.dst_lang = "zh"

    """Render the AST back to markdown document.

    It is useful for, e.g. merging sections and formatting documents.
    For convenience, markdown renderer provides all render functions for basic elements
    and those from common extensions.
    """

    def __enter__(self):  # type: () -> Renderer
        self._prefix = ""
        self._second_prefix = ""
        return super().__enter__()

    @contextmanager
    def container(self, prefix, second_prefix=""):
        old_prefix = self._prefix
        old_second_prefix = self._second_prefix
        self._prefix += prefix
        self._second_prefix += second_prefix
        yield
        self._prefix = old_prefix
        self._second_prefix = old_second_prefix

    def render_paragraph(self, element):
        children = self.render_children(element)
        children = translator.translate(children, target=self.dst_lang)
        time.sleep(0.2)
        line = self._prefix + children + "\n"
        self._prefix = self._second_prefix
        return line

    def render_list(self, element):
        result = []
        if element.ordered:
            num = element.start
            for child in element.children:
                item = self.render(child)
                item = translator.translate(item, self.dst_lang)
                with self.container(f"{num}. ", " " * (len(str(num)) + 2)):
                    result.append(item)
        else:
            for child in element.children:
                with self.container(f"{element.bullet} ", "  "):
                    item = self.render(child)
                    item = translator.translate(item, self.dst_lang)
                    time.sleep(0.2)
                    result.append(item)
        self._prefix = self._second_prefix
        return "".join(result)

    def render_list_item(self, element):
        return self.render_children(element)

    def render_quote(self, element):
        with self.container("> ", "> "):
            result = self.render_children(element)
        self._prefix = self._second_prefix
        result = translator.translate(result, self.dst_lang)
        time.sleep(0.2)
        return result + "\n"

    def render_fenced_code(self, element):
        extra = f" {element.extra}" if element.extra else ""
        lines = [self._prefix + f"```{element.lang}{extra}"]
        lines.extend(
            self._second_prefix + line
            for line in self.render_children(element).splitlines()
        )
        lines.append(self._second_prefix + "```")
        self._prefix = self._second_prefix
        return "\n".join(lines) + "\n"

    def render_code_block(self, element):
        indent = " " * 4
        lines = self.render_children(element).splitlines()
        lines = [self._prefix + indent + lines[0]] + [
            self._second_prefix + indent + line for line in lines[1:]
        ]
        self._prefix = self._second_prefix
        return "\n".join(lines) + "\n"

    def render_html_block(self, element):
        result = self._prefix + element.children + "\n"
        self._prefix = self._second_prefix
        return result

    def render_thematic_break(self, element):
        result = self._prefix + "* * *\n"
        self._prefix = self._second_prefix
        return result

    def render_heading(self, element):
        content = self.render_children(element)
        content = translator.translate(content, self.dst_lang)
        time.sleep(0.2)
        result = (
            self._prefix
            + "#" * element.level
            + " "
            + content
            + "\n"
        )
        self._prefix = self._second_prefix
        return result

    def render_setext_heading(self, element):
        return self.render_heading(element)

    def render_blank_line(self, element):
        result = self._prefix + "\n"
        self._prefix = self._second_prefix
        return result

    def render_link_ref_def(self, elemement):
        return ""

    def render_emphasis(self, element):
        content = self.render_children(element)
        content = translator.translate(content, self.dst_lang)
        time.sleep(0.2)
        return f"*{content}*"

    def render_strong_emphasis(self, element):
        content = self.render_children(element)
        content = translator.translate(content, self.dst_lang)
        time.sleep(0.2)
        return f"**{content}**"

    def render_inline_html(self, element):
        return element.children

    def render_link(self, element):
        title = (
            ' "{}"'.format(element.title.replace('"', '\\"')) if element.title else ""
        )
        return f"[{self.render_children(element)}]({element.dest}{title})"

    def render_auto_link(self, element):
        return f"<{element.dest}>"

    def render_image(self, element):
        template = "![{}]({}{})"
        title = (
            ' "{}"'.format(element.title.replace('"', '\\"')) if element.title else ""
        )
        return template.format(self.render_children(element), element.dest, title)

    def render_literal(self, element):
        return "\\" + element.children

    def render_raw_text(self, element):
        # content = translator.translate(element.children, self.dst_lang)
        # time.sleep(0.2)
        return element.children

    def render_line_break(self, element):
        return "\n" if element.soft else "\\\n"

    def render_code_span(self, element):
        text = element.children
        if text and text[0] == "`" or text[-1] == "`":
            return f"`` {text} ``"
        return f"`{element.children}`"

def test(path, out_path):
    with open(path, "rt") as f:
        content = f.read()
    
    md = Markdown(renderer=TranslatorRender)
    res = md.convert(content)
    # visitChildren(ast)
    with open(out_path, "wt", encoding="UTF-8") as fw:
        fw.write(res)
    print("finish")

if __name__ == "__main__":
    test(sys.argv[1], sys.argv[2])
