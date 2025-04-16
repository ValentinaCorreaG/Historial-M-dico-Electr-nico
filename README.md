# 🏥 API Segura para Gestión de Historial Médico Electrónico (EHR)

Una API RESTful segura para la gestión de historiales médicos electrónicos, diseñada con un enfoque en la **seguridad**, la **privacidad del paciente** y el **cumplimiento de normativas como HIPAA**. Soporta distintos roles de usuario (pacientes, médicos, administradores) y permite controlar el acceso a la información médica de forma granular.

---

## 🚀 Características

- 🔐 **Autenticación y Autorización**
  - Implementación de OAuth2 con JWT
  - Control de roles: Pacientes, Médicos y Administradores

- 🧩 **Sistema de Permisos Granulares**
  - Los médicos solo acceden a los registros autorizados
  - Administradores con privilegios extendidos

- 🔒 **Cifrado de Datos**
  - Cifrado simétrico con AES-256 o Fernet para proteger información sensible

- 📜 **Registro de Accesos (Auditoría)**
  - Logs detallados de accesos y modificaciones a datos

- 🛡️ **Protección contra Ataques**
  - Rate limiting
  - Validación y sanitización de inputs
  - Prevención de ataques comunes como inyección SQL, XSS, etc.

---

## 🧰 Tecnologías Utilizadas

- Python 3.11+
- [FastAPI](https://fastapi.tiangolo.com/) 
- PostgreSQL 
- OAuth2 + JWT (via `fastapi.security`)
- `cryptography` (AES / Fernet)
- `uvicorn` para servidor ASGI
- `slowapi` para rate limiting (opcional)
- `loguru` para logging detallado

---

## ⚙️ Instalación

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/secure-ehr-api.git
   cd secure-ehr-api
