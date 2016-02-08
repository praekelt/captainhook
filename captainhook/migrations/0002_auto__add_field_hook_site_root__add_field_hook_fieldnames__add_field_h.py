# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Hook.site_root'
        db.add_column(u'captainhook_hook', 'site_root',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Hook.fieldnames'
        db.add_column(u'captainhook_hook', 'fieldnames',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Hook.number_to_replay'
        db.add_column(u'captainhook_hook', 'number_to_replay',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Hook.speedup_factor'
        db.add_column(u'captainhook_hook', 'speedup_factor',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Hook.replay_log'
        db.add_column(u'captainhook_hook', 'replay_log',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Hook.site_root'
        db.delete_column(u'captainhook_hook', 'site_root')

        # Deleting field 'Hook.fieldnames'
        db.delete_column(u'captainhook_hook', 'fieldnames')

        # Deleting field 'Hook.number_to_replay'
        db.delete_column(u'captainhook_hook', 'number_to_replay')

        # Deleting field 'Hook.speedup_factor'
        db.delete_column(u'captainhook_hook', 'speedup_factor')

        # Deleting field 'Hook.replay_log'
        db.delete_column(u'captainhook_hook', 'replay_log')


    models = {
        u'captainhook.hook': {
            'Meta': {'object_name': 'Hook'},
            'fieldnames': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'number_to_replay': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'replay_log': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'repo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'site_root': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'speedup_factor': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['captainhook']