from django.forms import ModelForm
from .models import AccessLevelTokenDummy


class AccessLevelForm(ModelForm):
    class Meta:
        model = AccessLevelTokenDummy
        fields = ['access_level', 'state', 'district']
