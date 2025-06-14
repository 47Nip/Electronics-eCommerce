from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return   self.name  

class Brand(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return   self.name  

class Color(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=50)
    
    def __str__(self):
        return   self.name  
class Filter_Price(models.Model):
    FILTER_PRICE = (
        ('1000 TO 10000','1000 TO 10000'),
        ('10000 TO 20000','10000 TO 20000'),
        ('20000 TO 30000','20000 TO 30000'),
        ('30000 TO 40000','30000 TO 40000'),
        ('40000 TO 50000','40000 TO 50000'),
        ('50000 TO 60000','50000 TO 60000'),
        ('60000 TO 70000 ','60000 TO 70000'),
    )
    
    price = models.CharField(choices=FILTER_PRICE,max_length=60) 
    
    def __str__(self):
        return   self.price

class PRODUCT(models.Model):
    CONDITION = (('New','New'),('Old','Old'))
    STOCK = (('IN STOCK ','IN STOCK'),('OUT OF STOCK','OUT OF STOCK'))
    STATUS = (('Publish','Publish'),('Draft','Draft'))
    
    unique_id = models.CharField(unique=True,max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to='product_image/img')
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    condition = models.CharField(choices=CONDITION,max_length=100)
    information = RichTextField(null=True)
    description = RichTextField(null=True)
    stock = models.CharField(choices=STOCK,max_length=200)
    status = models.CharField(choices=STATUS,max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    
    
    categories = models.ForeignKey(Categories,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    filter_Price = models.ForeignKey(Filter_Price,on_delete=models.CASCADE)
    
    def save(self,*args,**kwargs):
        if self.unique_id is None and self.created_date and self.id:
            self.unique_id = self.created_date.strftime('75%Y%m%D23') + str(self.id)
        return super().save(*args,**kwargs)

    def __str__(self):
        return   self.name  
    
    
class Images(models.Model):
    image = models.ImageField(upload_to='product_image/img')
    product = models.ForeignKey(PRODUCT,on_delete=models.CASCADE)
    
class Tag(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(PRODUCT,on_delete=models.CASCADE)
    

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=200, blank=True, null=True)
    paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    image = models.ImageField(upload_to='product_image/order_items')
    quantity = models.CharField(max_length=10)    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    def __str__(self):
        return self.order.user.username


    
    