from django.contrib.auth.models import User
from django.db import models


class Clinic(models.Model):
    clinic_id = models.AutoField(primary_key=True)
    clinic_name = models.CharField(max_length=100)
    clinic_phone_number = models.CharField(max_length=15)
    clinic_address = models.TextField()
    clinic_email = models.EmailField()

class Vaccination(models.Model):
    vaccination_id = models.AutoField(primary_key=True)
    vaccination_name = models.CharField(max_length=100)
    dosage = models.FloatField()
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)    # Link to User
    D_id = models.AutoField(primary_key=True)
    D_Name = models.CharField(max_length=100, default="Unknown")
    D_phone_number = models.CharField(max_length=15)
    D_email = models.EmailField()
    License_number = models.CharField(max_length=50, default='ABC12345')
    Specialization = models.CharField(max_length=100, default="General")
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.D_Name

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)  # Link to User
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=100)
    Age = models.IntegerField()
    Gender = models.CharField(max_length=10, default="Unknown")
    patient_phone_number = models.CharField(max_length=15)
    patient_address = models.TextField()
    insurance = models.ForeignKey('Insurance', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.patient_name

    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='patients')
    condition = models.TextField()

    def __str__(self):
        return self.user.username

# Keep all other models the same



class Medicine(models.Model):
    m_id = models.AutoField(primary_key=True)
    m_name = models.CharField(max_length=100)
    dosage = models.FloatField()
    manufacture_date = models.DateField(default="2024-01-01")
    expiry_date = models.DateField(default="2025-01-01")
    price = models.FloatField()

class Pharmacy(models.Model):
    pharmacy_id = models.AutoField(primary_key=True)
    pharmacy_name = models.CharField(max_length=100)
    pharmacy_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.pharmacy_name

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=100)
    employee_phone_number = models.CharField(max_length=15)
    employee_address = models.TextField()
    job_title = models.CharField(max_length=100)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)  # Link to Pharmacy
    payroll = models.ForeignKey('Payroll', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.employee_name} ({self.job_title})"


class Payroll(models.Model):
    payroll_id = models.AutoField(primary_key=True)
    salary = models.FloatField()
    bonuses = models.FloatField()
    deductions = models.FloatField()

class Insurance(models.Model):
    insurance_id = models.AutoField(primary_key=True)
    insurance_name = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=50)
    coverage = models.FloatField()
    premium = models.FloatField()
    expiry_date = models.DateField()
    no_of_dependents = models.IntegerField()

class Prescription(models.Model):
    Prescription_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # Doctor is already linked
    pharmacy = models.ForeignKey('Pharmacy', on_delete=models.CASCADE, null=True, blank=True)
    medicine = models.ForeignKey('Medicine', on_delete=models.CASCADE)
    dosage_instructions = models.TextField()
    date_prescribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient.patient_name} by Dr. {self.doctor.D_Name}"
