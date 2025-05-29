from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import io

def crear_pdf_historia_clinica(paciente, historias):
    # 1. Crear PDF sin contraseña en memoria
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    text = c.beginText(40, 750)

    text.setFont("Helvetica", 12)
    text.textLine(f"Historia Clínica - {paciente.first_name} {paciente.last_name}")
    text.textLine(f"Documento: {paciente.document_type} {paciente.document_number}")
    text.textLine("")

    for historia in historias:
        text.textLine(f"Fecha: {historia.record_date}")
        text.textLine(f"Motivo: {historia.reason}")
        text.textLine(f"Presión arterial: {historia.blood_pressure}")
        text.textLine(f"Frecuencia cardíaca: {historia.heart_rate}")
        text.textLine(f"Temperatura: {historia.temperature}")
        text.textLine(f"Saturación de oxígeno: {historia.oxygen_saturation}")
        text.textLine(f"Diagnóstico: {historia.diagnosis}")
        text.textLine(f"Tratamiento: {historia.treatment}")
        if historia.medications:
            meds = ', '.join(
                f"{med.get('nombre', 'Sin nombre')} ({med.get('dosis', 'Sin dosis')})"
                for med in historia.medications
            )
            text.textLine(f"Medicamentos: {meds}")
        else:
            text.textLine("Medicamentos: N/A")
        text.textLine(f"Observaciones: {historia.observations}")
        text.textLine("-" * 80)

    c.drawText(text)
    c.showPage()
    c.save()

    buffer.seek(0)

    # 2. Cifrar con PyPDF2
    reader = PdfReader(buffer)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    # Contraseña = número de documento
    password = paciente.document_number
    writer.encrypt(user_password=password, owner_password=None, use_128bit=True)

    output_buffer = io.BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)

    return output_buffer
