# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-11 09:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_add_custom_ordering_to_reimbursement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reimbursement',
            name='document_number',
            field=models.CharField(blank=True, max_length=140, null=True, verbose_name='Document number'),
        ),
        migrations.AlterField(
            model_name='reimbursement',
            name='party',
            field=models.CharField(blank=True, db_index=True, max_length=7, null=True, verbose_name='Party'),
        ),
        migrations.AlterField(
            model_name='reimbursement',
            name='state',
            field=models.CharField(blank=True, db_index=True, max_length=2, null=True, verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='reimbursement',
            name='term',
            field=models.IntegerField(blank=True, null=True, verbose_name='Term'),
        ),
        migrations.AlterField(
            model_name='reimbursement',
            name='term_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Term ID'),
        ),
    ]
