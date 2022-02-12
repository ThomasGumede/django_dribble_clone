from django import forms
from shots.models import Shot
from django.core.validators import FileExtensionValidator


class ShotForm(forms.ModelForm):
    files  = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'mp4', 'webp'])])
    class Meta:
        model = Shot
        fields = ('title', 'category', 'cover_shot', 'description')