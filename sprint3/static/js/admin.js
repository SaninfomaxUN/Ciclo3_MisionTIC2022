function mostrarLogoSubido() {
    const [file] = fotoSubida.files
    if (file) {
      document.getElementById('fotoPerfil').setAttribute('src', URL.createObjectURL(file));
  }
}



function mostrarAlertaBootstrap(message, type) {
        var alertaMensaje = document.getElementById('divAlerta')
        var wrapper = document.createElement('div')
        wrapper.innerHTML = '<div class="alert alert-' + type + ' alert-dismissible" role="alert">' + message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'
        alertaMensaje.append(wrapper)

}

function activarAlerta(mensaje, tipoMensaje, boolean="False"){
    if (boolean == "True") {
        mostrarAlertaBootstrap(mensaje, tipoMensaje)
      }

}

function mostrarInformacionUsuario(jsonDatos){
    try {
        jsonDatos = JSON.parse(jsonDatos)
        document.getElementById('fotoPerfil').setAttribute('src', "../static/assets/img/Perfil/" + jsonDatos[0].numeroId + ".png");
        document.getElementsByName('nombre')[0].value = jsonDatos[0].nombre;
        document.getElementsByName('apellido')[0].value = jsonDatos[0].apellido;
        document.getElementById('rol').value = jsonDatos[0].rol;
        document.getElementsByName('tipo')[1].value = jsonDatos[0].tipo;
        document.getElementsByName('numeroId')[1].value = jsonDatos[0].numeroId;
        document.getElementsByName('direccion')[0].value = jsonDatos[0].direccion;
        document.getElementsByName('telefono')[0].value = jsonDatos[0].telefono;
        document.getElementsByName('fechaNacimiento')[0].value = jsonDatos[0].fechaNacimiento;
        document.getElementsByName('tipoContrato')[0].value = jsonDatos[0].tipoContrato;
        document.getElementsByName('fechaIngreso')[0].value  = jsonDatos[0].fechaIngreso;
        document.getElementsByName('cargo')[0].value = jsonDatos[0].cargo;
        document.getElementsByName('salario')[0].value = jsonDatos[0].salario;
        document.getElementsByName('fechaTerminoContrato')[0].value= jsonDatos[0].fechaTerminoContrato;
        document.getElementsByName('dependencia')[0].value = jsonDatos[0].dependencia;
    }catch{

    }
}
function habilitarCampos(){
        document.getElementsByName('nombre')[0].removeAttribute('readonly');
        document.getElementsByName('apellido')[0].removeAttribute('readonly');
        document.getElementById('rol').removeAttribute("disabled");
        document.getElementsByName('tipo')[1].removeAttribute("disabled");
        document.getElementsByName('numeroId')[1].removeAttribute('readonly');
        document.getElementsByName('direccion')[0].removeAttribute('readonly');
        document.getElementsByName('telefono')[0].removeAttribute('readonly');
        document.getElementsByName('fechaNacimiento')[0].removeAttribute('disabled');
        document.getElementsByName('tipoContrato')[0].removeAttribute('readonly');
        document.getElementsByName('fechaIngreso')[0].removeAttribute('disabled');
        document.getElementsByName('cargo')[0].removeAttribute('readonly');
        document.getElementsByName('salario')[0].removeAttribute('readonly');
        document.getElementsByName('fechaTerminoContrato')[0].removeAttribute('disabled');
        document.getElementsByName('dependencia')[0].removeAttribute('readonly');
        document.getElementsByName('btnEditar')[0].removeAttribute('disabled');
}
