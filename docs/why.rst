Why Stoat?
==========

Stoat was born at `Dumbwaiter Design`_ out of a desire for a simple CMS app that we
could use for client sites.

.. _Dumbwaiter Design: http://dwaiter.com/

We wanted something with enough features that didn't take over the site and didn't
break every time a new version of Django/Grappelli/Filebrowser was released.

There are many other CMS apps for Django out there, and they are plump with many
juicy features.

.. raw:: html

   <a href="http://www.flickr.com/photos/kappawayfarer/101441548/" title="Piggy over the Stupid Bunny by Kappa Wayfarer, on Flickr"><img src="http://farm1.static.flickr.com/32/101441548_2ce47d8c92.jpg" width="500" height="375" alt="Piggy over the Stupid Bunny"></a>

We wanted something sleeker.

.. raw:: html

   <a href="http://www.flickr.com/photos/p1hun/2987019221/" title="Stoat by JanetHoward, on Flickr"><img src="http://farm4.static.flickr.com/3239/2987019221_4618fdd251.jpg" width="500" height="333" alt="Stoat"></a>

What Stoat Has
--------------

Here are the currently implemented features:

* Arbitrary URLs.
* Few dependencies.  At the moment `treebeard`_ and `django-templatetag-sugar` are
  the only ones, and both install cleanly with pip.
* Support for (read: doesn't break) the ``APPEND_SLASH`` setting.
* Multiple templates for pages, with custom fields for each template.
* Multiple field types, like Filebrowser Image fields.
* Drag and drop reordering of pages, including making pages children of other pages.
* South support for migrating the Stoat database between versions.
* Built for and compatible with the latest version of Django (1.3), Grappelli and
  Filebrowser.
* Support for `django-ckeditor`_ for rich text editing.

.. _treebeard: https://tabo.pe/projects/django-treebeard/docs/1.61/
.. _django-ckeditor: http://github.com/dwaiter/django-ckeditor
.. _django-templatetag-sugar: https://github.com/alex/django-templatetag-sugar

What Stoat Doesn't Have Yet
---------------------------

Here's what we're planning on adding in the future:

* A test suite.
* More field types.
* More documentation.
* Publishing control.  But it will be configurable and opt-in!

What Stoat Will Never Have
--------------------------

Here are the things we don't want to have in Stoat:

* i18n support.  It adds complexity and many sites simply don't need it.
* Tagging.  Pages don't need to be tagged, and half of the Django tagging apps are
  broken anyway.
* Redirects.  The built-in redirects app handles these perfectly fine.
* "In-site" editing.  The admin interface is for editing, the site is for using.
* Complicated permissions.  Stoat embraces Django's admin permission system and
  doesn't try to add complexity on top of it.
* Revision control of pages (though some other apps that add this may happen to work
  with Stoat).

If you need some or all of these you then Stoat simply isn't for you.  You should
look at one of the `many other Django CMS apps`_ around.

.. _many other Django CMS apps: http://djangopackages.com/grids/g/cms/
