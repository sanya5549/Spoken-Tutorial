from django import forms
from .models import *


class Signupform(forms.Form):
    username=forms.CharField(max_length=15, required=True)
    email=forms.EmailField(max_length=30, required=True)
    password=forms.CharField(max_length=20, required=True)
    s=str(password)
    if len(s)<8:
        raise forms.ValidationError("Min length of password:8")


class Adminform(forms.Form):
    user1=forms.CharField(max_length=15, required=True)
    pwd=forms.CharField(max_length=20, required=True)


class Userlogin(forms.Form):
    user2 = forms.CharField(max_length=15, required=True)
    pass2 = forms.CharField(max_length=20, required=True)

    class Meta:
        model = Userdetails
        fields = ('user2', 'pass2')


class Createform(forms.Form):
    fossid = forms.CharField(max_length=20, required=True)
    tutorial1 = forms.CharField(max_length=50, required=True)
    deadline1 = forms.DateField(required=True)
    tutorial2 = forms.CharField(max_length=50, required=True)
    deadline2 = forms.DateField(required=True)
    tutorial3 = forms.CharField(max_length=50, required=True)
    deadline3 = forms.DateField(required=True)
    tutorial4 = forms.CharField(max_length=50, required=True)
    deadline4 = forms.DateField(required=True)
    tutorial5 = forms.CharField(max_length=50, required=True)
    deadline5 = forms.DateField(required=True)
    tutorial6 = forms.CharField(max_length=50, required=True)
    deadline6 = forms.DateField(required=True)
    tutorial7 = forms.CharField(max_length=50, required=True)
    deadline7 = forms.DateField(required=True)
    tutorial8 = forms.CharField(max_length=50, required=True)
    deadline8 = forms.DateField(required=True)
    tutorial9 = forms.CharField(max_length=50, required=True)
    deadline9 = forms.DateField(required=True)
    tutorial10 = forms.CharField(max_length=50, required=True)
    deadline10 = forms.DateField(required=True)


class Assignform(forms.Form):
    userassn = forms.CharField(max_length=15, required=True)
    fossassn = forms.CharField(max_length=20, required=True)


class Userform(forms.Form):
    usernm = forms.CharField(max_length=15)
    tutname = forms.CharField(max_length=50)
