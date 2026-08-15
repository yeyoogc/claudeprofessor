---
name: conviertelo-en-plantilla
description: Coge esa tarea que repites cada semana a mano y la deja convertida en una plantilla reutilizable - o en una skill propia - que la próxima vez sale sola. Úsala siempre que cuenten que hacen algo repetido (el informe semanal, el parte de ventas, las mismas respuestas, el acta, presupuestos, publicaciones), cuando digan "esto lo hago todos los lunes", "siempre le tengo que explicar lo mismo" o cuando hayan afinado un prompt que por fin funciona y no quieran perderlo.
---

# Conviértelo en plantilla

Casi todo el mundo usa la IA para lo fácil —un tuit, un correo suelto— y sigue
haciendo a mano la tarea de dos horas que repite cada semana. Ahí está todo el
tiempo. Esta skill convierte **una tarea repetida en un encargo reutilizable**,
para que la semana que viene no se empiece de cero.

## La regla que manda sobre todo lo demás

**La plantilla se saca de un ejemplo real, nunca de la imaginación.** Pide el
resultado de la última vez —el bueno, el que se entregó— antes de escribir una
línea. Una plantilla inventada produce trabajo con pinta de correcto que luego
hay que rehacer, y el usuario no vuelve.

## 1 · Delimita la tarea

Preguntas cortas, todas juntas:

> ¿Cada cuánto la haces y cuánto tardas? ¿Qué tienes delante cuando empiezas
> (un Excel, correos, notas)? ¿Quién recibe el resultado y qué hace con él?

Lo último es lo que más ordena. Un informe que alguien mira treinta segundos
antes de una reunión y un informe que se archiva no se escriben igual.

Si lo que cuenta son tres tareas distintas juntas, sepáralas y empieza por la
que más se repite. Una plantilla que intenta cubrirlo todo no cubre nada.

## 2 · Pide el material

Dos cosas, y espera a tenerlas:

- **El mejor resultado de la última vez.** El modelo a imitar.
- **Lo que había de entrada.** Los datos en bruto con los que se hizo.

Con dos ejemplos en vez de uno la plantilla sale mucho mejor: lo que se repite
entre los dos es la estructura, lo que cambia son los huecos. Pídelos, y si solo
hay uno, sigue pero dilo.

## 3 · Separa lo fijo de lo variable

Delante del usuario, marca sobre su ejemplo:

- **Lo fijo.** Secciones, orden, tono, longitud, fórmulas de apertura y cierre.
- **Los huecos.** Lo que cambia cada vez. Cada uno con un nombre claro —
  `[MES]`, `[CIFRA DE VENTAS]`, `[INCIDENCIA DE LA SEMANA]` — y con qué hacer
  si esa vez no hay dato.
- **Lo que hay que decidir cada vez.** Ojo con esto: no todo se automatiza. Si
  una parte pide criterio, la plantilla debe **pedir el criterio**, no fingirlo.

## 4 · Saca las reglas que no están escritas

El paso que separa una plantilla que funciona de una que decepciona. Esas
decisiones que el usuario toma sin pensar y que no aparecen en ningún sitio.
Pregunta por casos concretos, no en abstracto:

> - La última vez que faltó un dato, ¿qué hiciste?
> - ¿Qué es lo que nunca pondrías ahí aunque fuera verdad?
> - Si te lo devolvieran mal, ¿por qué habría sido?
> - ¿Hay alguien que lo lee y a quien hay que tener contento?

Esas respuestas son el 80 % del valor. Van a la plantilla escritas como reglas.

## 5 · Escribe la plantilla

Con estas cinco partes, en este orden:

1. **Para qué sirve y cuándo se usa.** Una línea.
2. **Qué hay que darle.** La lista exacta de entradas.
3. **Qué devuelve.** El formato exacto, con el esqueleto de secciones.
4. **Las reglas.** Las del paso 4, cada una con su porqué en media línea. El
   porqué no es adorno: sin él, se aplican mal en el caso raro.
5. **Cuándo parar y preguntar.** Qué falta obliga a preguntar en vez de rellenar
   a ojo. Sin esto, el hueco se rellena con algo verosímil, que es el peor
   resultado posible.

Y lo que casi nadie escribe: **el criterio de que está bien**. Una o dos frases
sobre cómo se distingue un resultado bueno de uno pasable. Es lo que evita la
media de internet.

## 6 · Pruébala delante, con el caso de esta semana

En el mismo chat. Ejecuta la plantilla con un caso real y enseña el resultado.

Cuando algo falle —y algo falla— **corrige la plantilla, no el resultado**. Esa
es toda la diferencia: arreglar la salida sirve para hoy; arreglar la plantilla
sirve para siempre. Dilo en voz alta al hacerlo, porque es el hábito que hay que
enseñar.

## 7 · Entrégala en el formato que le sirva

Pregunta cómo la va a usar y da una de las dos:

- **Texto para pegar** al principio de una conversación. La opción de siempre,
  sin instalar nada.
- **Una skill**, si es algo que va a hacer muchas veces y quiere que se active
  sola. Es una carpeta con un `SKILL.md` dentro que empieza así:

```
---
name: informe-semanal
description: Escribe el informe semanal de ventas a partir del
  Excel de la semana. Úsala cuando pase el export de ventas o
  pida el informe del lunes.
---

# Instrucciones…
```

La `description` es lo único que se lee para decidir si la skill entra: tiene
que decir **qué hace y cuándo usarla**, con las palabras que el usuario usaría
de verdad. Si dice «ayuda con informes», no se activará nunca a tiempo.

Cómo se instala, paso a paso, está en
[claudeprofessor.page/instalar-skills](https://claudeprofessor.page/instalar-skills).

## Errores que la dejan inservible

- **Escribirla de memoria.** Sale una plantilla razonable que no se parece a lo
  que esa persona entrega.
- **Sin criterio de salida.** Sin decir qué es estar bien, cada ejecución sale
  distinta y ninguna convence.
- **Fijarlo todo.** Si la plantilla decide lo que tiene que decidir la persona,
  se abandona a la tercera semana.
- **No probarla.** Una plantilla sin estrenar es una intención.
- **Meter dentro los datos de este caso.** Los nombres, cifras y fechas de esta
  semana van fuera; dentro solo van los huecos. Es el fallo más fácil de cometer
  y el que hace que la plantilla solo valga una vez.

## Cuando la tarea toca datos de otras personas

Si lo que se repite cada semana lleva datos de clientes, pacientes o alumnos,
la plantilla tiene que decir qué se anonimiza antes y qué no sale nunca del
ordenador. Ahí encaja
[`antes-de-pegarlo`](https://claudeprofessor.page/skills/antes-de-pegarlo/SKILL.md),
y conviene mencionarlo en vez de dejarlo a la suerte.

---
Skill abierta de [ClaudeProfessor](https://claudeprofessor.page). Si la mejoras,
mándala y se publica con tu nombre.
