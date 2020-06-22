from django.contrib import admin

from apps.line_app.models import LineChannel


@admin.register(LineChannel)
class LineChannelAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'line_bot_callback_uri',
        'bot_id',
        'numeric_id',
    )
    readonly_fields = ['line_bot_callback_uri', 'id']
    date_hierarchy = 'created_at'
