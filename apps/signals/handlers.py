from django.db.models.signals import post_save
from django.dispatch import receiver
from metaord.models import Order
from signals.postbacks import order_created, order_upd_status


@receiver(post_save, sender=Order) # care: post_save
def do_postback(sender, instance, **kwargs):
    old_order = sender.objects.filter(pk=instance.pk).first()
    if old_order is not None:
        if old_order.status != instance.status:
            order_upd_status(instance)
    else:
        order_created(instance)
