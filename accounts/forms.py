from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(
        label='username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя',
        })
    )
    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
        })
    )

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            users = User.objects.filter(username=username)
            if not users.exists():
                raise forms.ValidationError('Такого пользователя нет')
            if not check_password(password, users[0].password):
                raise forms.ValidationError('Неверный пароль')
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Данный пользователь неактивен')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя',
        })
    )
    password1 = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
        })
    )
    password2 = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
        })
    )

    class Meta:
        model = User
        fields = ('username',)

    def clean_password(self):
        data = self.cleaned_data
        if data['password1'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        else:
            return data['password2']
