Templating
==========

The templates you make to use with Stoat are simply Django templates that take
advantage of an extra variable.

The Page Variable
-----------------

When Stoat renders a template it adds a ``page`` variable to the context.  This
variable has a few properties you'll want to use.

The first is ``page.title``, which is the title of the page as defined in the admin
interface.

The next is ``page.fields``.  This contains all of the fields you've defined in
``STOAT_TEMPLATES``, with their names lowercased.

For example: look at the following ``STOAT_TEMPLATES`` setting::

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

Here's what ``pages/product.html`` might look like::

    {% extends "base.html" %}

    {% block content %}
        <h1>{{ page.title }}</h1>

        <img class="product-image" src="{{ page.fields.image }}" />

        <p class="price">Price: ${{ page.fields.price }}</p>

        {{ page.fields.description|linebreaks }}
    {% endblock %}

You can use ``page.f`` as a shortcut for ``page.fields`` if you'd like to save on
some typing.
