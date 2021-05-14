from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class BaseInfo(models.Model):
    name = models.CharField(max_length=100)
    

    class Meta:
        abstract = True
    
    def __str__(self):
        return '{}'.format(self.name)

class Category(BaseInfo):
    class Meta(BaseInfo.Meta):
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    def __str__(self):
        return '{}'.format(self.name)

    
class Provider(BaseInfo):
    description = models.TextField(blank=True)

    def __str__(self):
        return '{}'.format(self.name)


class ProductManager1(models.Manager):          #1 Manager
    def for_provider(self, provider):
        return self.filter(provider=provider)

class ProductManager2(models.Manager):          #2 Manager
    def for_category(self, category):
        return self.filter(category = category)

class Product(BaseInfo):
    category = models.ForeignKey(Category, related_name = 'category_products', on_delete = models.CASCADE)              #1 FK
    provider = models.ForeignKey(Provider, related_name='provider_products', on_delete=models.CASCADE, blank=True, null=True)        #2 FK
    image = models.FileField(upload_to='images/products',
                              null=True, blank=True)                             #FileUpload
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.name)


class OrderManager(models.Manager):         #3 Manager
    def for_user(self, user):
        return self.filter(user=user)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)          #3 FK
    product_name = models.CharField(max_length=100, default="TIE-DYE CROP TOP")
    count = models.IntegerField(default=1)
    objects = OrderManager()

    def __str__(self):
        return '{}: {}'.format(self.product_name, self.count)


class ReviewManager(models.Manager):            #4 Manager
    def for_user(self, user):
        return self.filter(author=user) 


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True)         #4 FK
    objects = ReviewManager()
    def __str__(self):
        return '{}'.format(self.author)



class Gender(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)      #5 FK
    info = models.TextField(max_length=1000, blank=True)
    DOB = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=Gender.choices, default=Gender.MALE, max_length=20, blank=True)
    avatar = models.ImageField(upload_to = 'images/avatars', null=True, blank=True)         #FileUpload
    
    def __str__(self):
        return '{}'.format(self.user)
