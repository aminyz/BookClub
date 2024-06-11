from django import forms
from .models import Comment, User, Account


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهادات', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش مشکل', 'گزارش مشکل'),
    )
    name = forms.CharField(max_length=150, label="نام")
    massage = forms.CharField(widget=forms.Textarea, required=True, label="پیام")
    email = forms.EmailField(label="ایمیل")
    phone = forms.CharField(required=True, max_length=11, label="شماره تلفن")
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, label="موضوع")


class CommentForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if len(name) < 2:
                raise forms.ValidationError("نام کوتاه است")
            else:
                return name

    class Meta:
        model = Comment
        fields = ['name', 'description']


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(max_length=28, widget=forms.PasswordInput, label='password1')
    password2 = forms.CharField(max_length=28, widget=forms.PasswordInput, label='password2')

    class Meta:
        model = User
        fields = ['username']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('رمز مطابقت ندارد')
        return cd['password2']


class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class EditAccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['date_of_birth', 'job', 'phone', 'photo', 'bio']

