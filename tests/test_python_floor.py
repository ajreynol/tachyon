"""Every program here must parse on the oldest Python this repository claims.

The tool guides say Python 3.9+ and the CI workflow pins it. A developer's
interpreter is usually much newer, so syntax that only works on a later version passes locally
and fails in CI, which pins 3.9 -- exactly what happened with a backslash
inside an f-string expression, legal from 3.12 and a SyntaxError before it.
`ast.parse(feature_version=...)` does not catch that one, because the f-string
restriction lives in the tokenizer rather than the grammar, so this reads the
source instead.
"""
import ast
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
FLOOR = (3, 9)
# Extensionless programs: the report builders and the gap reader.
SHEBANG = re.compile(rb"^#!.*python")


def programs():
    listed = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).split()
    for name in listed:
        path = ROOT / name
        if name.endswith(".py"):
            yield name, path
        elif path.is_file() and SHEBANG.match(path.read_bytes()[:64] or b""):
            yield name, path


class PythonFloorTests(unittest.TestCase):
    def setUp(self):
        self.programs = sorted(programs())
        self.assertGreater(len(self.programs), 10, "the program list stopped finding anything")

    def test_every_program_parses(self):
        for name, path in self.programs:
            with self.subTest(program=name):
                ast.parse(path.read_text(), filename=name, feature_version=FLOOR)

    def test_no_f_string_expression_uses_syntax_newer_than_the_floor(self):
        """A backslash, or the enclosing quote reused, inside `{...}`: 3.12+ only."""
        for name, path in self.programs:
            source = path.read_text()
            for node in ast.walk(ast.parse(source, filename=name)):
                if not isinstance(node, ast.JoinedStr):
                    continue
                literal = ast.get_source_segment(source, node) or ""
                # The opening quote is what may not be reused, so read it past
                # the f/r/b prefix rather than looking for whichever appears.
                body = literal.lstrip("fFrRbBuU")
                opened = body[:3] if body[:3] in ('"""', "'''") else body[:1]
                for part in node.values:
                    if not isinstance(part, ast.FormattedValue):
                        continue
                    expression = ast.get_source_segment(source, part.value) or ""
                    with self.subTest(program=name, line=part.value.lineno):
                        self.assertNotIn("\\", expression,
                                         "a backslash in an f-string expression needs Python 3.12")
                        self.assertNotIn(opened, expression,
                                         "reusing the f-string's own quote needs Python 3.12")


if __name__ == "__main__":
    unittest.main()
