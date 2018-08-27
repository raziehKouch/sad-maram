from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from django.core.mail import BadHeaderError, send_mail, mail_admins
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
import time
# Create your views here.
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse

from blog.forms import *
from blog.models import  MyUserManager,MyUser,Employee,Manager,Transaction,Message
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect


def redirect_index(request):
    if(isinstance(request.user, AnonymousUser)):
        url = reverse('index')
        return HttpResponseRedirect(url)
    else:
        if(request.user.is_employee == True):
            print("employee")
            url = reverse('index_employee')
            return HttpResponseRedirect(url)
        elif(request.user.is_admin == True):
            print("MANAGER")
            url = reverse('index_manager')
            return HttpResponseRedirect(url)
        elif (not (request.user.is_admin or request.user.is_employee)):
            url = reverse('index_user')
            return HttpResponseRedirect(url)
def index(request):
    response = requests.get('https://www.faranevis.com/api/currency/')
    geodata = response.json()
    answer = 0
    form = ContactForm()
    if request.method == 'POST':
        if 'contact_submit' in request.POST:
            if form.is_valid():
                form = ContactForm(request.POST)
                name = form.data['name']
                email = form.data['email']
                message = form.data['message']
                if message and email:
                    try:
                        send_mail(name, message, 'm.s.moosareza@gmail.com', ['m.mina1997@yahoo.com'])
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                else:
                    # In reality we'd use a form class
                    # to get proper validation errors.
                    return HttpResponse('Make sure all fields are entered and valid.')
                messages.success(request, 'پیام شما با موفقیت ارسال شد')
                return redirect('index')
            else:
                messages.success(request, 'مشکلی در ارسال پیام وجود دارد. ورودی های خود را بررسی کنید!')
        elif 'change_submit' in request.POST:
            fromCurr, toCurr, dollar, euro, amount = request.POST['from'], request.POST['to'], (request.POST['dollar']), (request.POST['euro']), (request.POST['amount-from'])
            dd = dollar.split(',')
            ee = euro.split(',')
            dollar = ""
            for i in range(len(dd)):
                dollar += dd[i]
            euro = ""
            for i in range(len(ee)):
                euro += ee[i]
            dollar = int(float(str(dollar)))
            euro = int(float(str(euro)))
            amount = int(float(str(amount)))
            if fromCurr != toCurr:
                if fromCurr == 'rial' and toCurr == 'euro':
                    answer = (amount*0.95) / euro
                if fromCurr == 'rial' and toCurr == 'dollar':
                    answer = (amount*0.95) / dollar
                if fromCurr == 'euro' and toCurr == 'rial':
                    answer = (amount*0.95) * euro
                if fromCurr == 'dollar' and toCurr == 'rial':
                    answer = (amount*0.95) * dollar
                if fromCurr == 'dollar' and toCurr == 'euro':
                    answer = ((amount*0.95) * dollar) / euro
                if fromCurr == 'euro' and toCurr == 'dollar':
                    answer = ((amount*0.95) * euro) / dollar
            else:
                answer = amount
    return render(request, 'index.html', {'form': form, 'answer': answer, 'dollar': geodata['دلار'], 'euro': geodata['یورو'], })

@login_required(redirect_field_name='login')
def index_user(request):
    response = requests.get('https://www.faranevis.com/api/currency/')
    geodata = response.json()
    answer = 0
    form = ContactForm()
    if request.method == 'POST':
        if 'contact_submit' in request.POST:
            if form.is_valid():
                form = ContactForm(request.POST)
                name = form.data['name']
                email = form.data['email']
                message = form.data['message']
                if message and email:
                    try:
                        send_mail(name, message, 'm.s.moosareza@gmail.com', ['m.mina1997@yahoo.com'])
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                else:
                    # In reality we'd use a form class
                    # to get proper validation errors.
                    return HttpResponse('Make sure all fields are entered and valid.')
                messages.success(request, 'پیام شما با موفقیت ارسال شد')
                return redirect('index_user')
            else:
                messages.success(request, 'مشکلی در ارسال پیام وجود دارد. ورودی های خود را بررسی کنید!')
        elif 'change_submit' in request.POST:
            fromCurr, toCurr, dollar, euro, amount = request.POST['from'], request.POST['to'], (
            request.POST['dollar']), (request.POST['euro']), (request.POST['amount-from'])
            dd = dollar.split(',')
            ee = euro.split(',')
            dollar = ""
            for i in range(len(dd)):
                dollar += dd[i]
            euro = ""
            for i in range(len(ee)):
                euro += ee[i]
            dollar = int(float(str(dollar)))
            euro = int(float(str(euro)))
            amount = int(float(str(amount)))
            if fromCurr != toCurr:
                if fromCurr == 'rial' and toCurr == 'euro':
                    answer = (amount * 0.95) / euro
                if fromCurr == 'rial' and toCurr == 'dollar':
                    answer = (amount * 0.95) / dollar
                if fromCurr == 'euro' and toCurr == 'rial':
                    answer = (amount * 0.95) * euro
                if fromCurr == 'dollar' and toCurr == 'rial':
                    answer = (amount * 0.95) * dollar
                if fromCurr == 'dollar' and toCurr == 'euro':
                    answer = ((amount * 0.95) * dollar) / euro
                if fromCurr == 'euro' and toCurr == 'dollar':
                    answer = ((amount * 0.95) * euro) / dollar
            else:
                answer = amount
    return render(request, 'index_user.html',
                  {'form': form, 'answer': answer, 'dollar': geodata['دلار'], 'euro': geodata['یورو'], })


def index_employee(request):
    response = requests.get('https://www.faranevis.com/api/currency/')
    geodata = response.json()
    answer = 0
    form = ContactForm()
    if request.method == 'POST':
        if 'contact_submit' in request.POST:
            if form.is_valid():
                form = ContactForm(request.POST)
                name = form.data['name']
                email = form.data['email']
                message = form.data['message']
                if message and email:
                    try:
                        send_mail(name, message, 'm.s.moosareza@gmail.com', ['m.mina1997@yahoo.com'])
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                else:
                    # In reality we'd use a form class
                    # to get proper validation errors.
                    return HttpResponse('Make sure all fields are entered and valid.')
                messages.success(request, 'پیام شما با موفقیت ارسال شد')
                return redirect('index_employee')
            else:
                messages.success(request, 'مشکلی در ارسال پیام وجود دارد. ورودی های خود را بررسی کنید!')
        elif 'change_submit' in request.POST:
            fromCurr, toCurr, dollar, euro, amount = request.POST['from'], request.POST['to'], (
            request.POST['dollar']), (request.POST['euro']), (request.POST['amount-from'])
            dd = dollar.split(',')
            ee = euro.split(',')
            dollar = ""
            for i in range(len(dd)):
                dollar += dd[i]
            euro = ""
            for i in range(len(ee)):
                euro += ee[i]
            dollar = int(float(str(dollar)))
            euro = int(float(str(euro)))
            amount = int(float(str(amount)))
            if fromCurr != toCurr:
                if fromCurr == 'rial' and toCurr == 'euro':
                    answer = (amount * 0.95) / euro
                if fromCurr == 'rial' and toCurr == 'dollar':
                    answer = (amount * 0.95) / dollar
                if fromCurr == 'euro' and toCurr == 'rial':
                    answer = (amount * 0.95) * euro
                if fromCurr == 'dollar' and toCurr == 'rial':
                    answer = (amount * 0.95) * dollar
                if fromCurr == 'dollar' and toCurr == 'euro':
                    answer = ((amount * 0.95) * dollar) / euro
                if fromCurr == 'euro' and toCurr == 'dollar':
                    answer = ((amount * 0.95) * euro) / dollar
            else:
                answer = amount
    return render(request, 'index_employee.html',
                  {'form': form, 'answer': answer, 'dollar': geodata['دلار'], 'euro': geodata['یورو'], })


def index_manager(request):
    response = requests.get('https://www.faranevis.com/api/currency/')
    geodata = response.json()
    answer = 0
    form = ContactForm()
    if request.method == 'POST':
        if 'contact_submit' in request.POST:
            if form.is_valid():
                form = ContactForm(request.POST)
                name = form.data['name']
                email = form.data['email']
                message = form.data['message']
                if message and email:
                    try:
                        send_mail(name, message, 'm.s.moosareza@gmail.com', ['m.mina1997@yahoo.com'])
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                else:
                    # In reality we'd use a form class
                    # to get proper validation errors.
                    return HttpResponse('Make sure all fields are entered and valid.')
                messages.success(request, 'پیام شما با موفقیت ارسال شد')
                return redirect('index_manager')
            else:
                messages.success(request, 'مشکلی در ارسال پیام وجود دارد. ورودی های خود را بررسی کنید!')
        elif 'change_submit' in request.POST:
            fromCurr, toCurr, dollar, euro, amount = request.POST['from'], request.POST['to'], (
            request.POST['dollar']), (request.POST['euro']), (request.POST['amount-from'])
            dd = dollar.split(',')
            ee = euro.split(',')
            dollar = ""
            for i in range(len(dd)):
                dollar += dd[i]
            euro = ""
            for i in range(len(ee)):
                euro += ee[i]
            dollar = int(float(str(dollar)))
            euro = int(float(str(euro)))
            amount = int(float(str(amount)))
            if fromCurr != toCurr:
                if fromCurr == 'rial' and toCurr == 'euro':
                    answer = (amount * 0.95) / euro
                if fromCurr == 'rial' and toCurr == 'dollar':
                    answer = (amount * 0.95) / dollar
                if fromCurr == 'euro' and toCurr == 'rial':
                    answer = (amount * 0.95) * euro
                if fromCurr == 'dollar' and toCurr == 'rial':
                    answer = (amount * 0.95) * dollar
                if fromCurr == 'dollar' and toCurr == 'euro':
                    answer = ((amount * 0.95) * dollar) / euro
                if fromCurr == 'euro' and toCurr == 'dollar':
                    answer = ((amount * 0.95) * euro) / dollar
            else:
                answer = amount
    return render(request, 'index_manager.html',
                  {'form': form, 'answer': answer, 'dollar': geodata['دلار'], 'euro': geodata['یورو'], })


def register(request):
    f=NameForm()
    return render (request , 'register.html' , {'form':f})




def user_unknownpay(request):
    form = UnknownPayment()
    if request.method == 'POST' :
        form = UnknownPayment(request.POST)
        anums=""
        if form.is_valid():
            try:
                anums = MyUser.objects.get(acc_num = form.cleaned_data['acc_num'] )
            except:
                pass
            pool = form.cleaned_data['cash']
            if anums is "":

                rec_usr = MyUser.objects.create(email = form.cleaned_data['email'], acc_num= form.cleaned_data['acc_num'])
                rec_usr.set_password("12345")

            else:
                print("yyyyyyyyyyyyyyyyyyyyyyyy")
                rec_usr = MyUser.objects.get(email =  form.cleaned_data['email'])

            snd_usr = request.user
            print("s")
            print(snd_usr)
            print("r")
            print(rec_usr)
            type = form.cleaned_data['type']
            print("t")
            print(type)
            print("p")
            print(pool)
            if (type is "1"):
                print("rialxxxxxxxxxxxxxxxxxxxxx")
                if (snd_usr.rial_wallet>=pool):
                    snd_usr.rial_wallet -= pool
                    rec_usr.rial_wallet += pool
                    snd_usr.save()
                    rec_usr.save()
                else:
                    messages.success(request, 'مبلغ مورد نظر بیشتر از موجودی است')
                    return render(request,'user_unknownpay.html', {'form':form })

            if (type is "2"):
                print("dxxxxxxxxxxxxxxxxxxxxx")
                if (snd_usr.dollar_wallet>=pool):
                    snd_usr.dollar_wallet -= pool
                    rec_usr.dollar_wallet += pool
                    snd_usr.save()
                    rec_usr.save()
                else:
                    messages.success(request, 'مبلغ مورد نظر بیشتر از موجودی است')
                    return render(request,'user_unknownpay.html', {'form':form })

            if (type is "3"):
                print("uxxxxxxxxxxxxxxxxxxxxx")
                if (snd_usr.euro_wallet >= pool):
                    snd_usr.euro_wallet -= pool
                    rec_usr.euro_wallet += pool
                    snd_usr.save()
                    rec_usr.save()
                else:
                    messages.success(request, 'مبلغ مورد نظر بیشتر از موجودی است')
                    return render(request,'user_unknownpay.html', {'form':form })


            messages.success(request, 'پرداخت ناشناس با موفقیت انجام شد')
            return render(request, 'user_unknownpay.html', {'form':form})
        else:
                messages.success(request, 'ورودی های خود را چک کنید')
                return render(request, 'user_unknownpay.html', {'form': form})

    return render(request, 'user_unknownpay.html', {'form':form })

def employee_charge(request):
    if request.method == 'POST':
        amount = float(request.POST['cash'])
        u = request.user
        if(request.POST['action'] == 'شارژ'):
            u.rial_wallet = u.rial_wallet + amount
            u.save()
            messages.success(request,'عملیات با موفقیت انجام شد')
        elif(request.POST['action'] == 'دشارژ'):
            if(u.rial_wallet >= amount):
                u.rial_wallet = u.rial_wallet - amount
                u.save()
                messages.success(request, 'عملیات با موفقیت انجام شد')
            else:
                messages.success(request, 'موجودی کافی نیست!')
    return render(request, 'employee_charge.html', {})



def manager_charge(request):
    if request.method == 'POST':
        amount = float(request.POST['cash'])
        wallet = request.POST['wallet']
        u = request.user
        if(request.POST['action'] == 'شارژ'):
            if(wallet == 'rial'):
                u.rial_wallet = u.rial_wallet + amount
            elif(wallet == 'dollar'):
                u.dollar_wallet = u.dollar_wallet + amount
            elif (wallet == 'euro'):
                u.euro_wallet = u.euro_wallet + amount
            u.save()
            messages.success(request,'عملیات با موفقیت انجام شد')
        elif(request.POST['action'] == 'دشارژ'):
            if (wallet == 'rial'):
                if(u.rial_wallet >= amount):
                    u.rial_wallet = u.rial_wallet - amount
                    u.save()
                    messages.success(request, 'عملیات با موفقیت انجام شد')
                else:
                    messages.success(request, 'موجودی کافی نیست!')
            elif (wallet == 'dollar'):
                if (u.dollar_wallet >= amount):
                    u.dollar_wallet = u.dollar_wallet - amount
                    u.save()
                    messages.success(request, 'عملیات با موفقیت انجام شد')
                else:
                    messages.success(request, 'موجودی کافی نیست!')
            elif (wallet == 'euro'):
                if (u.euro_wallet >= amount):
                    u.euro_wallet = u.euro_wallet - amount
                    u.save()
                    messages.success(request, 'عملیات با موفقیت انجام شد')
                else:
                    messages.success(request, 'موجودی کافی نیست!')
    return render(request, 'manager_charge.html', {})



def user_charge(request):
    if request.method == 'POST':
        amount = float(request.POST['cash'])
        u = request.user
        if(request.POST['action'] == 'شارژ'):
            u.rial_wallet = u.rial_wallet + amount
            u.save()
            messages.success(request,'عملیات با موفقیت انجام شد')
        elif(request.POST['action'] == 'دشارژ'):
            if(u.rial_wallet >= amount):
                u.rial_wallet = u.rial_wallet - amount
                u.save()
                messages.success(request, 'عملیات با موفقیت انجام شد')
            else:
                messages.success(request, 'موجودی کافی نیست!')
    return render(request, 'user_charge.html', {})

def user_change(request):
    response = requests.get('https://www.faranevis.com/api/currency/')
    geodata = response.json()
    answer = 0
    if request.method == 'POST':
        fromCurr = request.POST['from']
        toCurr = request.POST['to']
        dollar = (request.POST['dollar'])
        euro = (request.POST['euro'])
        amount = (request.POST['amount-from'])
        dd = dollar.split(',')
        ee = euro.split(',')
        dollar = ""
        for i in range(len(dd)):
            dollar += dd[i]
        euro = ""
        for i in range(len(ee)):
            euro += ee[i]
        dollar = float(str(dollar))
        euro = float(str(euro))
        amount = float(str(amount))
        if fromCurr != toCurr:
            u = request.user
            m = MyUser.objects.filter(is_admin=True).first()
            if fromCurr == 'rial' and toCurr == 'euro':
                if(amount <= u.rial_wallet):
                    answer = (amount * 0.95) / euro
                    u.rial_wallet = u.rial_wallet - amount
                    u.euro_wallet = u.euro_wallet + answer
                    u.save()
                    m.rial_wallet += (amount*0.05)
                    m.save()
                    messages.success(request, 'تبدیل با موفقیت انجام شده و مبلغ '+str(amount)+'ریال از کیف پول شما کسر شده و '+str(answer)+'یورو به کیف پول یورو اضافه شد.')
                else:
                    messages.success(request, 'موجودی کیف پول انتخاب شده کافی نیست!')
            if fromCurr == 'rial' and toCurr == 'dollar':
                if (amount <= u.rial_wallet):
                    answer = (amount * 0.95) / dollar
                    u.rial_wallet = u.rial_wallet - amount
                    u.dollar_wallet = u.dollar_wallet + answer
                    u.save()
                    m.rial_wallet += (amount*0.05)
                    m.save()
                    messages.success(request,
                                     'تبدیل با موفقیت انجام شده و مبلغ ' + str(amount) + 'ریال از کیف پول شما کسر شده و ' + str(answer) + 'دلار به کیف پول دلار اضافه شد.')
                else:
                    messages.success(request, 'موجودی کیف پول انتخاب شده کافی نیست!')
            if fromCurr == 'euro' and toCurr == 'rial':
                if (amount <= u.euro_wallet):
                    answer = (amount * 0.95) * euro
                    u.euro_wallet = u.euro_wallet - amount
                    u.rial_wallet = u.rial_wallet + answer
                    u.save()
                    m.euro_wallet += (amount*0.05)
                    m.save()
                    messages.success(request,
                                     'تبدیل با موفقیت انجام شده و مبلغ ' + str(amount) + 'یورو از کیف پول شما کسر شده و ' + str(answer) + 'ریال به کیف پول ریال اضافه شد.')
                else:
                    messages.success(request, 'موجودی کیف پول انتخاب شده کافی نیست!')
            if fromCurr == 'dollar' and toCurr == 'rial':
                if (amount <= u.dollar_wallet):
                    answer = (amount * 0.95) * dollar
                    u.dollar_wallet = u.dollar_wallet - amount
                    u.rial_wallet = u.rial_wallet + answer
                    u.save()
                    m.dollar_wallet += (amount*0.05)
                    m.save()
                    messages.success(request,
                                     'تبدیل با موفقیت انجام شده و مبلغ ' + str(amount) + 'دلار از کیف پول شما کسر شده و ' + str(answer) + 'ریال به کیف پول ریال اضافه شد.')
                else:
                    messages.success(request, 'موجودی کیف پول انتخاب شده کافی نیست!')
            if fromCurr == 'dollar' and toCurr == 'euro':
                if (amount <= u.dollar_wallet):
                    answer = ((amount * 0.95) * dollar) / euro
                    u.dollar_wallet = u.dollar_wallet - amount
                    u.euro_wallet = u.euro_wallet + answer
                    u.save()
                    m.dollar_wallet += (amount*0.05)
                    m.save()
                    messages.success(request,
                                     'تبدیل با موفقیت انجام شده و مبلغ ' + str(amount) + 'دلار از کیف پول شما کسر شده و ' + str(answer) + 'یورو به کیف پول یورو اضافه شد.')
                else:
                    messages.success(request, 'موجودی کیف پول انتخاب شده کافی نیست!')
            if fromCurr == 'euro' and toCurr == 'dollar':
                if (amount <= u.euro_wallet):
                    answer = ((amount * 0.95) * euro) / dollar
                    u.euro_wallet = u.euro_wallet - amount
                    u.dollar_wallet = u.dollar_wallet + answer
                    u.save()
                    m.euro_wallet += (amount*0.05)
                    m.save()
                    messages.success(request,
                                     'تبدیل با موفقیت انجام شده و مبلغ ' + str(amount) + 'یورو از کیف پول شما کسر شده و ' + str(answer) + 'دلار به کیف پول دلار اضافه شد.')
                else:
                    messages.success(request, 'موجودی کیف پول انتخاب شده کافی نیست!')
        else:
            answer = amount
    return render(request, 'user_change.html', {'answer': answer, 'dollar': geodata['دلار'], 'euro': geodata['یورو'], })


def user_service(request):
    return render(request, 'user_service.html', {})

def user_service_gre(request):
    form = GREForm()
    if request.method == "POST":
        form = GREForm(request.POST)
        if form.is_valid():
            gre = form.save()
            gre.save()
            u = MyUser.objects.get(pk=request.user.pk)
            if ( 250* (105 / 100)) > u.dollar_wallet:
                    messages.success(request, 'موجودی کافی نیست!')
                    return render(request, 'user_service_gre.html')
            e = Employee.objects.all()[0]
            transaction = Transaction.objects.create(type="GRE", employee=e, user=u, subject="GRE", greform=gre)
            transaction.save()
            sendmessage = Message.objects.create(author=request.user, reciever=request.user,
                                                 content='تراکنش ثبت نام در آزمون GRE برای شما ثبت شد',
                                                 subject='آزمون GRE',  transaction = transaction)
            sendmessage.save()
            messages.success(request, 'درخواست شما با موفقیت ثبت گردید')
            return render(request, 'user_service_gre.html', {'form':form })
            return redirect('user_service_gre')
        else:
            messages.success(request, 'مشکلی در ارسال پیام وجود دارد. ورودی های خود را بررسی کنید!')
    return render(request, 'user_service_gre.html', {'form': form})


def user_service_toefl(request):
    form = TOEFLForm()
    if request.method == "POST":
        print('A')
        form = TOEFLForm(request.POST)
        if form.is_valid():
            toefl = form.save()
            toefl.save()
            u = MyUser.objects.get(pk=request.user.pk)
            if ( 60* (105 / 100)) > u.dollar_wallet:
                    messages.success(request, 'موجودی کافی نیست!')
                    return render(request, 'user_service_toefl.html')
            e = Employee.objects.all()[0]
            transaction = Transaction.objects.create(type="TOEFT",employee=e,  user =u, subject = "TOEFL", toeflform = toefl)
            transaction.save()
            sendmessage = Message.objects.create(author=request.user, reciever = request.user, content='تراکنش ثبت نام در آزمون TOEFL برای شما ثبت شد', subject='آزمون TOEFL',  transaction = transaction)
            sendmessage.save()
            messages.success(request, 'درخواست شما با موفقیت ثبت گردید')
            return redirect('user_service_toefl')
        else:
            messages.success(request, 'مشکلی در ارسال پیام وجود دارد. ورودی های خود را بررسی کنید!')
    return render(request, 'user_service_toefl.html', {'form': form})

def user_service_ielts(request):
    form = IELTSForm()
    if request.method == "POST":
        form = IELTSForm(request.POST)
        if form.is_valid():
            ielts = form.save()
            ielts.save()
            u = MyUser.objects.get(pk=request.user.pk)
            if ( 340* (105 / 100)) > u.euro_wallet:
                    messages.success(request, 'موجودی کافی نیست!')
                    return render(request, 'user_service_ielts.html')
            e = MyUser.objects.filter(is_employee = True).first()
            transaction = Transaction.objects.create(type="IELTS",employee=e,  user =u, subject = "IELTS", ieltsform = ielts)
            transaction.save()
            sendmessage = Message.objects.create(author=request.user, reciever = request.user, content='تراکنش ثبت نام در آزمون IELTS برای شما ثبت شد', subject='آزمون IELTS',  transaction = transaction)
            sendmessage.save()
            messages.success(request, 'درخواست شما با موفقیت ثبت گردید')
            return redirect('user_service_ielts')
        else:
            messages.success(request, 'مشکلی در ارسال پیام وجود دارد. ورودی های خود را بررسی کنید!')
    return render(request, 'user_service_ielts.html', {'form': form})


@login_required(redirect_field_name='login')
def user_profile_edit(request):
    form = NameForm2(request = request)
    if request.method == 'POST' :
        form = NameForm2(request.POST , request = request)
        if form.is_valid():
            user =  MyUser.objects.get(pk = request.user.pk)
            user.name = form.cleaned_data['name']
            user.acc_num = form.cleaned_data['acc_num']
            try:
                user.email = form.cleaned_data['email']
            except:
                pass
            messages.success(request, 'ویرایش با موفقیت انجام شد')
            user.save()
            return render(request, 'user_profile_edit.html', {})
        else:
            user =  MyUser.objects.get(pk = request.user.pk)
            user.name = form.cleaned_data['name']
            user.acc_num = form.cleaned_data['acc_num']
            messages.success(request, 'ویرایش با موفقیت انجام شد')
            user.save()
            return render(request, 'user_profile_edit.html', {})
    return render(request, 'user_profile_edit.html', {'form':form})

@login_required(redirect_field_name='login')
def user_bala_pass(request):
    f=ChangePassWordForm()
    return render (request , 'user_change_password.html' , {'form':f})

@login_required(redirect_field_name='login')
def user_change_pass(request):
    form = ChangePassWordForm(request.POST)
    if request.method == 'POST' :
        if form.is_valid():
            u = MyUser.objects.get(pk=request.user.pk)
            if form.cleaned_data['new_pass'] == form.cleaned_data['repeat_pass']  :
                u.set_password(form.cleaned_data['new_pass'])
                u.save()
                messages.success(request, 'تغییر رمز با موفقیت انجام شد')
                u.save()
                return render(request, 'user_change_password.html', {})
            else:
                messages.success(request, 'ورودی های خود را چک کنید')
    return render(request, 'user_change_password.html', {'form':form})

@login_required(redirect_field_name='login')
def employee_profile_edit(request):
    form = NameForm2(request = request)
    if request.method == 'POST' :
        form = NameForm2(request.POST , request = request)
        if form.is_valid():
            user =  MyUser.objects.get(pk = request.user.pk)
            user.name = form.cleaned_data['name']
            user.acc_num = form.cleaned_data['acc_num']
            try:
                user.email = form.cleaned_data['email']
            except:
                pass
            messages.success(request, 'ویرایش با موفقیت انجام شد')
            user.save()
            return render(request, 'employee_profile_edit.html', {})
        else:
            user =  MyUser.objects.get(pk = request.user.pk)
            user.name = form.cleaned_data['name']
            user.acc_num = form.cleaned_data['acc_num']
            messages.success(request, 'ویرایش با موفقیت انجام شد')
            user.save()
            return render(request, 'employee_profile_edit.html', {})
    return render(request, 'employee_profile_edit.html', {'form':form})

@login_required(redirect_field_name='login')
def employee_bala_pass(request):
    f=ChangePassWordForm()
    return render (request , 'employee_change_password.html' , {'form':f})

@login_required(redirect_field_name='login')
def employee_change_pass(request):
    form = ChangePassWordForm(request.POST)
    if request.method == 'POST' :
        if form.is_valid():
            u = MyUser.objects.get(pk=request.user.pk)
            if form.cleaned_data['new_pass'] == form.cleaned_data['repeat_pass']  :
                u.set_password(form.cleaned_data['new_pass'])
                u.save()
                messages.success(request, 'تغییر رمز با موفقیت انجام شد')
                u.save()
                return render(request, 'employee_change_password.html', {})
            else:
                messages.success(request, 'ورودی های خود را چک کنید')
    return render(request, 'employee_change_password.html', {'form':form})

@login_required(redirect_field_name='login')
def manager_profile_edit(request):
    form = NameForm3(request = request)
    if request.method == 'POST' :
        form = NameForm3(request.POST , request = request)
        if form.is_valid():
            user =  MyUser.objects.get(pk = request.user.pk)
            user.name = form.cleaned_data['name']
            user.acc_num = form.cleaned_data['acc_num']
            user.dollor_account= form.cleaned_data['dollor_account']
            user.euro_account = form.cleaned_data['euro_account']
            user.save()
            try:
                user.email = form.cleaned_data['email']
            except:
                pass
            messages.success(request, 'ویرایش با موفقیت انجام شد')
            user.save()
            return render(request, 'manager_profile_edit.html', {})
        else:
            user =  MyUser.objects.get(pk = request.user.pk)
            user.name = form.cleaned_data['name']
            user.acc_num = form.cleaned_data['acc_num']
            user.dollor_account= form.cleaned_data['dollor_account']
            user.euro_account = form.cleaned_data['euro_account']
            messages.success(request, 'ویرایش با موفقیت انجام شد')
            user.save()
            return render(request, 'manager_profile_edit.html', {})
    return render(request, 'manager_profile_edit.html', {'form':form})

@login_required(redirect_field_name='login')
def manager_bala_pass(request):
    f=ChangePassWordForm()
    return render (request , 'manager_change_password.html' , {'form':f})

@login_required(redirect_field_name='login')
def manager_change_pass(request):
    form = ChangePassWordForm(request.POST)
    if request.method == 'POST' :
        if form.is_valid():
            u = MyUser.objects.get(pk=request.user.pk)
            if form.cleaned_data['new_pass'] == form.cleaned_data['repeat_pass']  :
                u.set_password(form.cleaned_data['new_pass'])
                u.save()
                messages.success(request, 'تغییر رمز با موفقیت انجام شد')
                u.save()
                return render(request, 'manager_change_password.html', {})
            else:
                messages.success(request, 'ورودی های خود را چک کنید')
    return render(request, 'manager_change_password.html', {'form':form})


@login_required(redirect_field_name='login')
def usr_list(request):
    employees = MyUser.objects.filter(is_employee=False , is_admin = False )
    return render(request, 'usr_list.html',{'employees':employees} )












@login_required(redirect_field_name='login')
def edit(request):
    f=NameForm2(request.POST, request=request)
    return render (request , 'user_profile_edit.html' , {'form':f , 'user': request.user})


@login_required(redirect_field_name='login')
def bala_edit_emp(request):
    f=NameForm2(instance=request.user)
    return render (request , 'employee_profile_edit.html' , {'form':f , 'user': request.user})



@login_required(redirect_field_name='login')
def bala_edit_manager(request):
    f=NameForm2(instance=request.user)
    return render (request , 'manager_profile_edit.html' , {'form':f , 'user': request.user})



@login_required(redirect_field_name='login')
def bala_add_employee(request):
    f=add_employee2(request=request)
    return render (request , 'add_employee.html' , {'form':f , 'user': request.user})

def upload_file(request):
    form = NameForm(request.POST, request.FILES)
    if request.method == 'POST' :
        if form.is_valid():
                user = form.save();
                user.set_password(form.data['password'])
                # user = MyUser.objects.create_user(name=form.data['name'], email=form.data['email'],  acc_num=form.data['acc_num'])
                messages.success(request, 'ثبت نام با موفقیت انجام شد')
                user.save();
                return render(request, 'register.html', { 'user':user
                })
    return render(request, 'register.html', {'form':form})







@login_required(redirect_field_name='login')
def add_employee(request):
    form = add_employee2(request.POST, request=request)
    if request.method == 'POST':
        print("hhhhhhhhhhhhhhhhhhhhhhhhh")
        if form.is_valid():
            print("yeeeeeeeeeeeeeeeeeeeeeeeees")
            user = form.save()
            user.set_password('12345')
            user.is_employee = True
            user.save()
            messages.success(request, 'ثبت کارمند با موفقیت انجام شد')
            return render(request, 'add_employee.html', {'user': user, 'form':form})

        return render(request, 'add_employee.html', {'form': form})

def employee_list(request):
    employees = MyUser.objects.filter(is_employee = True)
    print("fffffffffffffffffffffffffffffffff   ")
    print(employees)
    return render(request, 'employee_list.html',{'employees':employees} )



def see_employee_profile(request, pke):
    e = MyUser.objects.filter(pk = pke, is_employee = True).first()
    return render(request, 'employee_profile.html' , {'e': e})

def see_usr_profile(request, pke):
    e = MyUser.objects.filter(pk = pke).first()
    return render(request, 'usr_profile.html' , {'e': e})

def bala_change_employee_salary(request,pke):
    form = ChangeSalary()

    u = MyUser.objects.get(pk=pke ,  is_employee = True)

    return render(request, 'change_employee_salary.html' ,{'form':form , 'e':u} )

def change_salary(request , pke):
    form = ChangeSalary()
    if request.method == 'POST' :
        form = ChangeSalary(request.POST)
        if form.is_valid():

            u = MyUser.objects.get(pk=pke ,  is_employee = True)
            u.salary = form.data['new_salary']
            u.save()
            messages.success(request, 'تغییر حقوق با موفقیت انجام شد')
            return render(request, 'change_employee_salary.html', {'form':form , 'e':u})
        else:
                messages.success(request, 'ورودی های خود را چک کنید')
    return render(request, 'change_employee_salary.html', {'form':form })


def ban_employee(request, pke):
    u = MyUser.objects.filter(pk=pke, is_employee = True).first()
    u.status = "banned"
    u.save()
    e = AuthenticationFormWithChekUsersStatus(request.POST)
    r = e.confirm_login_allowed(u)
    if r == 1:
        u.is_active = False
        u.status = "banned"
        u.save()
        messages.success(request, 'محدود شد')
    if r == 2:
        u.is_active = True
        u.status = "enabled"
        u.save()
        messages.success(request, 'محدودیت رفع شد')

    employees = MyUser.objects.filter(is_employee=True, is_admin=False)
    return render(request, 'employee_list.html', {'e': u, 'employees': employees})


def see_employee_transactions(request, pke):
    e = MyUser.objects.filter(pk = pke ,  is_employee = True).first()
    t = Transaction.objects.filter(employee = e)
    return render(request, 'employee_transactions.html', {'transactions': t , 'e':e})


def see_usr_transactions(request, pke):
    e = MyUser.objects.filter(pk = pke).first()
    t = Transaction.objects.filter(user = e)
    return render(request, 'usr_transactions.html', {'transactions': t , 'e':e})


def see_transaction_context(request, pkt):
    t = Transaction.objects.filter(pk = pkt).first()
    return render(request , 'transaction_context.html' , {'t':t})


def ban_usr(request, pke):
    u = MyUser.objects.filter(pk = pke).first()
    u.status = "banned"
    u.save()
    e=AuthenticationFormWithChekUsersStatus(request.POST)
    r = e.confirm_login_allowed(u)
    if r ==1:
        u.is_active = False
        u.status="banned"
        u.save()
        messages.success(request, 'محدود شد')
    if r ==2:
        u.is_active = True
        u.status = "enabled"
        u.save()
        messages.success(request, 'نامحدود شد')
    employees = MyUser.objects.all()

    employees = MyUser.objects.filter(is_employee = False , is_admin = False)
    return render(request , 'usr_list.html', {'e':u , 'employees':employees})

def ban_emp(request, pke):
    u = MyUser.objects.filter(pk = pke , is_employee = True).first()
    if u.status == "enabled":
      u.status = "banned"
    else:
      u.status="enabled"
    u.save()
    e=AuthenticationFormWithChekUsersStatus(request.POST)
    r=e.confirm_login_allowed(u)
    if r ==1:
        messages.success(request, 'محدود شد')
    if r ==2:
        messages.success(request, 'نامحدود شد')
    employees = MyUser.objects.filter(is_employee= True)

    return render(request , 'employee_list.html', {'e':u , 'employees': employees})



def usertransactions(request, pke):
    u = MyUser.objects.get(pk=pke)
    transactions = Transaction.objects.filter(user = u)
    return render(request, 'usertransactions.html', {'transactions':transactions})

def runtransactions(request, pke):
    transactions = Transaction.objects.filter(status = 'قبول شده' , employee = MyUser.objects.filter(is_employee = True, pk=pke).first())
    return render(request, 'runtransactions.html', {'transactions':transactions})

def waitingtransactions(request):
    s = "در حال انتظار"
    transactions = Transaction.objects.filter(status = s)
    return render(request, 'waitingtransactions.html', {'transactions':transactions})

def employeetransactions(request):
    s = "در حال انتظار"
    transactions = Transaction.objects.filter(~Q(status = s), ~Q(status = 'قبول شده'))
    return render(request, 'employeetransactions.html', {'transactions':transactions})

def managertransactions(request):
    transactions = Transaction.objects.all()
    return render(request, 'managertransactions.html', {'transactions':transactions})

def transaction(request, pke):
    transaction = get_object_or_404(Transaction, pk=pke)
    if transaction.type == "GRE":
        f = transaction.greform
        return render(request, 'gretransaction.html', {'gre':f})
    elif transaction.type == "TOEFL":
        f = transaction.toeflform
        return render(request, 'toefltransaction.html', {'toefl':f})
    elif transaction.type == "IELTS":
        f = transaction.ieltsform
        return render(request, 'ieltstransaction.html', {'ielts':f})
    elif transaction.type == "Uni":
        f = transaction.uniform
        return render(request, 'unitransaction.html', {'uni':f})
    elif transaction.type == "Pay":
        f = transaction.payform
        return render(request, 'paytransaction.html', {'pay':f})
    return render(request, 'employeetransactions.html')

def accept(request, pke):
    transaction=get_object_or_404(Transaction, pk=pke)
    transaction.status = 'قبول شده'
    transaction.save()
    u = request.user
    transaction.employee = u
    messages.success(request, 'این تراکنش توسط شما پذیرفته شده است.')
    return render(request, 'accept.html', {'transaction':transaction})

def no(request, pke):
    transaction=get_object_or_404(Transaction, pk=pke)
    transaction.status = 'رد شده'
    transaction.save()
    messages.success(request, 'درخواست شما با موفقیت ثبت گردید')
    return render(request, 'accept.html', {'transaction':transaction})

def yes(request, pke):
    transaction=get_object_or_404(Transaction, pk=pke)

    u = transaction.user
    m = MyUser.objects.filter(is_admin = True).first()
    arzi = 0
    kind = "dollar"
    if transaction.ieltsform != None:
        arzi = 340
        kind = "euro"
    elif transaction.uniform != None:
        arzi = transaction.uniform.arzi
        kind = transaction.uniform.kind
    elif transaction.payform != None:
        arzi = transaction.payform.arzi
        kind = transaction.payform.kind
    elif transaction.toeflform != None:
        arzi = 60
        kind = "dollar"
    elif transaction.greform != None:
        arzi = 250
        kind = "dollar"
    if kind == "dollar":
        if (arzi*(105/100)) > u.dollar_wallet:
            messages.success(request, 'موجودی کافی نیست!')
            return render(request, 'accept.html', {'transaction': transaction})
        u.dollar_wallet -= arzi*(105/100)
        m.dollar_wallet -= arzi*(5/100)
    elif kind == "euro":
        if (arzi*(105/100)) > u.euro_wallet:
            messages.success(request, 'موجودی کافی نیست!')
            return render(request, 'accept.html', {'transaction': transaction})
        u.euro_wallet -= arzi*(105/100)
        m.euro_wallet -= arzi*(5/100)
    u.save()
    m.save()
    transaction.status = 'تایید شده'
    transaction.save()
    messages.success(request, 'درخواست شما با موفقیت ثبت گردید')
    return render(request, 'accept.html', {'transaction': transaction})


def inform(request, pke):
    if request.method == "POST":
        print("iiiiiiiinnnnnnnn")
        sendmessage = Message.objects.create(author=request.user, reciever=MyUser.objects.filter(is_admin = True).first(),
                                             content='اطلاع حالت غیر عادی برای تراکنش ', subject='حالت غیرعادی',
                                             transaction=get_object_or_404(Transaction, pk=pke))
        sendmessage.save()

        messages.success(request, 'درخواست شما با موفقیت ثبت گردید')
    print("iiiiiiiinnnnnnnn۲")
    return render(request, 'inform.html')

def message(request):
    messages = Message.objects.filter(reciever = request.user)
    return render(request, 'message.html', {'messages':messages})


def uni(request):
    form = UniForm()
    if request.method == "POST":
        form = UniForm(request.POST)
        if form.is_valid():
            uni = form.save()
            uni.save()
            u = MyUser.objects.get(pk=request.user.pk)
            arzi = form.cleaned_data['arzi']
            kind = form.cleaned_data['kind']
            if kind == "dollar":
                if (arzi * (105 / 100)) > u.dollar_wallet:
                    messages.success(request, 'موجودی کافی نیست!')
                    return render(request, 'uni.html')
            if kind == "euro":
                if (arzi * (105 / 100)) > u.euro_wallet:
                    messages.success(request, 'موجودی کافی نیست!')
                    return render(request, 'uni.html')
            e = MyUser.objects.filter(is_employee = True).first()
            transaction = Transaction.objects.create(type="Uni",employee=e,  user =u, subject = "Uni", uniform = uni)
            transaction.save()
            sendmessage = Message.objects.create(author=request.user, reciever = request.user, content='تراکنش ثبت نام یا واریز کردن هزینه به حساب  دانشگاه خارج از کشور برای شما ثبت شد', subject='ثبت نام یا واریز کردن هزینه به حساب  دانشگاه خارج از کشور',  transaction = transaction)
            sendmessage.save()
            messages.success(request, 'درخواست شما با موفقیت ثبت گردید')
            return redirect('uni')
        else:
            messages.success(request, 'مشکلی در ارسال پیام وجود دارد. ورودی های خود را بررسی کنید!')
    return render(request, 'uni.html', {'form': form})

def pay(request):
    form = PayForm()
    if request.method == "POST":
        form = PayForm(request.POST)
        if form.is_valid():
            pay = form.save()
            pay.save()
            u = MyUser.objects.get(pk=request.user.pk)
            arzi = form.cleaned_data['arzi']
            kind = form.cleaned_data['kind']
            if kind is "dollar":
                if (arzi * (105 / 100)) > u.dollar_wallet:
                    messages.success(request, 'موجودی کافی نیست!')
                    return render(request, 'pay.html')
            if kind is "euro":
                if (arzi * (105 / 100)) > u.euro_wallet:
                    messages.success(request, 'موجودی کافی نیست!')
                    return render(request, 'pay.html')
            e = MyUser.objects.filter(is_employee = True).first()
            transaction = Transaction.objects.create(type="Pay",employee=e,  user =u, subject = "Pay", payform = pay)
            transaction.save()
            sendmessage = Message.objects.create(author=request.user, reciever = request.user, content='تراکنش واریز کردن پول به حساب خارجی برای شما ثبت شد', subject='واریز کردن پول به حساب خارجی', transaction = transaction)
            sendmessage.save()
            messages.success(request, 'درخواست شما با موفقیت ثبت گردید')
            return redirect('pay')
        else:
            messages.success(request, 'مشکلی در ارسال پیام وجود دارد. ورودی های خود را بررسی کنید!')
    return render(request, 'pay.html', {'form': form})