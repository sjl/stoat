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

Each template definition consists of a path and a list of fields.

Each field is a list containing a name and a field type.

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

