import logging
from rest_framework import generics, serializers, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import filters
from api.models import Category, Product, Order, Review, Provider
from api.serializers import CategorySerializer, ProductSerializer, OrderSerializer, ReviewSerializer, UserProfileSerializer, UserSerializer, ProviderSerializer
from django.shortcuts import get_object_or_404
from django.shortcuts import render

logger = logging.getLogger('api')

@api_view(['GET', 'POST'])
def categories_view(request):   #1 FBV
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=200)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=500)


@api_view(['GET', 'PUT', 'DELETE'])
def category_view(request, pk):     #2 FBV
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CategorySerializer(instance=category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=204)


class CategoryViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(user)
        return Response(serializer.data)

    def create(self, request):
        category_data = request.data
        category = Category.objects.create(name=category_data['name'])
        category.save()
        serializer = CategorySerializer(category)
        logger.debug(f'Category {serializer.instance} was created')
        logger.info(f'Category {serializer.instance} was created')
        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            instance = Category.objects.get(id=pk)
            instance.delete()
            logger.debug(f'Category {instance} was deleted')
            logger.info(f'Category {instance} was deleted')
        except:
            logger.error(f'Category {instance} cannot be deleted')
        return Response()

    def update(self, request, pk):
        category = Category.objects.get(id=pk)
        category.name = request.data['name']
        category.save()
        serializer = CategorySerializer(category)
        logger.debug(f'Category {serializer.instance} was updated')
        logger.info(f'Category {serializer.instance} was updated')
        return Response(serializer.data)


class ProviderViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        queryset = Provider.objects.all()
        serializer = ProviderSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Provider.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProviderSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        provider_data = request.data
        provider = Provider.objects.create(name=provider_data['name'], description = provider_data['description'])
        provider.save()
        serializer = ProviderSerializer(provider)
        logger.debug(f'Provider {serializer.instance} was created')
        logger.info(f'Provider {serializer.instance} was created')
        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            instance = Provider.objects.get(id=pk)
            instance.delete()
            logger.debug(f'Provider {instance} was deleted')
            logger.info(f'Provider {instance} was deleted')
        except:
            logger.error(f'Provider {instance} cannot be deleted')
        return Response()

    def update(self, request, pk):
        provider = Provider.objects.get(id=pk)
        provider.name = request.data['name']
        provider.description = request.data['description']
        provider.save()
        serializer = ProviderSerializer(provider)
        logger.debug(f'Provider {serializer.instance} was updated')
        logger.info(f'Provider {serializer.instance} was updated')
        return Response(serializer.data)



class CategoryProductsView(APIView):            #1 CBV
    filter_backends = (filters.OrderingFilter,)
    ordering = ('price', )

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        products = category.category_products.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProviderProductsView(APIView):        #2 CBV
    def get(self, request, pk):
        provider = get_object_or_404(Provider, pk=pk)
        products = provider.provider_products.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductViewSet(viewsets.ViewSet):  #3 viewset
    #permission_classes = (IsAuthenticated, )

    def list(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Product.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        product_data = request.data
        category = Category.objects.get(id = product_data['category'])
        provider = Provider.objects.get(id = product_data['provider'])
        product = Product.objects.create(name=product_data['name'], description = product_data['description'], category = category, provider = provider, image = product_data['image'], price = product_data['price'] )
        product.save()
        serializer = ProductSerializer(product)
        logger.debug(f'Product {serializer.instance} was created')
        logger.info(f'Product {serializer.instance} was created')
        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            instance = Product.objects.get(id=pk)
            instance.delete()
            logger.debug(f'Product {instance} was deleted')
            logger.info(f'Product {instance} was deleted')
        except:
            logger.error(f'Product {instance} cannot be deleted')
        return Response()

    def update(self, request, pk):
        product = Product.objects.get(id=pk)
        category = Category.objects.get(id = request.data['category'])
        provider = Provider.objects.get(id = request.data['provider'])

        product.name = request.data['name']
        product.description = request.data['description']
        product.price = request.data['price']
        product.provider = provider
        product.category = category
        product.image = request.data['image']
        product.save()
        serializer = ProductSerializer(product)
        logger.debug(f'Product {serializer.instance} was updated')
        logger.info(f'Product {serializer.instance} was updated')
        return Response(serializer.data)


  
class ProductView(APIView):                     #3 CBV
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'Product with ID {serializer.instance} was updated')
            logger.debug(f'Product with ID {serializer.instance} was updated')
            return Response(serializer.data)

        logger.error(f'Product with ID {serializer.instance} cannot be updated')
        return Response(serializer.errors, status=500)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=204)


class ReviewViewSet(viewsets.ViewSet):    #4 viewset
    permission_classes = (IsAuthenticated, )
    def list(self, request):
        queryset = Review.objects.all()
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Review.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ReviewSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        review_data = request.data
        review = Review.objects.create(text=review_data['text'], author = self.request.user)
        review.save()
        serializer = ReviewSerializer(review)
        logger.debug(f'Review {serializer.instance} was created')
        logger.info(f'Review {serializer.instance} was created')
        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            instance = Review.objects.for_user(self.request.user).get(id=pk)
            instance.delete()
            logger.debug(f'Review {instance} was deleted')
            logger.info(f'Review {instance} was deleted')
        except:
            logger.error(f'Review {instance} cannot be deleted')
        return Response()

    def update(self, request, pk):
        review = Review.objects.for_user(self.request.user).get(id=pk)
        review.text = request.data['text']
        review.save()
        serializer = ReviewSerializer(review)
        logger.debug(f'Review {serializer.instance} was updated')
        logger.info(f'Review {serializer.instance} was updated')
        return Response(serializer.data)
   
class ReviewsView(generics.ListCreateAPIView):      #4 CBV
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated, )

class OrdersView(generics.ListCreateAPIView):       #5 CBV
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderViewSet(viewsets.ViewSet):     #5 viewset
    permission_classes = (IsAuthenticated, )
    def list(self, request):
        queryset = Order.objects.for_user(self.request.user)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Order.objects.for_user(self.request.user)
        user = get_object_or_404(queryset, pk=pk)
        serializer = OrderSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        order_data = request.data
        order = Order.objects.create(product_name=order_data['product_name'], count = order_data['count'], user = self.request.user)
        order.save()
        serializer = OrderSerializer(order)
        logger.debug(f'Order {serializer.instance} was created')
        logger.info(f'Order {serializer.instance} was created')
        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            instance = Order.objects.get(id=pk)
            instance.delete()
            logger.debug(f'Order {instance} was deleted')
            logger.info(f'Order {instance} was deleted')
        except:
            logger.error(f'Order {instance} cannot be deleted')
        return Response()

    def update(self, request, pk):
        order = Order.objects.get(id=pk)
        order.product_name = request.data['product_name']
        order.count = request.data['count']
        order.save()
        serializer = OrderSerializer(order)
        logger.debug(f'Order {serializer.instance} was updated')
        logger.info(f'Order {serializer.instance} was updated')
        return Response(serializer.data)

