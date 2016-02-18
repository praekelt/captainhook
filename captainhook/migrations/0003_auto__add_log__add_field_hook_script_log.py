# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Log'
        db.create_table(u'captainhook_log', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['captainhook.Hook'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('number_to_replay', self.gf('django.db.models.fields.PositiveIntegerField')(default=1000)),
            ('speedup_factor', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('raw_json', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'captainhook', ['Log'])

        # Adding field 'Hook.script_log'
        db.add_column(u'captainhook_hook', 'script_log',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Log'
        db.delete_table(u'captainhook_log')

        # Deleting field 'Hook.script_log'
        db.delete_column(u'captainhook_hook', 'script_log')


    models = {
        u'captainhook.hook': {
            'Meta': {'object_name': 'Hook'},
            'basic_auth_password': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'basic_auth_username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fieldnames': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'number_to_replay': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1000'}),
            'replay_log': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'script_after': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'script_before': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'script_log': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'site_root': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slack_channel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'speedup_factor': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        u'captainhook.log': {
            'Meta': {'object_name': 'Log'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'hook': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['captainhook.Hook']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_to_replay': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1000'}),
            'raw_json': ('django.db.models.fields.TextField', [], {}),
            'speedup_factor': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['captainhook']