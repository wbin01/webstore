from django.contrib import admin


from store.models import (
    ModelCart, ModelBuy, ModelFavorite, ModelHighlightProducts, ModelProduct,
    ModelStoreProfile, ModelUserProfile)

admin.site.register(ModelBuy)
admin.site.register(ModelCart)
admin.site.register(ModelFavorite)
admin.site.register(ModelHighlightProducts)
admin.site.register(ModelProduct)
admin.site.register(ModelStoreProfile)
admin.site.register(ModelUserProfile)
