# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'PageContent.extra'
        db.add_column('stoat_pagecontent', 'extra', self.gf('django.db.models.fields.CharField')(default='', max_length=42, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'PageContent.extra'
        db.delete_column('stoat_pagecontent', 'extra')


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
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '42', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stoat.Page']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'typ': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        }
    }

    complete_apps = ['stoat']
