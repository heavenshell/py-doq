doq
---

Docstring generator.

Installation
============

.. code::

  $ pip install doq

How to use
==========

.. code::

  $ cat foo.py
  def foo(arg1, arg2: str) -> str:
      pass

.. code::

  $ cat foo.py | doq
  def foo(arg1, arg2: str) -> str:
    """foo.

    :param arg1:
    :param arg2:
    :type arg2: str
    :rtype: str
    """
    pass

Default formatter is `sphinx`. You can choose `sphinx`, `google` or `numpy`.

.. code::

  $ cat foo.py | doq --formatter=google
  def foo(arg1, arg2: str) -> str:
    """ham.

    Args:
        arg1 : arg1
        arg2 (str): arg2

    Returns:
        str:
    """
    pass

Usage
=====

.. code::

  $ python -m doq.cli --help
  usage: cli.py [-h] [--file FILE] [--start START] [--end END]
                [--template_path TEMPLATE_PATH] [--style STYLE]
                [--formatter FORMATTER] [--indent INDENT]

  Docstring generator.

  optional arguments:
    -h, --help            show this help message and exit
    --file FILE           File or STDIN
    --start START         Start lineno
    --end END             End lineno
    --template_path TEMPLATE_PATH
                          Path to template directory
    --style STYLE         Output style string or json
    --formatter FORMATTER
                          Docstring formatter. sphinx,google,numpy
    --indent INDENT       Indent number

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

+-------------+--------------------------------------+
| Name        | Description                          |
+=============+======================================+
| name        | class, method, def's name            |
+-------------+------------+-------------------------+
| params      | argument   | Method, def's argument  |
|             +------------+-------------------------+
|             | annotation | Argument's type hint    |
|             +------------+-------------------------+
|             | default    | Defaut keyword argument |
+-------------+------------+-------------------------+
| return_type | Return type hint                     |
+-------------+--------------------------------------+

See `examples <https://github.com/heavenshell/py-doq/tree/master/examples>`_

LICENSE
=======
NEW BSD LICENSE.
