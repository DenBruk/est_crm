
# Create your models here.
from django.db import models
import datetime
from django.utils import timezone
# Create your models here.


class services(models.Model):
    service_name = models.TextField(default = '',max_length=100)
    def __unicode__(self):
        return self.service_name
    def __str__(self):
        return self.service_name

class company(models.Model):
    company_name = models.TextField(default = '',max_length=100)
    email = models.TextField(default=0)
    phone = models.TextField(default = '',max_length=100)
    def __unicode__(self):
        return self.company_name
    def __str__(self):
        return self.company_name
class data(models.Model):
    company = models.ForeignKey(company,default=1,on_delete=models.CASCADE)
    service = models.ForeignKey(services,default=1,on_delete=models.CASCADE)
    date_of_exp = models.DateField(default=timezone.now())
    qty = models.IntegerField(default=1)
    price = models.IntegerField(default=240) 
    def __str__(self):
        template = '{0.company} | {0.service}'
        return template.format(self)
