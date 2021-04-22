from django.contrib import admin
from .models import User,Subject,Ratings,Sessions,Bill,MyFile
# Register your models here.
admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Ratings)
admin.site.register(Sessions)
admin.site.register(Bill)
admin.site.register(MyFile)