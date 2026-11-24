from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Ebook(models.Model):
    TEMPLATE_CHOICES = [
        ('business', 'Minimalist Business'),
        ('tech', 'Modern Tech & AI'),
        ('cookbook', 'Creative Cookbook'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    author = models.CharField(max_length=100)
    template_style = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default='business')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE, related_name='chapters')
    order = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=200)
    content = models.TextField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.ebook.title} - Chapter {self.order}: {self.title}"


class Ebook(models.Model):
    TEMPLATE_CHOICES = [
        ('business', 'Minimalist Business'),
        ('tech', 'Modern Tech & AI'),
        ('cookbook', 'Creative Cookbook'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    author = models.CharField(max_length=100)
    template_style = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default='business')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE, related_name='chapters')
    order = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=200)
    content = models.TextField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.ebook.title} - Chapter {self.order}: {self.title}"


class UserProfile(models.Model):
    PLAN_CHOICES = [
        ('free', 'Free Plan'),
        ('pro', 'Pro Plan'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    paystack_reference = models.CharField(max_length=100, blank=True, null=True)
    subscription_active = models.BooleanField(default=False)

    def is_pro(self):
        return self.plan == 'pro' and self.subscription_active

    def __str__(self):
        return f"{self.user.username} ({self.plan})"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
