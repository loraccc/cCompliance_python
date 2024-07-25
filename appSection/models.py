from django.db import models

class Section(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    # category = models.ForeignKey('Compliance_app.Category', on_delete=models.CASCADE, related_name='single_sections')
    def __str__(self):
        return self.name