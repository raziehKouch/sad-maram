from django.contrib import admin

# Register your models here.

from .models import MyUserManager
from .models import MyUser
from .models import Employee
from .models import Manager
from .models import Transaction
from .models import Message

admin.site.register(MyUser)
admin.site.register(Employee)
admin.site.register(Manager)
admin.site.register(Transaction)
admin.site.register(Message)
