from flask import Flask
from flask import render_template,url_for,redirect

app = Flask(__name__)

@app.route('/admin/',methods=['GET'])
def dashboard():
    title = "Dashboard"
    return render_template('dashboard.html', title = title, nombrePag="Dashboard", nombreIcono="fas fa-clipboard-list")

@app.route("/admin/<palabra>",methods=['GET','POST'])
def aleatorio(palabra=None):
    return redirect(url_for("dashboard"))

@app.route("/login",methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route("/seleccionarRol",methods=['GET'])
def seleccionarRol():
    return render_template('dashboardRol.html')

@app.route('/empleado/retroalimentacion',methods=['GET'])
def retroalimentacion():
    title = "Retroaliemntacion"
    return render_template('retroalimentacion.html', title = title, nombrePag="Retro", nombreIcono="fas fa-clipboard-list")

@app.route('/empleado/')
def dashboardEmpleado():
    title = "Dashboard - Empleado"
    return render_template('dashboardEmpleado.html', title = title, nombrePag="Dashboard", nombreIcono="fas fa-clipboard-list")


@app.route('/admin/buscarEmpleado',methods=['GET','POST'])
def buscarEmpleado():
    title = "Buscar Empleado"
    return render_template('buscarEmpleado.html', title = title, nombrePag="Buscar Empleado", nombreIcono="fas fa-search")

@app.route('/admin/crearEmpleado',methods=['GET','POST'])
def crearEmpleado():
    title = "Crear Empleado"
    return render_template('crearEmpleado.html', title = title, nombrePag="Crear Empleado", nombreIcono="fas fa-user-plus")

@app.route('/admin/editarEmpleado',methods=['GET','POST'])
def editarEmpleado():
    title = "Editar Empleado"
    return render_template('editarEmpleado.html', title = title, nombrePag="Editar Empleado", nombreIcono="fas fa-user-edit")

@app.route('/admin/eliminarEmpleado',methods=['GET','POST'])
def eliminarEmpleado():
    title = "Eliminar Empleado"
    return render_template('eliminarEmpleado.html', title = title, nombrePag="Eliminar Empleado", nombreIcono="fas fa-user-slash")


if __name__ == '__main__':
    app.run(port=8000, debug=True)