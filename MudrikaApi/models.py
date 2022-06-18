from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.


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
        super().save(**args, **kwargs)


class subscribers(models.Model):
    sudu = models.ForeignKey(to=Sudu, on_delete=models.DO_NOTHING)
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

        def __str__(self):
            return self.email
