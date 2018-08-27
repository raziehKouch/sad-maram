import datetime

from django.conf import settings
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class Person(models.Model):
    class Meta:
        abstract = True

class MyUserManager(BaseUserManager):
    def create_user(self, email,acc_num="0",  name = "ناشناس", password=None ):
        if not email:
            raise ValueError('وارد کردن ایمیل ضروری است!')

        user = self.model(
            email=MyUserManager.normalize_email(email),
            name = name,

            acc_num = acc_num,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password):
        user = self.create_user(email,
                                password=password,
                                )
        user.is_admin = True
        user.save(using=self._db)
        return user





class MyUser(AbstractBaseUser, Person):
    email = models.EmailField(max_length=254, unique=True, db_index=True , null=False , blank=False)
    name = models.CharField(max_length=50 , null=True, blank=True)
    acc_num =  models.CharField(max_length=30 , null=False, blank=False)
    rial_wallet=models.FloatField(default=0)
    dollar_wallet=models.FloatField(default=0)
    euro_wallet=models.FloatField(default=0)
    salary = models.FloatField(default=0)
    dollor_account =  models.CharField(max_length=30 , null=False);
    euro_account = models.CharField(max_length=30 , null=False)
    status = models.CharField(max_length=10, default="enabled")

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



    def get_full_name(self):
        return self.name

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Employee(MyUser, BaseUserManager):
    salarry = models.IntegerField(default=0)
    def __init__(self):
        MyUser.__init__(self)

    def create_user(self, email,acc_num="0",salary="0",  name = "ناشناس", password=None ):
        if not email:
            raise ValueError('وارد کردن ایمیل ضروری است!')

        user = self.model(
            email=MyUserManager.normalize_email(email),
            name = name,
            salary = salary,
            acc_num = acc_num,
        )
        user.is_employee=True
        user.set_password(password)
        user.save(using=self._db)
        return user


class Manager(MyUser, BaseUserManager):
    dollor_accouunt =  models.CharField(max_length=30 , null=False , default="شماره حساب دلار");
    euro_accouunt = models.CharField(max_length=30 , null=False, default="شماره حساب یورو")
    def create_user(self, email,acc_num="0",salary="0",  name = "ناشناس", password=None ):
        if not email:
            raise ValueError('وارد کردن ایمیل ضروری است!')

        user = self.model(
            email=MyUserManager.normalize_email(email),
            name = name,
            acc_num = acc_num,
        )
        user.is_admin=True
        user.set_password(password)
        user.save(using=self._db)
        return user

class GREForm(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    center = models.CharField(max_length=200)
    placecode = models.CharField(max_length=200)
    education = models.CharField(max_length=200)
    citizen = models.CharField(max_length=200)
    major = models.CharField(max_length=200)
    majorcode = models.CharField(max_length=200)
    explanation = models.TextField(blank = True)
    date = models.DateTimeField(blank = True)

class TOEFLForm(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    kind = models.CharField(max_length=200)
    number = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    center = models.CharField(max_length=200)
    placecode = models.CharField(max_length=200)
    education = models.CharField(max_length=200)
    citizen = models.CharField(max_length=200)
    major = models.CharField(max_length=200)
    majorcode = models.CharField(max_length=200)
    explanation = models.TextField(blank = True)
    date = models.DateTimeField(blank = True)
    reason = models.TextField(blank=True)
    destination = models.CharField(max_length=200, blank=True)

class IELTSForm(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    site = models.URLField()

class UniForm(models.Model):
    name = models.CharField(max_length=200)
    site = models.URLField()
    process = models.TextField()
    arzi = models.FloatField(max_length=200)
    kind = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)

class PayForm(models.Model):
    number = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    arzi = models.FloatField(max_length=200)
    kind = models.CharField(max_length=200)

class Transaction(models.Model):
    date = models.DateTimeField(default = timezone.now())
    expiration_date = models.DateTimeField(default = timezone.now() + datetime.timedelta(days=1))
    type = models.CharField(max_length=30 , null=False , default="");
    status = models.CharField(max_length=30 , null=False , default="در حال انتظار");
    employee = models.ForeignKey(MyUser , on_delete = models.CASCADE , related_name='karmand')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE , related_name='karbar')
    subject =   models.CharField(max_length=30 , null=False , default="موضوع");
    content =  models.CharField(max_length=300 , null=False , default="محتوا");
    greform = models.ForeignKey( GREForm , on_delete=models.CASCADE, blank=True, null=True)
    toeflform = models.ForeignKey( TOEFLForm , on_delete=models.CASCADE, blank=True, null=True)
    ieltsform = models.ForeignKey( IELTSForm , on_delete=models.CASCADE, blank=True, null=True)
    uniform = models.ForeignKey( UniForm , on_delete=models.CASCADE, blank=True, null=True)
    payform = models.ForeignKey( PayForm , on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.type

class Message(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , blank=True, null=True,related_name='ferestande')
    created_date = models.DateTimeField(default=timezone.now())
    reciever =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , blank=True, null=True,related_name='girande')
    subject =  models.CharField(max_length=30 , null=False , default="موضوع");
    content =  models.TextField(null=False , default="محتوا");
    transaction = models.ForeignKey( Transaction , on_delete=models.CASCADE, blank=True, null=True)

