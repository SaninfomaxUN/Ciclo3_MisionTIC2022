import sqlite3

#try:
#    mi_conexion=sqlite3.connect("db/db_mayordomo")
#except Exception as ex:
#    print(ex) 

#Conectar a la bd
conexion = sqlite3.connect("db_mayordomo.db")

#Seleccionar el cursos para realizar la consulta
consulta = conexion.cursor()

#crear string con la consulta sql
sql = """
CREATE TABLE IF NOT EXISTS empleados(
    numeroId BIGINT PRIMARY KEY NOT NULL,
    tipo TEXT(2) NOT NULL,
    nombre TEXT(40) NOT NULL,
    apellido TEXT(40) NOT NULL,
    rol TEXT(15) NOT NULL,
    direccion TEXT(40) NOT NULL,
    telefono TEXT(10) NOT NULL,
    fechaNacimiento DATE NOT NULL,
    tipoContrato TEXT(10) NOT NULL,
    fechaIngreso DATE NOT NULL,
    cargo TEXT(15) NOT NULL,
    salario REAL(11,2) NOT NULL,
    fechaTerminoContrato DATE,
    dependencia TEXT(15) NOT NULL,
    clave TEXT(40) NOT NULL)"""

#Ejecutar la consulta
if(consulta.execute(sql)): 
    print("Tabla creada a satisfacción")
else:
    print("Falla en la creación")

#Terminar la consulta
consulta.close()

#Guardamos los cambios en la base de datos
conexion.commit()

#Cerramos la conexión a la BD
conexion.close()