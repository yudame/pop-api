from django.db import models


class Annotatable(models.Model):
    notes = models.ManyToManyField('common.Note', blank=True)

    @property
    def has_notes(self):
        return True if self.notes.count() else False

    def add_note(self, text_string):
        from apps.common.models import Note
        new_note = Note.objects.create(text=text_string)
        self.notes.add(new_note)

    class Meta:
        abstract = True
