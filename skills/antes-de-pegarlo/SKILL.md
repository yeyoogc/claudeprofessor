---
name: antes-de-pegarlo
description: Revisa un texto o documento antes de subirlo a una IA y sustituye lo que no debería salir de tu ordenador - nombres, DNI, teléfonos, direcciones, datos de clientes, pacientes o alumnos, cláusulas y claves. Úsala siempre que vayan a pegar o subir un documento con datos de terceros, cuando pregunten "¿esto se lo puedo pasar?", cuando mencionen confidencialidad, RGPD, secreto profesional, historiales o expedientes, y antes de mandar a revisar contratos, nóminas, listados de clientes o trabajos de alumnos.
---

# Antes de pegarlo

La pregunta no es si la IA es de fiar: es que **hay datos que no son tuyos**. Un
listado de clientes, un expediente o un parte médico no dejan de ser de esas
personas porque el archivo esté en tu carpeta. Esta skill deja el documento
utilizable sin llevarse por delante lo que no debe salir.

Esto no es asesoría jurídica. Es la revisión que evita el 90 % de los disgustos.

## La regla que manda sobre todo lo demás

**Sustituir, nunca borrar.** Si se tacha sin más, el texto pierde el sentido y
el resultado sale inservible o, peor, se rellena el hueco con algo inventado.
Cada dato sale y entra un marcador estable: `[CLIENTE 1]`, `[FECHA 1]`,
`[IMPORTE 1]`. La misma persona, el mismo marcador siempre, en todo el
documento. Así el texto sigue razonando igual y al final se puede deshacer.

## 1 · La pregunta que decide

> ¿Estos datos son tuyos o de otra persona?

- **Tuyos.** Es tu riesgo y tú decides. Aun así conviene el repaso: contraseñas
  y números de cuenta no se pegan nunca, ni siquiera propios.
- **De terceros** (clientes, pacientes, alumnos, empleados, la otra parte de un
  contrato). Aquí no es preferencia, es obligación, y el repaso completo va
  entero.

Y una segunda que ahorra trabajo: **¿qué necesita entender la IA para ayudarte?**
Casi siempre la respuesta es «la estructura del caso», no los nombres. Si el
análisis funciona igual con `[EMPLEADA 1]`, no hay nada que discutir.

## 2 · Qué se marca

Repasa el documento buscando estas cinco familias. Devuélvelas listadas, con la
línea o el apartado donde aparece cada una:

**Identificadores directos.** Nombre y apellidos, DNI/NIE/pasaporte, número de
la Seguridad Social, teléfono, email, dirección postal, IBAN o tarjeta,
matrícula, número de historia clínica o de expediente, IP, usuario de redes.

**Identificadores indirectos.** Los que por separado no dicen nada y juntos
señalan a una persona: cargo + empresa, fecha de baja + departamento, «el único
fisio de Martos», edad + pueblo pequeño. Este grupo es el que se escapa siempre,
porque no tiene pinta de dato personal.

**Categorías especiales.** Salud, diagnósticos y bajas, ideología, religión,
afiliación sindical, origen étnico, orientación sexual, condenas, situación
económica delicada. Estas pesan más que las demás: márcalas aparte y, si no son
imprescindibles para la consulta, quítalas del todo en vez de sustituirlas.

**Secretos del negocio.** Precios pactados, márgenes, cláusulas de un contrato
vivo, condiciones de un proveedor, ofertas sin adjudicar, código o procesos
internos.

**Credenciales.** Contraseñas, claves de API, tokens, respuestas de seguridad.
Estas no se anonimizan: **se cambian**. Si aparecen, dilo antes que nada — una
clave pegada en cualquier sitio ya está comprometida y hay que rotarla.

## 3 · Qué devolver

En este orden:

1. **El texto limpio**, listo para pegar, con los marcadores puestos.
2. **La tabla de equivalencias**, para deshacer al final. Con un aviso: esa
   tabla se queda en su ordenador y no se sube a ninguna parte, porque es
   justamente lo que reconstruye todo lo demás.
3. **Lo que sigue identificando**, si queda algo. Sé honesto: «con el sector, la
   fecha y el importe, cualquiera del gremio sabe de quién hablamos». Un
   documento «anonimizado» del que se deduce el nombre es peor que uno sin
   anonimizar, porque da confianza falsa.
4. **Lo que he quitado entero** y por qué, si has eliminado algo en vez de
   sustituirlo.

## 4 · El paso que todo el mundo olvida

Cuando llegue el resultado del análisis, **hay que deshacer los marcadores**
antes de usarlo. Ofrécelo tú al terminar:

> Cuando tengas la respuesta, pégamela y te la devuelvo con los nombres reales
> puestos.

Si no, o se manda un informe lleno de `[CLIENTE 1]`, o el usuario los sustituye a
mano y se le cuela uno cambiado. Las dos cosas pasan.

## Lo que ninguna limpieza arregla

Hay material que no se sube, por mucho que se tache. Dilo claro y sin sermón:

- **Documentos sujetos a secreto profesional** cuando el encargo no lo permite
  (abogacía, sanidad, servicios sociales). El deber es del profesional, no del
  archivo.
- **Datos de menores**, salvo que la anonimización sea completa. Los trabajos de
  clase llevan nombre y apellidos en la primera página, y es lo primero que se
  sube sin mirar.
- **Lo que tu empresa prohíbe por contrato.** Hay convenios y políticas internas
  que van por delante de cualquier ajuste de privacidad.
- **Lo que no soportarías ver publicado.** Prueba rápida y sorprendentemente
  fiable.

Cuando toque uno de estos, la salida no es «tacha más»: es trabajar con un caso
resumido, sin documento, o no usar la IA para eso.

## Antes de todo esto: mira dónde estás pegando

La limpieza no sustituye a tener bien los ajustes. Si el usuario no sabe si sus
chats se usan para entrenar, mándalo a
[claudeprofessor.page/privacidad](https://claudeprofessor.page/privacidad): son
tres ajustes en tres sitios distintos y cambian según la aplicación.

Y una diferencia que conviene explicar: en las cuentas de empresa el contrato
suele ser distinto del de una cuenta personal. Si es material de trabajo, la
pregunta correcta no es «¿es segura la IA?», sino «¿qué cuenta estoy usando?».

---
Skill abierta de [ClaudeProfessor](https://claudeprofessor.page). Si la mejoras,
mándala y se publica con tu nombre.
