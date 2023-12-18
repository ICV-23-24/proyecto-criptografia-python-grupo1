// Seleccionar el botón o elemento que cambiará entre modos
const botonModo = document.getElementById('theme-switch');

// Escuchar el evento de clic en el botón
botonModo.addEventListener('click', () => {
  // Obtener el elemento body
  const body = document.body;

  // Cambiar la clase del body para activar/desactivar el modo oscuro
  body.classList.toggle('modo-oscuro');

  // Opcional: Guardar el modo actual en localStorage para recordar la preferencia del usuario
  const modoActual = body.classList.contains('modo-oscuro') ? 'oscuro' : 'claro';
  localStorage.setItem('modo-preferido', modoActual);
});

// Verificar si el usuario ya tiene una preferencia guardada en localStorage
const modoGuardado = localStorage.getItem('modo-preferido');

// Aplicar el modo guardado si existe
if (modoGuardado) {
  document.body.classList.add(`modo-${modoGuardado}`);
}
