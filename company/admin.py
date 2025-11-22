from django.contrib import admin

from .models import Company, Vehicle, SPARE, Order , Cart ,ProductRating

admin.site.register(Company)
admin.site.register(Vehicle)
admin.site.register(SPARE)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(ProductRating)