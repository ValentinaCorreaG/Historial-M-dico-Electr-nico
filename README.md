# 🏥 EHR Seguro - API y Frontend Web

Una plataforma web segura desarrollada con **Flask** para gestionar **historias clínicas electrónicas** (EHR), diseñada bajo principios de seguridad, privacidad y cumplimiento de normativas como HIPAA.

---

## 🚀 Características principales

### 🔐 Autenticación y Autorización
- Inicio de sesión con autenticación basada en JWT
- Segundo factor de autenticación (2FA) con código enviado por email
- Roles soportados: paciente, médico y administrador

### 📋 Registro de Usuarios
- Formulario amigable y validado con Bootstrap
- Almacenamiento seguro (hash de contraseñas y cifrado de campos sensibles con Fernet AES-256)
- Campos incluidos: nombre, documento, nacimiento, EPS, tipo de sangre, alergias, etc.

### 📦 Cifrado de datos sensibles
- Uso de `cryptography.fernet` para encriptar:
  - Nombre completo
  - Documento
  - Dirección y alergias (si existen)

### 🛡️ Seguridad
- Rate limiting con Flask-Limiter (opcional)
- Validación de inputs
- Separación por Blueprints
- Sistema de logs (implementación sugerida con Loguru)

### 📊 Dashboard dinámico
- Panel estilo médico con Bootstrap 5
- Navegación lateral, tarjetas resumen, y bloque para historia clínica

---
## ✅ Pendientes y mejoras sugeridas

- Asociar usuarios con historias clínicas dinámicas
- Panel para médicos con control de accesos granular
- Exportar PDFs de historias clínicas
- Dashboard por rol (condicional en sesión)

