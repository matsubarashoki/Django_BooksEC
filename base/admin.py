from atexit import register
from pyexpat import model
from django.contrib import admin

from base.models.books_models import Books, Category, Tag

#TabularInline 表形式のインライン
class TagInline(admin.TabularInline):
    model = Books.tags.through #throughはManyToManyの関係用の属性

class BooksAdmin(admin.ModelAdmin):
    #BooksのtagフィールドはTaginlineがやるから元々のは除外するよ
    inlines = [TagInline]
    exclude = ['tags']


admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Books, BooksAdmin)
