from django.shortcuts import render, redirect, get_object_or_404
from .models import Clinic, Doctor, Patient, Medicine, Prescription, Vaccination, Employee,Pharmacy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Doctor, Patient
from django.http import HttpResponseForbidden
from .forms import AssignPatientForm


@login_required
def assign_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    # Ensure only doctors can assign
    if not hasattr(request.user, 'doctor'):
        return redirect('unauthorized')  # Redirect unauthorized users

    doctor = request.user.doctor  # Get the currently logged-in doctor

    if request.method == 'POST':
        form = AssignPatientForm(request.POST, instance=patient)
        if form.is_valid():
            patient.doctor = doctor  # Assign the patient to the doctor
            form.save()
            return redirect('doctor_dashboard')  # Redirect after success
    else:
        form = AssignPatientForm(instance=patient)

    return render(request, 'clinic_management/assign_patient.html', {'form': form, 'patient': patient})

def home(request):
    return render(request, 'clinic_management/home.html')
# Patients
@login_required
def list_patients(request):
    patients = Patient.objects.all()
    return render(request, 'clinic_management/patients.html', {'patients': patients})

@login_required
def add_patient(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        phone = request.POST['phone']
        address = request.POST['address']
        Patient.objects.create(patient_name=name, Age=age, Gender=gender, patient_phone_number=phone, patient_address=address)
        return redirect('/patients/')
    return render(request, 'clinic_management/add_patient.html')

# Doctors
@login_required
def list_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'clinic_management/doctors.html', {'doctors': doctors})


@login_required
def add_doctor(request):
    if not hasattr(request.user, 'doctor'):  # Check if the user is a doctor
        return HttpResponseForbidden("You are not authorized to perform this action.")

    clinics = Clinic.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        specialization = request.POST['specialization']
        clinic_id = request.POST['clinic']
        clinic = Clinic.objects.get(clinic_id=clinic_id)
        Doctor.objects.create(
            D_Name=name,
            D_phone_number=phone,
            D_email=email,
            Specialization=specialization,
            clinic=clinic
        )
        return redirect('/doctors/')
    return render(request, 'clinic_management/add_doctor.html', {'clinics': clinics})


# Medicines
@login_required
def list_medicines(request):
    medicines = Medicine.objects.all()
    return render(request, 'clinic_management/medicines.html', {'medicines': medicines})


@login_required
def add_medicine(request):
    if not hasattr(request.user, 'doctor'):  # Only patients can add medicines
        return HttpResponseForbidden("You are not authorized to perform this action.")

    if request.method == 'POST':
        name = request.POST['name']
        dosage = request.POST['dosage']
        price = request.POST['price']
        manufacture_date = request.POST['manufacture_date']
        expiry_date = request.POST['expiry_date']
        Medicine.objects.create(
            m_name=name,
            dosage=dosage,
            price=price,
            manufacture_date=manufacture_date,
            expiry_date=expiry_date
        )
        return redirect('/medicines/')
    return render(request, 'clinic_management/add_medicine.html')


# Vaccinations
@login_required
def list_vaccinations(request):
    vaccinations = Vaccination.objects.all()
    return render(request, 'clinic_management/vaccinations.html', {'vaccinations': vaccinations})
@login_required
def add_vaccination(request):
    clinics = Clinic.objects.all()  # Fetch all clinics to populate the dropdown
    if request.method == 'POST':
        name = request.POST['name']
        dosage = request.POST['dosage']
        clinic_id = request.POST['clinic']  # Get the selected clinic ID
        clinic = Clinic.objects.get(clinic_id=clinic_id)  # Fetch the clinic object
        Vaccination.objects.create(vaccination_name=name, dosage=dosage, clinic=clinic)
        return redirect('/vaccinations/')
    return render(request, 'clinic_management/add_vaccination.html', {'clinics': clinics})



# Delete Patient
@login_required
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    if request.method == 'POST':  # Confirm deletion
        patient.delete()
        return redirect('/patients/')
    return render(request, 'clinic_management/delete_patient.html', {'patient': patient})




# Register a Doctor
def register_doctor(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        name = request.POST['name']
        phone = request.POST['phone']
        specialization = request.POST['specialization']
        license_number = request.POST['license_number']
        clinic_id = request.POST['clinic']

        user = User.objects.create_user(username=username, password=password, email=email)
        clinic = Clinic.objects.get(clinic_id=clinic_id)
        Doctor.objects.create(user=user, D_Name=name, D_phone_number=phone, D_email=email,
                              Specialization=specialization, License_number=license_number, clinic=clinic)

        return redirect('login')
    clinics = Clinic.objects.all()
    return render(request, 'clinic_management/register_doctor.html', {'clinics': clinics})

# Register a Patient
def register_patient(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        phone = request.POST['phone']
        address = request.POST['address']

        user = User.objects.create_user(username=username, password=password)
        Patient.objects.create(user=user, patient_name=name, Age=age, Gender=gender,
                               patient_phone_number=phone, patient_address=address)

        return redirect('login')
    return render(request, 'clinic_management/register_patient.html')

# User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'clinic_management/login.html', {'error': 'Invalid credentials'})
    return render(request, 'clinic_management/login.html')

# User Logout
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def list_pharmacies(request):
    pharmacies = Pharmacy.objects.all()
    return render(request, 'clinic_management/pharmacies.html', {'pharmacies': pharmacies})

@login_required
def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    if request.method == 'POST':
        patient.patient_name = request.POST['name']
        patient.Age = request.POST['age']
        patient.Gender = request.POST['gender']
        patient.patient_phone_number = request.POST['phone']
        patient.patient_address = request.POST['address']
        patient.save()
        return redirect('/patients/')
    return render(request, 'clinic_management/edit_patient.html', {'patient': patient})


@login_required
def list_prescriptions(request):
    prescriptions = Prescription.objects.all()
    return render(request, 'clinic_management/list_prescriptions.html', {
        'prescriptions': prescriptions,
    })


def doctor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'doctor'):
            return HttpResponseForbidden("You are not authorized to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper

@doctor_required
@login_required

@login_required
def create_prescription(request):
    # Check if the logged-in user is a doctor
    if not hasattr(request.user, 'doctor'):
        return HttpResponseForbidden("You are not authorized to create prescriptions.")

    if request.method == 'POST':
        patient_id = request.POST['patient']
        medicine_id = request.POST['medicine']
        pharmacy_id = request.POST['pharmacy']
        dosage_instructions = request.POST['dosage_instructions']

        patient = Patient.objects.get(patient_id=patient_id)
        medicine = Medicine.objects.get(m_id=medicine_id)
        pharmacy = Pharmacy.objects.get(pharmacy_id=pharmacy_id)

        Prescription.objects.create(
            doctor=request.user.doctor,  # Use the doctor associated with the logged-in user
            patient=patient,
            medicine=medicine,
            pharmacy=pharmacy,
            dosage_instructions=dosage_instructions
        )
        return redirect('/prescriptions/')

    patients = Patient.objects.all()
    medicines = Medicine.objects.all()
    pharmacies = Pharmacy.objects.all()
    return render(request, 'clinic_management/create_prescription.html', {
        'patients': patients,
        'medicines': medicines,
        'pharmacies': pharmacies
    })


@login_required
def add_employee(request):
    pharmacies = Pharmacy.objects.all()  # Fetch all pharmacies for the dropdown
    if request.method == 'POST':
        name = request.POST['employee_name']
        phone = request.POST['employee_phone_number']
        address = request.POST['employee_address']
        job_title = request.POST['job_title']
        pharmacy_id = request.POST['pharmacy']
        pharmacy = Pharmacy.objects.get(pharmacy_id=pharmacy_id)

        Employee.objects.create(
            employee_name=name,
            employee_phone_number=phone,
            employee_address=address,
            job_title=job_title,
            pharmacy=pharmacy
        )
        return redirect('list_employees')
    return render(request, 'clinic_management/add_employee.html', {'pharmacies': pharmacies})

@login_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    pharmacies = Pharmacy.objects.all()
    if request.method == 'POST':
        employee.employee_name = request.POST['employee_name']
        employee.employee_phone_number = request.POST['employee_phone_number']
        employee.employee_address = request.POST['employee_address']
        employee.job_title = request.POST['job_title']
        pharmacy_id = request.POST['pharmacy']
        employee.pharmacy = Pharmacy.objects.get(pharmacy_id=pharmacy_id)
        employee.save()
        return redirect('list_employees')
    return render(request, 'clinic_management/edit_employee.html', {
        'employee': employee,
        'pharmacies': pharmacies
    })
@login_required
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    if request.method == 'POST':
        employee.delete()
        return redirect('list_employees')
    return render(request, 'clinic_management/delete_employee.html', {'employee': employee})
@login_required
def list_employees(request):
    employees = Employee.objects.select_related('pharmacy').all()
    return render(request, 'clinic_management/list_employees.html', {'employees': employees})
