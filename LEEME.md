# Sitio EPA Bienestar IA

## Cómo publicarlo

Subí todo el contenido de esta carpeta a la raíz del sitio. Son archivos
estáticos: no hace falta build step ni servidor de aplicaciones.

**Importante:** copiá tu carpeta `assets/img/` actual dentro de `assets/`.
No la incluimos acá para no pisar tus imágenes existentes. El sitio espera
al menos `logo.png`, `favicon.ico` y `8pasos_AHA.jpg`.

## Estructura

    index.html                        Home, con el hero de trazados
    bienestar_con_datos.html          La tesis + Índice EPA completo
    por_que_elegirnos.html            Tabla de diferenciales
    acerca_de_nosotros.html           Institucional, equipo, ecosistema
    roadmap.html                      Roadmap clínico, producto e IA
    integraciones.html                Wearables, laboratorio, FHIR, LOINC
    engagement.html                   Adherencia, MEPA-Express, SBAE
    prevencion.html                   Bandas de riesgo y escalamiento clínico
    modelo_de_atencion.html           Alcance y límites explícitos
    enlaces.html                      Hub de programas, Grupos A–D
    menopausia.html                   Landing de conversión Grupo C (45–65)
    embarazo.html                     Landing de conversión Grupo B (28–44)
    politica_de_privacidad.html       Ley 25.326 · PENDIENTE REVISIÓN LEGAL
    condiciones_del_servicio.html     Términos · PENDIENTE REVISIÓN LEGAL
    programa/residentes/index.html    FRICCAR

    assets/css/epa.css                Sistema de diseño completo
    assets/js/epa.js                  Tema, nav, reveal, trazados, estado
    assets/js/epa-analytics.js        Consent Mode + instrumentación del embudo
    snippet-evaluacion-inicial.html   PARA PEGAR EN info.epa-bienestar.com.ar
    MEDICION.md                       Plan de medición y lectura del embudo
    build.py                          Generador de las páginas internas

## Para modificar el sitio

**Colores, tipografía, espaciados** → `assets/css/epa.css`, bloque `:root`
al principio. Cambiar ahí impacta las 13 páginas.

**Header, footer o navegación** → editá la función `layout()` en `build.py`
y volvé a correr `python3 build.py`. Se regeneran las 12 páginas internas
de una sola vez. `index.html` tiene su propio header y footer: hay que
tocarlo aparte.

**Contenido de una página interna** → el diccionario `PAGES` en `build.py`.

## Medición — dos cosas obligatorias

1. **Pegar `snippet-evaluacion-inicial.html` en `evaluacion-inicial.php`.**
   La conversión ocurre en esa página. Sin el mismo measurement ID ahí,
   no hay embudo: GA4 ve un usuario nuevo sin origen y las dos landings
   quedan sin forma de compararse.
2. **Registrar las dimensiones personalizadas en GA4** antes de mandar
   tráfico. No son retroactivas. Lista completa en `MEDICION.md`.

Los enlaces internos hacia `info.` NO llevan `utm_*` a propósito: un
utm_source entre subdominios propios corta la sesión de GA4 y sobrescribe
la fuente real de adquisición. Usamos `epa_src` / `epa_cta`. Está explicado
en `MEDICION.md`; no lo cambies sin leer esa sección.

## Ponderaciones del Índice EPA — cambio de agosto 2026

Los pesos pasaron de **38/32/30 a 36/33/31**. Motivo: los porcentajes del
modelo de determinantes provenían de la v1 de la metodología de GoInvo, que
tenía un error aritmético (siete valores divididos por seis) que GoInvo
rectificó semanas después. Los valores vigentes son 36/24/22/11/7.

El origen del error, el análisis de impacto y la corrección están documentados
en la fe de erratas (§0) de `INDICE-EPA_SPEC_v1.1` y en la nota técnica
`NT-2026-01`.

**Si volvés a tocar estos números, tocá los tres lugares:**

1. El texto y las etiquetas — `build.py` e `index.html`
2. Los `data-w` de las barras de determinantes — `index.html`
3. **Los valores `flex` de `.seg-e` / `.seg-p` / `.seg-a`** en `epa.css`

El punto 3 es el que se olvida. Una barra que dice 36 % y dibuja 38 % es una
mentira visual, y en un sitio clínico eso no es un detalle estético.

**Atribución obligatoria.** El modelo está bajo CC BY 4.0 y exige acreditar a
los autores: Choi, E. & Sonin, J. (2019). *Determinants of Health.* GoInvo.
Debe aparecer donde se citen los porcentajes, indicando la versión de
metodología (v3, nov 2018). No es cortesía: es la licencia.

## Pendientes conocidos

1. Las dos páginas legales necesitan revisión de asesoría legal antes de
   publicarse. Están marcadas con un aviso visible en la propia página.
2. La API key de UptimeRobot está expuesta del lado cliente en `epa.js`.
   Es de solo lectura y acotada a un monitor, pero conviene proxearla
   por una Lambda.
3. El badge de AFIP apunta a `http://`, no `https://`, y va a generar un
   warning de contenido mixto.
5. `SEND_SYMPTOM_COUNT` en `epa-analytics.js` está en `false` y debe
   quedar así: enviar cuántos síntomas marcó alguien, aun sin decir
   cuáles, es un dato de salud vinculado a un identificador persistente.
6. Para California hay que pasar `analytics_storage` a `denied` por
   defecto y pedir opt-in. Está señalado en el código.
4. `localStorage` para persistir el tema está comentado en `epa.js` y en
   el script anti-flash de cada página. Descomentar en producción.

## Badge AAIP

El isologo del Registro Nacional de Bases de Datos está en el footer de las
14 páginas y enlaza a la constancia de inscripción. La política de privacidad
también lo referencia en la sección de marco legal.

## Landing de Grupo C

`menopausia.html` usa ciruela como color de acento en vez de teal. No es
decorativo: es la dimensión Armonía, la que representa la voz de la paciente,
y es la página que le habla a ella. El scope está en la clase `.pg-c` del
`<body>`; el resto del sistema no cambia.

## Landing de Grupo B

`embarazo.html` conserva el teal institucional a propósito: los eventos
adversos del embarazo son insumos de estratificación de riesgo, o sea que
esta página vive en la dimensión Precisión. Se diferencia por su elemento
firma —la curva de carga cardiovascular— y no por el color.

La curva está marcada como **esquemática** en el encabezado del panel y no
tiene eje Y numérico. Comunica la forma y la ventana posparto desaprovechada,
no valores hemodinámicos. Si alguna vez se le agregan números, deja de ser
esquemática y pasa a necesitar respaldo de fuente.

## Landing de Grupo C

El bloque de reconocimiento **no puntúa, no estratifica y no guarda nada**.
Es deliberadamente distinto de un test de autodiagnóstico: agrupa lo que la
persona marcó y la orienta hacia la evaluación. Si en algún momento se
convierte en algo que devuelve un resultado clínico, pasa a requerir revisión
del comité de ética.
