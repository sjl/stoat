Why Stoat?
==========

Stoat was born at Dumbwaiter Design out of a desire for a simple CMS app that we
could use for client sites.

We wanted something with enough features that didn't take over the site and didn't
break every time a new version of Django/Grappelli/Filebrowser was released.

There are many other CMS apps for Django out there, and they are plump with nice,
juicy features.

bunny

We wanted something sleeker.

stoat

What Stoat Has
--------------

Here are the currently implemented features:

* Arbitrary URLs.
* Support for (read: doesn't break) the ``APPEND_SLASH`` setting.
* Multiple templates for pages, with custom fields for each template.
* Multiple field types, like Filebrowser Image fields.
* Drag and drop reordering of pages, including making pages children of other pages.
* South support for migrating the Stoat database between versions.
* Built for and compatible with the latest version of Django (1.3), Grappelli and
  Filebrowser.

What Stoat Doesn't Have Yet
---------------------------

Here's what we're planning on adding in the future:

* A test suite.
* More field types.
* Support for Javascript WYSIWYG editors like CKEditor and Aloha Editor.
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
look at one of the many other Django CMS apps around.
