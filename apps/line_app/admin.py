from django.contrib import admin

from apps.line_app.models import LineChannel


@admin.register(LineChannel)
class LineChannelAdmin(admin.ModelAdmin):
    pass
