from django.db import models
from django.contrib.postgres.fields import ArrayField

class LanguageField(models.CharField):
    """
    A language field for Django models.
    """
    def __init__(self, *args, **kwargs):
        # Local import so the languages aren't loaded unless they are needed.
        from ..utilities.languages import LANGUAGES

        kwargs.setdefault('max_length', 3)
        kwargs.setdefault('choices', LANGUAGES)
        super(models.CharField, self).__init__(*args, **kwargs)


class Translatable(models.Model):

    base_language = LanguageField()
    languages = ArrayField(LanguageField(), default=list)

    class Meta:
        abstract = True


# credit: https://github.com/audiolion/django-language-field
