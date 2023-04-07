from rest_framework import serializers

from .models import (
    Brand,
    CustomerBagItem,
    CustomerFavoriteBrand,
    CustomerFavoriteItem,
    HomePageSection,
    InventoryItemColor,
    InventoryItemColorImage,
    InventoryItemColorSize,
)

class BrandSerializer(serializers.ModelSerializer):
    brand_page = serializers.HyperlinkedRelatedField(view_name='brand', read_only=True, source='pk')
    is_user_fav = serializers.SerializerMethodField()
    add_fav = serializers.HyperlinkedRelatedField(view_name='add_fav_brand', read_only=True, source='pk', lookup_url_kwarg='brand')
    remove_fav = serializers.HyperlinkedRelatedField(view_name='remove_fav_brand', read_only=True, source='pk', lookup_url_kwarg='brand')

    def get_is_user_fav(self, obj):
        return obj.is_user_fav(self.context['request'].user)

    class Meta:
        model = Brand
        exclude = ['id']


class InventoryItemColorSizeSerializer(serializers.ModelSerializer):
    size_display = serializers.CharField(source='get_size_display')

    class Meta:
        model = InventoryItemColorSize
        exclude = ['id', 'inventory_item_color']


class InventoryItemColorImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItemColorImage
        exclude = ['id', 'inventory_item_color']


class InventoryItemColorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='inventory_item.name')
    brand = serializers.CharField(source='inventory_item.collection.brand.name')
    collection = serializers.CharField(source='inventory_item.collection.name')
    image = serializers.ImageField(default=None)

    class Meta:
        model = InventoryItemColor
        exclude = ['id', 'inventory_item']


class BrandPageSerializer(serializers.ModelSerializer):
    items = InventoryItemColorSerializer(many=True)
    is_user_fav = serializers.SerializerMethodField()
    add_fav = serializers.HyperlinkedRelatedField(view_name='add_fav_brand', read_only=True, source='pk', lookup_url_kwarg='brand')
    remove_fav = serializers.HyperlinkedRelatedField(view_name='remove_fav_brand', read_only=True, source='pk', lookup_url_kwarg='brand')

    def get_is_user_fav(self, obj):
        return obj.is_user_fav(self.context['request'].user)

    class Meta:
        model = Brand
        exclude = ['id']


class CustomerBagItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerBagItem
        fields = '__all__'


class CustomerFavoriteBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerFavoriteBrand
        fields = '__all__'


class CustomerFavoriteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerFavoriteItem
        fields = '__all__'


class HomePageSectionSerializer(serializers.ModelSerializer):
    item = InventoryItemColorSerializer()
    brand = BrandSerializer()
    items = InventoryItemColorSerializer(many=True)
    brands = BrandSerializer(many=True)

    class Meta:
        model = HomePageSection
        exclude = ['id', 'show_on_home_page', 'order']

    def to_representation(self, instance):
        repr = super().to_representation(instance)

        if repr["section_type"] == 'item_image':
            repr["data"] = repr["item"]
        elif repr["section_type"] == 'brand_image':
            repr["data"] = repr["brand"]
        elif repr["section_type"] == 'items':
            repr["data"] = repr["items"]
        elif repr["section_type"] == 'brands':
            repr["data"] = repr["brands"]

        repr.pop("item")
        repr.pop("brand")
        repr.pop("items")
        repr.pop("brands")

        return repr
