Stoat
=====

`Stoat`_ is a sleek, lightweight, pluggable CMS app for Django.

.. _Stoat: http://stoat.rtfd.org/

Stoat is like flatpages on steroids.  No, scratch that, Stoat isn't that bulky.  It's
more like flatpages on a good exercise routine.

If you want to know why you should use Stoat instead of one of the many other
options, check out the :doc:`Why Stoat? </why>` page.

**At this moment Stoat is very much alpha software -- use it at your own risk!**

Installation
------------

Installing Stoat is just like installing any other Django app.

First, install the library (preferably into a virtualenv)::

    pip install -e hg+https://bitbucket.org/sjl/stoat#egg=stoat

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

If you've customized your admin dashboard with Grappelli's dashboard tools, you'll
need to add Stoat to the dashboard to be able to add pages and such::

        self.children.append(modules.ModelList(
            'Stoat',
            ('stoat.*',),
            column=1,
            css_classes=['collapse', 'open'],
        ))

Take a look at :doc:`Usage </usage>` to learn how to use Stoat.

Full Documentation
------------------

.. toctree::
   :maxdepth: 2

   why
   usage
   admin
   configuration
   templating
   contributing

