from django.contrib import admin

from apps.common.models import Image, Address, Note


class CSSAdminMixin(object):
    class Media:
        css = {
            'all': ('css/admin.css',),
        }


class MyModelAdmin(admin.ModelAdmin, CSSAdminMixin):
    pass


@admin.register(Image)
class ImageAdmin(MyModelAdmin):
    list_display = (
        'id',
        'created_at',
        'url',
    )
    list_filter = (
        'created_at',
        'modified_at',
    )
    date_hierarchy = 'created_at'


@admin.register(Address)
class AddressAdmin(MyModelAdmin):
    pass


@admin.register(Note)
class NoteAdmin(MyModelAdmin):
    pass
