from atexit import register
from pyexpat import model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from base.models import Profile, User,Books, Category, Tag
from base.forms import UserCreationForm
from base.models.order_models import Order

#TabularInline 表形式のインライン
class TagInline(admin.TabularInline):
    model = Books.tags.through #throughはManyToManyの関係用の属性

class BooksAdmin(admin.ModelAdmin):
    #BooksのtagフィールドはTaginlineがやるから元々のは除外するよ
    inlines = [TagInline]
    exclude = ['tags']

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class CustomeUserAdmin(UserAdmin):
    fieldsets  = (
        (None, {'fields': ('username', 'email', 'password', )}), #先頭のNoneは区分名
        (None, {'fields': ('is_active', 'is_admin',)}),
    )

    list_display = ('username', 'email','is_active',)
    list_filter = ()
    ordering = ()
    filter_horizontal = ()
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'is_active',)}),
    )
    add_form = UserCreationForm

    inlines = (ProfileInline,)

admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Books, BooksAdmin)
admin.site.register(User, CustomeUserAdmin)
admin.site.register(Order)