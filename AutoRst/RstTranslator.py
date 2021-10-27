import sys
import os

import docutils.nodes
import docutils.parsers.rst
import docutils.utils
import docutils.frontend

def parse_rst(text: str) -> docutils.nodes.document:
    parser = docutils.parsers.rst.Parser()
    components = (docutils.parsers.rst.Parser,)
    settings = docutils.frontend.OptionParser(components=components).get_default_values()
    document = docutils.utils.new_document('<rst-doc>', settings=settings)
    parser.parse(text, document)
    return document

class MyVisitor(docutils.nodes.NodeVisitor):

    def visit_reference(self, node: docutils.nodes.reference) -> None:
        print(node)

    def unknown_visit(self, node: docutils.nodes.Node) -> None:
        print(node)

def main(content):
    doc = parse_rst(content)
    visitor = MyVisitor(doc)
    doc.walk(visitor)

if __name__ == "__main__":
    path = sys.argv[1]
    with open(path, "rt") as fr:
        content = fr.read()
        main(content)
