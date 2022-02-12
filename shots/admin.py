from django.contrib import admin
from shots.models import ShotCategory, Shot, ShotFile
from actions.models import Feedback

@admin.register(ShotCategory)
class ShotCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

class ShotFileInline(admin.TabularInline):
    model = ShotFile

class FeedbackInline(admin.TabularInline):
    model = Feedback


@admin.register(Shot)
class ShotAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'user')
    inlines = [
        ShotFileInline,
        FeedbackInline
    ]