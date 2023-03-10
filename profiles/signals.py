from django.db.models.signals import post_save,pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Relationship

# create profile when create user
@receiver(post_save, sender=User)
# sender = User // django.contrib.auth.models.User
# instance = name of User
# created = bool
def post_save_create_profile(sender, instance, created, **kwargs):
    # print('sender', sender)
    # print('instance', instance)
    if created:
        Profile.objects.create(user=instance)


# create friends relationship
@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    # sender= from Relationship model
    sender_ = instance.sender
    # receiver from Relationship model
    receiver_ = instance.receiver
    # status from Relationship model
    if instance.status == 'accepted':
        # friends from Profile model
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()



# delate friend from profile
@receiver(pre_delete,sender=Relationship)
def pre_delete_remove_from_friends(sender,instance,**kwargs):
    sender=instance.sender
    receiver=instance.receiver
    # friends profile friends field
    sender.friends.remove(receiver.user)
    receiver.friends.remove(sender.user)
    sender.save()
    receiver.save()