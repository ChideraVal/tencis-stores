from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(blank=False, null=False, upload_to='product_images')

    def __str__(self):
        return self.name


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id}"

    def get_total_items(self):
        return sum(product.quantity for product in self.cartproduct_set.all())

    def get_total_price(self):
        return sum(product.product.price * product.quantity for product in self.cartproduct_set.all())


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True, db_index=True)

    def __str__(self):
        return self.product.name

    def name(self):
        return self.product.name
    
    def total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    order_id = models.CharField(max_length=150, null=True, blank=False, db_index=True)
    transaction_id = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=11, null=False, blank=False)
    address = models.CharField(max_length=150, null=False, blank=False)
    state = models.CharField(max_length=150, null=False, blank=False)
    zip_code = models.IntegerField(null=False, blank=False)
    active = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    cartproducts = models.ManyToManyField(CartProduct, blank=False)
    create_time = models.DateTimeField(auto_now_add=True)
    processed_time = models.DateTimeField(auto_now_add=True)
    shipped_time = models.DateTimeField(auto_now_add=True)
    delivered_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order for {self.email}"
    
    def get_total_items(self):
        return sum(product.quantity for product in self.cartproducts.all())

    def get_total_price(self):
        return sum(product.product.price * product.quantity for product in self.cartproducts.all())

