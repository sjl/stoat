Stoat
=====

Stoat is a sleek, lightweight, pluggable CMS app for Django.

Stoat is like flatpages on steroids.  No, scratch that, Stoat isn't that bulky.  It's
more like flatpages on a good exercise routine.

If you want to know why you should use Stoat instead of one of the many other
options, check out the :doc:`Why Stoat? </why>` page.

**At this moment Stoat is very much alpha software -- use it at your own risk!**

Installation
------------

Installing Stoat is just like installing any other Django app.

First, install the library (preferably into a virtualenv)::

    pip install -e https://bitbucket.org/sjl/stoat

Add ``stoat`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        ...
        'stoat',
        ...
    )

Finally, add the following line at the end of your ``MIDDLEWARE_CLASSES`` setting::

    MIDDLEWARE_CLASSES = (
        ...
        'stoat.middleware.StoatMiddleware',
    )

Usage
-----

Contents
--------

.. toctree::
   :maxdepth: 2

   why
   usage
   admin
   configuration
   templating
   contributing

