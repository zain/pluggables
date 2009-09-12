from django.contrib import admin
from appdir.models import App, Record, Repository

class RepoInline(admin.TabularInline):
    model = Repository
    extra = 1


class AppAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [RepoInline,]


class RecordAdmin(admin.ModelAdmin):
    pass


admin.site.register(App, AppAdmin)
admin.site.register(Record, RecordAdmin)
