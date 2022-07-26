from django.contrib import admin

from .models import Post, PostLike

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'edited_timestamp')
    search_fields = ('user__username', 'user__email')


class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'post_user', 'user', 'is_liked', 'timestamp')
    search_fields = ('user__username', 'user__email', 'post__user__username', 'post__user__email')

    def post_user(self, obj):
        return obj.post.user

admin.site.register(Post, PostAdmin)
admin.site.register(PostLike, PostLikeAdmin)
