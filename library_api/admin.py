from django.contrib import admin
from . import models

admin.site.register(models.Category)
admin.site.register(models.BookCopy)
admin.site.register(models.Book)
admin.site.register(models.Member)
admin.site.register(models.Publisher)
admin.site.register(models.Author)
admin.site.register(models.BurrowedBook)
admin.site.register(models.RequestedBook)
admin.site.register(models.ReservedBook)
