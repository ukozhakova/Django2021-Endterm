from django.urls import path, re_path
from django.conf.urls import url
from api.views import views, auth
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
router = DefaultRouter()
router.register('providers', views.ProviderViewSet, basename='providers')   #DONE
router.register('orders', views.OrderViewSet, basename='orders')            #DONE
router.register('categories', views.CategoryViewSet, basename='categories') #DONE
router.register('reviews', views.ReviewViewSet, basename='reviews')         #DONE
router.register('products', views.ProductViewSet, basename='products')      #DONE
router.register('profiles', auth.UserProfileViewSet, basename='profiles')   #DONE
router.register('logout', auth.LogoutViewSet, basename='logout')            #DONE
router.register('signup', auth.SignUpViewSet, basename='signup')            #DONE

urlpatterns = [
    path('categories/<int:pk>/products/', views.CategoryProductsView.as_view()), #DONE
    path('providers/<int:pk>/products/', views.ProviderProductsView.as_view()), #DONE
    path('users/', auth.UserList.as_view()),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),  #DONE
    path('login/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  #DONE
]
urlpatterns+=router.urls