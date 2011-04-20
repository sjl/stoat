Basic Usage
===========

The first step to using Stoat is defining the templates you want to use for pages.

Defining Templates
------------------

You define the templates Stoat will use in your Django settings.  Here's a quick
example to get you started::

    STOAT_TEMPLATES = {
        'Default': ['default.html', [
            ['Heading', 'char'],
            ['Body',    'text'],
            ['Sidebar', 'text'],
        ]],
        'Product': ['pages/product.html', [
            ['Price',       'int'],
            ['Description', 'text'],
            ['Image',       'image'],
        ]],
    }
    STOAT_DEFAULT_TEMPLATE = 'Default'

The ``STOAT_TEMPLATES`` setting contains a dictionary mapping template names to
template definitions.

Each template definition consists of a path and a list of fields.  The path is
a normal Django template path, like you might use with ``render_to_response``.

Each field is a list containing a name and a field type.  The field name is how the
field will be labels in the admin and referred to in your templates, and the field
type is one of the supported types detailed in the next section.

There's also a ``STOAT_DEFAULT_TEMPLATE`` setting that you need to set to the name of
the template that should be considered the default.

Field Types
-----------

The following types of fields are available for use.

Note: Stoat actually stores all field data as Text data.  The field types only change
the form field type used (and validated) in the admin.

char
````

A basic Django CharField.

image
`````

A FileBrowseField from django-filebrowser, with the ``'Image'`` type.

int
```

A basic Django IntegerField.

text
````

A basic Django TextField.

Further Usage
-------------

Next you'll want to check out the :doc:`Admin </admin>` documentation to learn how to
use the admin interface for adding pages (it's simple), and the :doc:`Templating
</templating>` documentation to learn how to create Django templates for use with
Stoat.
