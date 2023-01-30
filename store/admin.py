from django.contrib import admin


from store.models import (
    ModelPost, ModelHighlightPosts, ModelStoreProfile)

admin.site.register(ModelPost)
admin.site.register(ModelHighlightPosts)
admin.site.register(ModelStoreProfile)
