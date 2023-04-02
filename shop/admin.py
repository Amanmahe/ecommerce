from django.contrib import admin

# Register your models here.
from .models import product, Contact, Orders, OrderUpdate,register_table

admin.site.register(product)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
admin.site.register(register_table)