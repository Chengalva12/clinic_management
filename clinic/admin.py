from django.contrib import admin
from .models import Clinic, Vaccination, Doctor, Patient, Prescription, Medicine, Pharmacy, Employee, Payroll, Insurance

admin.site.register(Clinic)
admin.site.register(Vaccination)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Prescription)
admin.site.register(Medicine)
admin.site.register(Pharmacy)
admin.site.register(Employee)
admin.site.register(Payroll)
admin.site.register(Insurance)
