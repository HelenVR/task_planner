# from django import forms
# from django.contrib.auth.models import User
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit
# from django.contrib.auth.forms import AuthenticationForm
#
# from .models import Task
#
#
# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'email']
#
#     def __init__(self, *args, **kwargs):
#         super(UserRegistrationForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.add_input(Submit('register', 'Register'))
#
#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password'] != cd['password2']:
#             raise forms.ValidationError('Passwords don\'t match.')
#         return cd['password2']
#
#
# class UserLoginForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super(UserLoginForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.add_input(Submit('login', 'Login'))
#
#
# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         fields = ['name', 'task', 'deadline', 'telegram_nick', 'notification_interval', 'notification_time']
#         widgets = {
#             'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#             'notification_time': forms.TimeInput(attrs={'type': 'time'}),
#         }
#
#     def clean(self):
#         cleaned_data = super().clean()
#         telegram_nick = cleaned_data.get('telegram_nick')
#         notification_interval = cleaned_data.get('notification_interval')
#         notification_time = cleaned_data.get('notification_time')
#
#         if telegram_nick and (not notification_interval or not notification_time):
#             raise forms.ValidationError(
#                 "Please provide both notification interval and time if Telegram nick is provided.")
#         return cleaned_data


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Task

class BootstrapMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class UserRegistrationForm(BootstrapMixin, UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class TaskForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'task', 'deadline', 'email', 'notification_interval', 'notification_time']