Using the Admin Interface
=========================

Stoat uses the standard Django admin interface (through Grappelli) with a few
customizations to streamline page editing.

The process of adding and editing pages is slightly more complicated than adding and
editing standard Django models.  We think that in practice this extra complexity is
worth it for the power and flexibility it makes possible.

Creating and Editing Pages
--------------------------

Creating a new Stoat page has three steps:

* Add the new page (selecting a template in the process) and save it.
* Edit the page to fill in the template fields that weren't available in the "add"
  step.
* Move the page to its desired location in the hierarchy.

Changing Page Templates
-----------------------

When you select a different template for a page something important happens:

**Any data for fields that are not in the new template will be discarded.**

This behavior allows us to keep the Stoat codebase simple and free of extra
complexity.

This may seem awful at first, but in practice it's not a very painful sacrifice.
We've found that for most sites you almost never need to switch templates after
a page has been created.

Moving Pages
------------

You've probably already noticed the ``Move`` buttons on the ``Page`` admin
changelist.  To shuffle pages around in the hierarchy you can simply drag and drop
these buttons to their desired place.

One thing to note: pages cannot be dropped onto pages under themselves.  This would
be complex and nonobvious behavior if we allowed it, so Stoat simply chooses to make
it impossible.
