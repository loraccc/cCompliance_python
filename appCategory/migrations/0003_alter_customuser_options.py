# Generated by Django 4.2.4 on 2024-07-24 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appCategory', '0002_alter_customuser_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': [('view_dashboard', 'Can view dashboard'), ('add_dashboard', 'Can add dashboard'), ('change_dashboard', 'Can change dashboard'), ('view_menu', 'Can view menu'), ('add_menu', 'Can add menu'), ('delete_menu', 'Can delete menu')]},
        ),
    ]
