from django.contrib import admin
from applicants.models import Applicant, skill_list
from employees.models import Employee, job_post, service_type, category, company_type
from .models import User


# Register your models here.
admin.site.register(User)
admin.site.register(skill_list)
admin.site.register(Applicant)
admin.site.register(Employee)
admin.site.register(category)
admin.site.register(service_type)
admin.site.register(job_post)
admin.site.register(company_type)
