from api.validators import validate_extension, validate_size
from rest_framework import serializers
from django.utils.text import gettext_lazy as _
from api.models import Category, Product, Order, Review, BaseInfo, Profile, Provider
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class UserSerializer(serializers.ModelSerializer):      #1 Model Serializer
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'email', 'is_staff')

class UserProfileSerializer(serializers.ModelSerializer):       #2 Model Serializer
    user = UserSerializer(read_only=True)                       #Nested serializer
    info = serializers.CharField()
    DOB = serializers.DateField()
    gender = serializers.CharField()
    avatar = serializers.ImageField(validators=[validate_size, validate_extension])
    class Meta:
        model = Profile
        fields = '__all__'


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    token = None

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

class BaseInfoSerializer(serializers.Serializer):       #1 Serializer
    name = serializers.CharField()
    class Meta:
        model = BaseInfo
        fields = ('id', 'name')
        abstract = True



class CategorySerializer(BaseInfoSerializer, serializers.ModelSerializer):      #3 Model Serializer #1 Serializer Inheritance
    class Meta():
        model = Category
        fields = BaseInfoSerializer.Meta.fields
    def create(self, validated_data):
        category = Category(**validated_data)
        category.save()
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class ProviderSerializer(BaseInfoSerializer, serializers.ModelSerializer):      #4 Model Serializer  #2 Serializer Inheritance
    class Meta():
        model = Provider 
        fields = BaseInfoSerializer.Meta.fields + ('description', )
    def create(self, validated_data):
        provider = Provider(**validated_data)
        provider.save()
        return provider

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

class ProductSerializer(BaseInfoSerializer, serializers.ModelSerializer):       #3 Serializer Inheritance
    description = serializers.CharField(required=True)
    price = serializers.IntegerField(required=True)
    image = serializers.FileField(required=True,
                              validators=[validate_size, validate_extension])
    category = CategorySerializer(read_only=True)           #Nested serializer  
    provider = ProviderSerializer(read_only=True)           #Nested serializer     
    class Meta():
        model = Product 
        fields = BaseInfoSerializer.Meta.fields + ('description', 'price', 'image', 'category', 'provider', )

    def create(self, validated_data):
        product = Product(**validated_data)
        product.save()
        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.provider = validated_data.get('provider', instance.provider)
        instance.category = validated_data.get('category', instance.category)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
    
    def validate(self, object):                             
        if object['price'] <= 0:                    #validator 3
            raise serializers.ValidationError("Price should be positive number")
        if len(object['description'])   <=10:       #validator 4
            raise serializers.ValidationError("Description should contain at least 10 characters")
        if len(object['name'])   >=10:       #validator 5
            raise serializers.ValidationError("Name should contain at most 10 characters")
        return object


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)                   #Nested serializer
    product_name = serializers.CharField(required=True)
    count = serializers.IntegerField(required=True)
    class Meta:
        model = Order
        fields = '__all__'  
    def validate(self, object):                             
        if object['count'] <= 0:                            #validator 6
            raise serializers.ValidationError("You have to enter positive number for count")
        return object

class ReviewSerializer(serializers.Serializer):         #2 Serializer
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(required=True)
    author = UserSerializer(read_only=True)             #Nested serializer
    
    def create(self, validated_data):
        review = Review(**validated_data)
        review.save()
        return review

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance

    class Meta:
        model = Review 
        fields =('id', 'text', 'author',)