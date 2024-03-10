from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import formset_factory
from .models import Question, Choice

class CustomSignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

        self.fields['password1'].validators = [self.simple_password_validator]

    def simple_password_validator(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']

ChoiceFormSet = formset_factory(ChoiceForm, extra=2)
