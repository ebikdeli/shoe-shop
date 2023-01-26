from django import forms
from .models import Address


class AddressForm(forms.ModelForm):
    """Address Form to create or update Address"""
    class Meta:
        model = Address
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        """This is how we can change any model form or even any form behaviors"""
        super().__init__(*args, **kwargs)
        # If 'Address.user' field was '1t1', 'm2m' or 'ForeignKey', we could had changed queryset
        # for the field in the model form to something like this:
        # address_form.fields['user'].queryset = get_user_model().objects.filter(first_name__in='ehsan')
        # for field_name, field_value in self.fields.items():
        #     if field_name == 'user':
        #         print(field_value.queryset)
        #     if field_name == 'city':
        #         print(field_value.label)
