from django.contrib import admin
from .models import Post, PostTagList, PostTagName, PostComment


class PictureContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'upload_date')


class PictureTagListAdmin(admin.ModelAdmin):
    list_display = ('content', 'tag')


class PictureTagNameAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PictureCommentNameAdmin(admin.ModelAdmin):
    list_display = ('topic', 'message',)


admin.site.register(Post, PictureContentAdmin)
admin.site.register(PostTagList, PictureTagListAdmin)
admin.site.register(PostTagName, PictureTagNameAdmin)
admin.site.register(PostComment, PictureCommentNameAdmin)


# Register your models here.
