function mostrarLogoSubido() {
    const [file] = fotoPerfil.files
    if (file) {
      document.getElementById('fotoSubida').setAttribute('src', URL.createObjectURL(file));
  }
}

var alertaMensaje = document.getElementById('divAlerta')

function mostrarAlertaBootstrap(message, type) {
  var wrapper = document.createElement('div')
  wrapper.innerHTML = '<div class="alert alert-' + type + ' alert-dismissible" role="alert">' + message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'

  alertaMensaje.append(wrapper)
}

function activarAlerta(mensaje, tipoMensaje, boolean){
    if (boolean == "True") {
        mostrarAlertaBootstrap(mensaje, tipoMensaje)
      }

}



