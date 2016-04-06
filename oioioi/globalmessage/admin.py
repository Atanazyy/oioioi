from django.conf.urls import url
from django.core.urlresolvers import reverse
from oioioi.base import admin
from django.utils.translation import ugettext_lazy as _

from oioioi.base.permissions import is_superuser

from oioioi.globalmessage.models import GlobalMessage


class GlobalMessageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['enabled', 'message']}),
        (_('Auto show and hide'), {'fields': ['start', 'end']}),
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        pk = GlobalMessage.get_singleton().pk
        urls = super(GlobalMessageAdmin, self).get_urls()

        custom_urls = [
            url(r'^$',
                self.admin_site.admin_view(self.change_view),
                {'object_id': str(pk)}),
        ]

        return custom_urls + urls


admin.site.register(GlobalMessage, GlobalMessageAdmin)


admin.system_admin_menu_registry.register(
        'globalmessage',
        _("Global message"),
        lambda request: reverse(
            'oioioiadmin:globalmessage_globalmessage_changelist'
        ),
        condition=is_superuser,
        order=20
)