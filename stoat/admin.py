# Imports {{{
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.admin.util import unquote
from django.contrib.admin.views.main import ChangeList
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.forms.formsets import all_valid
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect

import forms as stoat_forms
import stemplates
from models import Page, PageContent, clean_field_title
from views import move_page

csrf_protect_m = method_decorator(csrf_protect)
# }}}

# Settings {{{
PAGE_FIELDS = ['title', 'slug', 'template',]
if not getattr(settings, 'STOAT_HIDE_NAVIGATION', False):
    PAGE_FIELDS.append('show_in_nav')

PAGE_COLS = ['indented_title', 'url']
if getattr(settings, 'STOAT_DEBUG', False):
    PAGE_COLS.append('template')
# }}}

def check_empty_dict(GET_dict):
    empty = True
    for k, v in GET_dict.items():
        # Don't disable on p(age) or 'all' GET param
        if v and k != 'p' and k != 'all':
            empty = False
    return empty


class TreeChangeList(ChangeList):
    def get_ordering(self):
        if not check_empty_dict(self.params):
            return super(TreeChangeList, self).get_ordering()
        return None, 'asc'



class PageAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = PAGE_COLS
    fieldsets = (
        (None, {
            'fields': PAGE_FIELDS,
        }),
    )
    prepopulated_fields = { 'slug': ('title',), }
    form = stoat_forms.PageForm

    def _find_inlines(self, page):
        fields = stemplates.get_fields(page.template)
        inline_fields = [f for f in fields if f[1] == 'inline']

        for inline_field in inline_fields:
            import_line = inline_field[2]['import']

            module_name, inline_name = import_line.rsplit('.', 1)
            admin_module = __import__(module_name, fromlist=[inline_name])

            yield getattr(admin_module, inline_name)

    def _create_inlines(self, page):
        instances = []
        for inline_class in self._find_inlines(page):
            inline_instance = inline_class(self.model, self.admin_site)
            instances.append(inline_instance)
        return instances


    def get_formsets(self, request, obj=None):
        if obj:
            for inline in self._create_inlines(obj):
                yield inline.get_formset(request, obj)

    def get_changelist(self, request):
        return TreeChangeList


    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}

        if request.POST:
            parent = request.POST.get('parent', '')
        else:
            parent = request.GET.get('parent', '')

        if parent:
            get_object_or_404(Page, id=parent)

        extra_context.update({
            'parent': request.GET.get('parent', ''),
        })

        return super(PageAdmin, self).add_view(request, form_url=form_url,
                                               extra_context=extra_context)


    def save_model(self, request, obj, form, change):
        obj.save()

        if not form.ignore_content:
            # Use the authoritative list of fields, because browsers won't send along
            # boolean fields that are unchecked (False) at all.

            # This is ugly, but we have to do it.
            #
            # fields: list of (clean_field_title, field_type) pairs
            # fieldnames: list of clean_field_title
            # fieldtypes: dict of clean_field_title -> field_type pairs

            fields = [(clean_field_title(f[0]), f[1])
                      for f in stemplates.get_fields_bare(obj.template)]
            fieldnames = [f[0] for f in fields]
            fieldtypes = dict(fields)

            # content is going to be a dict of
            # clean_field_title -> cleaned data pairs

            # Default to 0, because browsers won't even send along a field for
            # a checkbox element that's unchecked.
            content = dict([(f, 0) for f in fieldnames])

            # Now update content with the appropriate data from the form.
            for k, v in form.data.items():
                if k.startswith('content_'):
                    fieldname = k.split('_', 1)[1]
                    fieldtype = fieldtypes[fieldname]

                    if fieldtype == 'bool':
                        v = 1

                    content[fieldname] = v

            for k, v in content.items():
                pc = PageContent.objects.get(page=obj, cleaned_title=k)
                pc.content = v
                pc.save()


    @csrf_protect_m
    @transaction.commit_on_success
    def _django_change_view(self, request, object_id, extra_context=None):
        "The 'change' admin view for this model."
        model = self.model
        opts = model._meta

        obj = self.get_object(request, unquote(object_id))
        previous_template = obj.template                                                            # STOAT: Save previous template

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})

        if request.method == 'POST' and "_saveasnew" in request.POST:
            return self.add_view(request, form_url='../add/')

        ModelForm = self.get_form(request, obj)
        formsets = []
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=True)
            else:
                form_validated = False
                new_object = obj
            prefixes = {}
            if previous_template == new_object.template:                                            # STOAT: Template check
                for FormSet, inline in zip(self.get_formsets(request, new_object),
                                           self._create_inlines(obj)):                              # STOAT: _create_inlines
                    prefix = FormSet.get_default_prefix()
                    prefixes[prefix] = prefixes.get(prefix, 0) + 1
                    if prefixes[prefix] != 1:
                        prefix = "%s-%s" % (prefix, prefixes[prefix])
                    formset = FormSet(request.POST, request.FILES,
                                      instance=new_object, prefix=prefix,
                                      queryset=inline.queryset(request))

                    formsets.append(formset)

            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, change=True)
                form.save_m2m()
                for formset in formsets:
                    self.save_formset(request, form, formset, change=True)

                change_message = self.construct_change_message(request, form, formsets)
                self.log_change(request, new_object, change_message)
                return self.response_change(request, new_object)

        else:
            form = ModelForm(instance=obj)
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request, obj), self._create_inlines(obj)): # STOAT: _create_inlines
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(instance=obj, prefix=prefix,
                                  queryset=inline.queryset(request))
                formsets.append(formset)

        adminForm = helpers.AdminForm(form, self.get_fieldsets(request, obj),
            self.prepopulated_fields, self.get_readonly_fields(request, obj),
            model_admin=self)
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(self._create_inlines(obj), formsets):                            # STOAT: _create_inlines
            fieldsets = list(inline.get_fieldsets(request, obj))
            readonly = list(inline.get_readonly_fields(request, obj))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                fieldsets, readonly, model_admin=self)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media

        media = media + extra_context.pop('media')                                                 # STOAT
        context = {
            'title': _('Change %s') % force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'object_id': object_id,
            'original': obj,
            'is_popup': "_popup" in request.REQUEST,
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, change=True, obj=obj)

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        page = get_object_or_404(Page, id=object_id)

        parent = page.get_parent()
        parent = parent.id if parent else ''

        if request.POST:
            template = request.POST.get('template', page.template)

            content_form = stoat_forms.get_content_form(template, request.POST)
        else:
            initial = {}
            for pc in page.pagecontent_set.all():
                # Ugly hack to store booleans as text.
                if pc.typ == 'bool':
                    val = True if int(pc.content) else False
                else:
                    val = pc.content

                initial['content_' + clean_field_title(pc.title)] = val

            content_form = stoat_forms.get_content_form(page.template, initial=initial)

        extra_context.update({
            'content_form': content_form,
            'media': content_form.media + self.media,
            'parent': parent,
        })

        return self._django_change_view(request, object_id, extra_context=extra_context)


    def indented_title(self, obj):
        indent = ''.join(['&nbsp;'*6 for _ in obj.get_ancestors()])

        has_child = '1' if obj.get_children_count() else '0'

        first_child = '0'
        if obj.get_ancestors():
            try:
                parent = obj.get_parent()
            except Exception, e:
                return repr(e)

            if parent and parent.get_first_child() == obj:
                first_child = '1'

        descendants = ','.join(map(str, [p.id for p in obj.get_descendants()]))

        return (
            indent + obj.title +
            '<span class="indent" style="display: none;">' + indent + '</span>' +
            '<span class="has-child" style="display: none;">' + has_child + '</span>' +
            '<span class="first-child" style="display: none;">' + first_child + '</span>' +
            '<span class="descendants" style="display: none;">' + descendants + '</span>'
        )
    indented_title.allow_tags = True

    def urls(self):
        from django.conf.urls.defaults import patterns, url

        urlpatterns = patterns('',
            url(r'^move-page/$', move_page, name='stoat-move-page'),
        )
        urlpatterns += super(PageAdmin, self).urls

        return urlpatterns

    urls = property(urls)

    class Media:
        css = {
            'all': ('stoat.css',) + getattr(settings, 'STOAT_ADMIN_EXTRA_CSS', ()),
        }
        js = ('stoat.js',) + getattr(settings, 'STOAT_ADMIN_EXTRA_JS', ())
admin.site.register(Page, PageAdmin)


class PageContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'typ', 'page', 'content')
    list_filter = ('page', 'typ')


if getattr(settings, 'STOAT_DEBUG', False):
    admin.site.register(PageContent, PageContentAdmin)

