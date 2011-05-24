from django.conf import settings

# STOAT_TEMPLATES = {
#    'Default': ('pages/default.html', (
#         ('Title', 'char'),
#         ('Body',  'text', { OPTIONS }),
#     )),
#    'Special': ('pages/special.html', (
#         ('Title',    'char'),
#         ('Subtitle', 'char'),
#         ('Body',     'text'),
#         ('Sidebar',  'text'),
#         ('Count',    'int'),
#     )),
# }
# STOAT_DEFAULT_TEMPLATE = 'Default'

def get_template(tname=settings.STOAT_DEFAULT_TEMPLATE):
    return settings.STOAT_TEMPLATES[tname]

def get_fields(tname=settings.STOAT_DEFAULT_TEMPLATE):
    return [f if len(f) >= 3 else f + ({},)
            for f in get_template(tname)[1]]

def get_path(tname=settings.STOAT_DEFAULT_TEMPLATE):
    return get_template(tname)[0]

