from django.contrib import admin

from sections.models import Section


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    pass
