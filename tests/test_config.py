import argparse
import os
import shutil
from configparser import ConfigParser
from unittest import TestCase

from doq.config import (
    find_config,
    find_config_path,
    get_config_from_setup_cfg,
    read_pyproject_toml,
    read_setup_cfg,
)


class ConfigSetupCfgTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.basepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.fixtures_path = os.path.join(cls.basepath, 'tests', 'fixtures')

    def test_find_setupcfg(self):
        rootpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        expected = os.path.join(rootpath, 'setup.cfg')
        paths = []
        for path in find_config_path():
            paths.append(path)
        self.assertIn(expected, paths)

    def test_read_setupcfg(self):
        setupcfg = os.path.join(self.fixtures_path, 'setup.cfg')
        configs = read_setup_cfg(setupcfg)
        self.assertIsInstance(configs, ConfigParser)
        self.assertEqual('json', configs['doq'].get('style'))

    def test_not_read_setupcfg(self):
        configs = read_setup_cfg(None)
        self.assertIsNone(configs)

    def test_get_config_from_setup_cfg(self):
        args = argparse.Namespace(
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
            ignore_init=False,
        )
        setupcfg = os.path.join(self.fixtures_path, 'setup.cfg')
        configs = read_setup_cfg(setupcfg)
        self.assertDictEqual(
            {
                'style': 'json',
                'ignore_init': True,
            },
            get_config_from_setup_cfg(configs, args),
        )

    def test_find_config(self):
        setupcfg = os.path.join(self.fixtures_path, 'setup.cfg')
        args = argparse.Namespace(
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
            ignore_init=False,
            config=setupcfg,
        )
        configs = find_config(args)
        self.assertDictEqual(
            {
                'style': 'json',
                'ignore_init': True,
            },
            configs,
        )

    def test_find_config_not_found(self):
        pyproject_path = os.path.join(self.basepath, 'pyproject.toml')
        shutil.move(
            pyproject_path,
            os.path.join(self.basepath, '_pyproject.toml'),
        )

        args = argparse.Namespace(
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
            ignore_init=False,
            config=None,
        )
        configs = find_config(args)
        self.assertDictEqual({}, configs)
        shutil.move(
            os.path.join(self.basepath, '_pyproject.toml'),
            pyproject_path,
        )


class ConfigPyprojectTomlTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.basepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.fixtures_path = os.path.join(cls.basepath, 'tests', 'fixtures')

    def test_find_pyproject_toml(self):
        rootpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        expected = [
            os.path.join(rootpath, 'setup.cfg'),
            os.path.join(rootpath, 'pyproject.toml'),
        ]
        for path in find_config_path():
            self.assertIn(path, expected)

    def test_read_pyproject_toml(self):
        pyproject = os.path.join(self.fixtures_path, 'pyproject.toml')
        defaults = read_pyproject_toml(pyproject)
        self.assertEqual('json', defaults['style'])

    def test_find_config(self):
        pyproject = os.path.join(self.fixtures_path, 'pyproject.toml')
        args = argparse.Namespace(
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
            ignore_init=False,
            config=pyproject,
        )
        configs = find_config(args)
        self.assertDictEqual(
            {
                'style': 'json',
                'ignore_init': True,
            },
            configs,
        )
