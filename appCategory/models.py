from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Role(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    roles = models.ManyToManyField(Role, related_name='users')
    groups = models.ManyToManyField(Group, related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)

    def __str__(self):
        return self.username

    class Meta:
        permissions = [
            ('view_dashboard', 'Can view dashboard'),
            ('add_dashboard', 'Can add dashboard'),
            ('delete_dashboard', 'Can delete dashboard'),
            ('change_dashboard', 'Can change dashboard'),
            ('view_menu', 'Can view menu'),
            ('add_menu', 'Can add menu'),
            ('delete_menu', 'Can delete menu'),
            ('change_menu', 'Can change menu'),
        ]

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    sections = models.ManyToManyField('appSection.Section', related_name='many_categories', blank=True)
    def __str__(self):
        return self.name
