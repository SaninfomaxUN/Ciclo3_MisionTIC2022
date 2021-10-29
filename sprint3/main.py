from flask import Flask, request
from flask import render_template,url_for,redirect, session, render_template_string
import sqlite3 
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "asdfghjklñ"

@app.route("/",methods=['GET','POST'])
def redireccionar(palabra=None):
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
        
        with sqlite3.connect('db_mayordomo.db') as console:
            print("Conectado")
            cursor = console.cursor() 
            data = cursor.execute("SELECT * from empleados where numeroId = ?",(username,)).fetchone()
            if  data == None:
                print("No existe el usuario")
                return redirect(url_for("login"))
            elif check_password_hash(data[14], password) == True:
            # elif data[14] == password:
                session['ID'] = username
                session['rol'] = data[4]
                print("sesion creada con exito " + "rol: " + session['rol'] + " " + "ID: " + session['ID'])
                print("loggin success")
                if session['rol'] == "admin":
                    return redirect(url_for("seleccionarRol"))
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
    return render_template('dashboardRol.html')

@app.route('/empleado/retroalimentacion',methods=['GET'])
def retroalimentacion():
    if 'ID' in session:
        title = "Retroaliemntacion"
        return render_template('retroalimentacion.html', title = title, nombrePag="Retroalimentación", nombreIcono="fas fa-chart-bar")
    else:
        return render_template_string('acceso denegado')

@app.route('/empleado/')
def dashboardEmpleado():
    if 'ID' in session:
        title = "Dashboard - Empleado"
        return render_template('dashboardEmpleado.html', title = title, nombrePag="Dashboard", nombreIcono="fas fa-clipboard-list")
    else:
        return render_template_string('acceso denegado')

@app.route('/admin/',methods=['GET','POST'])
def dashboard():
    if session['rol'] == "admin":
        title = "Dashboard"
        return render_template('dashboard.html', title = title, nombrePag="Dashboard", nombreIcono="fas fa-clipboard-list")
    else:
        return render_template_string('acceso denegado')

@app.route('/admin/buscarEmpleado',methods=['GET','POST'])
def buscarEmpleado():
    if session['rol'] == "admin":
        if request.method == "POST": 
            try: 
                w_numeroId=request.form["numeroId"]
                w_tipo=request.form["tipo"]
                with sqlite3.connect("db_mayordomo.db") as console:  
                    console.row_factory = sqlite3.Row  
                    cursor=console.cursor()  
                    statement="SELECT * FROM empleados WHERE (numeroId=?)"
                    cursor.execute(statement,(w_numeroId))  
                    rows=cursor.fetchall()
                    msg="Empleado existente en la bd"
                    return render_template("mostrarEmpleado.html",rows=rows)
            except:
                msg = "Registro no encontrado en la BD"
            finally:  
                console.close() 
            return render_template("mostrarEmpleado.html",rows=rows) 

        title = "Buscar Empleado"
        return render_template('buscarEmpleado.html', title = title, nombrePag="Buscar Empleado", nombreIcono="fas fa-search")
    else:
        return render_template_string('acceso denegado')


@app.route('/admin/gestionarRetroalimentacion',methods=['GET','POST'])
def gestionarRetro():
    if session['rol'] == "admin":
        title = "Gestionar Retroalimentación"
        return render_template('gestionarRetro.html', title = title, nombrePag="Gestionar Retroalimentación", nombreIcono="fas fa-search")
    else:
        return render_template_string('acceso denegado')

@app.route('/admin/crearEmpleado',methods=['GET','POST'])
def crearEmpleado():
    if session['rol'] == "admin":
        title = "Crear Empleado"
        msg = ""  
        if request.method == "POST":  
            try: 
                print("entre")
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
                w_salario=request.form["salario"]
                w_fechaTerminoContrato=request.form["fechaTerminoContrato"]
                w_dependencia=request.form["dependencia"] 
                w_clave= generate_password_hash(request.form["clave"])
                # w_clave = request.form["clave"]

                with sqlite3.connect("db_mayordomo.db") as console:  
                    cursor=console.cursor()  
                    statement="INSERT into empleados (numeroId,tipo,nombre,apellido,direccion,telefono,fechaNacimiento, tipoContrato,fechaIngreso,cargo,salario,fechaTerminoContrato,dependencia,rol,clave) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                    cursor.execute(statement,(w_numeroId,w_tipo,w_nombre,w_apellido,w_direccion,w_telefono,w_fechaNacimiento,w_tipoContrato,w_fechaIngreso,w_cargo,w_salario,w_fechaTerminoContrato,w_dependencia,w_clave," ","plm"))                
                    console.commit()  
                    print("Empleado creado satisfactoriamente")
                    msg = "Empleado creado satisfactoriamente"  
            except:  
                console.rollback()  
                msg = "No se pudo agregar el empleado a la BD"  
            finally:  
                #return render_template("success.html",msg = msg)  
                msg = "Proceso finalizado"
            console.close() 

        return render_template('crearEmpleado.html', title = title, nombrePag="Crear Empleado", nombreIcono="fas fa-user-plus")
    else:
        return render_template_string('acceso denegado')

@app.route('/admin/editarEmpleado',methods=['GET','POST'])
def editarEmpleado():
    if session['rol'] == "admin":
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
                w_salario=request.form["salario"]
                w_fechaTerminoContrato=request.form["fechaTerminoContrato"]
                w_dependencia=request.form["dependencia"]    
                with sqlite3.connect("db/db_mayordomo.db") as console:  
                    cursor=console.cursor()  
                    statement="UPDATE empleados set tipo=?,nombre=?,apellido=?,direccion=?,telefono=?,fechaNacimiento=?,tipoContrato=?,fechaIngreso=?,cargo=?,salario=?,fechaTerminoContrato=?,dependencia=? WHERE numeroId=?"
                    cursor.execute(statement,(w_tipo,w_nombre,w_apellido,w_direccion,w_telefono,w_fechaNacimiento,w_tipoContrato,w_fechaIngreso,w_cargo,w_salario,w_fechaTerminoContrato,w_dependencia,w_numeroId))  
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
        return render_template_string('acceso denegado')


@app.route('/admin/eliminarEmpleado',methods=['GET','POST'])
def eliminarEmpleado():
    if session['rol'] == "admin":
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
        return render_template_string('acceso denegado')

if __name__ == '__main__':
    app.run(port=8000, debug=True)
