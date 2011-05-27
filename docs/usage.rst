Basic Usage
===========

The first step to using Stoat is defining the templates you want to use for pages.

Defining Templates
------------------

You define the templates Stoat will use in your Django settings.  Here's a quick
example to get you started::

    STOAT_TEMPLATES = {
        'Default': ['default.html', [
            ['Heading',       'char'],
            ['Body',          'ckeditor', { 'required': True }],
            ['Sidebar Body',  'text'],
            ['Sidebar Links', 'inline', { 'import': 'sidebar.admin.SidebarLinkInline' }],
        ]],
        'Product': ['pages/product.html', [
            ['Price',       'int', { 'required': True }],
            ['Description', 'text'],
            ['Image',       'img'],
            ['Salesperson', 'fk', { 'app': 'auth', 'model': 'User' }],
        ]],
    }
    STOAT_DEFAULT_TEMPLATE = 'Default'

The ``STOAT_TEMPLATES`` setting contains a dictionary mapping template names to
template definitions.

Each template definition consists of:

* A path
* A list of fields
* A dictionary of configuration options (optional)

The path is a normal Django template path, like you might use with
``render_to_response``.

Each field is a list containing a name and a field type.  The field name is how the
field will be labels in the admin and referred to in your templates, and the field
type is one of the supported types detailed in the next section.

The option dictionary maps options to values.  Some options (such as ``required``)
can be used with any kind of field, while others are specific to a certain field
type.  See the `Field Options`_ section for more information on universal
options, and the `Field Types`_ section for options specific to a single type.

There's also a ``STOAT_DEFAULT_TEMPLATE`` setting that you need to set to the name of
the template that should be considered the default.

Field Types
-----------

The following types of fields are available for use.

Note: Stoat actually stores all field data as Text data.  The field types only change
the form field type used (and validated) in the admin.

bool
~~~~

A basic Django `BooleanField`_.

char
~~~~

A basic Django `CharField`_.

ckeditor
~~~~~~~~

A `CKEditor`_ field.  This requires that `django-ckeditor`_ be installed.

**Options**

* ``config``: A string defining which of the ``CKEDITOR_CONFIGS`` should be used for
  this field.

decimal
~~~~~~~

A basic Django `DecimalField`_.

email
~~~~~

A basic Django `EmailField`_.

float
~~~~~

A basic Django `FloatField`_.

fk
~~

A foreign key to a model.  When using this field you *must* provide both of its
options.

**Options**

* ``app``: A string containing the name of the app the model is from.
* ``model``: A string containing the name of the model.

img
~~~

A `FileBrowseField`_ from `django-filebrowser`_, with the ``'Image'`` type.

inline
~~~~~~

An ``inline`` field allows you to create models that have a `ForeignKey`_ pointing at Stoat pages.

Check out the :doc:`Inlines </inlines>`_ documentation for more information.

int
~~~

A basic Django `IntegerField`_.

text
~~~~

A basic Django `CharField`_, but rendered as with a ``<textarea>`` widget.

url
~~~

A basic Django `URLField`_ (with ``verify_exists`` set to ``False``).

.. _BooleanField: http://docs.djangoproject.com/en/dev/ref/forms/fields/#booleanfield
.. _CharField: http://docs.djangoproject.com/en/dev/ref/forms/fields/#charfield
.. _FloatField: http://docs.djangoproject.com/en/dev/ref/forms/fields/#floatfield
.. _DecimalField: http://docs.djangoproject.com/en/dev/ref/forms/fields/#decimalfield
.. _ForeignKey: https://docs.djangoproject.com/en/1.3/ref/models/fields/#foreignkey
.. _URLField: http://docs.djangoproject.com/en/dev/ref/forms/fields/#urlfield
.. _EmailField: http://docs.djangoproject.com/en/dev/ref/forms/fields/#emailfield
.. _FileBrowseField: http://readthedocs.org/docs/django-filebrowser/latest/fieldswidgets.html#filebrowsefield
.. _IntegerField: http://docs.djangoproject.com/en/dev/ref/forms/fields/#integerfield
.. _django-filebrowser: http://readthedocs.org/docs/django-filebrowser/latest/#filebrowsefield
.. _ckeditor: http://ckeditor.com/
.. _django-ckeditor: http://github.com/dwaiter/django-ckeditor

Field Options
-------------

The following options can be used for any field.

``required``
~~~~~~~~~~~~

Ensures that this field is not left blank when editing the page in the admin
interface.

Further Usage
-------------

Next you'll want to check out the :doc:`Admin </admin>` documentation to learn how to
use the admin interface for adding pages (it's simple), and the :doc:`Templating
</templating>` documentation to learn how to create Django templates for use with
Stoat.
