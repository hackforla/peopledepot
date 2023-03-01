from docutils import nodes
from docutils.parsers.rst.directives.parts import Sectnum as SectnumDirective
from docutils.transforms.parts import SectNum as SectnumTransform


class Sectnum(SectnumDirective):
    """
    Override the Sectnum directive to call my own Sectnum transform
    """

    def run(self):
        pending = nodes.pending(SectNumTrans)
        pending.details.update(self.options)
        self.state_machine.document.note_pending(pending)
        return [pending]


class SectNumTrans(SectnumTransform):
    """
    Override `Sectnum` from docutils

    I do not want the big title of the page to be numbered:

        Document Name

        1. Section
           1.1. Subsection

    And not

        1. Document Name

        1.1 Section
           1.1.1. Subsection

    """

    start_depth = 1

    def update_section_numbers(self, node, prefix=(), depth=0, level=0):  # noqa: C901
        self.suffix = "."
        depth += 1
        if prefix:
            sectnum = 1
        else:
            sectnum = self.startvalue
        level += 1
        for child in node:
            if isinstance(child, nodes.section):
                title = child[0]

                if level > self.start_depth:
                    numbers = prefix + (str(sectnum),)
                    text = self.prefix + ".".join(numbers) + self.suffix + "\u00a0" * 2
                else:
                    numbers = prefix
                    text = ""

                generated = nodes.generated("", text, classes=["sectnum"])
                title.insert(0, generated)
                title["auto"] = 1
                if depth < self.maxdepth:
                    self.update_section_numbers(child, numbers, depth, level)
                sectnum += 1


def setup(app):
    app.add_directive("sectnum", Sectnum)
    return {"version": "0.1"}
