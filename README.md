# Sistema de Autenticación con Docker y Python

Prototipo de sistema de autenticación con arquitectura de microservicios usando Docker, Python, Flask, JWT y SQLite.

## 📁 Estructura de Archivos

```
app-prototipo-py/
├── docker-compose.yml          # Orquestación de contenedores
├── run_tests.py               # Script de pruebas automáticas
├── README.md                  # Documentación
├── database/                  # Contenedor de base de datos
│   ├── Dockerfile            # Imagen Docker para BD
│   ├── requirements.txt      # Dependencias Python
│   └── init_db.py           # Inicialización de BD (Python)
├── backend/                   # API REST Backend
│   ├── Dockerfile            # Imagen Docker para backend
│   ├── requirements.txt      # Dependencias Flask/JWT
│   └── app.py               # API Flask (Python)
├── frontend/                  # Interfaz web
│   ├── Dockerfile            # Imagen Docker para frontend
│   ├── requirements.txt      # Dependencias Flask
│   ├── app.py               # Servidor web Flask (Python)
│   └── templates/            # Plantillas HTML
│       ├── login.html        # Página de login (HTML/CSS)
│       └── dashboard.html    # Dashboard (HTML/CSS)
└── tests/                     # Pruebas automáticas
    ├── requirements.txt      # Dependencias pytest
    ├── test_unit.py         # Pruebas unitarias (Python)
    └── test_integration.py  # Pruebas integración (Python)
```

## 🔧 Explicación de Archivos

### Configuración
- **docker-compose.yml**: Orquesta 3 servicios (database, backend, frontend) con red compartida
- **run_tests.py**: Script Python para ejecutar pruebas automáticas con pytest

### Base de Datos (Python)
- **database/init_db.py**: Crea BD SQLite con tabla users y 3 usuarios de prueba
- **database/Dockerfile**: Imagen Python slim para contenedor de BD

### Backend (Python - Flask)
- **backend/app.py**: API REST con Flask que maneja:
  - Login con validación de credenciales
  - Generación y verificación de tokens JWT
  - Endpoints para recursos según rol de usuario
  - Refresh de tokens
- **backend/Dockerfile**: Imagen Python con Flask, CORS y PyJWT

### Frontend (Python - Flask + HTML)
- **frontend/app.py**: Servidor web Flask que sirve interfaz HTML
- **frontend/templates/login.html**: Formulario de login con CSS básico
- **frontend/templates/dashboard.html**: Dashboard con recursos según rol
- **frontend/Dockerfile**: Imagen Python con Flask y requests

### Pruebas (Python - Pytest)
- **tests/test_unit.py**: Pruebas unitarias de funciones de hash, JWT
- **tests/test_integration.py**: Pruebas de endpoints, roles, tokens

## 🚀 Instrucciones para Implementar

### Prerrequisitos
- Docker y Docker Compose instalados
- Puertos 3000 y 5000 disponibles

### Pasos de Instalación

1. **Clonar/Descargar el proyecto**
```bash
cd /ruta/del/proyecto
```

2. **Construir y ejecutar contenedores**
```bash
docker-compose up --build
```

3. **Verificar servicios**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Base de datos: Volumen compartido entre contenedores

### Acceso desde otros equipos
El frontend es accesible desde otros equipos en la red usando:
```
http://[IP_DEL_HOST]:3000
```

## 🧪 Pruebas Manuales Básicas

### 1. Prueba de Login
1. Abrir http://localhost:3000
2. Usar credenciales de prueba:
   - **Admin**: admin / admin123
   - **Usuario**: user / user123  
   - **Invitado**: guest / guest123
3. Verificar redirección al dashboard

### 2. Prueba de Roles
- **Admin**: Ve 4 recursos (Dashboard Admin, Gestión Usuarios, etc.)
- **User**: Ve 3 recursos (Dashboard Usuario, Mi Perfil, etc.)
- **Guest**: Ve 1 recurso (Vista Pública)

### 3. Prueba de Sesión
1. Cerrar sesión con botón "Cerrar Sesión"
2. Verificar redirección a login
3. Intentar acceder a /dashboard sin login (debe redirigir)

## 🔬 Listado de Pruebas Automáticas

### Pruebas Unitarias (test_unit.py)
- `test_hash_password`: Validación de función hash SHA256
- `test_generate_token`: Generación correcta de JWT
- `test_verify_token_valid`: Verificación de token válido
- `test_verify_token_invalid`: Rechazo de token inválido
- `test_password_consistency`: Consistencia en hashing

### Pruebas de Integración (test_integration.py)
- `test_login_admin_success`: Login exitoso admin
- `test_login_user_success`: Login exitoso usuario
- `test_login_guest_success`: Login exitoso invitado
- `test_login_invalid_credentials`: Rechazo credenciales inválidas
- `test_resources_admin`: Acceso recursos admin (4 recursos)
- `test_resources_user`: Acceso recursos user (3 recursos)
- `test_resources_guest`: Acceso recursos guest (1 recurso)
- `test_resources_without_token`: Rechazo sin token
- `test_resources_invalid_token`: Rechazo token inválido
- `test_token_refresh`: Funcionalidad refresh token
- `test_frontend_accessibility`: Accesibilidad del frontend

## 🧪 Pruebas Manuales Detalladas

### Login y Cookies
1. **Abrir herramientas de desarrollador** (F12)
2. **Ir a pestaña Network** y hacer login
3. **Verificar**: Petición POST a /login con credenciales
4. **Ir a pestaña Application/Storage** 
5. **Verificar**: Cookie de sesión Flask almacenada

### JWT Tokens
1. **Usar herramienta como Postman o curl**:
```bash
# Login para obtener token
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Usar token para acceder recursos
curl -X GET http://localhost:5000/resources \
  -H "Authorization: Bearer [TOKEN_OBTENIDO]"
```

### Roles y Permisos
1. **Login como cada rol** y verificar recursos mostrados
2. **Inspeccionar respuesta JSON** del endpoint /resources
3. **Verificar diferencias** en cantidad y tipo de recursos

### Refresh Token
```bash
# Refresh token existente
curl -X POST http://localhost:5000/refresh \
  -H "Authorization: Bearer [TOKEN_ACTUAL]"
```

## ⚡ Ejecutar Pruebas Automáticas

### Opción 1: Script Automático (Recomendado)
```bash
# Asegurar que los contenedores estén ejecutándose
docker-compose up -d

# Ejecutar todas las pruebas
python run_tests.py
```

### Opción 2: Pytest Manual
```bash
# Instalar dependencias
cd tests
pip install -r requirements.txt

# Ejecutar pruebas unitarias
pytest test_unit.py -v

# Ejecutar pruebas de integración  
pytest test_integration.py -v

# Ejecutar todas las pruebas
pytest -v
```

### Opción 3: Dentro de Docker
```bash
# Crear contenedor temporal para pruebas
docker run --rm --network app-prototipo-py_auth_network \
  -v $(pwd)/tests:/tests \
  python:3.11-slim \
  bash -c "cd /tests && pip install -r requirements.txt && pytest -v"
```

## 🔧 Comandos Útiles

### Gestión de Contenedores
```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar servicios
docker-compose down

# Reconstruir imágenes
docker-compose up --build

# Limpiar volúmenes
docker-compose down -v
```

### Debugging
```bash
# Acceder a contenedor de BD
docker exec -it auth_db bash

# Acceder a contenedor backend
docker exec -it auth_backend bash

# Ver base de datos
docker exec -it auth_db sqlite3 /app/data/auth.db ".tables"
```

## 🛡️ Características de Seguridad

- **Passwords hasheados** con SHA256
- **Tokens JWT** con expiración (1 hora)
- **Validación de tokens** en cada petición protegida
- **Separación de servicios** en contenedores
- **Red interna** Docker para comunicación entre servicios

## 📋 Usuarios de Prueba

| Usuario | Contraseña | Rol   | Recursos |
|---------|------------|-------|----------|
| admin   | admin123   | admin | 4 recursos |
| user    | user123    | user  | 3 recursos |
| guest   | guest123   | guest | 1 recurso |