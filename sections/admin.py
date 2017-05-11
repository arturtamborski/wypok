from django.contrib import admin
from . import models


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    pass
