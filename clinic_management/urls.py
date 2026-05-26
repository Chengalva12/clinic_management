from django.urls import path
from clinic import views

from django.contrib import admin
from django.urls import path
from clinic import views

urlpatterns = [
    path('', views.home, name='home'),
    path('patients/', views.list_patients, name='list_patients'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/edit/<int:patient_id>/', views.edit_patient, name='edit_patient'),  # Add this line
    path('patients/delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('doctors/', views.list_doctors, name='list_doctors'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    path('medicines/', views.list_medicines, name='list_medicines'),
    path('medicines/add/', views.add_medicine, name='add_medicine'),
    path('pharmacies/', views.list_pharmacies, name='list_pharmacies'),
    path('vaccinations/', views.list_vaccinations, name='list_vaccinations'),
    path('admin/', admin.site.urls),
    path('vaccinations/add/', views.add_vaccination, name='add_vaccination'),
    path('register/doctor/', views.register_doctor, name='register_doctor'),
    path('register/patient/', views.register_patient, name='register_patient'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('assign_patient/<int:patient_id>/', views.assign_patient, name='assign_patient'),
    path('prescriptions/create/', views.create_prescription, name='create_prescription'),
    path('prescriptions/', views.list_prescriptions, name='list_prescriptions'),
    path('employees/', views.list_employees, name='list_employees'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/edit/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('employees/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),
]



