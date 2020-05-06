from django.forms import ModelForm
from budget.models import *
from django import forms


class UserRegFormCreation(ModelForm):
    class Meta:
        model=Users
        fields=['name','address','email','phone','username','password']

class UserLogin(ModelForm):
    class Meta:
        model=Users
        fields=['username','password']
        widgets={
            'password':forms.PasswordInput(render_value=True),
        }


    def clean(self):
        cleaned_data= super().clean()
        username=cleaned_data.get("username")

        if (Users.objects.filter(username=username)):
            pass
        else:
            msg="no user exist"
            self.add_error('username',msg)


class BudgetFormCreation(ModelForm):
    date=forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model=Budget
        fields=['date','category_type','expenses','description']

class DatewiseReviewForm(forms.Form):

    from_date=forms.DateField(widget=forms.SelectDateWidget)
    to_date=forms.DateField(widget=forms.SelectDateWidget)

class CategorywiseForm(ModelForm):
    from_date = forms.DateField(widget=forms.SelectDateWidget)
    to_date = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model=Budget
        fields=['category_type']




