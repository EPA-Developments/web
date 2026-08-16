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
    politica_de_privacidad.html       Ley 25.326 · PENDIENTE REVISIÓN LEGAL
    condiciones_del_servicio.html     Términos · PENDIENTE REVISIÓN LEGAL
    programa/residentes/index.html    FRICCAR

    assets/css/epa.css                Sistema de diseño completo
    assets/js/epa.js                  Tema, nav, reveal, trazados, estado
    build.py                          Generador de las páginas internas

## Para modificar el sitio

**Colores, tipografía, espaciados** → `assets/css/epa.css`, bloque `:root`
al principio. Cambiar ahí impacta las 13 páginas.

**Header, footer o navegación** → editá la función `layout()` en `build.py`
y volvé a correr `python3 build.py`. Se regeneran las 12 páginas internas
de una sola vez. `index.html` tiene su propio header y footer: hay que
tocarlo aparte.

**Contenido de una página interna** → el diccionario `PAGES` en `build.py`.

## Pendientes conocidos

1. Las dos páginas legales necesitan revisión de asesoría legal antes de
   publicarse. Están marcadas con un aviso visible en la propia página.
2. La API key de UptimeRobot está expuesta del lado cliente en `epa.js`.
   Es de solo lectura y acotada a un monitor, pero conviene proxearla
   por una Lambda.
3. El badge de AFIP apunta a `http://`, no `https://`, y va a generar un
   warning de contenido mixto.
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

El bloque de reconocimiento **no puntúa, no estratifica y no guarda nada**.
Es deliberadamente distinto de un test de autodiagnóstico: agrupa lo que la
persona marcó y la orienta hacia la evaluación. Si en algún momento se
convierte en algo que devuelve un resultado clínico, pasa a requerir revisión
del comité de ética.
