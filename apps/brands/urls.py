from django.urls import path

from .views import (
    AllBrandsView,
    AddCustomerBagItemView,
    AddCustomerFavoriteBrandView,
    AddCustomerFavoriteItemView,
    BrandPageView,
    RemoveCustomerBagItemView,
    RemoveCustomerFavoriteBrandView,
    RemoveCustomerFavoriteItemView,
    ListCustomerBagItemsView,
    ListCustomerFavoriteBrandsView,
    ListCustomerFavoriteItemsView,
)

urlpatterns = [
    path('all-brands/', AllBrandsView.as_view()),
    path('brand/<int:pk>', BrandPageView.as_view(), name='brand'),
    path('add-bag-item/<int:item>', AddCustomerBagItemView.as_view(), name='add_bag_item'),
    path('add-fav-brand/<int:brand>', AddCustomerFavoriteBrandView.as_view(), name='add_fav_brand'),
    path('add-fav-item/<int:item>', AddCustomerFavoriteItemView.as_view(), name='add_fav_item'),
    path('remove-bag-item/<int:item>', RemoveCustomerBagItemView.as_view(), name='remove_bag_item'),
    path('remove-fav-brand/<int:brand>', RemoveCustomerFavoriteBrandView.as_view(), name='remove_fav_brand'),
    path('remove-fav-item/<int:item>', RemoveCustomerFavoriteItemView.as_view(), name='remove_fav_item'),
    path('list-bag-items/', ListCustomerBagItemsView.as_view()),
    path('list-fav-brands/', ListCustomerFavoriteBrandsView.as_view()),
    path('list-fav-items/', ListCustomerFavoriteItemsView.as_view()),
]
