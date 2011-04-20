from django.contrib import admin
from models import Page, PageContent
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.main import ChangeList
from views import move_page
import forms as stoat_forms

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
    list_display = ('indented_title', 'url')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'template'),
        }),
    )
    prepopulated_fields = { 'slug': ('title',), }
    form = stoat_forms.PageForm


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
                initial['content_' + pc.title.lower()] = pc.content

            content_form = stoat_forms.get_content_form(page.template, initial=initial)

        extra_context.update({
            'content_form': content_form,
            'parent': parent,
        })

        return super(PageAdmin, self).change_view(request, object_id,
                                                  extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        obj.save()

        if not form.ignore_content:
            content_data = [(k.split('_')[1], v)
                            for k, v in form.data.items()
                            if k.startswith('content_')]

            for title, content in content_data:
                pc = PageContent.objects.get(page=obj, title__iexact=title)
                pc.content = content
                pc.save()


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
            'all': ('stoat.css',),
        }
        js = ('stoat.js',)
admin.site.register(Page, PageAdmin)

class PageContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'typ', 'page', 'content')
    list_filter = ('page', 'typ')

admin.site.register(PageContent, PageContentAdmin)
