# Proyecto-Ingeniería-Web-Backend

## Descripción del proyecto  
Este proyecto constituye el backend de un sistema web desarrollado en el contexto de Ingeniería Web. Su objetivo es gestionar la lógica de negocio, persistencia de datos y exposición de servicios para una aplicación web que permite gestionar la administración de empleados en un parque de atracciones generando reportes relevantes para su administració.  
La arquitectura se basa en un enfoque MVC y está preparado para integrarse con un frontend desarrollado en con React Typescript y una base de datos relacional MSSSQL.

## Tecnologías utilizadas  
- Lenguaje de programación: Python (como se aprecia en los archivos)  
- Framework principal: FastAPI  
- ORM/Persistencia: aiodbc  
- Base de datos relacional: MSSQL  
- Controladores / Lógica de negocio: carpeta `Controllers`, `Managers`  
- Modelado de entidades: carpeta `Models`    

## Instalación y configuración  
1. Clona el repositorio:  
   ```bash
   git clone https://github.com/Pblackberry/Proyecto-Ingenieria-Web-Backend.git
   cd Proyecto-Ingenieria-Web-Backend
2. Crea y activa un entorno virtual (recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # para Linux/macOS  
   venv\Scripts\activate      # para Windows   
3. Instala las dependencias con pip install
4. Levanta la aplicación
   ```bash
   python main.py
## Estructura del proyecto
Proyecto-Ingenieria-Web-Backend/
- Controllers/             Lógica de los endpoints / APIs
- Managers/                Lógica de negocio / servicios
- Models/                  Entidades del dominio 
- main.py                  Punto de entrada de la aplicación
- .gitignore
- README.md                Este archivo
