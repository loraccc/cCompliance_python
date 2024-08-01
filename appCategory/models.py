from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Role(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    roles = models.ManyToManyField(Role, related_name='users', blank=True)
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

from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='uploaded_documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)
    expiration_date = models.DateTimeField(default=timezone.now() + timedelta(days=60))

    def save(self, *args, **kwargs):
        if not self.expiration_date:
            self.expiration_date = self.uploaded_at + timedelta(days=60)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expiration_date

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    sections = models.ManyToManyField('appSection.Section', related_name='many_categories', blank=True)

    def __str__(self):
        return self.name

# class Feature(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self) -> str:
#         return self.name
