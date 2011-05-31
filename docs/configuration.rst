Configuration
=============

Stoat aims for convention over configuration,  but there are still a few settings
required, and a few more available if you need them.

Required Settings
-----------------

These two settings need to be set for Stoat to work correctly.

STOAT_TEMPLATES
~~~~~~~~~~~~~~~

This setting defines the templates available for use, as described in the
:doc:`Templating Documentation </templating>`.

STOAT_DEFAULT_TEMPLATE
~~~~~~~~~~~~~~~~~~~~~~

This setting defines the default template, as described in the :doc:`Templating
Documentation </templating>`.

Optional Settings
-----------------

These settings are completely optional.

STOAT_DEBUG
~~~~~~~~~~~

Set this to ``True`` if you're working on Stoat itself.  It does the following:

* Show the ``PageContent`` model in the admin interface.
* Show the ``Template`` column in the Page admin listing page.

STOAT_HIDE_NAVIGATION
~~~~~~~~~~~~~~~~~~~~~

Set this to ``True`` to hide the ``show_in_nav`` field in the page admin.
