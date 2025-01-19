from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Student
from main.models import ChallengeTracker, Challenge

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(post_save, sender=Challenge)
def create_challenge_trackers(sender, instance, created, **kwargs):
    if created:  # Check if this is a new challenge
        students = Student.objects.filter(grade=instance.grade)  # Get students in the same grade
        for student in students:
            ChallengeTracker.objects.create(
                student=student,
                challenge=instance,
            )

@receiver(post_save, sender=Student)
def create_challenge_trackers(sender, instance, created, **kwargs):
    if created:  # Check if this is a new challenge
        challenges = Challenge.objects.filter(grade=instance.grade)
        for challenge in challenges:
            ChallengeTracker.objects.create(
                student=instance,
                challenge=challenge,
            )