from django.db import models

import items.models


class Payment(models.Model):
    order = models.ForeignKey(
        items.models.Order,
        on_delete=models.CASCADE,
        null=False,
    )
    session_id = models.TextField()
