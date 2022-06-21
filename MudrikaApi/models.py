from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
# 0xd1CfE5c03730C4F93ag76a7d8424bA9122Bb4742


class UserProfileDummy(models.Model):
    acc_address = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    state = models.CharField(max_length=60)
    district = models.CharField(max_length=60)
    username = models.CharField(max_length=24)
    type_phrase = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)


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
