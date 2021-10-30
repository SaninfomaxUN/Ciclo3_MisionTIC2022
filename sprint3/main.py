from sqlite3.dbapi2 import Cursor
from flask import Flask, request
from flask import render_template,url_for,redirect, session, flash
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
import random


app = Flask(__name__)
app.secret_key = "asdfghjklñ"
app.config['UPLOAD_FOLDER'] = './static/assets/img/Perfil'

@app.route("/",methods=['GET','POST'])
def redireccionar(palabra=None):
    # try:
    #     sql = """
    #             CREATE TABLE IF NOT EXISTS empleados(
    #                 numeroId BIGINT PRIMARY KEY NOT NULL,
    #                 tipo TEXT(2) NOT NULL,
    #                 nombre TEXT(40) NOT NULL,
    #                 apellido TEXT(40) NOT NULL,
    #                 rol TEXT(15) NOT NULL,
    #                 direccion TEXT(40) NOT NULL,
    #                 telefono TEXT(10) NOT NULL,
    #                 fechaNacimiento DATE NOT NULL,
    #                 tipoContrato TEXT(10) NOT NULL,
    #                 fechaIngreso DATE NOT NULL,
    #                 cargo TEXT(15) NOT NULL,
    #                 salario REAL(11,2) NOT NULL,
    #                 fechaTerminoContrato DATE,
    #                 dependencia TEXT(15) NOT NULL,
    #                 clave TEXT(40) NOT NULL)
    #             """
    #     if(consulta.execute(sql)):
    #         print("Tabla creada a satisfacción")
    #     else:
    #         print("Falla en la creación")
    #     conexion.commit()
    # except Error as e:
    #     print(e)
    # finally:
    #     if conexion:
    #         consulta.close()
    # try:
    #     conexion_2 = sqlite3.connect("db/db_mayordomo.db")
    #     consulta_2 = conexion.cursor()
    #     sql_2 = """
    #             CREATE TABLE IF NOT EXISTS retroalimentaciones (
    #                 numeroId          BIGINT     REFERENCES empleados (numeroId)
    #                                              NOT NULL,
    #                 retroalimentacion TEXT (500) NOT NULL
    #             );
    #             """
    #     if(consulta_2.execute(sql_2)):
    #         print("Tabla creada a satisfacción")
    #     else:
    #         print("Falla en la creación")
    #     conexion_2.commit()
    # except Error as e:
    #     print(e)
    # finally:
    #     if conexion_2:
    #         consulta_2.close()
    return redirect(url_for("login"))

@app.route("/<palabra>",methods=['GET','POST'])
def redireccionarLogin(palabra=None):
    return redirect(url_for("login"))

@app.route("/admin/<palabra>",methods=['GET','POST'])
def redireccionarDashAdmin(palabra=None):
    return redirect(url_for("dashboard"))

@app.route("/empleado/<palabra>",methods=['GET','POST'])
def redireccionarDashEmpleado(palabra=None):
    return redirect(url_for("dashboardEmpleado"))

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        print("POST")
        username = request.form['username']
        print(username)
        password = request.form['password']

        with sqlite3.connect('db/db_mayordomo.db') as console:
            print("Conectado")
            cursor = console.cursor()
            data = cursor.execute("SELECT * from empleados where numeroId = ?", (username,)).fetchone()
            print(data[14])
            if data == None:
                print("No existe el usuario")
                return redirect(url_for("login"))
            elif check_password_hash(data[14], password) == True:
                session['ID'] = username
                session['rol'] = data[4]
                print("sesion creada con exito " + "rol: " + session['rol'] + " " + "ID: " + session['ID'])
                print("loggin success")
                if session['rol'] == "SuperAdmin":
                    return redirect(url_for("seleccionarRol"))
                elif session['rol'] == "Admin":
                    return redirect(url_for("dashboard"))
                else:
                    return redirect(url_for("dashboardEmpleado"))
            else:
                print("usuario o contraseña incorrecto")
                return redirect(url_for("login"))
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/seleccionarRol",methods=['GET','POST'])
def seleccionarRol():
    if 'rol' in session:
        if session['rol'] == "SuperAdmin":
            return render_template('dashboardRol.html')
        else:
            return redirect(url_for('accesoDenegado'))
    else:
        return redirect(url_for("login"))

@app.route('/empleado/retroalimentacion',methods=['GET'])
def retroalimentacion():
    if 'rol' in session:
        if session['rol'] == "SuperAdmin" or session['rol'] == "Empleado":
            title = "Retroaliemntacion"
            if request.method == "POST":
                try:
                    w_numeroId = int(request.form["numeroId"])
                    w_retro = request.form["contenido"]
                    with sqlite3.connect("db/db_mayordomo.db") as console:
                        cursor = console.cursor()
                        statement = "UPDATE retroalimentaciones set retroalimentacion=? WHERE numeroId=?"
                        cursor.execute(statement, (w_retro, w_numeroId))
                        console.commit()
                #               La retroalimentación se pudo actualizar
                except:
                    console.rollback()
                #            La retroalimentación no se pudo guardar
                finally:
                    console.close()
            return render_template('retroalimentacion.html', title = title, nombrePag="Retroalimentación", nombreIcono="fas fa-chart-bar")
        else:
            return redirect(url_for('accesoDenegado'))
    else:
        return redirect(url_for("login"))


@app.route('/empleado/')
def dashboardEmpleado():
    if 'rol' in session:
        if session['rol'] == "SuperAdmin" or session['rol'] == "Empleado":
            title = "Dashboard - Empleado"
            return render_template('dashboardEmpleado.html', title = title, nombrePag="Dashboard", nombreIcono="fas fa-clipboard-list")
        else:
            return redirect(url_for('accesoDenegado'))
    else:
        return redirect(url_for("login"))


@app.route('/admin/',methods=['GET','POST'])
def dashboard():
    if 'rol' in session:
        if 'ID' in session and session['rol'] == "Admin" or session['rol'] == "SuperAdmin":
            title = "Dashboard"
            return render_template('dashboard.html', title = title, nombrePag="Dashboard", nombreIcono="fas fa-clipboard-list")
        else:
            return redirect(url_for('accesoDenegado'))
    else:
        return redirect(url_for("login"))

@app.route('/admin/buscarEmpleado',methods=['GET','POST'])
def buscarEmpleado():
    if 'rol' in session:
        if 'ID' in session and session['rol'] == "Admin" or session['rol'] == "SuperAdmin":
            print("entre a buscar")
            if request.method == "POST":
                try:
                    print("entre a buscar")
                    w_numeroId=request.form["numeroId"]
                    print(w_numeroId)
                    with sqlite3.connect("db/db_mayordomo.db") as console:
                        console.row_factory = sqlite3.Row
                        cursor=console.cursor()
                        cursor.execute("SELECT * from empleados where numeroId = ?",(w_numeroId,))
                        rows=cursor.fetchall()
                        return render_template("buscarEmpleado.html",rows=rows) 
                except:
                    print("Registro no encontrado en la BD")
                finally:
                    print("Conexion cerrada")
                    console.close()

            title = "Buscar Empleado"
            return render_template('buscarEmpleado.html', title = title, nombrePag="Buscar Empleado", nombreIcono="fas fa-search")
        else:
            return redirect(url_for('accesoDenegado'))
    else:
        return redirect(url_for("login"))

@app.route('/admin/gestionarRetroalimentacion',methods=['GET','POST'])
def gestionarRetro():
    if 'rol' in session:
        if 'ID' in session and session['rol'] == "Admin" or session['rol'] == "SuperAdmin":
            title = "Gestionar Retroalimentación"
            return render_template('gestionarRetro.html', title = title, nombrePag="Gestionar Retroalimentación", nombreIcono="fas fa-search")
        else:
            return redirect(url_for('accesoDenegado'))
    else:
        return redirect(url_for("login"))

@app.route('/admin/crearEmpleado',methods=['GET','POST'])
def crearEmpleado():
    if 'rol' in session:
        if 'ID' in session and session['rol'] == "Admin" or session['rol'] == "SuperAdmin":
            title = "Crear Empleado"
            w_numeroId = "";
            w_tipo="";
            msg = ""
            if request.method == "POST":
                try:
                    minus="abcdefghijklmnopqrstuvwxyz"
                    mayus=minus.upper()
                    numeros="0123456789"
                    simbolos="@(){}[]*.;:-_¿?|!¡><*/+%=,"
                    base=minus+mayus+numeros+simbolos
                    longitud=10
                    muestra=random.sample(base,longitud)
                    password="".join(muestra)
                    pass_salt = "H*%+L*d.:c"+password
                    password_cifrado=generate_password_hash(pass_salt)

                    w_numeroId=request.form["numeroId"]
                    w_tipo=request.form["tipo"]
                    w_nombre=request.form["nombre"]
                    w_apellido=request.form["apellido"]
                    w_direccion=request.form["direccion"]
                    w_telefono=request.form["telefono"]
                    w_fechaNacimiento=request.form["fechaNacimiento"]
                    w_tipoContrato=request.form["tipoContrato"]
                    w_fechaIngreso=request.form["fechaIngreso"]
                    w_cargo=request.form["cargo"]
                    w_rol = request.form["rol"]
                    w_salario=request.form["salario"]
                    w_fechaTerminoContrato=request.form["fechaTerminoContrato"]
                    w_dependencia=request.form["dependencia"]
                    w_clave = password_cifrado

                    with sqlite3.connect("db/db_mayordomo.db") as console:
                        cursor=console.cursor()
                        statement="INSERT into empleados (numeroId,tipo,nombre,apellido,direccion,telefono,fechaNacimiento,tipoContrato,fechaIngreso,cargo,salario,fechaTerminoContrato,dependencia,rol,clave) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                        cursor.execute(statement,(w_numeroId,w_tipo,w_nombre,w_apellido,w_direccion,w_telefono,w_fechaNacimiento,w_tipoContrato,w_fechaIngreso,w_cargo,w_salario,w_fechaTerminoContrato,w_dependencia,w_rol, w_clave))
                        console.commit()


                    # Almacenar la Imagen del perfil
                    f = request.files['fotoPerfil']
                    # Guardamos el archivo en el directorio "Archivos PDF"
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], w_numeroId + ".png"))

                    console.close()
                    return render_template('crearEmpleado.html', title=title, nombrePag="Crear Empleado",
                                        nombreIcono="fas fa-user-plus",
                                        mensaje="El usuario con " + w_tipo + " " + w_numeroId + " ha sido creado Correctamente!" + " Su contraseña es: " + pass_salt,
                                        tipoMensaje="success", mostrar="True")

                except Exception as e:
                    console.rollback()
                    console.close()
                    mensaje="";
                    tipoMensaje = ""
                    if "UNIQUE constraint failed" in str(e):
                        mensaje="El usuario " + w_tipo + " " + w_numeroId + " ya se encuentra registrado!!"
                        tipoMensaje="warning"
                    else:
                        mensaje="Lo sentimos. El usuario NO ha sido creado Correctamente :("
                        tipoMensaje="danger"
                    return render_template('crearEmpleado.html', title=title, nombrePag="Crear Empleado",
                                        nombreIcono="fas fa-user-plus",
                                        mensaje=mensaje,
                                        tipoMensaje=tipoMensaje, mostrar="True")

            return render_template('crearEmpleado.html', title = title, nombrePag="Crear Empleado", nombreIcono="fas fa-user-plus",
                                mostrar="False")
        else:
            return redirect(url_for('accesoDenegado'))
    else:
        return redirect(url_for("login"))

@app.route('/admin/editarEmpleado',methods=['GET','POST'])
def editarEmpleado():
    if 'rol' in session:
        if 'ID' in session and session['rol'] == "Admin" or session['rol'] == "SuperAdmin":
            title = "Editar Empleado"
            msg = ""
            if request.method == "POST":
                try:
                    w_numeroId=int(request.form["numeroId"])
                    w_tipo=request.form["tipo"]
                    w_nombre=request.form["nombre"]
                    w_apellido=request.form["apellido"]
                    w_direccion=request.form["direccion"]
                    w_telefono=request.form["telefono"]
                    w_fechaNacimiento=request.form["fechaNacimiento"]
                    w_tipoContrato=request.form["tipoContrato"]
                    w_fechaIngreso=request.form["fechaIngreso"]
                    w_cargo=request.form["cargo"]
                    w_rol = request.form["rol"]
                    w_salario=request.form["salario"]
                    w_fechaTerminoContrato=request.form["fechaTerminoContrato"]
                    w_dependencia=request.form["dependencia"]
                    with sqlite3.connect("db/db_mayordomo.db") as console:
                        cursor=console.cursor()
                        statement="UPDATE empleados set tipo=?,nombre=?,apellido=?,direccion=?,telefono=?,fechaNacimiento=?,tipoContrato=?,fechaIngreso=?,cargo=?,salario=?,fechaTerminoContrato=?,dependencia=?, rol=? WHERE numeroId=?"
                        cursor.execute(statement,(w_tipo,w_nombre,w_apellido,w_direccion,w_telefono,w_fechaNacimiento,w_tipoContrato,w_fechaIngreso,w_cargo,w_salario,w_fechaTerminoContrato,w_dependencia,w_rol,w_numeroId))
                        console.commit()
                        msg = "Empleado actualizado satisfactoriamente"
                except:
                    console.rollback()
                    msg = "No se pudo actualizar la información del empleado en la BD"
                finally:
                    #return render_template("success.html",msg = msg)
                    msg = "Proceso finalizado"

                console.close()

            return render_template('editarEmpleado.html', title = title, nombrePag="Editar Empleado", nombreIcono="fas fa-user-edit")
        else:
            return redirect(url_for('accesoDenegado'))
    else:
        return redirect(url_for("login"))

@app.route('/admin/eliminarEmpleado',methods=['GET','POST'])
def eliminarEmpleado():
    if 'rol' in session:
        if 'ID' in session and session['rol'] == "Admin" or session['rol'] == "SuperAdmin":
            title = "Eliminar Empleado"
            msg=""
            if request.method == "POST":
                try:
                    w_numeroId = request.form["numeroId"]
                    with sqlite3.connect("db/db_mayordomo.db") as console:
                        cursor = console.cursor()
                        cursor.execute("delete from empleados where numeroId=?",(w_numeroId,))
                        msg = "Registro de empleado borrado satisfactoriamente"
                except:
                    print(sqlite3.Error.mensaje)
                    msg = "Error en el borrado del registro"
                finally:
                    #return render_template("delete_record.html",msg = msg)
                    msg = "proceso finalizado"

                console.close()

            return render_template('eliminarEmpleado.html', title = title, nombrePag="Eliminar Empleado", nombreIcono="fas fa-user-slash")
        else:
            return redirect(url_for('accesoDenegado'))
    else:
        return redirect(url_for("login"))

@app.route("/accesodenegado")
def accesoDenegado():
    return render_template("accesoDenegado.html")

@app.route("/empleado/cambiarPassword", methods=['GET','POST'])
def cambiarPassword():
    if 'rol' in session:
        if 'ID' in session and session['rol'] == "Empleado" or session['rol'] == "SuperAdmin":
            if request.method == "POST":
                try:
                    w_numeroId = session['ID']
                    w_password = request.form["password"]
                    w_newPassword = request.form["newPassword"]
                    w_cNewPassword = request.form["cNewPassword"]
                    print(w_newPassword)

                    with sqlite3.connect("db/db_mayordomo.db") as console:
                        cursor = console.cursor()
                        cursor.execute("select clave from empleados where numeroId=?",(w_numeroId,))
                        password = cursor.fetchone()
                        print(password)
                        if check_password_hash(password[0], w_password):
                            if w_newPassword == w_cNewPassword:
                                cursor.execute("update empleados set clave=? where numeroId=?",(generate_password_hash(w_newPassword),w_numeroId))
                                console.commit()
                                print("Contraseña actualizada correctamente")
                            else:
                                print("Las contraseñas no coinciden")
                        else:
                            print("Contraseña incorrecta")
                except:
                    return render_template("cambiarPassword.html",msg="No se pudo actualizar la contraseña")
            return render_template('cambiarPassword.html', title = "Cambiar Password", nombrePag="Cambiar contraseña", nombreIcono="fas fa-key")
        else:
            return redirect(url_for('accesoDenegado'))
    else:
        return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(port=8000, debug=True)