from django.shortcuts import render
from django.shortcuts import render_to_response,HttpResponse,redirect
from django.http import JsonResponse
from datetime import timedelta
import datetime
# Create your views here.
from .models import data,company,services
import codecs
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from .forms import dataForm,clientForm,serviceForm
import pdfkit



def menu(request):
    if request.user.is_authenticated:
        return render_to_response('menu.html')
    else:
        return redirect('/auth/login/')
def showClients(request): # список всех мероприятий
    if request.user.is_authenticated:
        if request.GET:
            allClients = data.objects.all()
        else:
            allClients = data.objects.all()
        args = {'allClients' : allClients}
        print(args)
        return render_to_response('clients.html',args)
    else:
        return redirect('/auth/login/')
def showCompanys(request): # список всех мероприятий
    if request.user.is_authenticated:
        if request.GET:
            allClients = company.objects.all()
        else:
            allClients = company.objects.all()
        args = {'allClients' : allClients}
        print(args)
        return render_to_response('companys.html',args)
    else:
        return redirect('/auth/login/')

def showServices(request): # список всех мероприятий
    if request.user.is_authenticated:
        if request.GET:
            allClients = services.objects.all()
        else:
            allClients = services.objects.all()
        args = {'allClients' : allClients}
        print(args)
        return render_to_response('services.html',args)
    else:
        return redirect('/auth/login/')
def extendClient(request):
    if request.user.is_authenticated:
        client_id=request.GET.get('my_id')
        myinstance = data.objects.get(pk=client_id)
        myinstance.date_of_exp = myinstance.date_of_exp + timedelta(days=365)
        myinstance.save()
        my_data = {
            'date': myinstance.date_of_exp
        }
        return JsonResponse(my_data)
    else:
        return redirect('/auth/login/')
def shortenClient(request):
    if request.user.is_authenticated:
        client_id=request.GET.get('my_id')
        myinstance = data.objects.get(pk=client_id)
        myinstance.date_of_exp = myinstance.date_of_exp - timedelta(days=365)
        myinstance.save()
        my_data = {
            'date': myinstance.date_of_exp
        }
        return JsonResponse(my_data)
    else:
        return redirect('/auth/login/')


def sendEmail(mdays):
    text = ''
    allClients = data.objects.all()
    allCompanies = company.objects.all()
    allClients30 = data.objects.filter(date_of_exp=datetime.date.today()+timedelta(days=mdays)).order_by('company')
    HtmlFile = open('/home/v/vladim6g/crm.estoniancompany.eu/HelloDjango/invoice_template/index.html', 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    try:
        prevcompany=allClients30.values()[0]['company_id']
    except:
        return

    i=0
    list_of_clients = []
    list_of_services = []
    list_of_qty = []
    list_of_price = []
    for x in list(allClients30.values()):
        list_of_clients.append(x['company_id'])
        list_of_services.append(x['service_id'])
        list_of_qty.append(x['qty'])
        list_of_price.append(x['price'])
    print(list_of_clients)
    client_unique = set(list_of_clients)
    records = [i for i, x in enumerate(list_of_clients) if x == 1]
    for y in client_unique:
        records = [i for i, x in enumerate(list_of_clients) if x == y] #индексы всех записей в листе list_of_clients
        text=""
        totalsum=0
        for record in records:
            print('---------')
            text+='<tr><td class="service">'+'</td><td class="desc">'+str(services.objects.get(pk=list_of_services[record]))+'</td><td class="unit">€'+str(list_of_price[record])+'</td><td class="qty">'+str(list_of_qty[record])+'</td><td class="total">€'+str(int(list_of_qty[record])*int(list_of_price[record]))+'</td></tr>'
            totalsum +=int(list_of_qty[record])*int(list_of_price[record])
        client = company.objects.get(pk=y)
        print(client)
        my_code = source_code.replace('+++INFO+++',text)
        my_code = my_code.replace('+++CLIENT+++',client.company_name)
        my_code = my_code.replace('+++EMAIL+++',client.email)
        my_code = my_code.replace('+++PHONENUMBER+++',client.phone)
        my_code = my_code.replace('+++DATE+++',datetime.date.today().strftime("%Y-%m-%d"))
        my_code = my_code.replace('+++DUEDATE+++',(datetime.date.today()+timedelta(days=mdays)).strftime("%Y-%m-%d"))
        my_code =my_code.replace('+++TOTALSUM+++',str(totalsum))
        Html_file = open('/home/v/vladim6g/crm.estoniancompany.eu/HelloDjango/invoice_template/invoice'+str(y)+'.html', 'w', encoding='utf-8')
        Html_file.write(my_code)
        Html_file.close()
        pdfkit.from_file(['/home/v/vladim6g/crm.estoniancompany.eu/HelloDjango/invoice_template/invoice'+str(y)+'.html'], '/home/v/vladim6g/crm.estoniancompany.eu/HelloDjango/invoice_template/invoice'+str(y)+'.pdf')
        email = EmailMessage('New Invoice From Ruber Zeppelin', 'Добрый день, '+str(client.company_name)+ '. ' +(datetime.date.today()+timedelta(days=mdays)).strftime("%Y-%m-%d") + ' заканчивается первый год аренды юридического адреса и услуги контактного лица компании Ruber Zeppelin  OÜ Для продления услуг на следующий год необходимо оплатить счет в приложении данного письма. Оплатить можно банковским переводом, платежными системами вроде WesternUnion, Unistream, MoneyGram, а также PayPal или банковской картой через интернет (я тогда пришлю ссылку для оплаты картой). Благодарю за своевременную оплату! Владимир.', settings.EMAIL_HOST_USER, [str(client.email)])

        print(client.email)
        email.attach_file('/home/v/vladim6g/crm.estoniancompany.eu/HelloDjango/invoice_template/invoice'+str(y)+'.pdf')
        email.send()
    return None

def createInvoices(request):
    if request.GET['key']=="YApgMR46zjJmXc8DBqxr5GTfNWuhZd3tysUv9":
        sendEmail(7)
        sendEmail(14)
        sendEmail(21)
        sendEmail(30)
        my_data = {
            'date': 'ok'
        }
        return JsonResponse(my_data)
    else:
        my_data = {
            'date': 'bad'
        }
        return JsonResponse(my_data)

def edit(request, client_id):
    try:
        myinstance = data.objects.get(pk=client_id)
    except:
        raise Http404("Такого мероприятия еще не создали :(")
    if request.POST:
        form = dataForm(request.POST)
        if form.is_valid():
            form = dataForm(request.POST, instance=myinstance)
            form.save()
        else:
            print('Form is not valid')
        return redirect('/clients/showAll/')
    else:
        form = dataForm(instance=myinstance)
        return render(request, 'edit.html', {'form': form, 'id':client_id}, )

def editServices(request, client_id):
    if request.user.is_authenticated:
        try:
            myinstance = services.objects.get(pk=client_id)
        except:
            raise Http404("Такого клиента еще не создали :(")
        if request.POST:
            form = serviceForm(request.POST)
            if form.is_valid():
                form = serviceForm(request.POST, instance=myinstance)
                form.save()
            else:
                print('Form is not valid')
            return redirect('/clients/showServices/')
        else:
            form = serviceForm(instance=myinstance)
            return render(request, 'editServices.html', {'form': form, 'id':client_id}, )
    else:
        print('No')
        return redirect('/')

def editCompany(request, client_id):
    if request.user.is_authenticated:
        try:
            myinstance = company.objects.get(pk=client_id)
        except:
            raise Http404("Такого клиента еще не создали :(")
        if request.POST:
            form = clientForm(request.POST)
            if form.is_valid():
                form = clientForm(request.POST, instance=myinstance)
                form.save()
            else:
                print('Form is not valid')
            return redirect('/clients/showCompany/')
        else:
            form = clientForm(instance=myinstance)
            return render(request, 'editCompany.html', {'form': form, 'id':client_id}, )
    else:
        print('No')
        return redirect('/')

def addclient(request):
    if request.user.is_authenticated:
        if request.POST:
            form = dataForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                print('Form is not valid')
            return redirect('/')
        else:
            form = dataForm()
            return render(request, 'addclient.html', {'form': form})
    else:
        print('No')
        return redirect('/')
def addcompany(request):
    if request.user.is_authenticated:
        if request.POST:
            form = clientForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                print('Form is not valid')
            return redirect('/')
        else:
            form = clientForm()
            return render(request, 'addcompany.html', {'form': form})
    else:
        print('No')
        return redirect('/')
def addservice(request):
    if request.user.is_authenticated:
        if request.POST:
            form = serviceForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                print('Form is not valid')
            return redirect('/')
        else:
            form = serviceForm()
            return render(request, 'addservice.html', {'form': form})
    else:
        print('No')
        return redirect('/')

def delCompany(request, company_id):
    try:
        p = company.objects.get(pk=event_id)
        p.delete()
        return redirect('/clients/showCompanys/')
    except:
        raise Http404("Такой компании еще не создали :(")

def delData(request, data_id):
    try:
        p = data.objects.get(pk=data_id)
        p.delete()
        return redirect('/clients/showAll/')
    except:
        raise Http404("Такой даты еще не создали :(")

def delService(request, service_id):
    try:
        p = userEvent.objects.get(pk=service_id)
        p.delete()
        return redirect('/clients/showServices/')
    except:
        raise Http404("Такого Сервиса еще не создали :(")
