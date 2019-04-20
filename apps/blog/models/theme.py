from django.db import models



class Theme(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)

    license_href = models.URLField()
    js_href = models.URLField()
    css_href = models.URLField()

    live = models.BooleanField(default=False)


    # MODEL PROPERTIES
    # @property
    # def slug_source(self):
    #     return self.trello_board.name

    # MODEL FUNCTIONS
