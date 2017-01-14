from django.db.models.signals import post_save                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
from django.dispatch import receiver
from metaord.models import Order
from signals.postbacks import order_created, order_upd_status


@receiver(post_save, sender=Order) # care: post_save
def do_postback(sender, instance, **kwargs):
    print('postBACK!!!', instance.pk, instance.is_new)

    if instance.is_new == False:
        Order.objects.filter(id=instance.id).update(is_new=False)
        order_upd_status(instance)
    else:
        print('\tcall me')
        order_created(instance)
