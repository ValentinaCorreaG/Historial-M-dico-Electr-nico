import smtplib

EMAIL = "ehrsystem9@gmail.com"
PASSWORD = "bnyb pqmj rjhc kzgh"

try:
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(EMAIL, PASSWORD)
    print("[OK] Conexión SMTP exitosa ✅")
    s.quit()
except Exception as e:
    print("[ERROR] No se pudo conectar:", e)
