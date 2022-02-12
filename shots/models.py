import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from utils.file_upload_helpers import upload_shotcover_hook, upload_shotfiles_hook

class ShotCategory(models.Model):
    title = models.CharField(max_length=80, unique="True", db_index=True)
    slug = models.SlugField(_("Slug"), max_length=80, blank=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.title
    


class ShotFile(models.Model):
    shot = models.ForeignKey("Shot", on_delete=models.CASCADE, related_name="shot_files")
    file = models.FileField(upload_to=upload_shotfiles_hook, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'mp4', 'webp'])])

class Shot(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='shots')
    shot_uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    category = models.ForeignKey(ShotCategory, related_name="shots", on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60, blank=True)
    description = models.TextField(help_text=_("Describe your shots"),blank=True)
    cover_shot = models.FileField(upload_to=upload_shotcover_hook, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'mp4', 'webp'])])
    user_like = models.ManyToManyField(get_user_model(), related_name='likes', blank=True)
    view_count = models.PositiveIntegerField(default=0, db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("shots:shot_details", kwargs={"shot_uuid": self.shot_uuid})

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-created"]

    def save(self, *args, **kwargs):
        original_slug = slugify(self.title)
        queryset =  Shot.objects.all().filter(slug__iexact=original_slug).count()

        count = 1
        slug = original_slug
        while(queryset):
            slug = original_slug + '-' + str(count)
            count += 1
            queryset = Shot.objects.all().filter(slug__iexact=slug).count()

        self.slug = slug
        super(Shot, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ('-created', )

#
@receiver(pre_delete, sender=ShotFile)
def delete_shot_files_hook(sender, instance, using, **kwargs):
    """
        Before deleting ShoFile object, delete the file on disc 
    """
    instance.file.delete()

@receiver(pre_delete, sender=Shot)
def delete_shot_files_hook(sender, instance, using, **kwargs):
    instance.cover_shot.delete()