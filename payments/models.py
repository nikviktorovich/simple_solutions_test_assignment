from django.db import models

import items.models


class Payment(models.Model):
    item = models.ForeignKey(items.models.Item, on_delete=models.CASCADE)
    session_id = models.TextField()
