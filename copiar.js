// Un botón de copiar en cada bloque de código de la bóveda.
//
// Estas páginas existen para copiar de ellas: son prompts y plantillas. Hasta
// ahora había que seleccionar a mano, y en el móvil —que es de donde llega casi
// todo el tráfico, porque el enlace se manda por DM— seleccionar un bloque de
// diez líneas sin pasarte es una pelea.
//
// Se monta desde JavaScript en vez de escribirlo en el HTML para que las
// veinticuatro páginas no tengan que tocarse una a una, y para que si mañana
// falla el script las páginas sigan leyéndose igual: sin él solo se pierde el
// botón, no el contenido.
(function () {
  'use strict';
  if (!navigator.clipboard) return;   // navegador viejo: mejor sin botón que con uno roto

  document.querySelectorAll('main pre').forEach(function (pre) {
    var caja = document.createElement('div');
    caja.className = 'copiable';
    pre.parentNode.insertBefore(caja, pre);
    caja.appendChild(pre);

    var boton = document.createElement('button');
    boton.type = 'button';
    boton.className = 'copiar';
    boton.textContent = 'Copiar';
    // El bloque ya se lee; lo que hay que anunciar es qué hace el botón.
    boton.setAttribute('aria-label', 'Copiar este bloque');
    caja.appendChild(boton);

    boton.addEventListener('click', function () {
      navigator.clipboard.writeText(pre.innerText).then(function () {
        boton.textContent = 'Copiado';
        boton.classList.add('hecho');
        setTimeout(function () {
          boton.textContent = 'Copiar';
          boton.classList.remove('hecho');
        }, 1600);
      }).catch(function () {
        // Si el navegador lo bloquea, decirlo en vez de fingir que ha ido bien.
        boton.textContent = 'Copia a mano';
      });
    });
  });
})();
