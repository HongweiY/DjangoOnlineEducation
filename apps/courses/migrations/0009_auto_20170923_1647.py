# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-23 16:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_teacher_image'),
        ('courses', '0008_video_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='organization.Teacher', verbose_name='\u8bfe\u7a0b\u8bb2\u5e08'),
        ),
        migrations.AddField(
            model_name='video',
            name='learn_times',
            field=models.IntegerField(default=0, verbose_name='\u5b66\u4e60\u65f6\u957f\u5355\u4f4d\u5206\u949f'),
        ),
    ]
