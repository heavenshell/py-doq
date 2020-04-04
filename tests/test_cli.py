import argparse
import os
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from parameterized import parameterized

from doq.cli import (
    find_files,
    generate_docstrings,
    get_lines,
    get_targets,
    get_template_path,
    run,
)


class CliTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = [
            'async.txt',
            'class.txt',
            'classes.txt',
            'defs.txt',
            'issues.txt',
            'mix.txt',
            'nested.txt',
            'nested_classes.txt',
            'nested_defs.txt',
            'return_type.txt',
        ]
        cls.ignore_files = [
            'exists.txt',
        ]
        cls.basepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.fixtures_path = os.path.join(cls.basepath, 'tests', 'fixtures')

    def test_output_with_sphinx_style(self):
        expected_path = os.path.join(self.basepath, 'tests', 'expected', 'sphinx')
        for file in self.files:
            with open(os.path.join(self.fixtures_path, file)) as f:
                args = argparse.Namespace(
                    file=f,
                    start=1,
                    end=0,
                    template_path=None,
                    formatter='sphinx',
                    style='string',
                    indent=4,
                    recursive=False,
                    write=False,
                    omit=None,
                    ignore_exception=False,
                    ignore_yield=False,
                )
                with patch('doq.cli.sys.stdout', new_callable=StringIO) as p:
                    run(args)
            actual = p.getvalue().split('\n')
            with open(os.path.join(expected_path, file)) as f:
                expected = f.read().rstrip().split('\n')

            self.assertSequenceEqual(expected, actual)

    def test_no_output_with_sphinx_style(self):
        for file in self.ignore_files:
            with open(os.path.join(self.fixtures_path, file)) as f:
                args = argparse.Namespace(
                    file=f,
                    start=1,
                    end=0,
                    template_path=None,
                    formatter='sphinx',
                    style='string',
                    indent=4,
                    recursive=False,
                    write=False,
                    omit=None,
                    ignore_exception=False,
                    ignore_yield=False,
                )
                with patch('doq.cli.sys.stdout', new_callable=StringIO) as p:
                    run(args)
            actual = p.getvalue().split('\n')
            self.assertSequenceEqual([''], actual)

    def test_output_with_google_style(self):
        expected_path = os.path.join(self.basepath, 'tests', 'expected', 'google')

        for file in self.files:
            with open(os.path.join(self.fixtures_path, file)) as f:
                args = argparse.Namespace(
                    file=f,
                    start=1,
                    end=0,
                    template_path=None,
                    formatter='google',
                    style='string',
                    indent=4,
                    recursive=False,
                    write=False,
                    omit=None,
                    ignore_exception=False,
                    ignore_yield=False,
                )
                with patch('doq.cli.sys.stdout', new_callable=StringIO) as p:
                    run(args)
            actual = p.getvalue().split('\n')
            with open(os.path.join(expected_path, file)) as f:
                expected = f.read().rstrip().split('\n')

            self.assertSequenceEqual(expected, actual)

    def test_no_output_with_google_style(self):
        for file in self.ignore_files:
            with open(os.path.join(self.fixtures_path, file)) as f:
                args = argparse.Namespace(
                    file=f,
                    start=1,
                    end=0,
                    template_path=None,
                    formatter='google',
                    style='string',
                    indent=4,
                    recursive=False,
                    write=False,
                    omit=None,
                    ignore_exception=False,
                    ignore_yield=False,
                )
                with patch('doq.cli.sys.stdout', new_callable=StringIO) as p:
                    run(args)
            actual = p.getvalue().split('\n')
            self.assertSequenceEqual([''], actual)

    def test_output_with_numpy_style(self):
        expected_path = os.path.join(self.basepath, 'tests', 'expected', 'numpy')

        for file in self.files:
            with open(os.path.join(self.fixtures_path, file)) as f:
                args = argparse.Namespace(
                    file=f,
                    start=1,
                    end=0,
                    template_path=None,
                    formatter='numpy',
                    style='string',
                    indent=4,
                    recursive=False,
                    write=False,
                    omit=None,
                    ignore_exception=False,
                    ignore_yield=False,
                )
                with patch('doq.cli.sys.stdout', new_callable=StringIO) as p:
                    run(args)
            actual = p.getvalue().split('\n')
            with open(os.path.join(expected_path, file)) as f:
                expected = f.read().rstrip().split('\n')

            self.assertSequenceEqual(expected, actual)

    def test_no_output_with_numpy_style(self):
        for file in self.ignore_files:
            with open(os.path.join(self.fixtures_path, file)) as f:
                args = argparse.Namespace(
                    file=f,
                    start=1,
                    end=0,
                    template_path=None,
                    formatter='numpy',
                    style='string',
                    indent=4,
                    recursive=False,
                    write=False,
                    omit=None,
                    ignore_exception=False,
                    ignore_yield=False,
                )
                with patch('doq.cli.sys.stdout', new_callable=StringIO) as p:
                    run(args)
            actual = p.getvalue().split('\n')
            self.assertSequenceEqual([''], actual)

    def test_find_files(self):
        files = find_files('.')
        for f in files:
            self.assertTrue(f.endswith('.py'))

    def test_no_files(self):
        files = find_files('./fixtures')
        self.assertEqual(0, len(files))

    def test_get_lines(self):
        path = os.path.join(self.fixtures_path, 'defs.txt')
        with open(path) as f:
            expected = [l.rstrip() for l in f.readlines()]

        with open(path) as f:
            actual = get_lines(f, 1, 0)
            self.assertEqual(expected, actual)

    @parameterized.expand(['sphinx', 'google', 'numpy'])
    def test_get_defalt_template_path(self, formatter):
        expected_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'doq',
            'templates',
            formatter,
        )
        path = get_template_path(template_path=None, formatter=formatter)
        self.assertEqual(expected_path, path)

    def test_get_template_path(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template_path = os.path.join(base, 'examples')

        path = get_template_path(template_path=template_path, formatter=None)
        self.assertEqual(template_path, path)

    def test_get_target(self):
        target_file = os.path.join(
            self.basepath,
            'doq',
            'template.py',
        )
        with open(target_file) as f:
            args = argparse.Namespace(
                file=f,
                start=1,
                end=0,
                template_path=None,
                formatter='sphinx',
                style='string',
                indent=4,
                recursive=False,
                write=False,
                omit=None,
                ignore_exception=False,
                ignore_yield=False,
            )
            targets = get_targets(args)
            self.assertEqual(1, len(targets))

    def test_run_with_defs(self):
        docstrings = [
            'def foo(arg1):',
            '   pass',
            '',
            '',
            'def bar(arg1, arg2):',
            '   pass',
        ]
        template_path = os.path.join(
            self.basepath,
            'doq',
            'templates',
            'sphinx',
        )

        expected_docstrings = [
            [
                '"""foo.',
                '',
                ':param arg1:',
                '"""',
            ],
            [
                '"""bar.',
                '',
                ':param arg1:',
                ':param arg2:',
                '"""',
            ],
        ]
        results = generate_docstrings(docstrings, template_path)
        self.assertEqual(
            '\n'.join(expected_docstrings[0]),
            results[0]['docstring'],
        )
        self.assertEqual(0, results[0]['start_col'])
        self.assertEqual(0, results[0]['end_col'])
        self.assertEqual(1, results[0]['start_lineno'])
        self.assertEqual(3, results[0]['end_lineno'])
        self.assertEqual(
            '\n'.join(expected_docstrings[1]),
            results[1]['docstring'],
        )
        self.assertEqual(0, results[1]['start_col'])
        self.assertEqual(0, results[1]['end_col'])
        self.assertEqual(5, results[1]['start_lineno'])
        self.assertEqual(6, results[1]['end_lineno'])

    def test_run_with_classes(self):
        docstrings = [
            'class Foo:',
            '   def foo(arg1):',
            '       pass',
            '',
            '',
            'class Bar:',
            '   def bar(arg1, arg2):',
            '      pass',
        ]
        template_path = os.path.join(
            self.basepath,
            'doq',
            'templates',
            'sphinx',
        )
        expected = [
            {
                'docstring': ['"""Foo."""', ''],
                'start_col': 0,
                'end_col': 0,
                'start_lineno': 1,
                'end_lineno': 4,
            },
            {
                'docstring': [
                    '"""foo.',
                    '',
                    ':param arg1:',
                    '"""',
                ],
                'start_col': 3,
                'end_col': 3,
                'start_lineno': 2,
                'end_lineno': 4,
            },
            {
                'docstring': ['"""Bar."""', ''],
                'start_col': 0,
                'end_col': 10,
                'start_lineno': 6,
                'end_lineno': 8,
            },
            {
                'docstring': [
                    '"""bar.',
                    '',
                    ':param arg1:',
                    ':param arg2:',
                    '"""',
                ],
                'start_col': 3,
                'end_col': 3,
                'start_lineno': 7,
                'end_lineno': 8,
            },
        ]
        results = generate_docstrings(docstrings, template_path)
        for k, v in enumerate(results):
            self.assertEqual(
                '\n'.join(expected[k]['docstring']),
                v['docstring'],
            )
            self.assertEqual(expected[k]['start_col'], v['start_col'])
            self.assertEqual(expected[k]['end_col'], v['end_col'])
            self.assertEqual(expected[k]['start_lineno'], v['start_lineno'])
            self.assertEqual(expected[k]['end_lineno'], v['end_lineno'])

    def test_is_doc_exists(self):
        docstrings = [
            'def foo(arg1):',
            '   """foo.',
            '',
            '   :param arg1',
            '   pass',
        ]
        template_path = os.path.join(
            self.basepath,
            'doq',
            'templates',
            'sphinx',
        )

        expected_docstrings = [
            [
                '"""foo.',
                '',
                ':param arg1:',
                '"""',
            ],
        ]
        results = generate_docstrings(docstrings, template_path)
        self.assertEqual(
            '\n'.join(expected_docstrings[0]),
            results[0]['docstring'],
        )
        self.assertEqual(0, results[0]['start_col'])
        self.assertEqual(0, results[0]['end_col'])
        self.assertEqual(1, results[0]['start_lineno'])
        self.assertEqual(5, results[0]['end_lineno'])

    def test_omit_one(self):
        docstrings = [
            'def foo(self, arg1):',
            '   """foo.',
            '',
            '   :param arg1',
            '   pass',
        ]

        template_path = os.path.join(
            self.basepath,
            'doq',
            'templates',
            'sphinx',
        )
        results = generate_docstrings(
            docstrings,
            template_path,
            omissions=['self'],
        )
        expected_docstrings = [
            [
                '"""foo.',
                '',
                ':param arg1:',
                '"""',
            ],
        ]
        self.assertEqual(
            '\n'.join(expected_docstrings[0]),
            results[0]['docstring'],
        )
        self.assertEqual(0, results[0]['start_col'])
        self.assertEqual(0, results[0]['end_col'])
        self.assertEqual(1, results[0]['start_lineno'])
        self.assertEqual(5, results[0]['end_lineno'])

    def test_omit_two(self):
        docstrings = [
            'def foo(self, arg1):',
            '   pass',
            '',
            '',
            'def bar(cls, arg1):',
            '   pass',
        ]

        template_path = os.path.join(
            self.basepath,
            'doq',
            'templates',
            'sphinx',
        )
        results = generate_docstrings(
            docstrings,
            template_path,
            omissions=['self', 'cls'],
        )

        expected_docstrings = [
            [
                '"""foo.',
                '',
                ':param arg1:',
                '"""',
            ],
            [
                '"""bar.',
                '',
                ':param arg1:',
                '"""',
            ],
        ]
        self.assertEqual(
            '\n'.join(expected_docstrings[0]),
            results[0]['docstring'],
        )
        self.assertEqual(0, results[0]['start_col'])
        self.assertEqual(0, results[0]['end_col'])
        self.assertEqual(1, results[0]['start_lineno'])
        self.assertEqual(3, results[0]['end_lineno'])
        self.assertEqual(
            '\n'.join(expected_docstrings[1]),
            results[1]['docstring'],
        )
        self.assertEqual(0, results[1]['start_col'])
        self.assertEqual(0, results[1]['end_col'])
        self.assertEqual(5, results[1]['start_lineno'])
        self.assertEqual(6, results[1]['end_lineno'])

    def test_not_ignore_exception(self):
        docstrings = [
            'def foo(arg1):',
            '   raise Exception()',
        ]

        template_path = os.path.join(
            self.basepath,
            'examples',
        )
        results = generate_docstrings(
            docstrings,
            template_path,
            omissions=['self'],
            ignore_exception=False,
        )
        expected_docstrings = [
            [
                '"""Summary of foo.',
                '',
                'Args:',
                '    arg1',
                '',
                'Raises:',
                '    Exception:',
                '"""',
            ],
        ]
        self.assertEqual(
            '\n'.join(expected_docstrings[0]),
            results[0]['docstring'],
        )
        self.assertEqual(0, results[0]['start_col'])
        self.assertEqual(0, results[0]['end_col'])
        self.assertEqual(1, results[0]['start_lineno'])
        self.assertEqual(2, results[0]['end_lineno'])

    def test_not_ignore_yield(self):
        docstrings = [
            'def foo(arg1):',
            '   for i in range(10):',
            '       yield i',
        ]

        template_path = os.path.join(
            self.basepath,
            'examples',
        )
        results = generate_docstrings(
            docstrings,
            template_path,
            omissions=['self'],
            ignore_exception=False,
            ignore_yield=False,
        )
        expected_docstrings = [
            [
                '"""Summary of foo.',
                '',
                'Args:',
                '    arg1',
                '',
                'Yields:',
                '    i:',
                '"""',
            ],
        ]
        self.assertEqual(
            '\n'.join(expected_docstrings[0]),
            results[0]['docstring'],
        )
        self.assertEqual(0, results[0]['start_col'])
        self.assertEqual(0, results[0]['end_col'])
        self.assertEqual(1, results[0]['start_lineno'])
        self.assertEqual(3, results[0]['end_lineno'])
