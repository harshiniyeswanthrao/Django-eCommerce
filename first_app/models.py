from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # image = models.ImageField(upload_to='product_images/')
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    def __str__(self):
        return self.title

class Product_detail(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='details')
    sizes = models.CharField(max_length=255)  # e.g., 'S, M, L, XL'
    colors = models.CharField(max_length=255)  # e.g., 'Red, Black'
    offers = models.CharField(max_length=255)  # e.g., 'Buy 1 Get 1 Free'

    def get_sizes(self):
        return self.sizes.split(', ')

    def get_colors(self):
        return self.colors.split(', ')

    def get_offers(self):
        return self.offers.split(', ')

    def __str__(self):
        return f"Details for {self.product.title}"

class Order(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)
    products = models.ManyToManyField(Product, through='OrderItem')
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.name}"

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     # price = models.DecimalField(max_digits=10, decimal_places=2)
#
#     def get_total_item_price(self):
#         return self.quantity * self.product.price


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_item_price(self):
        return self.product.price * self.quantity  # Assuming 'price' is a field in your Product model

    # def __str__(self):
    #     return f"{self.quantity} x {self.product.name} for Order {self.order.id}"














