# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Hook'
        db.create_table(u'captainhook_hook', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('repo', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('site_root', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('fieldnames', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('number_to_replay', self.gf('django.db.models.fields.PositiveIntegerField')(default=1000)),
            ('speedup_factor', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('replay_log', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('script_before', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('script_after', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('slack_channel', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'captainhook', ['Hook'])


    def backwards(self, orm):
        # Deleting model 'Hook'
        db.delete_table(u'captainhook_hook')


    models = {
        u'captainhook.hook': {
            'Meta': {'object_name': 'Hook'},
            'fieldnames': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'number_to_replay': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1000'}),
            'replay_log': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'repo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'script_after': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'script_before': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'site_root': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slack_channel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'speedup_factor': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['captainhook']