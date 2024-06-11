from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter

admin.sites.AdminSite.site_header = 'پنل مدیریت بوک کلاب'
admin.sites.AdminSite.site_title = 'پنل'
admin.sites.AdminSite.index_title = 'پنل مدیریت'


# inline
class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


# Register your models here.
@admin.register(Literature)
class LiteratureAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'author_post', 'id']
    ordering = ['-publish_post_time',]
    list_filter = ['status', ('publish_post_time', JDateFieldListFilter),]
    search_fields = ['title', 'description', 'author', 'author_post',]
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status',]
    inlines = [ImageInline, CommentInline]


@admin.register(Authors)
class AuthorsAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'status',]
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['status']


@admin.register(Ticket)
class TicketsAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'phone',]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'created', 'active']
    list_filter = ['active', ('created', JDateFieldListFilter), ('updated', JDateFieldListFilter)]
    search_fields = ['name', 'description']
    list_editable = ['active']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'title', 'created']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'phone', 'photo']
