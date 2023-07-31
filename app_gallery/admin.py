from django.contrib import admin
from .models import Picture, PictureHashtagRelation, Hashtag
from django.utils.html import format_html

class PictureHashtagRelationInline(admin.TabularInline):
    """Inline edition of hashtags for a picture, it allow add hashtags for a picture"""
    model = PictureHashtagRelation

class PictureAdmin(admin.ModelAdmin):
    """Set the display on django admin of the Picture"""
    list_display = ('title', 'uploaded_at', 'imagen')
    list_display_links = ('title', 'imagen')
    search_fields = ('title', )
    exclude = ('thumbnail',)
    inlines = [PictureHashtagRelationInline]
    readonly_fields = ('uploaded_at',)

    def imagen(self, obj):
        """Return the image to watch it on the admin"""
        return format_html("<img src={} height='100' />", obj.thumbnail.url)
 

admin.site.register(Hashtag)
admin.site.register(Picture, PictureAdmin)