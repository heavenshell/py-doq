doq
---

.. image:: https://github.com/heavenshell/py-doq/workflows/build/badge.svg
    :target: https://github.com/heavenshell/py-doq/actions

.. image:: https://pyup.io/repos/github/heavenshell/py-doq/python-3-shield.svg
    :target: https://pyup.io/repos/github/heavenshell/py-doq/
    :alt: Python 3

.. image:: https://pyup.io/repos/github/heavenshell/py-doq/shield.svg
    :target: https://pyup.io/repos/github/heavenshell/py-doq/
    :alt: Updates

Docstring generator.

Installation
============

.. code::

  $ pip install doq

How to use
==========

.. code::

  $ cat spam.py
  def spam(arg1, arg2: str) -> str:
      pass

.. code::

  $ cat spam.py | doq
  def spam(arg1, arg2: str) -> str:
    """spam.

    :param arg1:
    :param arg2:
    :type arg2: str
    :rtype: str
    """
    pass

Default formatter is `sphinx`. You can choose `sphinx`, `google` or `numpy`.

.. code::

  $ cat spam.py | doq --formatter=google
  def spam(arg1, arg2: str) -> str:
    """spam.

    Args:
        arg1 : arg1
        arg2 (str): arg2

    Returns:
        str:
    """
    pass

.. code::

  $ cat spam.py | doq --formatter=numpy
  def spam(arg1, arg2: str) -> str:
    """spam.

    Parameters
    ----------
    arg1
          arg1
    arg2 : str
         arg2

    Returns
    -------
    str

    """
    pass

Usage
=====

.. code::

  $ python -m doq.cli --help
  usage: doq [-h] [-f FILE] [--start START] [--end END] [-t TEMPLATE_PATH]
           [-s STYLE] [--formatter FORMATTER] [--indent INDENT] [--omit OMIT]
           [-r] [-d DIRECTORY] [-w] [-v] [--ignore_exception] [--ignore_yield]
           [--ignore_init]

  Docstring generator.

  optional arguments:
    -h, --help            show this help message and exit
    -f FILE, --file FILE  File or STDIN
    --start START         Start lineno
    --end END             End lineno
    -t TEMPLATE_PATH, --template_path TEMPLATE_PATH
                          Path to template directory
    -s STYLE, --style STYLE
                          Output style string or json
    --formatter FORMATTER
                          Docstring formatter. sphinx,google or numpy
    --indent INDENT       Indent number
    --omit OMIT           Omit first argument such as self
    -r, --recursive       Run recursively over directories
    -d DIRECTORY, --directory DIRECTORY
                          Dire
    -w, --write           Edit files in-place
    -v, --version         Output the version number
    --ignore_exception    Ignore exception statements
    --ignore_yield        Ignore yield statements
    --ignore_init         Ignore genereate docstring to __init__ method

Customize template
==================

doq use Jinja2 template. So you can create your own template.

.. note::

    You must create 3 template files.

+-----------+-----------------------------------------+
| File name | Description                             |
+===========+=========================================+
| class.txt | class docstring                         |
+-----------+-----------------------------------------+
| def.txt   | def / method docstring                  |
+-----------+-----------------------------------------+
| noarg.txt | def / method without argument docstring |
+-----------+-----------------------------------------+

Available Jinja2's variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~

+--------------------------+---------------------------+
| Name                     | Description               |
+==========================+===========================+
| name                     | class, method, def's name |
+-------------+------------+---------------------------+
| params      | argument   | Method, def's argument    |
|             +------------+---------------------------+
|             | annotation | Argument's type hint      |
|             +------------+---------------------------+
|             | default    | Defaut keyword argument   |
+-------------+------------+---------------------------+
| exceptions               | List of exception         |
+--------------------------+---------------------------+
| yields                   | List of yield             |
+--------------------------+---------------------------+
| return_type              | Return type hint          |
+--------------------------+---------------------------+

See `examples <https://github.com/heavenshell/py-doq/tree/master/examples>`_

LICENSE
=======

NEW BSD LICENSE.
