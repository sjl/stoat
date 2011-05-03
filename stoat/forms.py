from django import forms
from django.conf import settings
from models import Page
from stemplates import get_fields
from models import clean_field_title


class PageContentForm(forms.Form):
    pass

def get_content_form(tname, data=None, initial=None):
    fs = get_fields(tname)

    if data:
        data = dict((k, v) for k, v in data.items() if k.startswith('content_'))
        form = PageContentForm(data)
    elif initial:
        form = PageContentForm(initial=initial)
    else:
        form = PageContentForm()

    for title, typ in fs:
        if typ.lower() == 'char':
            f = forms.CharField(max_length=140, label=title, required=False)
        elif typ.lower() == 'text':
            f = forms.CharField(widget=forms.Textarea(), label=title, required=False)
        elif typ.lower() == 'int':
            f = forms.IntegerField(label=title, required=False)
        elif typ.lower() == 'url':
            f = forms.URLField(label=title, required=False, verify_exists=False)
        elif typ.lower() == 'ckeditor':
            from ckeditor.widgets import CKEditor
            config = getattr(settings, 'STOAT_CKEDITOR_CONFIG', 'default')
            f = forms.CharField(widget=CKEditor(ckeditor_config=config), label=title, required=False)
        elif typ.lower() == 'email':
            f = forms.EmailField(label=title, required=False)
        elif typ.lower() == 'bool':
            f = forms.BooleanField(label=title, required=False)
        elif typ.lower() == 'float':
            f = forms.FloatField(label=title, required=False)
        elif typ.lower() == 'decimal':
            f = forms.DecimalField(label=title, required=False)

        form.fields['content_' + clean_field_title(title)] = f

    return form


class PageForm(forms.ModelForm):
    parent = forms.IntegerField(required=False)

    class Meta:
        model = Page


    def _clean_content(self):
        '''Clean the content_* fields in self.data.

        Only done when:

        1. This is not a create.
        2. We're not changing the template.

        '''

        self.ignore_content = ((not self.instance or not self.instance.id)
                               or (self.instance.template != self.cleaned_data['template']))
        if self.ignore_content:
            return

        form = get_content_form(self.instance.template, self.data)
        if not form.is_valid():
            raise forms.ValidationError('Invalid page content!')

    def clean(self):
        cd = self.cleaned_data

        if 'slug' in cd:
            if cd.get('parent', ''):
                peers = Page.objects.get(id=cd['parent']).get_children()
            else:
                peers = Page.get_root_nodes()

            peers = [peer.slug for peer in list(peers) if peer.id != self.instance.id]
            if cd['slug'] in peers:
                raise forms.ValidationError('A sibling page with that slug already exists!')

        self._clean_content()

        return cd


    def save(self, *args, **kwargs):
        cd = self.cleaned_data

        pid = cd.pop('parent', '')
        parent = Page.objects.get(pk=pid) if pid else None

        if self.instance.pk is None:
            if parent:
                self.instance = parent.add_child(**cd)
                self.instance.move(parent, pos='first-child')
            else:
                self.instance = Page.add_root(**cd)
        else:
            self.instance.save()
            if parent:
                self.instance.move(parent, pos='first-child')
            else:
                self.instance.move(Page.get_first_root_node(), pos='first-sibling')

        self.instance = Page.objects.get(pk=self.instance.pk)

        super(PageForm, self).save(*args, **kwargs)
        return self.instance



MOVE_POSITIONS = (('above', 'above'), ('below', 'below'), ('inside', 'inside'))

class MovePageForm(forms.Form):
    page = forms.ModelChoiceField(queryset=Page.objects.all())
    target = forms.ModelChoiceField(queryset=Page.objects.all())
    position = forms.ChoiceField(choices=MOVE_POSITIONS)
