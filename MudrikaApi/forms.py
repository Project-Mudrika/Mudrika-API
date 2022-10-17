from django.forms import ModelForm
from .models import UserProfileSignUpData, AccessLevelTokenData


class AccessLevelForm(ModelForm):
    class Meta:
        model = AccessLevelTokenData
        fields = ['access_level', 'state', 'district']


class SignUpForm(ModelForm):
    class Meta:
        model = UserProfileSignUpData
        fields = "__all__"
