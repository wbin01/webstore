from django.contrib import admin


from store.models import (
    ModelBuy, ModelFavorites, ModelHighlightPosts, ModelProduct,
    ModelStoreProfile, ModelUserProfile)

admin.site.register(ModelBuy)
admin.site.register(ModelFavorites)
admin.site.register(ModelHighlightPosts)
admin.site.register(ModelProduct)
admin.site.register(ModelStoreProfile)
admin.site.register(ModelUserProfile)
