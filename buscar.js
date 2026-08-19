// Buscador de la bóveda.
//
// Con catorce tarjetas se encontraba todo bajando; con veinticuatro, no. Y quien
// llega aquí viene de un DM buscando UNA cosa concreta —la que le prometía el
// carrusel—, así que lo que necesita no es explorar: es encontrar.
//
// Filtra sobre lo que ya está en el HTML, sin índice ni datos aparte: así una
// tarjeta nueva entra en el buscador por el hecho de existir, y no hay una
// segunda lista que se quede desincronizada. Si el script no carga, quedan las
// veinticuatro tarjetas visibles, que es exactamente lo que había antes.
(function () {
  'use strict';
  var rejilla = document.querySelector('.rejilla');
  if (!rejilla) return;

  var tarjetas = Array.prototype.slice.call(rejilla.querySelectorAll('.tarjeta'));
  if (tarjetas.length < 12) return;   // con pocas, el buscador estorba más que ayuda

  // Sin tildes y en minúscula: quien escribe «boveda» tiene que encontrar «bóveda».
  function llano(t) {
    return t.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  }

  tarjetas.forEach(function (t) { t.dataset.busca = llano(t.textContent); });

  var caja = document.createElement('div');
  caja.className = 'buscador';
  caja.innerHTML =
    '<label class="visually-hidden" for="q">Buscar en la bóveda</label>' +
    '<input id="q" type="search" placeholder="Buscar: skills, prompts, diseño…" ' +
    'autocomplete="off" spellcheck="false">' +
    '<p class="cuenta" role="status" aria-live="polite"></p>';
  rejilla.parentNode.insertBefore(caja, rejilla);

  var input = caja.querySelector('input');
  var cuenta = caja.querySelector('.cuenta');

  function filtrar() {
    var q = llano(input.value.trim());
    var vistas = 0;
    tarjetas.forEach(function (t) {
      var cabe = !q || t.dataset.busca.indexOf(q) !== -1;
      t.hidden = !cabe;
      if (cabe) vistas++;
    });
    // Con la caja vacía no se dice nada: el número solo importa al filtrar.
    if (!q) cuenta.textContent = '';
    else if (vistas === 0) cuenta.textContent = 'Nada con «' + input.value.trim() + '». Prueba con una palabra más corta.';
    else cuenta.textContent = vistas === 1 ? '1 resultado' : vistas + ' resultados';
  }

  input.addEventListener('input', filtrar);
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { input.value = ''; filtrar(); }
  });
})();
