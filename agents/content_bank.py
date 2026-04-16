"""
Curated content bank for @claudeprofessor.
Used as fallback when Gemini API is rate-limited or unavailable.
Each entry is a complete carousel dataset ready for rendering.
"""

import random

CONTENT_BANK = [
    {
        "topic": "Claude Projects — Tu asistente con memoria",
        "hook": {
            "tag": "Productividad",
            "title": 'Claude <span class="accent">Projects</span>:<br>tu asistente con<br>memoria infinita',
            "subtitle": "Crea un espacio donde Claude recuerda todo sobre tu negocio, proyecto o estudio."
        },
        "slides": [
            {
                "step_label": "Qué es",
                "title": 'Un <span class="accent">workspace</span> persistente',
                "body": "Projects es un espacio donde Claude mantiene contexto entre conversaciones sin repetir instrucciones.",
                "tip": "Ideal para proyectos largos donde necesitas <strong>continuidad</strong>."
            },
            {
                "step_label": "Cómo usarlo",
                "title": 'Sube archivos y <span class="accent">define reglas</span>',
                "body": "Añade documentos, guías de estilo o datos. Claude los usa como referencia permanente.",
                "tip": "El <strong>system prompt</strong> del proyecto define la personalidad y reglas."
            },
            {
                "step_label": "Ejemplo real",
                "title": 'Crea tu <span class="accent">asistente de marca</span>',
                "body": "Sube tu brand guide y Claude escribirá siempre en tu tono de voz exacto.",
                "tip": "Funciona para <strong>copywriting, emails y redes sociales</strong>."
            },
            {
                "step_label": "Pro tip",
                "title": 'Comparte con tu <span class="accent">equipo</span>',
                "body": "Los Projects se pueden compartir. Todo tu equipo accede al mismo contexto.",
                "tip": "Un solo project puede tener <strong>múltiples conversaciones</strong> activas."
            }
        ],
        "cta": {
            "cta_title": "¡Domina Claude Projects hoy! 🧡",
            "cta_subtitle": "Tips diarios para ser más productivo con IA"
        },
        "caption": "¿Sabías que Claude puede recordar TODO sobre tu proyecto? 🧠\n\nCon Projects, no tienes que repetir instrucciones nunca más. Es como tener un asistente que ya conoce tu negocio.\n\n¿Ya usas Projects o sigues empezando desde cero cada vez? 👇",
        "hashtags": "#ClaudeAI #AnthropicAI #AITips #PromptEngineering #ClaudeProfessor #LearnAI #AITools #ArtificialIntelligence #Productividad #TechTips"
    },
    {
        "topic": "5 trucos de prompting que nadie te cuenta",
        "hook": {
            "tag": "Prompting",
            "title": '5 trucos de<br><span class="accent">prompting</span> que<br>nadie te cuenta',
            "subtitle": "Técnicas avanzadas que separan a los usuarios básicos de los expertos en Claude."
        },
        "slides": [
            {
                "step_label": "Truco 1",
                "title": 'El método <span class="accent">XML tags</span>',
                "body": "Envuelve datos en tags XML para que Claude los organice mejor mentalmente.",
                "tip": "Usa <strong>&lt;context&gt;</strong>, <strong>&lt;task&gt;</strong> y <strong>&lt;format&gt;</strong>."
            },
            {
                "step_label": "Truco 2",
                "title": 'Dale <span class="accent">ejemplos</span> siempre',
                "body": "Few-shot prompting: muéstrale 2-3 ejemplos del output exacto que quieres.",
                "tip": "Los ejemplos valen más que <strong>mil palabras</strong> de instrucciones."
            },
            {
                "step_label": "Truco 3",
                "title": 'Pide que <span class="accent">piense en pasos</span>',
                "body": "Añade 'piensa paso a paso' para tareas complejas. Mejora la precisión un 40%.",
                "tip": "Combínalo con <strong>Extended Thinking</strong> para máximo poder."
            },
            {
                "step_label": "Truco 4",
                "title": 'Define el <span class="accent">rol</span> primero',
                "body": "Empieza con 'Eres un experto en X con 15 años de experiencia'. Cambia todo.",
                "tip": "Sé <strong>específico</strong>: no 'experto', sino 'especialista en SEO B2B SaaS'."
            }
        ],
        "cta": {
            "cta_title": "¡Aprende prompting avanzado! 🧡",
            "cta_subtitle": "Cada día un nuevo truco para dominar Claude AI"
        },
        "caption": "La mayoría usa Claude como un Google glorificado 😅\n\nPero con estos 5 trucos de prompting, tus resultados van a ser COMPLETAMENTE diferentes.\n\nEl truco #3 es el que más impacto tiene. ¿Cuál usas tú más? 👇",
        "hashtags": "#ClaudeAI #PromptEngineering #AITips #AnthropicAI #ClaudeProfessor #LearnAI #Productividad #TechTips #AIHacks #FutureOfWork"
    },
    {
        "topic": "Claude Artifacts — Crea apps sin código",
        "hook": {
            "tag": "Artifacts",
            "title": 'Claude puede<br>crear <span class="accent">apps</span><br>sin que escribas código',
            "subtitle": "Artifacts convierte instrucciones en texto en aplicaciones interactivas funcionales."
        },
        "slides": [
            {
                "step_label": "Qué son",
                "title": '<span class="accent">Artifacts</span> = código visual',
                "body": "Claude genera HTML, React o SVG que se renderiza en tiempo real al lado del chat.",
                "tip": "Puedes ver y usar la app <strong>mientras hablas</strong> con Claude."
            },
            {
                "step_label": "Ejemplo",
                "title": 'Crea una <span class="accent">calculadora</span> en 30 seg',
                "body": "Pide 'crea una calculadora de hipotecas' y tendrás una app funcional al instante.",
                "tip": "También sirve para <strong>gráficos, dashboards y juegos</strong>."
            },
            {
                "step_label": "Itera rápido",
                "title": 'Modifica con <span class="accent">lenguaje natural</span>',
                "body": "Di 'hazlo más oscuro' o 'añade un botón de exportar' y Claude actualiza el artifact.",
                "tip": "Es como tener un <strong>developer on-demand</strong> gratis."
            },
            {
                "step_label": "Comparte",
                "title": 'Publica con <span class="accent">un click</span>',
                "body": "Los artifacts se pueden compartir con un enlace público. Tu mini-app online en segundos.",
                "tip": "Ideal para <strong>prototipos y MVPs</strong> que necesitas validar rápido."
            }
        ],
        "cta": {
            "cta_title": "¡Crea tu primera app con Claude! 🧡",
            "cta_subtitle": "Tutoriales diarios de IA aplicada"
        },
        "caption": "¿Necesitas una app pero no sabes programar? 🤯\n\nCon Claude Artifacts puedes crear aplicaciones funcionales solo describiendo lo que quieres. Sin código, sin frameworks, sin dolor de cabeza.\n\n¿Qué app crearías si pudieras hacerla en 30 segundos? 💬",
        "hashtags": "#ClaudeAI #Artifacts #NoCode #AnthropicAI #ClaudeProfessor #AITools #WebDev #Productividad #TechTips #AIHacks"
    },
    {
        "topic": "System Prompts — El secreto de los power users",
        "hook": {
            "tag": "System Prompts",
            "title": 'El <span class="accent">secreto</span> que<br>usan los power<br>users de Claude',
            "subtitle": "Los system prompts transforman a Claude de asistente genérico a experto especializado."
        },
        "slides": [
            {
                "step_label": "Qué es",
                "title": 'Las <span class="accent">instrucciones</span> invisibles',
                "body": "El system prompt es texto que Claude lee antes de tu mensaje. Define su comportamiento base.",
                "tip": "Es como un <strong>manual de empleado</strong> para tu asistente IA."
            },
            {
                "step_label": "Estructura",
                "title": 'Rol + Reglas + <span class="accent">Formato</span>',
                "body": "Define quién es, qué debe hacer, qué NO debe hacer, y cómo debe responder.",
                "tip": "Siempre incluye <strong>ejemplos del output</strong> que esperas."
            },
            {
                "step_label": "Ejemplo",
                "title": 'Tu <span class="accent">copywriter</span> personal',
                "body": "'Eres un copywriter senior. Escribe en tono directo, frases cortas, sin jerga corporativa.'",
                "tip": "Añade: <strong>'Si no tienes datos, pregunta antes de inventar'</strong>."
            },
            {
                "step_label": "Avanzado",
                "title": 'Combina con <span class="accent">Projects</span>',
                "body": "Pon el system prompt en un Project y cada conversación nueva ya tendrá el contexto.",
                "tip": "Un buen system prompt <strong>ahorra horas</strong> de trabajo repetitivo."
            }
        ],
        "cta": {
            "cta_title": "¡Crea tu system prompt perfecto! 🧡",
            "cta_subtitle": "Tips de IA aplicada cada día en tu feed"
        },
        "caption": "El 90% de la gente usa Claude sin system prompt... y se nota 😬\n\nEs como contratar a alguien sin decirle cuál es su trabajo. Con un buen system prompt, Claude pasa de 'meh' a 'WOW'.\n\n¿Ya usas system prompts o es nuevo para ti? 🤔",
        "hashtags": "#ClaudeAI #SystemPrompt #PromptEngineering #AnthropicAI #ClaudeProfessor #AITips #Productividad #LearnAI #TechTips #AIHacks"
    },
    {
        "topic": "Claude vs ChatGPT — Cuándo usar cada uno",
        "hook": {
            "tag": "Comparativa",
            "title": 'Claude vs ChatGPT:<br>¿cuándo usar<br><span class="accent">cada uno</span>?',
            "subtitle": "No es cuál es mejor — es cuál es mejor PARA TI según lo que necesites."
        },
        "slides": [
            {
                "step_label": "Escritura",
                "title": 'Claude gana en <span class="accent">textos largos</span>',
                "body": "Para ensayos, análisis y escritura creativa, Claude produce texto más natural y detallado.",
                "tip": "Claude tiene una ventana de contexto de <strong>200K tokens</strong>."
            },
            {
                "step_label": "Código",
                "title": 'Claude Code es <span class="accent">otra liga</span>',
                "body": "Para programación, Claude Code permite editar proyectos enteros con un solo prompt.",
                "tip": "Claude puede leer <strong>repositorios completos</strong> de golpe."
            },
            {
                "step_label": "Multimedia",
                "title": 'ChatGPT gana en <span class="accent">imágenes</span>',
                "body": "DALL-E y GPT-4o generan imágenes. Claude se enfoca en texto y análisis.",
                "tip": "Para <strong>generar imágenes</strong>, ChatGPT sigue siendo la opción."
            },
            {
                "step_label": "Veredicto",
                "title": 'Usa <span class="accent">ambos</span> estratégicamente',
                "body": "Claude para pensar y escribir. ChatGPT para crear y visualizar. Combo ganador.",
                "tip": "Los pros usan <strong>múltiples IAs</strong>. No te cases con una sola."
            }
        ],
        "cta": {
            "cta_title": "¡Más comparativas cada semana! 🧡",
            "cta_subtitle": "Síguenos para dominar todas las IAs"
        },
        "caption": "La guerra Claude vs ChatGPT... pero el ganador eres tú si sabes cuándo usar cada uno 🏆\n\nClaude para textos y código. ChatGPT para imágenes y multimedia. ¿Por qué elegir uno si puedes dominar ambos?\n\n¿Cuál prefieres tú? ¡Comenta! 💬",
        "hashtags": "#ClaudeAI #ChatGPT #AIComparison #AnthropicAI #OpenAI #ClaudeProfessor #AITips #TechTips #Productividad #FutureOfWork"
    },
]


STYLE_ROTATION = ["editorial", "flat", "news"]
BG_QUERY_FALLBACK = "artificial intelligence abstract technology orange"


def get_random_content() -> dict:
    """Return a random pre-curated content set from the bank."""
    content = dict(random.choice(CONTENT_BANK))
    content.setdefault("template_style", random.choice(STYLE_ROTATION))
    content.setdefault("bg_query", BG_QUERY_FALLBACK)
    print(f"  [FALLBACK] Using content bank: {content['topic']} (style={content['template_style']})")
    return content
