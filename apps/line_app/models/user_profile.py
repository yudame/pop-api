# from django.db import models
#
# class LineUserProfile(models.Model):
#     # get from line
#     # user = models.OneToOneField(User, on_delete=models.CASCADE) #OneToOneField is used to extend the original User object provided from Django.
#     line_id = models.CharField(max_length=50)
#     name = models.CharField(max_length=100)
#     picture_url = models.URLField()
#     status_message = models.CharField(max_length=100, blank=True, null=True)
#     unfollow = models.BooleanField(default=False)
#     promotable = models.BooleanField(default=False)
