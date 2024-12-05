primer paso
arquitectura del proyecto

Que vamos hacer¿
Proyecto completo de mi portafolio hecho en 
Django Python Mysql Sqlite3 MysqlAlchemyORM Postgresql MongoDB FirebaseGoogle

aplicacion 1: portafolio No contiene base de datos
    Mi pagina principal
    Mi pagina de proyectos

apliacion 2: condominios  ORM DJANGO sql
    Pagina INDEX:
        En el portafolio Menu de herramientas de los condominios
            Usuario para cada casa del condominios propietarios
                Prodrán_: 
                    Registrar Una visita diaria 
                        (se elimina cada 12media noche)
                        Actualizar la visita - Eliminar la visita -  Ver mis visitas
                    
                    Registrar sus automóviles y mascotas (Editarlos, eliminarlos)
                    Registrar integrantes permanentes (Editarlos, eliminarlos)
    
    Base de datos: condominios
        Tablas: UsuarioDjango, PerfilUsername, VisitaUsername, MascotasUsername, AutosUsername

            PerfilUsername: ( Username - integrantesPermanentes - placasPermanentes )
            VisitaUsername: ( Username - Personas - Placas - FechaCreada - Eliminada)
            MascotasUsername: ( Username - Foto - Nombre - Caracteristicas )
            AutosUsername: ( Username - Foto - Placa - Caracteristicas )

    Cascada:

        Servidor
            portafolio
                conectar paginas urls 
            condominios
                general el sistema de login con django por derecto
                    pero aun asi deber crear las carpetas de los templates que django busca por defecto
                    En la documentacion oficial estan los pasos
                
                crear models en la base de datos
                crear nueva visita, editarla, eliminarla, verla, y ver todas


#se realiza commit sistema logged realizado y pagina web personal y proyectos 21112024:8.50pm
#se realiza version condominio terminado solo queda la esterica 22112024 10am



    Aplicacion 2 Oficiales:  23112024
        (deben estar logeados con su usuario , en el proyecto general estan
         logeados general a todas las aplicaciones registradas en el proyecto)
            
        Ver todas las visitas diarias registradas
        Ver todos los usuarios permanentes
        Ver todos los automoviles
        Ver todas las mascotas
        
        Ver los reportes
        realizar comentario a los reportes

        realizar entrada con qr del celular de la empresa, valido por 4 horas
        realizar salida

        
            FALTA CLEAN CODE 
            USO D BASE DE DATOS DEL Condominios
            USO D BASE DE DATOS DE los oficiales

