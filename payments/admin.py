from django.contrib import admin

from payments import models


class PaymentAdmin(admin.ModelAdmin):
    model = models.Payment


admin.site.register(models.Payment, admin_class=PaymentAdmin)
