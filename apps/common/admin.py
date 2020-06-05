from django.contrib import admin


class CSSAdminMixin(object):
    class Media:
        css = {
            'all': ('css/admin.css',),
        }


class MyModelAdmin(admin.ModelAdmin, CSSAdminMixin):
    pass
