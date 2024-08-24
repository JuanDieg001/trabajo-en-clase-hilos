from accessData.conexion import Database
from accessData.entities.models import Estudiante
from dominio.modelsDto import EstudianteDto
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

class EstudianteService:
    
    def __init__(self, database: Database):
        self.db = database
        
    def create_student(self, est: EstudianteDto):
        session = self.db.get_session()
        db_estudiante = Estudiante(nombre = est.nombre, apellido = est.apellido, edad = est.edad, mail = est.mail, matricula = est.matricula, carrera = est.carrera)
        session.add(db_estudiante)
        session.commit()
        session.refresh(db_estudiante)
        session.close()
        return db_estudiante

    def get_student_all(self):
        session = self.db.get_session()
        personas = session.query(Estudiante).all()
        session.close()
        return personas


    def get_student(self, person_id):
        session = self.db.get_session()
        person = session.query(Estudiante).filter(Estudiante.id == person_id).first()
        session.close()
        return person


    def update_student(self, est: EstudianteDto):
        session = self.db.get_session()
        estudiante = session.query(Estudiante).filter(Estudiante.id == est.id).first()
        if est.nombre:
            estudiante.nombre = est.nombre
        if est.apellido:
            estudiante.apellido = est.apellido
        if est.edad:
            estudiante.edad = est.edad
        if est.mail:
            estudiante.mail = est.mail
        session.commit()
        session.refresh(estudiante)
        session.close()
        return estudiante


    def delete_person(self, person_id):
        session = self.db.get_session()
        person = session.query(Estudiante).filter(Estudiante.id == person_id).first()
        session.delete(person)
        session.commit()
        session.close()
        return {"message": "Deleted successfully"}
    

    def cerrarConexion(self):
        session = self.db.get_session()
        session.close()


    def cargar_estudiantes_desde_txt(self, ruta_archivo):
        try:
            with open(ruta_archivo, 'r') as file:
                inicio = datetime.now()
                print(f"Iniciando la carga masiva: {inicio}")
                for linea in file:
                    nombre, apellido, edad, mail, matricula, carrera = linea.strip().split(',')
                    #estudiateArchivo = linea.strip().split(',')
                    #print(estudiateArchivo)
                    estudiante = Estudiante(nombre = nombre, apellido = apellido, edad = int(edad), mail = mail, matricula = matricula, carrera = carrera)
                    self.create_student(estudiante)
            fin = datetime.now()
            print(f"Finalizando la carga masiva: {fin}")
            tiempo_total = fin - inicio
            print(f"Tiempo total de inserción: {tiempo_total}")
            print("Carga masiva de estudiantes completada exitosamente.")
        except Exception as e:
            print(f"Error al cargar estudiantes desde el archivo: {e}")

    def cargar_estudiantes_desde_txt_hilos(self, ruta_archivo, num_hilos=10):
        try:
            inicio = datetime.now()
            print(f"Iniciando la carga masiva hilos: {inicio}")
            with open(ruta_archivo, 'r') as file:
                lineas = file.readlines()
                
            """
            bloques = []
            for i in range(num_hilos):
                # Crear un bloque con líneas que corresponden al hilo `i`
                bloque = lineas[i::num_hilos]
                bloques.append(bloque)
            """
            # Dividir las líneas en bloques para cada hilo
            bloques = [lineas[i::num_hilos] for i in range(num_hilos)]
            print(bloques.count)

            # Usar ThreadPoolExecutor para manejar los hilos
            with ThreadPoolExecutor(max_workers=num_hilos) as executor:
                for bloque in bloques:
                    executor.submit(self._procesar_bloque, bloque)
            
            fin = datetime.now()
            print(f"Finalizando la carga masiva hilos: {fin}")
            tiempo_total = fin - inicio
            print(f"Tiempo total de inserción: {tiempo_total}")
            print("Carga masiva de estudiantes completada exitosamente.")
        except Exception as e:
            print(f"Error al cargar estudiantes desde el archivo: {e}")

    def _procesar_bloque(self, bloque):
        session = self.db.get_session()
        try:
            for linea in bloque:
                nombre, apellido, edad, mail, matricula, carrera = linea.strip().split(',')
                estudiante = Estudiante(nombre=nombre, apellido=apellido, edad=int(edad), mail=mail, matricula=matricula, carrera=carrera)
                session.add(estudiante)

            session.commit()  # Hacer commit una vez por bloque
        except Exception as e:
            print(f"Error al procesar el bloque: {e}")
            session.rollback()
        finally:
            session.close()