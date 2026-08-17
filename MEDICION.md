# Plan de medición — Embudo de evaluación inicial

**Sitio:** epa-bienestar.com.ar · **Property GA4:** `G-5J3NZ57F9D`
**Versión:** 1.0 · Agosto 2026

---

## Regla que no se negocia

**Ningún dato de salud sale hacia GA4.** No se envía qué síntomas marcó una
persona, ni cuántos, ni nada de lo que se pueda inferir su estado clínico.

En `epa-analytics.js` hay una constante `SEND_SYMPTOM_COUNT` fijada en `false`.
Dejarla así. Aunque solo fuera un número agregado, queda vinculado al
`client_id` de GA4, que es un identificador pseudónimo persistente — y eso lo
convierte en un dato de salud asociado a una persona identificable en los
términos del artículo 2 de la Ley 25.326.

El valor de producto que aportaría —saber si la gente marca tres o siete
casilleros— no justifica el riesgo regulatorio ni la incoherencia con lo que
el propio sitio le promete a la usuaria.

---

## Los dos requisitos previos

Sin esto el resto no funciona, por más código que haya del lado del sitio.

**1. El mismo measurement ID en `info.epa-bienestar.com.ar`.**
Está en `snippet-evaluacion-inicial.html`. La conversión ocurre en esa página:
si no lleva `G-5J3NZ57F9D`, GA4 ve a la persona como un usuario nuevo sin
origen y las dos landings quedan sin forma de compararse. Es el paso más
importante de todo este documento.

**2. Registrar las dimensiones personalizadas en GA4.**
Admin → Definiciones personalizadas → ámbito Evento:

| Parámetro | Para qué sirve |
|---|---|
| `origen_pagina` | Qué landing mandó a la persona |
| `origen_cta` | Qué botón tocó |
| `cta_id` | Identidad estable del llamado a la acción |
| `cta_destination` | evaluacion · whatsapp · demo · formulario |
| `page_group` | home · landing_b · landing_c · institucional · legal |
| `faq_pregunta` | Qué pregunta abrió |
| `paso` | Paso del formulario alcanzado |

**No son retroactivas.** Si se registran después, los datos previos no
aparecen en los informes aunque se hayan enviado. Hacerlo antes de mandar
tráfico.

---

## Por qué no usamos UTMs internos

Es el error que arruina estos embudos sin dar señal de que algo anda mal.

Si un enlace de `menopausia.html` hacia `info.epa-bienestar.com.ar` lleva
`utm_source=web`, GA4 interpreta que empezó una **sesión nueva de una fuente
nueva**. Alguien que llegó desde una campaña de Instagram pasa a figurar como
tráfico propio, y la atribución original se pierde. En los informes todo se ve
prolijo: simplemente todas las conversiones aparecen viniendo de "web".

Por eso usamos `epa_src` y `epa_cta`, que GA4 ignora para atribución y la
página de destino lee y reenvía como parámetros de evento.

Los UTM sí van, y son necesarios, en enlaces **externos** hacia el sitio:
campañas de Instagram, newsletters, códigos QR en consultorios.

---

## Eventos que emite el sitio

| Evento | Cuándo | Parámetros |
|---|---|---|
| `cta_click` | Clic en cualquier llamado a la acción | `cta_id`, `cta_text`, `cta_destination` |
| `salida_evaluacion` | Clic específico hacia la evaluación | igual que arriba |
| `profundidad_lectura` | 25 / 50 / 75 / 90 % de la página | `percent` |
| `faq_abierta` | Se despliega una pregunta frecuente | `faq_pregunta` |
| `reconocimiento_usado` | Grupo C: se tocó el bloque. **Una vez, sin contenido.** | — |
| `cambio_tema` | Se cambia claro/oscuro | `tema` |

Todos llevan además `page_slug` y `page_group`.

## Eventos de la página de destino

| Evento | Cuándo |
|---|---|
| `evaluacion_inicio` | Carga de `evaluacion-inicial.php` |
| `evaluacion_paso` | Se alcanza un paso del formulario |
| `evaluacion_completa` | Se envía el formulario ← **la conversión** |
| `evaluacion_abandono` | Se empezó a completar y se abandonó sin enviar |

---

## El embudo

Explorar → Exploración de embudo:

```
1. page_view                       ¿cuánta gente llega?
2. profundidad_lectura ≥ 50 %      ¿lee o rebota?
3. salida_evaluacion               ¿hace clic?
4. evaluacion_inicio               ¿la página cargó?
5. evaluacion_completa             ¿la terminó?
```

Desglosar por `origen_pagina`. Ese desglose responde la pregunta que motivó
todo esto: **cuál de las dos tesis convierte mejor** — la varianza menopáusica
de Grupo C o la prueba de esfuerzo del embarazo de Grupo B.

### Qué mirar en cada caída

| Caída entre | Qué significa | Qué tocar |
|---|---|---|
| 1 → 2 | La página no engancha en los primeros segundos | Titular y primer bloque |
| 2 → 3 | Lee pero no actúa | Posición y texto de los botones |
| 3 → 4 | Clics que no llegan a destino | Problema técnico: enlace, redirección o carga |
| 4 → 5 | Empieza el formulario y lo deja | Largo del formulario, campos pedidos |

La caída **3 → 4** casi siempre es un bug, no un problema de conversión. Si
aparece, revisarla antes que cualquier otra cosa.

---

## Qué esperar y cuándo decidir

Con dos landings compitiendo, para distinguir una diferencia real de ruido
hacen falta del orden de **300 a 400 sesiones por landing**. Con menos, una
diferencia de tres o cuatro puntos de conversión no significa nada.

Antes de llegar a ese volumen, la instrumentación sirve igual para lo otro:
detectar que un botón no funciona, que una página se lee al 20 % y se
abandona, o que el formulario pierde gente en un paso puntual. Eso se ve con
pocas visitas.

---

## Consentimiento

`epa-analytics.js` implementa Consent Mode v2:

- **Publicidad denegada siempre** (`ad_storage`, `ad_user_data`,
  `ad_personalization`). EPA no hace remarketing ni comparte datos con
  plataformas publicitarias, y el código lo hace cumplir, no solo la política.
- **Analítica concedida por defecto**, con barra visible que ofrece
  desactivarla. Proporcionado bajo Ley 25.326 para analítica pseudónima
  declarada en la política de privacidad.

**Para California:** CCPA/CPRA exige un estándar distinto. Antes de publicar
en ese mercado hay que cambiar `analytics_storage` a `"denied"` por defecto y
pedir opt-in explícito. Está señalado en el código; es una línea.

---

## Lo que esta instrumentación no puede decirte

- **Si la evaluación sirve clínicamente.** Mide conversión, no resultado en salud.
- **Por qué la gente abandona.** Para eso hacen falta cinco entrevistas con
  usuarias, que van a rendir más que cualquier informe de GA4.
- **Nada con volumen bajo.** Con veinte visitas por landing, los porcentajes
  son ruido. Resistir la tentación de decidir con eso.
