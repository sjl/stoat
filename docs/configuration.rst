Configuration
=============

Stoat aims for convention over configuration,  but there are still a few settings
required, and a few more available if you need them.

Required Settings
-----------------

These two settings need to be set for Stoat to work correctly.

STOAT_TEMPLATES
```````````````

This setting defines the templates available for use, as described in the
:doc:`Templating Documentation </templating>`.

STOAT_DEFAULT_TEMPLATE
``````````````````````

This setting defines the default template, as described in the :doc:`Templating
Documentation </templating>`.

Optional Settings
-----------------

These settings are completely optional.

STOAT_CKEDITOR_CONFIG
`````````````````````

This setting defines which of the the ``CKEDITOR_CONFIGS`` `django-ckeditor`_ should
use.  For example::

    CKEDITOR_CONFIGS = {
        'default': {
            'toolbar': [
                [      'Undo', 'Redo',
                  '-', 'Bold', 'Italic', 'Underline',
                  '-', 'Link', 'Unlink', 'Anchor',
                  '-', 'Format',
                  '-', 'SpellChecker', 'Scayt',
                  '-', 'Maximize',
                  '-', 'HorizontalRule',
                  '-', 'Table',
                  '-', 'BulletedList', 'NumberedList',
                  '-', 'Cut','Copy','Paste','PasteText','PasteFromWord',
                  '-', 'Image',
                  '-', 'Source',
                  '-', 'About',
                ]
            ],
            'width': 840,
            'height': 300,
            'toolbarCanCollapse': False,
        },
        'simple': {
            'toolbar': [
                [      'Undo', 'Redo',
                  '-', 'Link', 'Unlink', 'Anchor',
                  '-', 'Source',
                  '-', 'About',
                ]
            ],
            'width': 600,
            'height': 150,
            'toolbarCanCollapse': False,
        }
    }
    STOAT_CKEDITOR_CONFIG = 'simple'

.. _django-ckeditor: http://github.com/dwaiter/django-ckeditor

STOAT_DEBUG
```````````

Set this to ``True`` if you're working on Stoat itself.  It does the following:

* Show the ``PageContent`` model in the admin interface.
