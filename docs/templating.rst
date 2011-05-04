Templating
==========

The templates you make to use with Stoat are simply Django templates that take
advantage of an extra variable.

The Page Variable
-----------------

When Stoat renders a template it adds a ``page`` variable to the context.  This
variable has a few properties you'll want to use.

``page.title``
``````````````

``page.title`` contains the title of the page as defined in the admin interface.

``page.get_absolute_url``
``````````````

``page.get_absolute_url`` is a normal Django ``get_absolute_url`` method.

``page.fields``
```````````````

``page.fields`` contains all of the fields you've defined in ``STOAT_TEMPLATES``,
with their names lowercased and every non-letter/number replaced by an underscore.

For example: look at the following ``STOAT_TEMPLATES`` setting::

    STOAT_TEMPLATES = {
        'Default': ['default.html', [
            ['Heading',         'char'],
            ['Body',            'text'],
            ['Sidebar Heading', 'text'],
        ]],
        'Product': ['pages/product.html', [
            ['Price',       'int'],
            ['Description', 'text'],
            ['Image',       'image'],
            ['Image 2',     'image'],
        ]],
    }

Here's what ``pages/product.html`` might look like::

    {% extends "base.html" %}

    {% block content %}
        <h1>{{ page.title }}</h1>

        <img class="product-image" src="{{ page.fields.image }}" />
        <img class="product-image" src="{{ page.fields.image_2 }}" />

        <p class="price">Price: ${{ page.fields.price }}</p>

        {{ page.fields.description|linebreaks }}
    {% endblock %}

You can use ``page.f`` as a shortcut for ``page.fields`` if you'd like to save on
some typing.

``page.breadcrumbs``
````````````````````

``page.breadcrumbs`` is a list of the page's ancestors and itself.  For example,
imagine you have the following page layout::

    About Us
    |
    +-> The Team
        |
        +-> Jimmy
        |
        +-> Timmy

For the "Timmy" page ``page.breadcrumbs`` will be ``[<About Us>, <The Team>,
<Timmy>]``.

Each item in the list is a normal page object.

Here's an example of creating a simple list of breadcrumbs in an HTML template::

    <ul>
        {% for p in page.breadcrumbs %}
            <li {% if forloop.last %}class="active"{% endif %}>
                <a href="{{ p.get_absolute_url }}">{{ p.title }}</a>
                {% if not forloop.last %}
                    &gt;
                {% endif %}
            </li>
        {% endfor %}
    </ul>

