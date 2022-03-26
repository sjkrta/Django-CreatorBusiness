from django.contrib import admin
from .models import Tag, Account, Category, Post, Message
# Register your models here.

admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Account)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('category','title','content')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('content','sender','reciever')
