Installation
============

Installing Stoat is just like installing any other Django app.

First, install the library (preferably into a virtualenv)::

    pip install -e hg+https://bitbucket.org/sjl/stoat@v0.1.0#egg=stoat

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

Now that you've got Stoat installed you'll want to take a look at :doc:`Usage
</usage>` to learn how to use Stoat.

