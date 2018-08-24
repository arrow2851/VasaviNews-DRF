from django.contrib import admin

from sub.models import Post, Comment, Class, News, Clubs

admin.site.register(Comment)
admin.site.register(News)
admin.site.register(Clubs)
admin.site.register(Class)
admin.site.register(Post)

# Register your models here.
