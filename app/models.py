from django.db import models
from django.contrib.auth.models import User


class AccountType(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='accounts/')
    contact = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    id_name = models.CharField(max_length=50, null=True, blank=True)
    id_link = models.CharField(max_length=150, null=True, blank=True)
    status = models.TextField(max_length=100, null=True, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'

class Tag(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    creator = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    content = models.TextField(max_length=1000, null=True, blank=True)
    id_link = models.CharField(max_length=50, null=True, blank=True)
    likes = models.ManyToManyField(User, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='creator')
    reciever = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='business')
    content = models.TextField(max_length=1000, null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = 'Messages'