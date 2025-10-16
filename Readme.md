# 📦 API de Números con JWT

API REST construida con **FastAPI** para autenticación JWT y gestión de números.

---

## 🚀 Requisitos

- [Docker]

---

## 📥 Instalación y ejecución

1. Clona este repositorio:

```bash
git clone https://github.com/MayLuna23/backend-mongo.git
cd backend-mongo
```

2. Inicia los servicios con Docker Compose:

```bash
docker-compose up -d
```

Esto levantará la API con FastAPI, la Base de datos MongoDB y
la interfaz grafica Mongo Express en segundo plano.

### Swagger ###
Una vez iniciada la API esta corre en el puerto 8080,
puedes acceder a la documentación desde tu navegador:

Swagger UI: http://localhost:8080/docs

En el endpoint  /numbers se incluye el id de los documentos para facilitar luego
el consumo del endpoint /numbers/{number_id}

### Mongo Express ###
Para navegar en la base de datos a traves de la UI puedes hacerlo desde
http://localhost:8081
username_db: admin
password_db: admin123

Se incluye el .env para fines de prueba