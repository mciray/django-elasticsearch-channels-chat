from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'user_status',
        {
            'type': 'user_status',
            'username': user.username,
            'is_online': True,
        }
    )

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'user_status',
        {
            'type': 'user_status',
            'username': user.username,
            'is_online': False,
        }
    )