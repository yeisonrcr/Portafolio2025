# 🚀 Proyecto Completo de Mi Portafolio

¡Bienvenidos a mi proyecto de portafolio 2024! 
🌟Este proyecto está construido con una variedad de tecnologías, incluyendo Django y Flask - Python, MySQL, SQLite3, entre otras. 📚🌐

## 🎯 Primer Paso: Arquitectura del Proyecto

### 🏗️ ¿Qué Vamos a Hacer?
Un portafolio completo que incluye múltiples aplicaciones.

### 🗂️ Aplicación 1: Portafolio
- **Descripción**: Esta aplicación no contiene base de datos. Es simplemente mi página principal y mi página de proyectos.
  - 📄 **Mi página principal**
  - 📄 **Mi página de proyectos**

### 🏢 Aplicación 2: Condominios (Usando ORM de Django con SQL)
- **Página INDEX**:
  - En el portafolio, un menú de herramientas para condominios:
    - Usuarios para cada casa del condominio (propietarios) podrán:
      - Registrar una visita diaria (se elimina cada medianoche)
      - Actualizar, eliminar y ver sus visitas
      - Registrar, editar y eliminar sus automóviles y mascotas
      - Registrar, editar y eliminar integrantes permanentes

- **Base de Datos**: condominios
  - **Tablas**:
    - `UsuarioDjango`
    - `PerfilUsername`
    - `VisitaUsername`
    - `MascotasUsername`
    - `AutosUsername`
  - **Campos**:
    - `PerfilUsername`: (Username, integrantesPermanentes, placasPermanentes)
    - `VisitaUsername`: (Username, Personas, Placas, FechaCreada, Eliminada)
    - `MascotasUsername`: (Username, Foto, Nombre, Características)
    - `AutosUsername`: (Username, Foto, Placa, Características)

- **Cascada**:
  - **Servidor**:
    - **Portafolio**:
      - Conectar páginas urls
    - **Condominios**:
      - General el sistema de login con Django por defecto
      - Crear carpetas de templates que Django busca por defecto
      - Crear models en la base de datos
      - Crear nueva visita, editarla, eliminarla y verla

### 🏢 Aplicación 3: Oficiales (Usando base de datos del condominio)
- Ver todas las visitas diarias registradas
- Ver todos los usuarios permanentes
- Ver todos los automóviles
- Ver todas las mascotas
- Ver reportes y realizar comentarios
- Realizar entrada con QR del celular de la empresa, válido por 4 horas
- Realizar salida

### 🛠 Actualización Diciembre 2025
- Configuración del proyecto para uso de MySQL, Gestor MySQL WorkBench o XAMMP Php
  
![image](https://github.com/user-attachments/assets/fcae26db-97f0-4d99-a6c6-7f56e32a502e)

### 🛒 Aplicación 4: Ecommerce
- Tiendas con productos y relaciones
- Solo usuarios root pueden crear tiendas y agregar productos
- Carrito de productos por tienda, cada carrito tiene productos de una única tienda y se elimina automáticamente cuando está vacío

### 🏥 Aplicación 5: Control de Consulta

### 📝 Aplicación 6: Blog Personal

### 📝 Otras...
