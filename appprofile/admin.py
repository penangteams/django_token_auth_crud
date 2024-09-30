from django.contrib import admin
from .models import Profile
from django.utils.html import format_html


# Register the Profile model with the admin site
class ProfileAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html(
            '<img src="{}" width="50" height="50"/>'.format(obj.media_file.url)
        )

    image_tag.short_description = "Image"

    list_display = [
        "name",
        "image_tag",
    ]


admin.site.register(Profile, ProfileAdmin)
