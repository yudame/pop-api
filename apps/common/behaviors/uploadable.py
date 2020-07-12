import json
import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models


# USE CLOUDINARY AS DEFUALT CLOUD HOST
import cloudinary
cloudinary.config()


class Uploadable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    url = models.URLField(default="")

    original_url = models.URLField(default="", blank=True)
    backup_url = models.URLField(default="", blank=True)  # pretty much always on AWS S3
    meta_data = JSONField(blank=True, null=True)

    class Meta:
        abstract = True

    # MODEL PROPERTIES
    @property
    def file_name(self):
        try: return self.meta_data.get('original_filename', "")
        except AttributeError: pass

    @property
    def file_type(self):
        try: return self.meta_data.get('type', "")
        except AttributeError: return ""

    @property
    def file_format(self):
        try: return self.meta_data.get('format', "")
        except AttributeError: return ""


    # MODEL FUNCTIONS
    def upload_file(self, local_filename):
        if not self.url:
            import cloudinary.uploader
            cloudinary_response_dict = cloudinary.uploader.upload(local_filename)
            if cloudinary_response_dict['bytes'] > 0:
                self.metadata = cloudinary_response_dict
                self.original_url = cloudinary_response_dict['url']
                self.url = cloudinary_response_dict['url']
