# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Hook.repo'
        db.delete_column(u'captainhook_hook', 'repo')

        # Deleting field 'Hook.user'
        db.delete_column(u'captainhook_hook', 'user')

        # Adding field 'Hook.basic_auth_username'
        db.add_column(u'captainhook_hook', 'basic_auth_username',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Hook.basic_auth_password'
        db.add_column(u'captainhook_hook', 'basic_auth_password',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Hook.repo'
        db.add_column(u'captainhook_hook', 'repo',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'Hook.user'
        db.add_column(u'captainhook_hook', 'user',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Deleting field 'Hook.basic_auth_username'
        db.delete_column(u'captainhook_hook', 'basic_auth_username')

        # Deleting field 'Hook.basic_auth_password'
        db.delete_column(u'captainhook_hook', 'basic_auth_password')


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
            'site_root': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slack_channel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'speedup_factor': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['captainhook']