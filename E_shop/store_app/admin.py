from django.contrib import admin

# Register your models here.

from .models  import *

class imagetublarinline(admin.TabularInline):
    model = Images

class tagtublarinline(admin.TabularInline):
    model = Tag
    
class productAdmin(admin.ModelAdmin):
    inlines = [imagetublarinline,tagtublarinline]
    

class orderItemInline(admin.TabularInline):
    model = OrderItem

class orderAdmin(admin.ModelAdmin):
    inlines = [orderItemInline]
    list_display = ['first_name',  'email', 'amount', 'paid', 'date']
    search_fields = ['first_name', 'email','payment_id']

admin.site.register(Categories)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Filter_Price)
admin.site.register(PRODUCT,productAdmin)
admin.site.register(Images)
admin.site.register(Tag)
admin.site.register(Contact)
admin.site.register(Order,orderAdmin)
admin.site.register(OrderItem)