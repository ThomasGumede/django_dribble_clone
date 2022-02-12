from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.db.models.signals import pre_delete
from django.dispatch import receiver

def handle_profile_upload(instance, filename):
    return f"profile/myimage_{instance.pk}/{filename}"

class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to="profile/", blank=True)
    biography = models.TextField(blank=True)
    location = models.CharField(max_length=150, blank=True)
    website = models.URLField(blank=True, null=True)
    following = models.ManyToManyField('self', through='Contact', symmetrical=False, related_name='followers')


    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'driblle@clone.com',
            [self.email],
            fail_silently=False,
        )
    
    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse_lazy("accounts:user_details", kwargs={"username": self.username, 'pk': self.pk})
    
class Contact(models.Model):
    user_from = models.ForeignKey(CustomUser, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(CustomUser, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'

# Signals for deleting object file from memory disk
@receiver(pre_delete, sender=CustomUser)
def delete_content_files_hook(sender, instance, using, **kwargs):
	instance.photo.delete()