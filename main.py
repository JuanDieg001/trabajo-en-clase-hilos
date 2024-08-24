from accessData.conexion import Database, DATABASE_URL
from accessData.entities.models import BaseDeDatos, Estudiante
from dominio.modelsDto import EstudianteDto
from services.estudianteService import EstudianteService
from services.genericService import GenericRepository


def mostrar_estudiante(estudiantes):
    for est in estudiantes:
        print(vars(est))


def main():
    #implentar servicio para consumir estudiante
    estudianteService = EstudianteService(db)
    serviceGeneric = GenericRepository[Estudiante](Estudiante, db)

    while True:
        print("\n--- MENU ---")
        print("1. Crear estudiante")
        print("2. Mostrar todos estudiantes")
        print("3. Mostrar estudiante")
        print("4. Actualizar estudiante")
        print("5. Eliminar estudiante")
        print("6. Carga masiva estudiante")
        print("7. aquì")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre: ")
            apellido = input("Ingrese el apellido: ")
            edad = int(input("Ingrese la edad: "))
            mail = input("Ingrese el correo electrónico: ")
            matricula = input("Ingrese la matricula: ")
            carrera = input("Ingrese la carrera: ")

            student = EstudianteDto(None, nombre, apellido, edad, mail, matricula, carrera)
            
            #estudianteService.create_student(student)
            student = serviceGeneric.create(nombre=student.nombre, apellido=student.apellido, 
                                            edad=student.edad, mail=student.mail, 
                                            matricula = student.matricula, 
                                            carrera = student.carrera)
            print(vars(student))


        elif opcion == "2":
            #estudiante = estudianteService.get_student_all()
            estudiante = serviceGeneric.getAll()
            mostrar_estudiante(estudiante)

        elif opcion == "3":
            estudianteId = int(input("Ingrese el ID del estudiante a consultar: "))
            #estudiante = estudianteService.get_student(estudianteId)
            student = serviceGeneric.get(estudianteId)
            print(vars(student))


        elif opcion == "4":
            id_persona = int(input("Ingrese el ID de la estudiante que desea actualizar: "))
            nombre = input("Ingrese el nuevo nombre: ")
            apellido = input("Ingrese el nuevo apellido: ")
            edad = int(input("Ingrese la nueva edad: "))
            mail = input("Ingrese el nuevo correo electrónico: ")
            matricula = input("Ingrese la matricula: ")
            carrera = input("Ingrese la carrera: ")
            student = EstudianteDto(id_persona, nombre, apellido, edad, mail, matricula, carrera)
            #estudianteService.update_student(student)
            serviceGeneric.update(id_persona, student)
            print("Estudiante actualizado")
            
        elif opcion == "5":
            estudianteId = int(input("Ingrese el ID de la persona que desea eliminar: "))
            #estudianteService.delete_person(estudianteId)
            serviceGeneric.delete(estudianteId)
            print("Estudiante borrado de la basde de datos")

        elif opcion == "6":
            #implementar otra clase servicio que lea el archivo txt 
            # y se recorra cada registro y lo guarde en la base de datos
            archivo = "estudiantes.txt"
            estudianteService.cargar_estudiantes_desde_txt(archivo)
            
        
        elif opcion == "7":
            archivo = "estudiantes.txt"
            estudianteService.cargar_estudiantes_desde_txt_hilos(archivo)
            

        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")



if __name__ == "__main__":
    db = Database(DATABASE_URL)
    engine = db.engine
    BaseDeDatos.metadata.create_all(bind=engine)
    main()
    