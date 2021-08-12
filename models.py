from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL
from django.db.models.expressions import F
from django.db.models.fields import BooleanField
from django.urls import reverse

class Customer(models.Model):
    username = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255,db_index=True)
    slug = models.SlugField(max_length=255,unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    #We creating a link between category class to product
    category = models.ForeignKey(Category,related_name='product',on_delete=models.CASCADE)
    #Who actually make this data
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='product_creator')
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255,default='Admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/',default='images/placeholder.png')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4,decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    #will create when we create a product,going to happend onence
    created = models.DateTimeField(auto_now_add=True)
    #We want to recoding when we update a product 
    updated = models.DateTimeField(auto_now=True)
    digital = BooleanField(default=False,null=True,blank=True)
    
    
    class Meta:
        verbose_name_plural = 'Products'
        #By ascending and descending we are using descending order (the last product that created show first)
        ordering = ('-created',)

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=200,null=False)
    city = models.CharField(max_length=200,null=False)
    state = models.CharField(max_length=200,null=False)
    zipcode = models.CharField(max_length=200,null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address