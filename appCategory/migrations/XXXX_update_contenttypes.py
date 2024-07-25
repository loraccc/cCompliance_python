from django.db import migrations

def update_contenttypes(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    old_app_name = 'Compliance_app'
    new_app_name = 'appCategory'

    content_types = ContentType.objects.filter(app_label=old_app_name)
    for content_type in content_types:
        content_type.app_label = new_app_name
        content_type.save()

class Migration(migrations.Migration):

    dependencies = [
        ('appCategory', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_contenttypes),
    ]
