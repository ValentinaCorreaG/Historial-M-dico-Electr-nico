from flask_mail import Message
from flask import current_app
from eh_app import mail

def enviar_codigo(destinatario, codigo):
    try:
        mail_user = current_app.config.get("MAIL_USERNAME")
        mail_pass = current_app.config.get("MAIL_PASSWORD")

        if not mail_user or not mail_pass:
            print("[ERROR] MAIL_USERNAME o MAIL_PASSWORD no están cargados correctamente")
            return

        print("[DEBUG] Enviando código a:", destinatario)
        print("[DEBUG] Usando cuenta:", mail_user)

        msg = Message(
            subject="Tu código de verificación - EHR",
            sender=mail_user,
            recipients=[destinatario],
            body=f"Hola 👋\n\nTu código de verificación es: {codigo}\n\nNo lo compartas con nadie.\n"
        )

        mail.send(msg)
        print("[✅] Correo enviado correctamente")

    except Exception as e:
        print("[❌ ERROR] Falló el envío de email:", e)
