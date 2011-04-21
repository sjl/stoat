# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Page'
        db.create_table('stoat_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('depth', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('numchild', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=100, blank=True)),
            ('template', self.gf('django.db.models.fields.CharField')(default='Default', max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, blank=True)),
        ))
        db.send_create_signal('stoat', ['Page'])

        # Adding model 'PageContent'
        db.create_table('stoat_pagecontent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stoat.Page'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('cleaned_title', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('typ', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('stoat', ['PageContent'])

        # Adding unique constraint on 'PageContent', fields ['title', 'page']
        db.create_unique('stoat_pagecontent', ['title', 'page_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'PageContent', fields ['title', 'page']
        db.delete_unique('stoat_pagecontent', ['title', 'page_id'])

        # Deleting model 'Page'
        db.delete_table('stoat_page')

        # Deleting model 'PageContent'
        db.delete_table('stoat_pagecontent')


    models = {
        'stoat.page': {
            'Meta': {'object_name': 'Page'},
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'Default'", 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'blank': 'True'})
        },
        'stoat.pagecontent': {
            'Meta': {'unique_together': "(('title', 'page'),)", 'object_name': 'PageContent'},
            'cleaned_title': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stoat.Page']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'typ': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        }
    }

    complete_apps = ['stoat']
