from unittest import TestCase

from parameterized import parameterized

from doq.parser import (
    get_return_type,
    parse,
    parse_return_type,
)


class ParseTestCase(TestCase):
    def test_without_argument(self):
        line = """def foo(): pass"""

        actual = parse(line)[0]
        self.assertDictEqual(
            {
                'name': 'foo',
                'params': [],
                'return_type': None,
                'start_lineno': 1,
                'start_col': 0,
                'end_lineno': 1,
                'end_col': len(line),
                'is_doc_exists': False,
            },
            actual,
        )

    def test_with_one_argument(self):
        line = """def foo(arg1): pass"""

        actual = parse(line)[0]
        self.assertDictEqual(
            {
                'name': 'foo',
                'params': [{
                    'argument': 'arg1',
                    'annotation': None,
                    'default': None,
                }],
                'return_type': None,
                'start_lineno': 1,
                'start_col': 0,
                'end_lineno': 1,
                'end_col': len(line),
                'is_doc_exists': False,
            },
            actual,
        )

    def test_with_one_argument_and_default(self):
        line = """def foo(arg1='foo'): pass"""

        actual = parse(line)[0]
        self.assertDictEqual(
            {
                'name': 'foo',
                'params': [{
                    'argument': 'arg1',
                    'annotation': None,
                    'default': '\'foo\'',
                }],
                'return_type': None,
                'start_lineno': 1,
                'start_col': 0,
                'end_lineno': 1,
                'end_col': len(line),
                'is_doc_exists': False,
            },
            actual,
        )

    def test_with_one_argument_and_annotaion(self):
        line = """def foo(arg1: str): pass"""
        actual = parse(line)[0]
        self.assertDictEqual(
            {
                'name': 'foo',
                'params': [{
                    'argument': 'arg1',
                    'annotation': 'str',
                    'default': None,
                }],
                'return_type': None,
                'start_lineno': 1,
                'start_col': 0,
                'end_lineno': 1,
                'end_col': len(line),
                'is_doc_exists': False,
            },
            actual,
        )

    def test_with_one_argument_annotaion_and_default(self):
        line = """def foo(arg1: str='bar'): pass"""
        actual = parse(line)[0]
        self.assertDictEqual(
            {
                'name': 'foo',
                'params': [{
                    'argument': 'arg1',
                    'annotation': 'str',
                    'default': '\'bar\'',
                }],
                'return_type': None,
                'start_lineno': 1,
                'start_col': 0,
                'end_lineno': 1,
                'end_col': len(line),
                'is_doc_exists': False,
            },
            actual,
        )

    def test_with_args(self):
        line = """def foo(*args): pass"""
        actual = parse(line)[0]
        self.assertDictEqual(
            {
                'name': 'foo',
                'params': [{
                    'argument': 'args',
                    'annotation': None,
                    'default': None,
                }],
                'return_type': None,
                'start_lineno': 1,
                'start_col': 0,
                'end_lineno': 1,
                'end_col': len(line),
                'is_doc_exists': False,
            },
            actual,
        )

    def test_with_kwargs(self):
        line = """def foo(**kwargs): pass"""
        actual = parse(line)[0]
        self.assertDictEqual(
            {
                'name': 'foo',
                'params': [{
                    'argument': 'kwargs',
                    'annotation': None,
                    'default': None,
                }],
                'return_type': None,
                'start_lineno': 1,
                'start_col': 0,
                'end_lineno': 1,
                'end_col': len(line),
                'is_doc_exists': False,
            },
            actual,
        )

    def test_with_two_arguments(self):
        line = """def foo(arg1, arg2): pass"""
        actual = parse(line)[0]
        self.assertDictEqual(
            {
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
                'start_lineno': 1,
                'start_col': 0,
                'end_lineno': 1,
                'end_col': len(line),
                'is_doc_exists': False,
            },
            actual,
        )

    def test_with_args_and_kwargs(self):
        line = """def foo(*args, **kwargs): pass"""
        actual = parse(line)[0]
        self.assertDictEqual(
            {
                'name': 'foo',
                'params': [
                    {
                        'argument': 'args',
                        'annotation': None,
                        'default': None,
                    },
                    {
                        'argument': 'kwargs',
                        'annotation': None,
                        'default': None,
                    },
                ],
                'return_type': None,
                'start_lineno': 1,
                'start_col': 0,
                'end_lineno': 1,
                'end_col': len(line),
                'is_doc_exists': False,
            },
            actual,
        )

    def test_with_two_arguments_with_default(self):
        fixtures = [
            {
                'given': """def foo(arg1, arg2=None): pass""",
                'expected': {
                    'name': 'foo',
                    'params': [
                        {
                            'argument': 'arg1',
                            'annotation': None,
                            'default': None,
                        }, {
                            'argument': 'arg2',
                            'annotation': None,
                            'default': 'None',
                        },
                    ],
                    'return_type': None,
                    'start_lineno': 1,
                    'start_col': 0,
                    'end_lineno': 1,
                    'end_col': 30,
                    'is_doc_exists': False,
                },
            },
            {
                'given': """def foo(arg1='foo', arg2=None): pass""",
                'expected': {
                    'name': 'foo',
                    'params': [
                        {
                            'argument': 'arg1',
                            'annotation': None,
                            'default': '\'foo\'',
                        }, {
                            'argument': 'arg2',
                            'annotation': None,
                            'default': 'None',
                        },
                    ],
                    'return_type': None,
                    'return_type': None,
                    'start_lineno': 1,
                    'start_col': 0,
                    'end_lineno': 1,
                    'end_col': 36,
                    'is_doc_exists': False,
                },
            },
        ]
        for fixture in fixtures:
            actual = parse(fixture['given'])[0]
            self.assertDictEqual(fixture['expected'], actual)

    def test_with_two_arguments_with_annotation(self):
        fixtures = [
            {
                'given': """def foo(arg1, arg2: str): pass""",
                'expected': {
                    'name': 'foo',
                    'params': [
                        {
                            'argument': 'arg1',
                            'annotation': None,
                            'default': None,
                        }, {
                            'argument': 'arg2',
                            'annotation': 'str',
                            'default': None,
                        },
                    ],
                    'return_type': None,
                    'start_lineno': 1,
                    'start_col': 0,
                    'end_lineno': 1,
                    'end_col': 30,
                    'is_doc_exists': False,
                },
            },
            {
                'given': """def foo(arg1: str, arg2: Callable[List[init]]): pass""",
                'expected': {
                    'name': 'foo',
                    'params': [
                        {
                            'argument': 'arg1',
                            'annotation': 'str',
                            'default': None,
                        }, {
                            'argument': 'arg2',
                            'annotation': 'Callable[List[init]]',
                            'default': None,
                        },
                    ],
                    'return_type': None,
                    'start_lineno': 1,
                    'start_col': 0,
                    'end_lineno': 1,
                    'end_col': 52,
                    'is_doc_exists': False,
                },
            },
        ]
        for fixture in fixtures:
            actual = parse(fixture['given'])[0]
            self.assertDictEqual(fixture['expected'], actual)

    def test_with_two_arguments_with_annotation_and_default(self):
        fixtures = [
            {
                'given': """def foo(arg1: str='foo', arg2: str): pass""",
                'expected': {
                    'name': 'foo',
                    'params': [
                        {
                            'argument': 'arg1',
                            'annotation': 'str',
                            'default': '\'foo\'',
                        }, {
                            'argument': 'arg2',
                            'annotation': 'str',
                            'default': None,
                        },
                    ],
                    'return_type': None,
                    'start_lineno': 1,
                    'start_col': 0,
                    'end_lineno': 1,
                    'end_col': 41,
                    'is_doc_exists': False,
                },
            },
            {
                'given': """def foo(arg1: str='foo', arg2: str=None): pass""",
                'expected': {
                    'name': 'foo',
                    'params': [
                        {
                            'argument': 'arg1',
                            'annotation': 'str',
                            'default': '\'foo\'',
                        }, {
                            'argument': 'arg2',
                            'annotation': 'str',
                            'default': 'None',
                        },
                    ],
                    'return_type': None,
                    'start_lineno': 1,
                    'start_col': 0,
                    'end_lineno': 1,
                    'end_col': 46,
                    'is_doc_exists': False,
                },
            },
        ]
        for fixture in fixtures:
            actual = parse(fixture['given'])[0]
            self.assertDictEqual(fixture['expected'], actual)

    def test_with_two_arguments_with_asterisk(self):
        fixtures = [
            {
                'given': """def foo(arg1: str='foo', *, arg2: str='foo'): pass""",
                'expected': {
                    'name': 'foo',
                    'params': [
                        {
                            'argument': 'arg1',
                            'annotation': 'str',
                            'default': '\'foo\'',
                        }, {
                            'argument': 'arg2',
                            'annotation': 'str',
                            'default': '\'foo\'',
                        },
                    ],
                    'return_type': None,
                    'start_lineno': 1,
                    'start_col': 0,
                    'end_lineno': 1,
                    'end_col': 50,
                    'is_doc_exists': False,
                },
            },
            {
                'given': """def foo(arg1: str='foo', arg2: str=None): pass""",
                'expected': {
                    'name': 'foo',
                    'params': [
                        {
                            'argument': 'arg1',
                            'annotation': 'str',
                            'default': '\'foo\'',
                        }, {
                            'argument': 'arg2',
                            'annotation': 'str',
                            'default': 'None',
                        },
                    ],
                    'return_type': None,
                    'start_lineno': 1,
                    'start_col': 0,
                    'end_lineno': 1,
                    'end_col': 46,
                    'is_doc_exists': False,
                },
            },
        ]
        for fixture in fixtures:
            actual = parse(fixture['given'])[0]
            self.assertDictEqual(fixture['expected'], actual)

    def test_with_return_type(self):
        line = """def foo(arg1) -> List[str]: pass"""
        actual = parse(line)[0]
        self.assertDictEqual(
            {
                'name': 'foo',
                'params': [
                    {
                        'argument': 'arg1',
                        'annotation': None,
                        'default': None,
                    },
                ],
                'return_type': 'List[str]',
                'start_lineno': 1,
                'start_col': 0,
                'end_lineno': 1,
                'end_col': 32,
                'is_doc_exists': False,
            },
            actual,
        )

    def test_with_defs(self):
        line = '\n'.join([
            'def bar(arg1) -> List[str]:',
            '    pass',
            '',
            '',
            'def foo(arg1, arg2):',
            '    pass',
        ])

        actual = parse(line)
        self.assertDictEqual(
            {
                'name': 'bar',
                'params': [
                    {
                        'argument': 'arg1',
                        'annotation': None,
                        'default': None,
                    },
                ],
                'return_type': 'List[str]',
                'start_lineno': 1,
                'start_col': 0,
                'end_lineno': 3,
                'end_col': 0,
                'is_doc_exists': False,
            },
            actual[0],
        )

        self.assertDictEqual(
            {
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
                'start_lineno': 5,
                'start_col': 0,
                'end_lineno': 6,
                'end_col': 8,
                'is_doc_exists': False,
            },
            actual[1],
        )

    def test_with_class(self):
        line = '\n'.join([
            'class Foo:',
            '   def bar(self, arg1) -> List[str]:',
            '       pass',
            '   def foo(self, arg1, arg2):',
            '       pass',
        ])

        actual = parse(line)[0]
        self.assertDictEqual(
            {
                'name': 'Foo',
                'defs': [
                    {
                        'name': 'bar',
                        'params': [
                            {
                                'argument': 'arg1',
                                'annotation': None,
                                'default': None,
                            },
                        ],
                        'return_type': 'List[str]',
                        'start_lineno': 2,
                        'start_col': 3,
                        'end_lineno': 4,
                        'end_col': 0,
                        'is_doc_exists': False,
                    },
                    {
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
                        'start_lineno': 4,
                        'start_col': 3,
                        'end_lineno': 5,
                        'end_col': 11,
                        'is_doc_exists': False,
                    },
                ],
                'start_lineno': 1,
                'start_col': 0,
                'end_lineno': 5,
                'end_col': 11,
                'is_doc_exists': False,
            },
            actual,
        )

    def test_with_classes(self):
        line = '\n'.join([
            'class Foo:',
            '   def bar(self, arg1) -> List[str]:',
            '       pass',
            '   def foo(self, arg1, arg2):',
            '       pass',
            '',
            '',
            'class Bar:',
            '   def foo(self, arg1, arg2):',
            '       pass',
            '   def bar(self, arg1) -> List[str]:',
            '       pass',
        ])

        actual = parse(line)
        self.assertDictEqual(
            {
                'name': 'Foo',
                'defs': [
                    {
                        'name': 'bar',
                        'params': [
                            {
                                'argument': 'arg1',
                                'annotation': None,
                                'default': None,
                            },
                        ],
                        'return_type': 'List[str]',
                        'start_lineno': 2,
                        'start_col': 3,
                        'end_lineno': 4,
                        'end_col': 0,
                        'is_doc_exists': False,
                    },
                    {
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
                        'start_lineno': 4,
                        'start_col': 3,
                        'end_lineno': 6,
                        'end_col': 0,
                        'is_doc_exists': False,
                    },


                ],
                'start_lineno': 1,
                'start_col': 0,
                'end_lineno': 6,
                'end_col': 0,
                'is_doc_exists': False,
            },
            actual[0],
        )

        self.assertDictEqual(
            {
                'name': 'Bar',
                'defs': [
                    {
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
                        'start_lineno': 9,
                        'start_col': 3,
                        'end_lineno': 11,
                        'end_col': 0,
                        'is_doc_exists': False,
                    },
                    {
                        'name': 'bar',
                        'params': [
                            {
                                'argument': 'arg1',
                                'annotation': None,
                                'default': None,
                            },
                        ],
                        'return_type': 'List[str]',
                        'start_lineno': 11,
                        'start_col': 3,
                        'end_lineno': 12,
                        'end_col': 11,
                        'is_doc_exists': False,
                    },
                ],
                'start_lineno': 8,
                'start_col': 0,
                'end_lineno': 12,
                'end_col': 11,
                'is_doc_exists': False,
            },
            actual[1],
        )

    def test_doc_exists(self):
        line = '\n'.join([
            'def foo(arg1):',
            '   """foo.'
            '',
            '   :param arg1',
            '   """',
            '   pass',
        ])

        actual = parse(line)[0]
        self.assertDictEqual(
            {
                'name': 'foo',
                'params': [{
                    'argument': 'arg1',
                    'annotation': None,
                    'default': None,
                }],
                'return_type': None,
                'start_lineno': 1,
                'start_col': 0,
                'end_lineno': 5,
                'end_col': 7,
                'is_doc_exists': True,
            },
            actual,
        )


class ReturnTypeTestCase(TestCase):
    @parameterized.expand([
        ('def foo(arg: str):', None),
        ('def foo(arg: str)->int:', 'int'),
        ('def foo(arg: str) ->int:', 'int'),
        ('def foo(arg: str)-> int:', 'int'),
        ('def foo(arg: str) -> int:', 'int'),
        ('def foo(arg: str) -> int :', 'int'),
        ("""def foo(
                arg: str
            )->int:""", 'int'),
        ("""def foo(
                arg: str
            ) ->int:""", 'int'),
        ("""def foo(
                arg: str
            ) -> int:""", 'int'),
        ("""def foo(
                arg: str
            ) -> int :""", 'int'),
    ])
    def test_get_return_type(self, given, expected):
        actual = get_return_type(given)
        self.assertEqual(expected, actual)

    @parameterized.expand([
        ('def foo(arg: str):', None),
        ('def foo(arg: str)->int:', 'int'),
        ('def foo(arg: str) ->int:', 'int'),
        ('def foo(arg: str)-> int:', 'int'),
        ('def foo(arg: str) -> int:', 'int'),
        ('def foo(arg: str) -> int :', 'int'),
        ("""def foo(
                arg: str
            )->int:""", 'int'),
        ("""def foo(
                arg: str
            ) ->int:""", 'int'),
        ("""def foo(
                arg: str
            ) -> int:""", 'int'),
        ("""def foo(
                arg: str
            ) -> int :""", 'int'),
    ])
    def test_parse_return_type(self, given, expected):
        lineno = len(given.split('\n')) + 1
        actual = parse_return_type(given, start_lineno=0, end_lineno=lineno)
        self.assertEqual(expected, actual)
