from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'shoes', views.ShoeViewSet, basename="shoe")
# router.register(r'customers', views.CustomerViewSet, basename="customer")
router.register(r'categories', views.CategoryViewSet, basename="category")
router.register(r'cart_details', views.CartDetailViewSet,
                basename="cart_detail")
router.register(r'comments', views.CommentCreateViewSet,
                basename="comment")
router.register(r'customers', views.CustomerView,
                basename="customer")
router.register(r'sales', views.SaleViewSet,
                basename="sale")


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('signup/', views.SignUpView.as_view())
]
