Inlines
=======

Stoat allows you to create your own models that have a `ForeignKey`_ field pointing
to ``stoat.models.Page`` and display them as inlines on the ``Page`` admin.

This can be useful if you want to allow an arbitrary number of a certain kind of data
to be attached to a ``Page``.  We'll use the idea of a "sidebar link" as an example.

Creating Models
---------------

The first step is to create the ``SidebarLink`` model and make sure it has
a ForeignKey to ``stoat.models.Page``.

**IMPORTANT:**  You *must* use a string when specifying the model for the ForeignKey,
and not try to import ``stoat.models.Page`` directly, otherwise you'll get circular
imports.

Here's a sample of a simple ``models.py`` file for our ``SidebarLink`` example::

    from django.db import models

    class SidebarLink(models.Model):
        title = models.CharField(max_length=140)
        link = models.URLField(verify_exists=True)
        page = models.ForeignKey('stoat.Page')

Creating Admins
---------------

The next step is to create the inline admin class as normal.

Here's a sample ``admin.py`` file for our example::

    from django.contrib import admin
    from models import SidebarLink

    class SidebarLinkInline(admin.TabularInline):
        model = SidebarLink
        extra = 1

Both ``TabularInline`` and ``StackedInline`` will work, and you can configure the
inline however you like.

Configuring Stoat
-----------------

To tell Stoat to use this inline, you add a field to your template definition in
``settings.py``::

    STOAT_TEMPLATES = {
        'Default': ['default.html', [
            ['Heading',       'char'],
            ['Body',          'ckeditor', { 'required': True }],
            ['Sidebar Links', 'inline', { 'import': 'sidebar.admin.SidebarLinkInline' }],
        ]],
    }

The definition for our new inline on its own looks like this::

    ['Sidebar Links', 'inline', { 'import': 'sidebar.admin.SidebarLinkInline' }],

The field options *must* contain the full path to import the inline.


.. _ForeignKey: https://docs.djangoproject.com/en/1.3/ref/models/fields/#foreignkey
