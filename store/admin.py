from django.contrib import admin


from store.models import (
    ModelProduct, ModelHighlightPosts, ModelStoreProfile, ModelUserProfile)

admin.site.register(ModelProduct)
admin.site.register(ModelHighlightPosts)
admin.site.register(ModelStoreProfile)
admin.site.register(ModelUserProfile)
