# 📘 – Inventory Service (Microservicio de Inventario)**

## 📦 **Descripción del proyecto**

Este microservicio forma parte de una arquitectura basada en **eventos**.
Su responsabilidad es administrar el inventario de productos y reaccionar a los eventos provenientes del **Order Service**.

Cuando el Order Service genera una orden, envía un evento a este microservicio para actualizar el stock. El Inventory Service:

* Recibe eventos vía HTTP (event-driven)
* Valida stock disponible
* Actualiza la base de datos de inventario
* Emite logs o eventos de respuesta (StockUpdated, StockInsufficient)

---

# 🏗 **Arquitectura del Microservicio**

```
OrderService  --(POST Event)-->  InventoryService
```

📌 **Este microservicio NO llama a otros.**
📌 **Solo expone un endpoint para recibir eventos.**

---

# 🛢️ **Base de Datos – SQL Server (AWS RDS)**

Este servicio usa una base de datos SQL Server alojada en AWS RDS:

```
Host: servidor-trip.cml202ma0txy.us-east-1.rds.amazonaws.com
Port: 1433
User: admin
Password: martinez1234
```

### Crear la base de datos:

```sql
CREATE DATABASE InventoryDB;
GO
```

### Crear la tabla:

```sql
USE InventoryDB;
GO

CREATE TABLE Product (
    IdProduct INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(200),
    CurrentStock INT
);
GO
```

---

# 🧩 **Tecnologías usadas**

* Python 3
* Django 5
* Django REST Framework
* SQL Server (RDS AWS)
* mssql-django (driver)
* Arquitectura orientada a eventos

---

# 📁 **Estructura del proyecto**

```
Inventory-Service/
│
├── servicio/         # Configuración del proyecto Django
├── inventario/                 # App principal
│   ├── models.py              # Modelo Product
│   ├── views.py               # Endpoints
│   ├── urls.py                # Rutas
│   ├── serializers.py         # Serializadores
│   ├── events.py              # Logs / emisiones de eventos
│
├── requirements.txt
└── README.md
```

---

# ⚙️ **Configuración del entorno**

### 1️⃣ Crear entorno virtual

```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2️⃣ Instalar dependencias

```
pip install -r requirements.txt
```

### 3️⃣ Configurar conexión SQL Server en `settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'InventoryDB',
        'USER': 'admin',
        'PASSWORD': 'martinez1234',
        'HOST': 'servidor-trip.cml202ma0txy.us-east-1.rds.amazonaws.com',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
        },
    }
}
```

---

# 🚀 Ejecutar servidor

```sh
python manage.py runserver
```

---

# 🔥 **Endpoints del microservicio**

## 📌 1. **Recibir evento desde Order Service**

### `POST /inventory/events/order-created/`

#### Body esperado:

```json
{
  "IdProduct": 1,
  "Quantity": 2
}
```

#### Respuestas:

| Estado            | Descripción                          |
| ----------------- | ------------------------------------ |
| `200 OK`          | Stock actualizado                    |
| `400 Bad Request` | Stock insuficiente / datos inválidos |
| `404 Not Found`   | Producto no existe                   |

#### Ejemplo de respuesta exitosa:

```json
{
  "message": "Stock actualizado correctamente"
}
```

---

# 📜 **Eventos emitidos**

Solo se imprimen como logs (simulación de un broker):

```
[EVENT] StockUpdated → product=1, stock=45
[EVENT] StockInsufficient → product=2
```

---

# 🧪 Pruebas con Postman

```
POST http://localhost:8000/inventory/events/order-created/
Body (JSON):
{
  "IdProduct": 1,
  "Quantity": 5
}
```

---

# 🤝 **Integración con Order Service**

Tu compañero debe enviar un POST al endpoint:

```
http://<tu-ip-o-dominio>/inventory/events/order-created/
```

---

# 🧑‍💻 Autor

Jeff Robert — Inventory Service
Arquitectura basada en microservicios y eventos.

¿Quieres que el README incluya imágenes/diagramas?
