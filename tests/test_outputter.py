import json
from unittest import TestCase

from doq import (
    JSONOutputter,
    StringOutptter,
)


class StringOutptterTestCase(TestCase):
    def test_same_lines(self):
        lines = [
            'def foo(arg1, arg2=None):',
            '    pass',
        ]
        docstrings = [{
            'docstring': '"""foo.\n\n:param arg1:\n:param arg2:\n"""',
            'start_lineno': 1,
            'start_col': 0,
            'end_lineno': 2,
            'end_col': 0,
            'is_doc_exists': False,
        }]
        output = StringOutptter().format(lines=lines, docstrings=docstrings, indent=4)
        expected = '\n'.join([
            'def foo(arg1, arg2=None):',
            '    """foo.',
            '',
            '    :param arg1:',
            '    :param arg2:',
            '    """',
            '    pass',
        ])
        self.assertEqual(expected, output)

    def test_multi_lines(self):
        lines = [
            'def foo(',
            '    arg1,',
            '    arg2=None,',
            '    arg3=None,',
            "    arg4={'foo': 'spam', 'bar': 'ham'},",
            '):',
            '    pass',
        ]

        docstrings = [{
            'docstring': '"""foo.\n\n:param arg1:\n:param arg2:\n:param arg3:\n:param arg4:\n"""',
            'start_lineno': 1,
            'start_col': 0,
            'end_lineno': 8,
            'end_col': 0,
            'is_doc_exists': False,
        }]
        output = StringOutptter().format(lines=lines, docstrings=docstrings, indent=4)
        expected = '\n'.join([
            'def foo(',
            '    arg1,',
            '    arg2=None,',
            '    arg3=None,',
            "    arg4={'foo': 'spam', 'bar': 'ham'},",
            '):',
            '    """foo.',
            '',
            '    :param arg1:',
            '    :param arg2:',
            '    :param arg3:',
            '    :param arg4:',
            '    """',
            '    pass',
        ])
        self.assertEqual(expected, output)

    def test_multi_lines_with_space(self):
        lines = [
            'def foo(',
            '    arg1,',
            '    arg2,',
            '    arg3,',
            ') :',
            '    pass',
        ]

        docstrings = [{
            'docstring': '"""foo.\n\n:param arg1:\n:param arg2:\n:param arg3:\n"""',
            'start_lineno': 1,
            'start_col': 0,
            'end_lineno': 8,
            'end_col': 0,
            'is_doc_exists': False,
        }]
        output = StringOutptter().format(lines=lines, docstrings=docstrings, indent=4)
        expected = '\n'.join([
            'def foo(',
            '    arg1,',
            '    arg2,',
            '    arg3,',
            ') :',
            '    """foo.',
            '',
            '    :param arg1:',
            '    :param arg2:',
            '    :param arg3:',
            '    """',
            '    pass',
        ])
        self.assertEqual(expected, output)

    def test_multi_lines_with_space_and_return_type(self):
        lines = [
            'def foo(',
            '    arg1,',
            '    arg2,',
            '    arg3,',
            ') -> int :',
            '    pass',
        ]

        docstrings = [{
            'docstring': '"""foo.\n\n:param arg1:\n:param arg2:\n:param arg3:\n:rtype: int\n"""',
            'start_lineno': 1,
            'start_col': 0,
            'end_lineno': 8,
            'end_col': 0,
            'is_doc_exists': False,
        }]
        output = StringOutptter().format(lines=lines, docstrings=docstrings, indent=4)
        expected = '\n'.join([
            'def foo(',
            '    arg1,',
            '    arg2,',
            '    arg3,',
            ') -> int :',
            '    """foo.',
            '',
            '    :param arg1:',
            '    :param arg2:',
            '    :param arg3:',
            '    :rtype: int',
            '    """',
            '    pass',
        ])
        self.assertEqual(expected, output)

    def test_multi_lines_with_return_type(self):
        lines = [
            'def foo(',
            '    arg1,',
            '    arg2=None,',
            "    arg3={'foo': 'spam', 'bar': 'ham'},",
            ') -> List[int]:',
            '    pass',
        ]

        docstrings = [{
            'docstring': '"""foo.\n\n:param arg1:\n:param arg2:\n:param arg3:\n:rtype List[int]:\n"""',
            'start_lineno': 1,
            'start_col': 0,
            'end_lineno': 7,
            'end_col': 0,
            'is_doc_exists': False,
        }]
        output = StringOutptter().format(lines=lines, docstrings=docstrings, indent=4)
        expected = '\n'.join([
            'def foo(',
            '    arg1,',
            '    arg2=None,',
            "    arg3={'foo': 'spam', 'bar': 'ham'},",
            ') -> List[int]:',
            '    """foo.',
            '',
            '    :param arg1:',
            '    :param arg2:',
            '    :param arg3:',
            '    :rtype List[int]:',
            '    """',
            '    pass',
        ])
        self.assertEqual(expected, output)

    def test_multi_return_type(self):
        lines = [
            'def foo(arg1) -> List[',
            '    int,',
            '    int,',
            ']:',
            '    pass',
        ]
        docstrings = [{
            'docstring': '"""foo.\n\n:param arg1:\n:rtype List[\n    int,\n    int,\n]:\n"""',
            'start_lineno': 1,
            'start_col': 0,
            'end_lineno': 7,
            'end_col': 0,
            'is_doc_exists': False,
        }]
        output = StringOutptter().format(lines=lines, docstrings=docstrings, indent=4)
        expected = '\n'.join([
            'def foo(arg1) -> List[',
            '    int,',
            '    int,',
            ']:',
            '    """foo.',
            '',
            '    :param arg1:',
            '    :rtype List[',
            '        int,',
            '        int,',
            '    ]:',
            '    """',
            '    pass',
        ])
        self.assertEqual(expected, output)


class JSONOutptterTestCase(TestCase):
    def test_same_lines(self):
        lines = [
            'def foo(arg1, arg2=None):',
            '    pass',
        ]
        docstrings = [{
            'docstring': '"""foo.\n\n:param arg1:\n:param arg2:\n"""',
            'start_lineno': 1,
            'start_col': 0,
            'end_lineno': 2,
            'end_col': 0,
            'is_doc_exists': False,
        }]
        output = JSONOutputter().format(
            lines=lines,
            docstrings=docstrings,
            indent=4,
        )

        expected = [{
            'docstring': '\n'.join([
                '    """foo.',
                '',
                '    :param arg1:',
                '    :param arg2:',
                '    """',
            ]),
            'start_col': 4,
            'start_lineno': 1,
            'end_col': 0,
            'end_lineno': 2,
        }]
        self.assertEqual(json.dumps(expected), output)
