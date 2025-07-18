# Generated by Django 5.2.1 on 2025-06-25 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_paper_journal_abbreviation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paper',
            name='data_type',
        ),
        migrations.RemoveField(
            model_name='paper',
            name='disease_category',
        ),
        migrations.RemoveField(
            model_name='paper',
            name='field_category',
        ),
        migrations.RemoveField(
            model_name='paper',
            name='model_type',
        ),
        migrations.RemoveField(
            model_name='paper',
            name='sample_size',
        ),
        migrations.RemoveField(
            model_name='paper',
            name='technique',
        ),
        migrations.AddField(
            model_name='paper',
            name='chemical_class',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='paper',
            name='experimental_model',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='paper',
            name='exposure_route',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='paper',
            name='health_effects',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='paper',
            name='mechanism',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='paper',
            name='target_organism',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
