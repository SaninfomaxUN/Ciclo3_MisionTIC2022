from flask import Flask
from flask import render_template,url_for,redirect

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def dashboard():
    title = "Dashboard"
    return render_template('dashboard.html', title = title, nombrePag="Dashboard", nombreIcono="fas fa-clipboard-list")

@app.route("/<palabra>",methods=['GET','POST'])
def aleatorio(palabra=None):
    return redirect(url_for("dashboard"))

@app.route('/buscarEmpleado',methods=['GET','POST'])
def buscarEmpleado():
    title = "Buscar Empleado"
    return render_template('buscarEmpleado.html', title = title, nombrePag="Buscar Empleado", nombreIcono="fas fa-search")

@app.route('/crearEmpleado',methods=['GET','POST'])
def crearEmpleado():
    title = "Crear Empleado"
    return render_template('crearEmpleado.html', title = title, nombrePag="Crear Empleado", nombreIcono="fas fa-user-plus")

@app.route('/editarEmpleado',methods=['GET','POST'])
def editarEmpleado():
    title = "Editar Empleado"
    return render_template('editarEmpleado.html', title = title, nombrePag="Editar Empleado", nombreIcono="fas fa-user-edit")

@app.route('/eliminarEmpleado',methods=['GET','POST'])
def eliminarEmpleado():
    title = "Eliminar Empleado"
    return render_template('eliminarEmpleado.html', title = title, nombrePag="Eliminar Empleado", nombreIcono="fas fa-user-slash")




if __name__ == '__main__':
    app.run(port=8000, debug=True)