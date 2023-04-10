# REST Framework Imports
from rest_framework.routers import SimpleRouter

from .views import v1

brands_router_v1 = SimpleRouter(trailing_slash=False)
brands_router_v1.register(r"", v1.BrandViewSet, basename="brands")


urlpatterns = [
    # path('add-bag-item/<int:item>', AddCustomerBagItemView.as_view(), name='add_bag_item'),
    # path('add-fav-brand/<int:brand>', AddCustomerFavoriteBrandView.as_view(), name='add_fav_brand'),
    # path('add-fav-item/<int:item>', AddCustomerFavoriteItemView.as_view(), name='add_fav_item'),
    # path('remove-bag-item/<int:item>', RemoveCustomerBagItemView.as_view(), name='remove_bag_item'),
    # path('remove-fav-brand/<int:brand>', RemoveCustomerFavoriteBrandView.as_view(), name='remove_fav_brand'),
    # path('remove-fav-item/<int:item>', RemoveCustomerFavoriteItemView.as_view(), name='remove_fav_item'),
    # path('list-bag-items/', ListCustomerBagItemsView.as_view()),
    # path('list-fav-brands/', ListCustomerFavoriteBrandsView.as_view()),
    # path('list-fav-items/', ListCustomerFavoriteItemsView.as_view()),
]
