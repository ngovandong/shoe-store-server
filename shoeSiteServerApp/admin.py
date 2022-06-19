from django.contrib import admin
from .models import Shoe, Customer, CartDetail, Sale, SaleDetail, Stock, Comment, Category
# Register your models here.
admin.site.register(Shoe)
admin.site.register(Customer)
admin.site.register(CartDetail)
admin.site.register(Sale)
admin.site.register(SaleDetail)
admin.site.register(Stock)
admin.site.register(Comment)
admin.site.register(Category)
