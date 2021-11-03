import sys
import os
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(ROOT_PATH)

import docutils.nodes
import docutils.parsers.rst
import docutils.utils
import docutils.frontend
from Utils.FileFunc import PathManager

def parse_rst(text: str) -> docutils.nodes.document:
    parser = docutils.parsers.rst.Parser()
    components = (docutils.parsers.rst.Parser,)
    settings = docutils.frontend.OptionParser(components=components).get_default_values()
    document = docutils.utils.new_document('<rst-doc>', settings=settings)
    parser.parse(text, document)
    return document

global_type_set = set()
class RstVisitor(docutils.nodes.NodeVisitor):

    def visit_reference(self, node: docutils.nodes.reference) -> None:
        pass

    def visit_title(self, node: docutils.nodes.title):
        pass

    def visit_paragraph(self, node: docutils.nodes.paragraph):
        pass

    def visit_section(self, node: docutils.nodes.section):
        pass

    def visit_emphasis(self, node: docutils.nodes.emphasis):
        pass

    def visit_text(self, node: docutils.nodes.Text) -> None:
        print(node.rawsource)

    def unknown_visit(self, node: docutils.nodes.Node) -> None:
        global_type_set.add(str(type(node)))

def main(content):
    doc = parse_rst(content)
    visitor = RstVisitor(doc)
    doc.walk(visitor)

if __name__ == "__main__":
    path = sys.argv[1]
    pm = PathManager()
    if pm.isPathDir(path):
        filelist = pm.getFileList(path)
    
    for f_path in filelist:
        with open(f_path, "rt") as fr:
            content = fr.read()
            main(content)
    
    for t in global_type_set:
        print(t)

'''
TODO: support node class
 <class 'docutils.nodes.warning'>
 <class 'docutils.nodes.problematic'>
 <class 'docutils.nodes.Text'>
 <class 'docutils.nodes.inline'>
 <class 'docutils.nodes.title'>
 <class 'docutils.nodes.topic'>
 <class 'docutils.nodes.paragraph'>
 <class 'docutils.nodes.reference'>
 <class 'docutils.nodes.section'>
 <class 'docutils.nodes.emphasis'>
 <class 'docutils.nodes.list_item'>
 <class 'docutils.nodes.literal'>
 <class 'docutils.nodes.figure'>
 <class 'docutils.nodes.caption'>
 <class 'docutils.nodes.target'>
 <class 'docutils.nodes.pending'>
 <class 'docutils.nodes.image'>
 <class 'docutils.nodes.enumerated_list'>
 <class 'docutils.nodes.system_message'>
 <class 'docutils.nodes.document'>
 <class 'docutils.nodes.strong'>
 <class 'docutils.nodes.bullet_list'>
 <class 'docutils.nodes.literal_block'>

unsupport nodes in docutils: Unknown directive.
<rst-doc>:879: (ERROR/3) Unknown directive type "literalinclude".

.. literalinclude:: ../../../examples/Kaleidoscope/Chapter7/toy.cpp
   :language: c++

<rst-doc>:5: (ERROR/3) Unknown directive type "toctree".

.. toctree::
   :hidden:

   LangImpl01
   LangImpl02
   LangImpl03
   LangImpl04
   LangImpl05
   LangImpl06
   LangImpl07
   LangImpl08
   LangImpl09
   LangImpl10

<rst-doc>:355: (ERROR/3) Unknown interpreted text role "ref".
<rst-doc>:355: (ERROR/3) Unknown interpreted text role "ref".
<rst-doc>:810: (ERROR/3) Unknown directive type "literalinclude".

.. literalinclude:: ../../../examples/Kaleidoscope/Chapter5/toy.cpp
   :language: c++

<rst-doc>:495: (ERROR/3) Unknown directive type "TODO".

.. TODO:: Abandon Pygments' horrible `llvm` lexer. It just totally gives up
   on highlighting this due to the first line.

'''