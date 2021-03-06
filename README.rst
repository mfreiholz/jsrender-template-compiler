JS-Render Template Compiler
===========================
Minifies a set of template files into a single template file.

Usage examples
--------------
Copy the contents of all template files into a single file.
::

  compiler.py --directory tmpl/ --output templates.tmpl

Minifying requires the additional parameter ``--trim``, which will remove all
leading and trailing spaces, new lines and tabs from file. The resulting
output will contain only a single line with all templates.
::

  compiler.py --directory tmpl/ --output templates.tmpl --trim

Minifying with one template per row is also possible by providing the ``--newline``
and ``--trim`` parameter.
::

   compiler.py --directory tmpl/ --output templates.tmpl --trim --newline

Minifying a set of specific files can be done with the ``--file`` option.
::

  compiler.py --file MyTemplate1.tmpl --file subdir/MyTemplate2.tmpl --output templates.tmpl --trim --newline

