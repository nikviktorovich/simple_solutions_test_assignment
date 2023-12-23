from django.db import migrations
from django.db import models
import django.db.models.deletion


def migrate_item_to_order(apps, schema_editor):
    Order = apps.get_model('items', 'Order')
    Payment = apps.get_model('payments', 'Payment')

    for payment in Payment.objects.all():
        item = payment.item
        order = Order.objects.create()
        order.items.add(item)
        payment.order = order
        payment.save()


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_order'),
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='items.order'),
        ),
        migrations.RunPython(code=migrate_item_to_order),
        migrations.AlterField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(null=False, on_delete=django.db.models.deletion.CASCADE, to='items.order'),
        ),
        migrations.RemoveField(
            model_name='payment',
            name='item',
        )
    ]
