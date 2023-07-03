from django.db import models

# Create your models here.


class PABaseModel(models.Model):
    """
    This is a base model for all models to inherit from.
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
