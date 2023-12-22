from django.contrib import admin

from items import models


class ItemAdmin(admin.ModelAdmin):
    model = models.Item


admin.site.register(models.Item, admin_class=ItemAdmin)
