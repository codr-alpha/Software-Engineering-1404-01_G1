from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import User
from .models import UserDetails


@receiver(post_save, sender=User)
def create_user_details(sender, instance, created, **kwargs):
    
    if created:
        UserDetails.objects.get_or_create(
            user=instance,
            defaults={
                'email': instance.email,
                'role': 'student',
            }
        )


@receiver(post_save, sender=User)
def update_user_details(sender, instance, created, **kwargs):
    if not created:
        try:
            user_details = UserDetails.objects.get(user=instance)
            if user_details.email != instance.email:
                user_details.email = instance.email
                user_details.save()
        except UserDetails.DoesNotExist:
            pass
