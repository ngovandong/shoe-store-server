from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from io import BytesIO
from PIL import Image
from shoeSiteServer.settings import BASE_URL


class Category(models.Model):
    name = models.TextField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Shoe(models.Model):
    name = models.TextField(max_length=200)
    desc = models.TextField()
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(
        "Category", related_name="shoes", on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.thumbnail:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
        super().save(*args, **kwargs)

    def get_thumbnail(self):
        return BASE_URL + self.thumbnail.url

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, "JPEG", quality=85)
        return File(thumb_io, name=image.name)


class Comment(models.Model):
    name = models.TextField(max_length=200)
    content = models.TextField(max_length=300)
    star = models.IntegerField(default=5)
    shoe = models.ForeignKey(
        "Shoe", related_name="comments", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Stock(models.Model):
    size = models.IntegerField(default=36)
    qty = models.IntegerField(default=0)
    shoe = models.ForeignKey(
        "Shoe", related_name="stocks", on_delete=models.CASCADE)

    class Meta:
        ordering = ["shoe", "size"]
        constraints = [
            models.UniqueConstraint(
                fields=['size', 'shoe'], name='unique_migration_stock_size'
            )
        ]

    def __str__(self) -> str:
        return "shoe: {}, size: {}, qty: {}".format(self.shoe.id, self.size, self.qty)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=50)
    email = models.TextField(max_length=50)
    phone = models.TextField(max_length=20)
    address = models.TextField(max_length=200)
    stocks = models.ManyToManyField(Stock, through="CartDetail")

    def __str__(self) -> str:
        return self.name


class Sale(models.Model):
    total = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.today())
    customer = models.ForeignKey(
        "Customer", related_name="sales", on_delete=models.CASCADE)
    stocks = models.ManyToManyField(Stock, through="SaleDetail")

    def __str__(self) -> str:
        return "customer: {}, total: {}".format(self.customer.id, self.total)


class CartDetail(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    qty = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['stock', 'customer'], name='unique_migration_stock_customer'
            )
        ]

    def __str__(self) -> str:
        return "customer: {}, stock: {}, qty: {}".format(self.customer.id, self.stock.id, self.qty)


class SaleDetail(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    sale = models.ForeignKey(
        Sale, related_name="details", on_delete=models.CASCADE)
    qty = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sale', 'stock'], name='unique_migration_stock_sale'
            )
        ]

    def __str__(self) -> str:
        return "sale: {}, stock: {}, qty: {}".format(self.sale.id, self.stock.id, self.qty)
