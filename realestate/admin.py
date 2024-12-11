from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(House)
admin.site.register(Client)
admin.site.register(Realtor)
admin.site.register(Appointment)
admin.site.register(Image)