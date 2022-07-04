from django.db import models
from django.forms import ValidationError
from django.template.defaultfilters import slugify

# Create your models here.

# 0xd1CfE5c03730C4F93ag76a7d8424bA9122Bb4742


class UserProfileSignUpData(models.Model):
    acc_address = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    username = models.CharField(max_length=24)
    access_level_token = models.CharField(max_length=20, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)


class AccessLevelTokenData(models.Model):
    access_phrase = models.CharField(max_length=20, primary_key=True)
    access_level_choices = [
        ('national', 'NATIONAL'),
        ('state', 'STATE'),
        ('district', 'DISTRICT')
    ]
    access_level = models.CharField(
        max_length=8, null=False, choices=access_level_choices, default='district', blank=False)
    state = models.CharField(max_length=20, null=True, blank=True)
    district = models.CharField(max_length=42, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def clean(self):
        if (self.access_level == "state" or self.access_level == "district") and not self.state:
            raise ValidationError("State not provided!")
        elif self.access_level == "district" and not self.district:
            raise ValidationError("District not provided!")


class Sudu(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    slug = models.SlugField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        to_assign = slugify(self.title)

        if Sudu.objects.filter(slug=to_assign).exists():
            to_assign = to_assign+str(Sudu.objects.all().count())

        self.slug = to_assign
        super().save(*args, **kwargs)

       # super().save(**args,**kwargs)


class subscribers(models.Model):
    sudu = models.ForeignKey(to=Sudu, on_delete=models.DO_NOTHING)
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

        def __str__(self):
            return self.email
