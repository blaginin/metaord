from django.contrib.auth.models import User, Group, Permission
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from uuid import UUID
from worker.models import Operator
from metaord.models import Order
from chief.models import WebmsInvite


def is_valid_uuid(uuid_str, version=4):
    """
    Check if uuid_str has a valid UUID format.
    #Parameters: @uuid_str : str, @version : {1, 2, 3, 4}
    #Returns: `True` if uuid_str is a valid UUID, otherwise `False`.
    """
    try:
        uuid_obj = UUID(uuid_str, version=version)
    except:
        return False
    return True

class Groups:
    @staticmethod
    def is_user_chief(user):
        return user.groups.filter(name='chief').exists()

    @staticmethod
    def get_or_create_worker():
        group, created = Group.objects.get_or_create(name='worker')
        if created:
            group.permissions.add(Permissions.change_order_status())
            # logger.info('operator_user Group created')
        return group

    @staticmethod
    def get_or_create_webms():
        group, created = Group.objects.get_or_create(name='webms')
        if created:
            group.permissions.add(Permissions.change_webms_invite_status())
            # logger.info('operator_user Group created')
        return group

    @staticmethod
    def get_or_create_chief():
        group, created = Group.objects.get_or_create(name='chief')
        if created:
            group.permissions.add(Permissions.delete_orders(), Permissions.delete_operators())
            # logger.info('chief Group created')
        return group


class Permissions:
    @staticmethod
    def change_webms_invite_status():
        perm = Permission.objects.filter(codename='change_webms_invite_status').first()
        if perm is not None:
            return perm
        else:
            content_type = ContentType.objects.get_for_model(WebmsInvite)
            return Permission.objects.create(codename='change_webms_invite_status',
                                            name='change webms invite status',
                                            content_type=content_type)

    @staticmethod
    def change_order_status():
        perm = Permission.objects.filter(codename='change_order_status').first()
        if perm is not None:
            return perm
        else:
            content_type = ContentType.objects.get_for_model(Order)
            return Permission.objects.create(codename='change_order_status',
                                            name='Can change order status',
                                            content_type=content_type)

    @staticmethod
    def delete_orders():
        content_type = ContentType.objects.get_for_model(Order)
        return Permission.objects.create(codename='delete_orders',
                                       name='delete_orders',
                                       content_type=content_type)

    @staticmethod
    def delete_operators():
        content_type = ContentType.objects.get_for_model(Operator)
        return Permission.objects.create(codename='delete_operators',
                                       name='delete_operators',
                                       content_type=content_type)