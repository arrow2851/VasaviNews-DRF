from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from sub.models import Post, Comment, Class, News, Clubs
class CommentAdmin(DjangoMpttAdmin):
    pass


admin.site.register(Comment, CommentAdmin)
admin.site.register(News)
admin.site.register(Clubs)
admin.site.register(Class)
admin.site.register(Post)

# Register your models here.
