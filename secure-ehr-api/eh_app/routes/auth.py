from flask import Blueprint, request, render_template, redirect, url_for
from eh_app.models.user import User
from eh_app.models.paciente import Paciente
from eh_app import db
from sqlalchemy.exc import IntegrityError
from eh_app.utils.email import enviar_codigo
from eh_app.utils.security import decrypt_data

auth_bp = Blueprint('auth', __name__)



@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            form = request.form

            # Crear usuario
            user = User(
                username=form.get("email").split('@')[0],  # o un campo separado
                email=form.get("email"),
                full_name=form.get("full_name"),
                document_number=form.get("document_number"),
                birth_date=form.get("birth_date"),
                address=form.get("address"),
                phone=form.get("phone"),
                eps=form.get("eps"),
                blood_type=form.get("blood_type"),
                allergies=form.get("allergies"),
                gender=form.get("gender"),
                role="paciente"
            )

            user.set_password(form.get("password"))
            user.encrypt_fields()

            db.session.add(user)
            db.session.commit()

            return render_template("register.html", success="Registro exitoso. Ya puedes iniciar sesión.")
        except IntegrityError:
            db.session.rollback()
            return render_template("register.html", error="El correo ya está registrado.")
        except Exception as e:
            return render_template("register.html", error=f"Ocurrió un error: {str(e)}")

    return render_template("register.html")

from flask import jsonify
from eh_app.models.user import User

@auth_bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    usuarios = User.query.all()
    datos = []
    for u in usuarios:
        try:
            u.decrypt_fields()
        except Exception:
            pass  # por si algún campo no se puede descifrar

        datos.append({
            "email": u.email,
            "rol": u.role,
            "nombre": u.full_name,
            "documento": u.document_number
        })
    return jsonify(datos)

import random
from flask import session
from eh_app.models.user import User
from eh_app.utils.email import enviar_codigo

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        print("[DEBUG] Email ingresado:", email)
        print("[DEBUG] Password ingresado:", password)

        user = User.query.filter_by(email=email).first()
        if not user:
            print("[ERROR] Usuario no encontrado.")
            return render_template("login.html", error="Usuario no encontrado")

        print("[DEBUG] Usuario encontrado:", user.email)

        if not user.check_password(password):
            print("[ERROR] Contraseña incorrecta para:", user.email)
            return render_template("login.html", error="Contraseña incorrecta")

        print("[DEBUG] Contraseña correcta. 2FA habilitado:", user.two_factor_enabled)

        if user.two_factor_enabled:
            codigo = f"{random.randint(100000, 999999)}"
            print("[DEBUG] Código generado:", codigo)
            user.two_factor_code = codigo
            db.session.commit()
            enviar_codigo(user.email, codigo)
            print("[DEBUG] Código enviado a:", user.email)

            session["2fa_user_id"] = user.id
            return redirect(url_for("auth.verify_2fa"))

        session["user_id"] = user.id
        session["rol"] = user.role
        return redirect("/dashboard")

    return render_template("login.html")


@auth_bp.route('/verify-2fa', methods=['GET', 'POST'])
def verify_2fa():
    if request.method == "POST":
        codigo = request.form.get("codigo")
        user_id = session.get("2fa_user_id")
        user = User.query.get(user_id)

        if user and user.two_factor_code == codigo:
            user.two_factor_code = None
            db.session.commit()
            session["user_id"] = user.id
            session["rol"] = user.role
            return redirect("/dashboard")
        return render_template("verify_2fa.html", error="Código inválido")

    return render_template("verify_2fa.html")

@auth_bp.route('/dashboard')
def dashboard():
    total_pacientes = Paciente.query.count()
    return render_template('dashboard.html', total_pacientes=total_pacientes)

@auth_bp.route('/records', methods=['GET'])
def records():
    # Verificar si el usuario está logueado
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Aquí puedes agregar lógica para obtener los registros médicos
    # Por ejemplo:
    # records = MedicalRecord.query.filter_by(user_id=session['user_id']).all()
    
    # Renderizar la plantilla de registros
    return render_template("records.html") 

@auth_bp.route('/records/new', methods=['GET'])
def new_record():
    # Obtener lista de pacientes para el dropdown
    return render_template('new_record.html')
@auth_bp.route('/patients', methods=['GET'])
def patients():
    from eh_app.models.paciente import Paciente

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    search_query = request.args.get('q', '').lower()

    if search_query:
        pacientes = Paciente.query.filter(
            (Paciente.document_number.ilike(f'%{search_query}%')) |
            (Paciente.first_name.ilike(f'%{search_query}%')) |
            (Paciente.last_name.ilike(f'%{search_query}%'))
        ).all()
    else:
        pacientes = Paciente.query.all()

    return render_template('patients.html', pacientes=pacientes, search_query=search_query)


@auth_bp.route('/patients/new', methods=['GET','POST'])
def new_patient(): 
    from eh_app.models.paciente import Paciente
    

    if "user_id" not in session:
        return redirect("/login")
    if request.method == "POST":
            
        paciente = Paciente(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        document_type=request.form['document_type'],
        document_number=request.form['document_number'],
        birth_date=request.form['birth_date'],
        gender=request.form['gender'],
        email=request.form.get('email', ''),
        phone=request.form['phone'],
        address=request.form.get('address', ''),
        city=request.form.get('city', ''),
        blood_type=request.form.get('blood_type', ''),
        allergies=request.form.get('allergies', ''),
        medical_history=request.form.get('medical_history', ''),
        insurance=request.form.get('insurance', ''),
        occupation=request.form.get('occupation', ''),
        referred_by=request.form.get('referred_by', ''),
        notes=request.form.get('notes', '')
        )

        db.session.add(paciente)
        db.session.commit()

        return redirect('/patients')
    # Aquí puedes agregar lógica para crear un nuevo paciente
    return render_template("new_patient.html")

@auth_bp.route('/patients/<int:paciente_id>', methods=['GET'])
def patient_detail(paciente_id):
    from eh_app.models.paciente import Paciente  # Asegúrate de que el modelo Paciente esté definido correctamente.
    
    # Obtener el paciente o retornar un error 404 si no se encuentra.
    paciente = Paciente.query.get_or_404(paciente_id)
    
    return render_template('patient.html', paciente=paciente)


@auth_bp.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    if user is None:
        return redirect("/login")

    # Desencriptar
    user.decrypt_fields()

    # Extraer campos desencriptados (evita re-acceso desde Jinja)
    user_data = {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "document_number": user.document_number,
        "birth_date": user.birth_date,
        "phone": user.phone,
        "address": user.address,
        "eps": user.eps,
        "blood_type": user.blood_type,
        "allergies": user.allergies,
        "gender": user.gender,
        "role": user.role,
        "two_factor_enabled": user.two_factor_enabled
    }

    return render_template("profile.html", user=user_data)


# eh_app/routes/main.py

@auth_bp.route("/schedule")
def schedule_page():
    if "user_id" not in session:
        return redirect("/login")

    from eh_app.models.user import User
    from eh_app.models.appointment import Appointment

    user = User.query.get(session["user_id"])

    if user.role == "doctor":
        appointments = Appointment.query.filter_by(doctor_id=user.id).all()
    elif user.role == "paciente":
        appointments = Appointment.query.filter_by(patient_id=user.id).all()
    else:  # admin
        appointments = Appointment.query.all()

    # Desencriptar pacientes y doctores para cada cita
    for appt in appointments:
        try:
            if appt.patient:
                appt.patient.decrypt_fields()
            if appt.doctor:
                appt.doctor.decrypt_fields()
        except Exception as e:
            print("[ERROR] Fallo al desencriptar:", e)

    return render_template("schedule.html", user=user, appointments=appointments)



@auth_bp.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():
    if "user_id" not in session:
        return redirect("/login")

    from eh_app.models.user import User

    user = User.query.get(session["user_id"])
    if user is None:
        return redirect("/login")

    if request.method == "POST":
        # Actualizar datos con lo que el usuario envía en el formulario
        user.full_name = request.form["full_name"]
        user.document_number = request.form["document_number"]
        user.address = request.form["address"]
        user.phone = request.form["phone"]
        user.email = request.form["email"]
        user.eps = request.form["eps"]
        user.birth_date = request.form["birth_date"]

        # Encriptar los campos antes de guardar (si aplica)
        user.encrypt_fields()

        # Guardar en la base de datos
        from eh_app import db
        db.session.commit()

        return redirect("/profile")

    # GET: mostrar formulario con los datos actuales
    user.decrypt_fields()
    return render_template("edit_profile.html", user=user)


import datetime

@auth_bp.route('/schedule/new', methods=['GET', 'POST'])
def new_schedule():
    if "user_id" not in session:
        return redirect("/login")

    from eh_app.models.user import User
    from eh_app.models.appointment import Appointment

    # Si el usuario es un administrador o médico, obtener la lista de pacientes y médicos
    patients = User.query.filter_by(role='paciente').all()
    doctors = User.query.filter_by(role='doctor').all()

    # Desencriptar los datos sensibles de pacientes y médicos
    for patient in patients:
        try:
            patient.decrypt_fields()  # Desencriptar campos del paciente
        except Exception as e:
            pass  # Si ocurre un error, los datos se dejan sin desencriptar

    for doctor in doctors:
        try:
            doctor.decrypt_fields()  # Desencriptar campos del médico
        except Exception as e:
            pass  # Si ocurre un error, los datos se dejan sin desencriptar

    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        date_str = request.form['date']
        time_str = request.form['time']
        reason = request.form['reason']

        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.datetime.strptime(time_str, '%H:%M').time()

    # Crear nueva cita
        new_appointment = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            date=date,
            time=time,
            reason=reason
        )
        db.session.add(new_appointment)
        db.session.commit()
        
        return redirect('/schedule')


    return render_template('schedule_new.html', patients=patients, doctors=doctors)


