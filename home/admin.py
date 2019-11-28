from django.contrib import admin
from .models import mobiles,mobilesAmazon,mobilesFlipkart,mobilesSnapdeal

# Register your models here.
admin.site.register(mobiles)
admin.site.register(mobilesAmazon)
admin.site.register(mobilesFlipkart)
admin.site.register(mobilesSnapdeal)