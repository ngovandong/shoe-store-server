from rest_framework import serializers
from .models import Shoe, Category, Comment, Sale, CartDetail, Stock, Customer, SaleDetail
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class ShoeSerializer(serializers.ModelSerializer):
    stocks = StockSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Shoe
        # fields = '__all__'
        fields = ['id', 'stocks', 'comments', 'price',
                  'name', 'desc', 'image', 'category', 'thumbnail']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ShoeNotDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoe
        fields = ["name", "get_thumbnail", "price"]


class CustomShoeField(serializers.RelatedField):
    def to_representation(self, value):
        return ShoeNotDepthSerializer(Shoe.objects.get(pk=value.id)).data


class CustomStockSerializer(serializers.ModelSerializer):
    shoe = CustomShoeField(read_only=True)

    class Meta:
        model = Stock
        fields = ["id", "size", "shoe"]


class CartDetailSerializer(serializers.ModelSerializer):
    stock = CustomStockSerializer(read_only=True)

    class Meta:
        model = CartDetail
        fields = ['id', 'qty', 'stock']


class SaleDetailSerializer(serializers.ModelSerializer):
    stock = CustomStockSerializer(read_only=True)

    class Meta:
        model = SaleDetail
        fields = ['qty', 'stock']


class SaleSerializer(serializers.ModelSerializer):
    # stocks = CustomStockSerializer(many=True, read_only=True)
    details = SaleDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = ['id', 'total', 'date', "details"]


class AddCartDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartDetail
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=4, max_length=127)
    password = serializers.CharField(
        min_length=4, max_length=127, write_only=True)

    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'phone',
                  'address', 'username', 'password']

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        user = User.objects.create_user(username=username, password=password)

        customer = Customer.objects.create(**validated_data, user=user)
        return customer


class CustomerDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'
