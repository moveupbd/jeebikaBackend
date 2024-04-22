from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from common.models import BaseModelWithUID
from accountio.models import User
from common.choices import CompanySize

class company_type(BaseModelWithUID):
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name
    

class category(BaseModelWithUID):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

# Create your models here.
class Employee(AbstractBaseUser, BaseModelWithUID):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='employee')
    category = models.ForeignKey(category, default="", on_delete=models.CASCADE) # this is business category
    company_address = models.TextField(blank=True, null=True)
    company_logo = models.ImageField(upload_to='images/company_logos/', blank=True, null=True)
    website_url = models.TextField(blank=True, null=True)
    company_type = models.ForeignKey(company_type, default="", on_delete=models.CASCADE, null=True, blank=True)
    company_subtype = models.CharField(max_length=100, blank=True, null=True)
    year_of_eastablishment = models.PositiveIntegerField(blank=True, null=True)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    license_copy = models.ImageField(upload_to='images/license_copies/', blank=True, null=True)
    representative_name = models.CharField(max_length=200, blank=True, null=True)
    representative_designation = models.CharField(max_length=100, blank=True, null=True)
    representative_mobile = models.CharField(max_length=100, blank=True, null=True)
    representative_email = models.CharField(max_length=100, blank=True, null=True)
    id_card_front = models.ImageField(upload_to='images/id_pics_front/', blank=True, null=True)
    id_card_back = models.ImageField(upload_to='images/id_pics_back/', blank=True, null=True)
    company_size = models.CharField(max_length=10,choices=CompanySize.choices, default=CompanySize.ONETOFIFTY)
    business_desc= models.TextField(blank=True, null=True)
    

    def __str__(self):
        return self.user.username
    
    
    
class service_type(models.Model):
    service = models.CharField(max_length=100)
    
    def __str__(self):
        return self.service
    
      
class job_post(BaseModelWithUID):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="", related_name='job_posts')
    category = models.ForeignKey(category,default="", on_delete=models.CASCADE)
    service_type = models.ForeignKey(service_type, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    company_type = models.ForeignKey(company_type, default="", on_delete=models.CASCADE, null=True, blank=True)
    job_designation = models.CharField(max_length=100, null=True, blank=True)
    vacancy = models.PositiveIntegerField(null=True, blank=True)
    department = models.CharField(max_length=200, null=True, blank=True)
    job_desc = models.TextField(null=True, blank=True)
    published = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    skill = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    requirements= models.TextField(null=True, blank=True)
    responsibilities = models.TextField(null=True, blank=True)
    expertise = models.CharField(max_length=200,null=True, blank=True)
    employment_status = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    company_info = models.CharField(max_length=100, null=True, blank=True)
    compensation = models.CharField(max_length=200, null=True, blank=True)
    other_facilities = models.TextField(null=True, blank=True)
    apply_procedure = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.job_designation
    