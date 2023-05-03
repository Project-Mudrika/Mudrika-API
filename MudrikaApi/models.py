from django.db import models
from django.forms import ValidationError
from django.template.defaultfilters import slugify

# Create your models here.

# 0xd1CfE5c03730C4F93ag76a7d8424bA9122Bb4742


class VolunteerProfileSignUpData(models.Model):
    walletid = models.CharField(max_length=42, primary_key=True)
    aadharngoid = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    profileimg = models.CharField(max_length=255)
    voltype = models.CharField(max_length=32)


class VolunteerActivityData(models.Model):
    walletid = models.CharField(max_length=42, primary_key=True)
    description = models.CharField(max_length=255)
    date = models.DateTimeField()
    imageLink = models.URLField()


class UserProfileSignUpData(models.Model):
    walletid = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    username = models.CharField(max_length=24)
    access_level_token = models.CharField(
        max_length=20, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class NewConsignmentData(models.Model):
    cons_id = models.CharField(max_length=32, primary_key=True)
    con_name = models.CharField(max_length=50)
    quantity = models.CharField(max_length=16)
    location = models.CharField(max_length=60)
    sender = models.CharField(max_length=45)
    receiver = models.CharField(max_length=45)


class DriverProfile(models.Model):
    wallet_id = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    state = models.CharField(max_length=35)
    district = models.CharField(max_length=35)
    mobile_number = models.IntegerField(blank=True)


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
