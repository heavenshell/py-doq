import os
from unittest import TestCase

from doq import Template


class SphinxTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'doq',
            'templates',
            'sphinx',
        )
        cls.template = Template(paths=cls.path)

    def test_without_argument(self):
        params = {
            'name': 'foo',
            'params': [],
            'return_type': None,
        }
        actual = self.template.load(params=params, filename='noarg.txt')
        expected = '"""foo."""'

        self.assertEqual(expected, actual)

    def test_without_argument_and_return_type(self):
        params = {
            'name': 'foo',
            'params': [],
            'return_type': 'str',
        }
        actual = self.template.load(params=params, filename='def.txt')
        expected = '\n'.join([
            '"""foo.',
            '',
            ':rtype: str',
            '"""',
        ])
        self.assertEqual(expected, actual)

    def test_with_one_argument(self):
        params = {
            'name': 'foo',
            'params': [{
                'argument': 'arg1',
                'annotation': None,
                'default': None,
            }],
            'return_type': None,
        }
        actual = self.template.load(params=params, filename='def.txt')
        expected = '\n'.join(['"""foo.', '', ':param arg1:', '"""'])
        self.assertEqual(expected, actual)

    def test_with_one_argument_and_default(self):
        params = {
            'name': 'foo',
            'params': [{
                'argument': 'arg1',
                'annotation': None,
                'default': '\'foo\'',
            }],
            'return_type': None,
        }
        actual = self.template.load(params=params, filename='def.txt')
        expected = '\n'.join(['"""foo.', '', ':param arg1:', '"""'])
        self.assertEqual(expected, actual)

    def test_with_one_argument_and_annotaion(self):
        params = {
            'name': 'foo',
            'params': [{
                'argument': 'arg1',
                'annotation': 'str',
                'default': None,
            }],
            'return_type': None,
        }
        actual = self.template.load(params=params, filename='def.txt')
        expected = '\n'.join([
            '"""foo.',
            '',
            ':param arg1:',
            ':type arg1: str',
            '"""',
        ])
        self.assertEqual(expected, actual)

    def test_with_one_argument_annotation_and_return_type(self):
        params = {
            'name': 'foo',
            'params': [{
                'argument': 'arg1',
                'annotation': 'str',
                'default': None,
            }],
            'return_type': 'str',
        }
        actual = self.template.load(params=params, filename='def.txt')
        expected = '\n'.join([
            '"""foo.',
            '',
            ':param arg1:',
            ':type arg1: str',
            ':rtype: str',
            '"""',
        ])
        self.assertEqual(expected, actual)

    def test_with_two_arguments(self):
        params = {
            'name': 'foo',
            'params': [
                {
                    'argument': 'arg1',
                    'annotation': None,
                    'default': None,
                },
                {
                    'argument': 'arg2',
                    'annotation': None,
                    'default': None,
                },
            ],
            'return_type': None,
        }
        actual = self.template.load(params=params, filename='def.txt')
        expected = '\n'.join([
            '"""foo.',
            '',
            ':param arg1:',
            ':param arg2:',
            '"""',
        ])
        self.assertEqual(expected, actual)

    def test_with_two_arguments_and_defaults(self):
        params = {
            'name': 'foo',
            'params': [
                {
                    'argument': 'arg1',
                    'annotation': None,
                    'default': '\'foo\'',
                },
                {
                    'argument': 'arg2',
                    'annotation': None,
                    'default': 'None',
                },
            ],
            'return_type': None,
        }
        actual = self.template.load(params=params, filename='def.txt')
        expected = '\n'.join([
            '"""foo.',
            '',
            ':param arg1:',
            ':param arg2:',
            '"""',
        ])
        self.assertEqual(expected, actual)

    def test_with_two_arguments_and_annotation(self):
        params = {
            'name': 'foo',
            'params': [
                {
                    'argument': 'arg1',
                    'annotation': 'str',
                    'default': None,
                },
                {
                    'argument': 'arg2',
                    'annotation': 'int',
                    'default': None,
                },
            ],
            'return_type': None,
        }
        actual = self.template.load(params=params, filename='def.txt')
        expected = '\n'.join([
            '"""foo.',
            '',
            ':param arg1:',
            ':type arg1: str',
            ':param arg2:',
            ':type arg2: int',
            '"""',
        ])
        self.assertEqual(expected, actual)

    def test_with_two_arguments_annotation_and_defaults(self):
        params = {
            'name': 'foo',
            'params': [
                {
                    'argument': 'arg1',
                    'annotation': 'str',
                    'default': '\'foo\'',
                },
                {
                    'argument': 'arg2',
                    'annotation': 'int',
                    'default': 'None',
                },
            ],
            'return_type': None,
        }
        actual = self.template.load(params=params, filename='def.txt')
        expected = '\n'.join([
            '"""foo.',
            '',
            ':param arg1:',
            ':type arg1: str',
            ':param arg2:',
            ':type arg2: int',
            '"""',
        ])
        self.assertEqual(expected, actual)

    def test_with_two_arguments_annotation_defaults_and_return_type(self):
        params = {
            'name': 'foo',
            'params': [
                {
                    'argument': 'arg1',
                    'annotation': 'str',
                    'default': '\'foo\'',
                },
                {
                    'argument': 'arg2',
                    'annotation': 'int',
                    'default': 'None',
                },
            ],
            'return_type': 'str',
        }
        actual = self.template.load(params=params, filename='def.txt')
        expected = '\n'.join([
            '"""foo.',
            '',
            ':param arg1:',
            ':type arg1: str',
            ':param arg2:',
            ':type arg2: int',
            ':rtype: str',
            '"""',
        ])
        self.assertEqual(expected, actual)

    def test_class(self):
        params = {
            'name': 'foo',
            'defs': [
                {
                    'params': [],
                },
            ],
        }
        actual = self.template.load(params=params, filename='class.txt')
        expected = '"""foo."""\n'
        self.assertEqual(expected, actual)
