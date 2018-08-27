from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm

from blog.models import *


class AuthenticationFormWithChekUsersStatus(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if user.is_active == False:
            return 2
        else:
            return 1

class NameForm(forms.ModelForm):
    error_css_class = "error"
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "ایمیل"
        self.fields['name'].label = "نام و نام خانوادگی"
        self.fields['password'].label = "رمز عبور"
        self.fields['acc_num'].label = "شماره حساب"
        self.fields['email'].required = True
    class Meta:
        model =MyUser
        fields = ['name', 'email', 'password', 'acc_num']
        error_messages = {
            'email': {
                'unique': ('این ایمیل قبلا استفاده شده است.'),
                'required': ('وارد کردن ایمیل ضروری است'),
            }
        }
        widgets = {'password': forms.TextInput(
                     attrs={'type': 'password', 'required': True}
            ),
        }


class NameForm3(forms.ModelForm):

    def __init__(self , *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(NameForm3, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['value'] = self.request.user.name
        self.fields['email'].widget.attrs['value'] = self.request.user.email
        self.fields['acc_num'].widget.attrs['value'] = self.request.user.acc_num
        self.fields['dollor_account'].widget.attrs['value'] = self.request.user.dollor_account
        self.fields['euro_account'].widget.attrs['value'] = self.request.user.euro_account
    class Meta:
        model =MyUser
        fields = ['name', 'email',  'euro_account','dollor_account','acc_num' ]
        labels ={
            'email': "ایمیل",
            'name': "نام و نام خانوادگی",
            'acc_num': 'شماره حساب ریالی',
            'dollor_account': 'شماره حساب دلار',
            'euro_account': 'شماره حساب یورو',
        }

class NameForm2(forms.ModelForm):

    def __init__(self , *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(NameForm2, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['value'] = self.request.user.name
        self.fields['email'].widget.attrs['value'] = self.request.user.email
        self.fields['acc_num'].widget.attrs['value'] = self.request.user.acc_num
    class Meta:
        model =MyUser
        fields = ['name', 'email',  'acc_num' ]
        labels ={
            'email': "ایمیل",
            'name': "نام و نام خانوادگی",
            'acc_num': 'شماره حساب',
        }


class ChangePassWordForm(forms.Form):
    # old_pass = forms.CharField(max_length=80, widget=forms.PasswordInput(), label=u"رمز عبور")
    new_pass = forms.CharField(max_length=80, widget=forms.PasswordInput(), label=u"رمز عبور جديد")
    repeat_pass = forms.CharField(max_length=80, widget=forms.PasswordInput(), label=u"تکرار رمز عبور جدید")


class add_employee2(forms.ModelForm):

    def __init__(self , *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(add_employee2, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['value'] = ""
        self.fields['email'].widget.attrs['value'] = ""
        self.fields['acc_num'].widget.attrs['value'] = ""
        self.fields['salary'].widget.attrs['value'] = ""
    class Meta:
        model =MyUser
        fields = ['name', 'email',  'acc_num' , 'salary' ]
        labels ={
            'email': "ایمیل",
            'name': "نام و نام خانوادگی",
            'acc_num': 'شماره حساب',
            'salary': "حقوق",
        }

class ChangeSalary(forms.Form):
    new_salary = forms.CharField(max_length=80, widget=forms.NumberInput(), label=u"حقوق جدید")


class Nform():
    class Meta:
        pass

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()







class ContactForm(forms.Form):
    name = forms.CharField(max_length=200, label=u"نام")
    email = forms.EmailField(max_length=200, label=u"ایمیل")
    message = forms.CharField(widget=forms.Textarea, label=u"پیام")

class UnknownPayment(forms.Form):
    STATUS_CHOICES = (
        (1, "ریال"),
        (2, "دلار"),
        (3, "یورو")
    )
    type = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(), required=True, label="نوع ارز")
    email = forms.CharField(max_length=70, widget=forms.TextInput, required=True, label="ایمیل گیرنده")
    acc_num = forms.CharField(max_length=36, required=True, label="شماره حساب")
    cash = forms.IntegerField(widget=forms.NumberInput, required=True, label="مبلغ واریزی")

class GREForm(forms.ModelForm):
    class Meta:
        model = GREForm
        fields = ['name', 'password', 'city', 'country', 'center', 'placecode', 'education', 'citizen', 'major',
                  'majorcode', 'explanation', 'date', ]
        labels = {
            'name': "نام کاربری",
            'password': "رمز عبور",
            'city': 'شهر',
            'country': "کشور",
            'center': "مرکز محل آزمون",
            'placecode': "کد محل آزمون",
            'education': "وضعیت تحصیلی",
            'citizen': "وضعیت شهروندی",
            'major': "نام رشته",
            'majorcode': "کد رشته",
            'explanation': "توضیحات",
            'date': "تاریخ آزمون",
        }


class TOEFLForm(forms.ModelForm):
    class Meta:
        model = TOEFLForm
        fields = ['name', 'password', 'kind', 'number', 'city', 'country', 'center', 'placecode', 'education',
                  'citizen', 'major', 'majorcode', 'explanation', 'date', 'reason', 'destination']
        labels = {
            'name': "نام کاربری",
            'password': "رمز عبور",
            'kind': "نوع هویت",
            'number': "شماره ی هویت",
            'city': 'شهر',
            'country': "کشور",
            'center': "مرکز محل آزمون",
            'placecode': "کد محل آزمون",
            'education': "وضعیت تحصیلی",
            'citizen': "وضعیت شهروندی",
            'major': "نام رشته",
            'majorcode': "کد رشته",
            'explanation': "توضیحات",
            'date': "تاریخ آزمون",
            'reason': "دلیل شرکت در آزمون",
            'destination': "کشور مقصد تحصیل",
        }


class IELTSForm(forms.ModelForm):
    class Meta:
        model =IELTSForm
        fields = ['name', 'password', 'site']
        labels ={
            'name': "نام کاربری",
            'password': "رمز عبور",
            'site': "لینک سایت ثبت نام",
        }

class UniForm(forms.ModelForm):
    class Meta:
        model =UniForm
        fields = ['name', 'site', 'process',  'arzi' , 'kind', 'email']
        labels ={
            'name': "نام دانشگاه",
            'site': "آدرس سایت دانشگاه",
            'process': "توضیح کامل روند کار",
            'arzi': 'مبلغ ارزی',
            'kind': "نوع ارز",
            'email': "ایمیل",
        }

class PayForm(forms.ModelForm):
    STATUS_CHOICES = (

        ("dollar", "دلار"),
        ("euro", "یورو"),
    )
    kind = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(), required=True, label="نوع ارز")

    class Meta:
        model =PayForm
        fields = ['number', 'country', 'arzi' , 'kind']
        labels ={
            'number': "شماره حساب مقصد",
            'country': "کشور مقصد",
            'arzi': 'مبلغ ارزی',
            'kind': "نوع ارز",
        }
