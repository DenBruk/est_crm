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
from .forms import dataForm
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
