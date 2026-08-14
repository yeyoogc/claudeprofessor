# Skills abiertas de ClaudeProfessor

Tres skills de Claude, gratuitas y abiertas. Cada una empaqueta un método que
he explicado en un carrusel, para que no tengas que acordarte de él.

| Skill | Para qué |
|---|---|
| `escribe-como-yo` | Aprende tu voz de tres textos tuyos antes de escribir una línea |
| `interroga-documentos` | Lee un PDF largo como si tuviera que defenderlo mañana |
| `reunion-a-tareas` | Notas sueltas → decisiones y tareas con responsable y fecha |

## Cómo se instalan

Una skill es una carpeta con un `SKILL.md` dentro. Se copia y ya está.

**En Claude Code**, al directorio de skills de tu usuario:

```bash
cp -r escribe-como-yo ~/.claude/skills/
```

**En la app de Claude**, se suben en ZIP desde Personalizar → Skills, con el
botón `+` → «Crear skill» → «Subir una skill». Antes hay que tener encendida la
ejecución de código, que está en otro sitio: Ajustes → Capacidades →
«Ejecución de código y creación de archivos». Sin eso las skills no hacen nada,
y es donde se atasca casi todo el mundo.

Después se invocan solas cuando la conversación lo pide, o a mano escribiendo
`/escribe-como-yo`.

## Cómo comprobar que funcionan

Cada `SKILL.md` empieza con un bloque `name` y `description`. Esa descripción
es lo que Claude lee para decidir si la skill aplica: si la cambias, cambia
cuándo se activa.

Prueba rápida: abre una conversación nueva y pide algo que encaje con la
descripción. Si la skill entra, verás que sigue su flujo en vez de responder
directamente.

## Si la mejoras

Mándamela por [@claudeprofessor](https://instagram.com/claudeprofessor) y la
publico aquí con tu nombre. Lo que más se agradece:

- Casos donde la skill se queda corta o se activa cuando no debe.
- Reglas nuevas que hayas comprobado que funcionan, no que suenen bien.
- Traducciones o adaptaciones a otro oficio.

## Licencia

Úsalas, cámbialas y compártelas. Si las publicas modificadas, deja una
referencia a [claudeprofessor.page](https://claudeprofessor.page).
