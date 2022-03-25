from django.contrib import admin
from .models import Tag, Account, Category, Post, Message, AccountType
# Register your models here.

admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(AccountType)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user','account_type','contact','address','verified')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('category','title','content')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('content','sender','reciever')
