from django.contrib import admin

from eventlog.models import Event


class EventAdmin(admin.ModelAdmin):
    raw_id_fields = ["user"]
    list_filter = ["label", "timestamp", "user"]
    list_display = ["timestamp", "user", "label", "message", "extra"]
    search_fields = ["user__username", "user__email", "label", "message", "extra"]


admin.site.register(Event, EventAdmin)
