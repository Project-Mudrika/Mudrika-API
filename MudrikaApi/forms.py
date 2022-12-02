from django.forms import ModelForm
from .models import UserProfileSignUpData, AccessLevelTokenData, NewConsignmentData


class AccessLevelForm(ModelForm):
    class Meta:
        model = AccessLevelTokenData
        fields = ['access_level', 'state', 'district']


class SignUpForm(ModelForm):
    class Meta:
        model = UserProfileSignUpData
        fields = "__all__"


class ConsignmentForm(ModelForm):
    class Meta:
        model = NewConsignmentData
        fields = "__all__"
