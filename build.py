#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPA Bienestar IA — generador estático del sitio.

Produce HTML plano en ./site. No hace falta build step en el servidor:
son archivos estáticos que se suben tal cual. Volvé a correr este script
cuando cambies el layout (header, footer, nav) para propagarlo a todas
las páginas de una sola vez.
"""
import os, html, re

OUT = "site"

NAV = [
    ("indice",      "Índice EPA",     "bienestar_con_datos.html#indice"),
    ("programa",    "Programa Mujer", "enlaces.html"),
    ("estandares",  "Estándares",     "integraciones.html"),
    ("modelo",      "Modelo",         "modelo_de_atencion.html"),
    ("roadmap",     "Roadmap",        "roadmap.html"),
    ("acerca",      "Acerca",         "acerca_de_nosotros.html"),
]


def layout(slug, title, desc, body, depth=0, active=None, home=False, cls=""):
    """Arma una página completa. `depth` = niveles de subcarpeta."""
    up = "../" * depth
    BODYCLS = f' class="{cls}"' if cls else ""
    nav = "\n".join(
        '      <a href="{}{}"{}>{}</a>'.format(
            up, href if not home else (("#" + key) if key in ("indice",) else href),
            ' aria-current="page"' if key == active else "", label)
        for key, label, href in NAV)

    return f"""<!DOCTYPE html>
<html lang="es-AR" data-theme="light">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title} | EPA Bienestar IA</title>
<meta name="description" content="{html.escape(desc, quote=True)}" />
<link rel="canonical" href="https://www.epa-bienestar.com.ar/{slug}" />
<meta name="theme-color" content="#0F5257" media="(prefers-color-scheme: light)" />
<meta name="theme-color" content="#0B0F14" media="(prefers-color-scheme: dark)" />
<meta http-equiv="Content-Language" content="es-AR" />

<meta property="og:locale" content="es_AR" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="EPA Bienestar IA" />
<meta property="og:title" content="{html.escape(title, quote=True)} — EPA Bienestar IA" />
<meta property="og:description" content="{html.escape(desc, quote=True)}" />
<meta property="og:url" content="https://www.epa-bienestar.com.ar/{slug}" />
<meta property="og:image" content="https://www.epa-bienestar.com.ar/assets/img/logo.png" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:site" content="@epabienestar" />

<link rel="icon" href="{up}assets/img/favicon.ico" type="image/x-icon" />
<link rel="icon" type="image/png" href="{up}assets/img/logo.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Instrument+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="{up}assets/css/epa.css" />
<script>
/* Evita el flash de tema claro antes de que cargue el JS diferido. */
(function(){{var t=window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";
/* try{{t=localStorage.getItem("epa-theme")||t;}}catch(e){{}} */
document.documentElement.setAttribute("data-theme",t);}})();
</script>
</head>

<body{BODYCLS}>
<a href="#main" class="skip">Ir al contenido</a>

<header class="hdr">
  <div class="wrap hdr-in">
    <a href="{up}index.html" class="brand" aria-label="EPA Bienestar IA — inicio">
      <img src="{up}assets/img/logo.png" alt="" />
      <span class="brand-tx">
        <b>EPA Bienestar IA</b>
        <span>Equilibrio · Precisión · Armonía</span>
      </span>
    </a>

    <nav class="nav" id="nav" aria-label="Principal">
{nav}
    </nav>

    <div class="hdr-act">
      <button class="tgl" id="tgl" type="button" aria-label="Cambiar entre modo claro y oscuro">
        <svg class="ico-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        <svg class="ico-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>
      </button>
      <a class="btn btn-solid" data-cta="header" href="https://info.epa-bienestar.com.ar/evaluacion-inicial.php">Evaluación inicial</a>
      <button class="burger" id="burger" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="nav">
        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>
    </div>
  </div>
</header>

<main id="main">
{body}
</main>

<footer class="ft">
  <div class="wrap">
    <div class="ft-grid">
      <div>
        <div class="ft-brand">
          <img src="{up}assets/img/logo.png" alt="" />
          <div>
            <div style="font-family:var(--f-display);font-weight:800;font-size:1.05rem;letter-spacing:-.03em">EPA Bienestar IA</div>
            <div class="ft-tag">Equilibrio · Precisión · Armonía</div>
          </div>
        </div>
        <address>
          Húsares 2248, CP 1428<br />
          CABA · Argentina<br />
          <a href="mailto:hola@epa-bienestar.com">hola@epa-bienestar.com</a><br />
          <a href="tel:+541169315830">+54 11 6931-5830</a>
        </address>
        <div class="status" id="status-container">
          <span id="status-dot"></span>
          <span id="status-text">Verificando estado…</span>
        </div>
      </div>

      <div>
        <h4>Plataformas</h4>
        <ul>
          <li><a href="https://seguimiento.epa-bienestar.com.ar">Seguimiento</a></li>
          <li><a href="https://profesionales.epa-bienestar.com.ar">Profesionales</a></li>
          <li><a href="https://tareas.epa-bienestar.com.ar">Tareas</a></li>
          <li><a href="https://app.epa-bienestar.com.ar">Developers</a></li>
          <li><a href="{up}enlaces.html">Programas</a></li>
        </ul>
      </div>

      <div>
        <h4>Recursos</h4>
        <ul>
          <li><a href="{up}menopausia.html">Menopausia y corazón</a></li>
          <li><a href="{up}embarazo.html">Embarazo y corazón</a></li>
          <li><a href="{up}bienestar_con_datos.html">Bienestar con datos</a></li>
          <li><a href="{up}por_que_elegirnos.html">Por qué elegirnos</a></li>
          <li><a href="{up}modelo_de_atencion.html">Modelo de atención</a></li>
          <li><a href="{up}acerca_de_nosotros.html">Acerca de nosotros</a></li>
          <li><a href="{up}roadmap.html">Roadmap</a></li>
        </ul>
      </div>

      <div>
        <h4>Contacto</h4>
        <ul>
          <li><a href="https://docs.google.com/forms/d/e/1FAIpQLSeqeXaSt2gi3CbaCO1xVIIRwdxittwh5AYaSoj8VuLSQ4OMOg/viewform">Escribinos</a></li>
          <li><a href="https://www.calendly.com/epabienestar/entrevistas">Entrevistas</a></li>
          <li><a href="https://chat.epa-bienestar.com.ar">Chat</a></li>
          <li><a href="{up}politica_de_privacidad.html">Privacidad</a></li>
          <li><a href="{up}condiciones_del_servicio.html">Legales</a></li>
        </ul>
      </div>
    </div>

    <div class="ft-bot">
      <span class="cr">© 2026 EPA Bienestar IA</span>
      <div class="socials">
        <a href="https://www.twitter.com/epabienestar" aria-label="Twitter"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.2 2H21l-6.5 7.4L22.2 22h-6l-4.7-6.2L6.1 22H3.3l7-8L2.1 2h6.2l4.3 5.7L18.2 2Zm-1 18h1.7L7.9 3.8H6.1L17.2 20Z"/></svg></a>
        <a href="https://github.com/EPA-Bienestar-com/" aria-label="GitHub"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2A10 10 0 0 0 8.8 21.5c.5.1.7-.2.7-.5v-1.7c-2.8.6-3.4-1.3-3.4-1.3-.5-1.2-1.1-1.5-1.1-1.5-.9-.6.1-.6.1-.6 1 .1 1.5 1 1.5 1 .9 1.5 2.4 1.1 3 .8.1-.6.3-1.1.6-1.4-2.2-.2-4.6-1.1-4.6-5 0-1.1.4-2 1-2.7-.1-.3-.4-1.3.1-2.7 0 0 .8-.3 2.7 1a9.4 9.4 0 0 1 5 0c1.9-1.3 2.7-1 2.7-1 .5 1.4.2 2.4.1 2.7.6.7 1 1.6 1 2.7 0 3.9-2.4 4.8-4.6 5 .4.3.7.9.7 1.9v2.8c0 .3.2.6.7.5A10 10 0 0 0 12 2Z"/></svg></a>
        <a href="https://instagram.com/epabienestar/" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg></a>
      </div>
      <a href="https://aws.amazon.com/what-is-cloud-computing" aria-label="Powered by AWS Cloud Computing">
        <img src="https://d0.awsstatic.com/logos/powered-by-aws.png" alt="Powered by AWS" style="height:34px;width:auto" loading="lazy" />
      </a>
      <a href="http://qr.afip.gob.ar/?qr=7c4YSAiX1AG7JLRkyAdzTQ,," target="_F960AFIPInfo" aria-label="Data Fiscal AFIP">
        <img src="http://www.afip.gob.ar/images/f960/DATAWEB.jpg" alt="Data Fiscal" style="height:46px;width:auto" loading="lazy" />
      </a>
      <a href="https://www.argentina.gob.ar/aaip/datospersonales/reclama/20205419935--RL-2023-154634293-APN-DNPDP#AAIP" target="_blank" rel="noopener" aria-label="Inscripción en el Registro Nacional de Bases de Datos — AAIP">
        <img src="https://www.argentina.gob.ar/sites/default/files/aaip-isologo.png" alt="AAIP — Registro Nacional de Bases de Datos" style="height:46px;width:auto" loading="lazy" />
      </a>
    </div>

    <p class="legal">
      PLAN BIENESTAR 100 DÍAS® es una marca registrada del Dr. Alejandro Sergio D'Alessandro para EPA Bienestar IA.
      Life's Essential 8™ y PREVENT™ son marcas de la American Heart Association, referenciadas con fines científicos.
      El Índice EPA es una herramienta de apoyo a la decisión clínica: no diagnostica, no indica tratamientos
      y no sustituye la evaluación de un profesional de la salud.
    </p>
  </div>
</footer>

<a href="https://wa.me/5491169315830?text=Hola%20EPA%20Bienestar,%20quisiera%20m%C3%A1s%20informaci%C3%B3n." class="wa" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">
  <svg viewBox="0 0 24 24"><path d="M.057 24l1.687-6.163a11.87 11.87 0 0 1-1.587-5.946C.16 5.335 5.495 0 12.05 0a11.82 11.82 0 0 1 8.413 3.488 11.82 11.82 0 0 1 3.48 8.414c-.003 6.557-5.338 11.892-11.893 11.892a11.9 11.9 0 0 1-5.688-1.448L.057 24zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885a9.86 9.86 0 0 0-9.881-9.892c-5.452 0-9.887 4.434-9.889 9.884 0 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.463 1.065 2.875 1.213 3.074.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>
</a>

<script src="{up}assets/js/epa.js" defer></script>

<!-- Analítica. epa-analytics.js define Consent Mode e instrumenta el embudo;
     debe cargar ANTES del tag de Google para que el consentimiento por
     defecto esté aplicado cuando gtag arranque. -->
<script src="{up}assets/js/epa-analytics.js"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-5J3NZ57F9D"></script>
</body>
</html>
"""


def phero(crumb, eyebrow, h1, lede, fx_title=None, fx_rows=None, depth=0):
    up = "../" * depth
    fx = ""
    if fx_rows:
        rows = "\n".join(
            f'        <div class="fx-row"><span class="k">{k}</span><span class="v">{v}</span></div>'
            for k, v in fx_rows)
        fx = f"""
      <aside class="card-fx">
        <h4>{fx_title}</h4>
{rows}
      </aside>"""
    return f"""<section class="phero">
  <div class="wrap phero-grid">
    <div>
      <p class="crumb"><a href="{up}index.html">Inicio</a><span>/</span>{crumb}</p>
      <p class="eyebrow">{eyebrow}</p>
      <h1>{h1}</h1>
      <p class="lede">{lede}</p>
    </div>{fx}
  </div>
</section>
"""


CTA = """<section class="band band-ink cta-fin">
  <div class="wrap rv">
    <p class="eyebrow" style="justify-content:center">Empezá hoy</p>
    <h2>Lo que no se conoce, no se previene.</h2>
    <p class="lede">La evaluación inicial es gratuita, toma diez minutos y devuelve tu punto de partida con el marco Life's Essential 8.</p>
    <div class="row">
      <a class="btn btn-signal" data-cta="cierre" href="https://info.epa-bienestar.com.ar/evaluacion-inicial.php">Hacer mi evaluación inicial</a>
      <a class="btn btn-ghost" style="border-color:rgba(255,255,255,.3);color:#fff" href="https://calendar.app.google/NeygNDb51VM6RLqb8">Agendar una demo</a>
    </div>
  </div>
</section>
"""


def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)
    return len(content)


PAGES = {}

# ═══════════════════════════════════════════════════════════════
# 1 · BIENESTAR CON DATOS  — la tesis intelectual
# ═══════════════════════════════════════════════════════════════
PAGES["bienestar_con_datos.html"] = dict(
    title="Bienestar con datos", active="indice",
    desc="Por qué medimos varianza y no solo niveles. El Índice EPA, el modelo de determinantes de salud y la arquitectura FHIR R4 que lo sostiene.",
    body=phero(
        "Bienestar con datos", "La tesis",
        "Un valor puntual no ve lo que un trazado sí ve.",
        "Life's Essential 8 mide niveles. La transición menopáusica es un fenómeno de varianza. "
        "Esta página explica por qué esa diferencia importa y qué construimos a partir de ella.",
        "Índice EPA v1.0",
        [("Dimensiones", "3"), ("Subcomponentes", "15"), ("Ventana estándar", "28 días"),
         ("Estado", "En validación"), ("Cohorte", "MAMA-LE8 · n=100")]) + """
<section class="band">
  <div class="wrap prose rv">
    <h3>El problema con medir solo niveles</h3>
    <p>Life's Essential 8, publicado por la American Heart Association en 2022, es el estándar de oro
    para cuantificar salud cardiovascular. Su diseño es deliberadamente transversal: cada uno de los
    ocho componentes se puntúa a partir de <strong>un valor puntual</strong>. Una presión arterial.
    Un LDL. Una glucemia. Horas de sueño autorreportadas.</p>
    <p>Ese diseño es apropiado para vigilancia poblacional. Es insuficiente para la transición
    menopáusica, y las razones son fisiológicas, no cosméticas.</p>

    <h4>La menopausia es un fenómeno de varianza</h4>
    <p>La perimenopausia se caracteriza por variabilidad extrema de estradiol y FSH <em>antes</em>
    de que cualquier valor medio se desplace. Los efectos cardiovasculares acompañan ese patrón:
    la variabilidad de la presión arterial aumenta antes de que la presión media suba; la
    fragmentación del sueño precede a la reducción de la duración total; la variabilidad glucémica
    se deteriora antes de que la HbA1c cruce cualquier umbral.</p>
    <p>Dicho de otro modo: <strong>dos pacientes pueden tener el mismo puntaje LE8 mientras una
    está estable y la otra se está desestabilizando.</strong></p>

    <h4>La variabilidad predice eventos por sí sola</h4>
    <p>La variabilidad de la presión arterial visita a visita predice accidente cerebrovascular y
    eventos coronarios de forma independiente de la presión media. La irregularidad del ritmo
    sueño-vigilia predice mortalidad de forma independiente —y con mayor magnitud— que la duración
    del sueño. Ninguna de esas dos señales entra en LE8.</p>

    <h4>Y falta la voz de la paciente</h4>
    <p>Los síntomas vasomotores, la calidad de sueño percibida, el ánimo y la carga urogenital no
    aparecen en el puntaje. Sin embargo, la carga de síntomas vasomotores moderados a severos es
    el determinante principal de si una mujer sostiene o abandona un plan de intervención.
    Un score que ignora lo que la mujer siente no puede anticipar la adherencia.</p>
  </div>
</section>

<section class="band band-alt" id="indice">
  <div class="wrap">
    <div class="head rv">
      <p class="eyebrow">Índice EPA</p>
      <h2>Tres capas, tres fuentes, tres recursos FHIR</h2>
      <p class="lede">El Índice EPA no reemplaza a LE8: lo envuelve. LE8 se sigue reportando de forma
      independiente bajo el código LOINC 96607-7.</p>
    </div>

    <div class="rv">
      <div class="idx-bar" role="img" aria-label="Ponderación: Equilibrio 36 %, Precisión 33 %, Armonía 31 %.">
        <div class="idx-seg seg-e">Equilibrio <span>36 %</span></div>
        <div class="idx-seg seg-p">Precisión <span>33 %</span></div>
        <div class="idx-seg seg-a">Armonía <span>31 %</span></div>
      </div>
      <p class="idx-src">Derivadas del modelo de determinantes — comportamiento 36 % → E · genética 22 % + cuidado médico 11 % → P · social 24 % + ambiente 7 % → A<br />
      Choi, E. &amp; Sonin, J. (2019). <em>Determinants of Health.</em> GoInvo. CC BY 4.0 · metodología v3, nov 2018.</p>
    </div>

    <div class="tbl-wrap rv">
      <table class="tbl">
        <thead><tr><th>Dimensión</th><th>Pregunta que responde</th><th>Fuente de datos</th><th>Recurso FHIR</th></tr></thead>
        <tbody>
          <tr><td><strong>E — Equilibrio</strong></td><td>¿Qué hace el cuerpo a lo largo del tiempo?</td><td>Wearables continuos y monitoreo domiciliario</td><td class="yes">Observation</td></tr>
          <tr><td><strong>P — Precisión</strong></td><td>¿Qué dice el riesgo estructural?</td><td>Laboratorio y estadificación clínica</td><td class="yes">RiskAssessment</td></tr>
          <tr><td><strong>A — Armonía</strong></td><td>¿Qué reporta la propia paciente?</td><td>Instrumentos validados vía WhatsApp</td><td class="yes">QuestionnaireResponse</td></tr>
        </tbody>
      </table>
    </div>

    <div class="callout callout-warn rv" style="margin-top:28px">
      <p><b>Estado de validación, sin ambigüedad.</b> Los instrumentos que componen el índice
      están validados individualmente en la literatura. Las ponderaciones, los cortes de puntuación
      y la diferencia mínima clínicamente importante son <b>propuestos por EPA y todavía no
      validados empíricamente</b>.</p>
      <p>La calibración se realiza sobre la cohorte MAMA-LE8, en tres sitios de la Federación
      Argentina de Cardiología. El protocolo se registra antes de la recolección de datos.
      No presentamos el índice como validado hasta completar esa etapa.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="head rv">
      <p class="eyebrow">Metodología</p>
      <h2>De dónde salen los pesos</h2>
      <p class="lede">Los porcentajes no son estimaciones internas. Surgen del promedio de
      fuentes primarias: OMS, NEJM, Health Affairs, Institute of Medicine, JAMA, DHHS y
      Universidad de Wisconsin.</p>
      <p class="lede" style="font-size:.92rem;opacity:.78">Modelo de Choi, E. &amp; Sonin, J. (2019),
      <em>Determinants of Health</em>, GoInvo, bajo licencia CC BY 4.0 · metodología v3, noviembre de 2018.</p>
    </div>
    <div class="cards rv">
      <div class="card"><div class="kicker">36 %</div><h3>Comportamiento individual</h3><p>Nutrición, actividad física, sueño y gestión del estrés. Es el determinante de mayor peso y también el más modificable.</p></div>
      <div class="card"><div class="kicker">24 %</div><h3>Circunstancias sociales</h3><p>Situación familiar, acceso a recursos, apoyo comunitario e inequidades de género.</p></div>
      <div class="card"><div class="kicker">22 %</div><h3>Genética y biología</h3><p>Antecedentes familiares, riesgo predispuesto, tamizaje selectivo. Acá vive Lp(a).</p></div>
      <div class="card"><div class="kicker">11 %</div><h3>Cuidado médico</h3><p>Evaluación cardiovascular, medicación cuando corresponde, seguimiento clínico.</p></div>
      <div class="card"><div class="kicker">7 %</div><h3>Ambiente físico</h3><p>Acceso a espacios de actividad, seguridad comunitaria, calidad del aire.</p></div>
      <div class="card"><div class="kicker">Nota</div><h3>Alineación, no identidad</h3><p>La correspondencia entre determinante y dimensión del índice es conceptual, no estricta. Lo declaramos en toda publicación, junto con la versión de metodología usada.</p></div>
    </div>
  </div>
</section>

<section class="band band-alt">
  <div class="wrap prose rv">
    <h3>Lo que este sistema no hace</h3>
    <p>Ser específico sobre los límites es parte del rigor, no una concesión.</p>
    <ul>
      <li><strong>No diagnostica.</strong> El Índice EPA es una herramienta de estratificación y seguimiento longitudinal de apoyo a la decisión clínica.</li>
      <li><strong>No indica ni ajusta medicación.</strong> Esa decisión es del profesional tratante, siempre.</li>
      <li><strong>No predice eventos.</strong> No podemos afirmar que un índice más alto se asocie a menos eventos cardiovasculares. Esa afirmación requiere seguimiento a cinco años o más, y todavía no lo tenemos.</li>
      <li><strong>No sustituye la evaluación médica.</strong> Programa Mujer es un complemento del equipo de salud, nunca un reemplazo.</li>
    </ul>
    <h4>Y un sesgo que declaramos</h4>
    <p>La dimensión Equilibrio depende de wearables y monitoreo domiciliario de presión. Eso
    introduce un sesgo socioeconómico sistemático: las pacientes con menos recursos van a tener
    índices con menor completitud. La redistribución automática de peso lo mitiga parcialmente,
    pero no lo elimina. Lo monitoreamos como métrica de equidad, no lo tratamos como ruido.</p>
  </div>
</section>
""" + CTA)

# ═══════════════════════════════════════════════════════════════
# 2 · POR QUÉ ELEGIRNOS
# ═══════════════════════════════════════════════════════════════
PAGES["por_que_elegirnos.html"] = dict(
    title="Por qué elegirnos", active=None,
    desc="Qué diferencia a EPA Bienestar de una aplicación de bienestar genérica: marco científico, interoperabilidad FHIR R4, red clínica y validación local.",
    body=phero(
        "Por qué elegirnos", "Diferenciales",
        "No somos una app de bienestar.",
        "Somos infraestructura clínica interoperable, construida sobre un marco científico "
        "publicado y validada con la red cardiológica argentina. La diferencia se ve en los detalles.") + """
<section class="band">
  <div class="wrap">
    <div class="tbl-wrap rv">
      <table class="tbl">
        <thead><tr><th style="width:20%">Aspecto</th><th style="width:42%">EPA Bienestar IA</th><th>Aplicación de bienestar genérica</th></tr></thead>
        <tbody>
          <tr><td><strong>Marco científico</strong></td><td class="yes">Life's Essential 8 (AHA 2022) + modelo de determinantes de salud de GoInvo (CC BY 4.0), promediado de fuentes primarias</td><td class="no">Puntaje de salud propietario, sin publicación revisada por pares</td></tr>
          <tr><td><strong>Qué mide</strong></td><td class="yes">Niveles, variabilidad y outcomes reportados por la paciente</td><td class="no">Valores puntuales</td></tr>
          <tr><td><strong>Localización</strong></td><td class="yes">MEPA-Express, tamizaje dietario adaptado a Argentina; español rioplatense</td><td class="no">Traducción de una app global, sin contexto regional</td></tr>
          <tr><td><strong>Etapas de vida</strong></td><td class="yes">Cuatro grupos con lógica clínica propia (A/B/C/D)</td><td class="no">Segmentación por edad</td></tr>
          <tr><td><strong>Interoperabilidad</strong></td><td class="yes">FHIR R4 nativo, LOINC y SNOMED CT en todos los recursos</td><td class="no">Silo de datos, exportación en PDF si acaso</td></tr>
          <tr><td><strong>Conexión clínica</strong></td><td class="yes">Derivación a la red de la Federación Argentina de Cardiología</td><td class="no">Teléfono de atención genérico</td></tr>
          <tr><td><strong>Validación</strong></td><td class="yes">Protocolo MAMA-LE8, cohorte prospectiva en tres sitios FAC</td><td class="no">Sin validación en población local</td></tr>
          <tr><td><strong>Soberanía de datos</strong></td><td class="yes">AWS Local Zone Buenos Aires · Ley 25.326 · registro AAIP</td><td class="no">Servidores fuera de jurisdicción</td></tr>
          <tr><td><strong>Portabilidad</strong></td><td class="yes">La usuaria se lleva sus datos en formato estándar cuando quiere</td><td class="no">Los datos quedan en la plataforma</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="band band-alt">
  <div class="wrap">
    <div class="head rv">
      <p class="eyebrow">Compromiso</p>
      <h2>Código abierto y estándares abiertos</h2>
      <p class="lede">Los proyectos de salud digital más relevantes del siglo XXI son de código
      abierto y están enfocados en prevención basada en datos de investigación. Nos sumamos a esa
      línea, no la esquivamos.</p>
    </div>
    <div class="cards rv">
      <div class="card"><div class="kicker">Estándar</div><h3>HL7 FHIR R4</h3><p>No es una función que agregamos después. Es la arquitectura sobre la que está construido todo, incluido el backend FAVALORO.</p></div>
      <div class="card"><div class="kicker">Terminología</div><h3>LOINC y SNOMED CT</h3><p>Cada observación lleva su código. Un sistema externo puede leer nuestros datos sin traducción intermedia.</p></div>
      <div class="card"><div class="kicker">Trazabilidad</div><h3>Provenance en cada dato</h3><p>Un auditor —o el revisor de una publicación— puede reconstruir cualquier puntaje desde los datos crudos sin acceso al código.</p></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap prose rv">
    <h3>El equipo detrás</h3>
    <p>EPA Bienestar IA está fundada y dirigida por un cardiólogo en ejercicio. Eso cambia la
    conversación con instituciones médicas: no llegamos a vender software, llegamos a proponer
    colaboración clínica.</p>
    <p>El asesoramiento médico está a cargo del <strong>Dr. Alejandro Barbagelata</strong> (MD, FAHA,
    FSCAI), profesor adjunto en Duke University School of Medicine y fellow de la American Heart
    Association. El liderazgo científico en inteligencia artificial está en el
    <strong>Laboratorio de IA del ITBA</strong>. La validación clínica se coordina con el Comité de
    Enfermedades Cardiovasculares en la Mujer de la <strong>Federación Argentina de Cardiología</strong>
    y con la <strong>Sociedad Argentina de Cardiología</strong>.</p>
    <p><a href="acerca_de_nosotros.html">Conocer al equipo y al ecosistema →</a></p>
  </div>
</section>
""" + CTA)

# ═══════════════════════════════════════════════════════════════
# 3 · ACERCA DE NOSOTROS
# ═══════════════════════════════════════════════════════════════
PAGES["acerca_de_nosotros.html"] = dict(
    title="Acerca de nosotros", active="acerca",
    desc="EPA Bienestar IA: quiénes somos, qué construimos y con quién. Salud cardiovascular de la mujer en Argentina, México y California.",
    body=phero(
        "Acerca de nosotros", "Quiénes somos",
        "Lo que no se conoce, no se previene.",
        "EPA Bienestar IA es una empresa argentina de salud digital enfocada en prevención "
        "cardiovascular para mujeres en cada etapa de la vida.",
        "Ficha institucional",
        [("Fundación", "2024"), ("Sede", "CABA, Argentina"),
         ("Mercados", "Argentina · México · California"),
         ("Producto insignia", "Programa Mujer"),
         ("Backend", "FAVALORO · FHIR R4")]) + """
<section class="band">
  <div class="wrap prose rv">
    <h3>El punto de partida</h3>
    <p>La enfermedad cardiovascular es la primera causa de muerte en mujeres, por encima de todos
    los cánceres combinados. Y sin embargo, alrededor del <strong>62 % de las mujeres percibe al
    cáncer como su principal amenaza de salud</strong>, mientras la enfermedad cardiovascular
    causa el <strong>27,3 % de las muertes femeninas</strong>.</p>
    <p>Esa brecha entre percepción y mortalidad es el punto de partida de todo lo que construimos.
    No es un dato de color para una presentación: es el problema.</p>

    <h3>Dónde ponemos el foco</h3>
    <p>Ponemos a las personas en el centro y trabajamos sobre dos frentes que, juntos, afectan a
    más del 80 % de la población mundial:</p>
    <ul>
      <li><strong>Enfermedades no transmisibles</strong>, con foco en riesgo cardiovascular femenino.</li>
      <li><strong>Salud mental</strong>, integrada al seguimiento y no tratada como un anexo.</li>
    </ul>
    <p>Entramos por la transición menopáusica, porque es el momento en que el riesgo cardiovascular
    femenino se vuelve visible y clínicamente urgente. Desde ahí la misma infraestructura se
    extiende hacia atrás —desarrollo y maternidad— y hacia adelante —envejecimiento activo.</p>
  </div>
</section>

<section class="band band-alt" id="equipo">
  <div class="wrap">
    <div class="head rv"><p class="eyebrow">Equipo</p><h2>Miembros fundadores</h2></div>
    <div class="team rv">
      <article class="team-c">
        <h3>Alejandro S. D'Alessandro</h3>
        <div class="role">CEO &amp; Co-Fundador · Cardiólogo</div>
        <p style="font-size:.9rem;color:var(--muted)">Dirige la visión clínica y la arquitectura de interoperabilidad de la plataforma.</p>
        <a class="mail" href="mailto:ceo@epa-bienestar.com">ceo@epa-bienestar.com</a>
        <a class="li-btn" href="https://www.linkedin.com/in/drdalessandro" target="_blank" rel="noopener">Seguir en LinkedIn</a>
      </article>
      <article class="team-c">
        <h3>Gustavo Brey</h3>
        <div class="role">CTO &amp; Co-Fundador</div>
        <p style="font-size:.9rem;color:var(--muted)">Responsable de plataforma, infraestructura cloud y seguridad.</p>
        <a class="mail" href="mailto:cto@epa-bienestar.com">cto@epa-bienestar.com</a>
        <a class="li-btn" href="https://www.linkedin.com/in/gbrey" target="_blank" rel="noopener">Seguir en LinkedIn</a>
      </article>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="head rv">
      <p class="eyebrow">Ecosistema</p>
      <h2>Integrarnos es la estrategia</h2>
      <p class="lede">Crecemos con quienes encuentran valor clínico en lo que construimos.
      Programa Mujer es un complemento del equipo médico, nunca un reemplazo.</p>
    </div>
    <div class="eco rv">
      <div class="eco-c"><div class="n">FAC</div><div class="r">38 sociedades federadas</div></div>
      <div class="eco-c"><div class="n">SAC</div><div class="r">Validación clínica</div></div>
      <div class="eco-c"><div class="n">AHA · Go Red</div><div class="r">Marco Life's Essential 8™</div></div>
      <div class="eco-c"><div class="n">Duke University</div><div class="r">Dr. A. Barbagelata, MD FAHA FSCAI</div></div>
      <div class="eco-c"><div class="n">ITBA AI Lab</div><div class="r">Liderazgo científico en IA</div></div>
      <div class="eco-c"><div class="n">CMU Tepper</div><div class="r">Capstone de estrategia</div></div>
      <div class="eco-c"><div class="n">AWS Startups</div><div class="r">Local Zone Buenos Aires</div></div>
      <div class="eco-c"><div class="n">NVIDIA Inception</div><div class="r">Infraestructura de IA</div></div>
      <div class="eco-c"><div class="n">DinoCloud</div><div class="r">Seguridad cloud</div></div>
      <div class="eco-c"><div class="n">Hospital Marie Curie</div><div class="r">Módulo cardio-oncología</div></div>
    </div>
  </div>
</section>

<section class="band band-ink">
  <div class="wrap">
    <div class="head rv">
      <p class="eyebrow">FAVALORO</p>
      <h2>El nombre del backend no es casual</h2>
      <p class="lede">Nuestra infraestructura FHIR R4 se llama FAVALORO, en tributo a René Favaloro.
      Es la columna de interoperabilidad y soberanía de datos sobre la que se apoya la futura
      investigación federada en América Latina. Los datos de las pacientes argentinas viven en
      Argentina.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap prose rv">
    <h3>Marco normativo</h3>
    <p>Operamos bajo el marco legal argentino de protección de datos y derechos del paciente:</p>
    <ul>
      <li><strong>Ley 25.326</strong> — Protección de Datos Personales. Registro ante la Agencia de Acceso a la Información Pública (AAIP).</li>
      <li><strong>Ley 26.529</strong> — Derechos del Paciente, Historia Clínica y Consentimiento Informado.</li>
      <li><strong>Ley 25.506</strong> — Firma Digital, aplicada a los registros que lo requieren.</li>
      <li><strong>Comité de Ética en Investigación</strong> — todo protocolo de investigación pasa por evaluación de un CEI antes de comenzar.</li>
      <li><strong>HL7 FHIR R4</strong> — estándar internacional de interoperabilidad en salud.</li>
    </ul>
    <p><a href="politica_de_privacidad.html">Leer la política de privacidad →</a></p>
  </div>
</section>
""" + CTA)

# ═══════════════════════════════════════════════════════════════
# 4 · ROADMAP
# ═══════════════════════════════════════════════════════════════
PAGES["roadmap.html"] = dict(
    title="Roadmap", active="roadmap",
    desc="Hacia dónde va EPA Bienestar IA: validación clínica MAMA-LE8, expansión regional e infraestructura de inteligencia artificial.",
    body=phero(
        "Roadmap", "Hacia dónde vamos",
        "Qué estamos construyendo, y cuándo.",
        "Un roadmap público obliga a ser honesto. Lo que sigue son intenciones planificadas, "
        "no compromisos contractuales: las fechas pueden moverse y lo vamos a decir cuando pase.") + """
<section class="band">
  <div class="wrap">
    <div class="head rv"><p class="eyebrow">Clínico</p><h2>Validación y evidencia</h2></div>
    <ol class="tl rv">
      <li><span class="when">En curso</span><div><h3>Cohorte MAMA-LE8</h3><p>Estudio prospectivo en tres sitios de la Federación Argentina de Cardiología: Buenos Aires, Córdoba y Rosario. Fase I dirigida a mujeres de 45 a 65 años en CABA.</p></div></li>
      <li><span class="when">Q4 2026</span><div><h3>Consenso de contenido del Índice EPA</h3><p>Panel Delphi con el Comité de Enfermedades Cardiovasculares en la Mujer de FAC sobre subcomponentes y cortes de puntuación.</p></div></li>
      <li><span class="when">Q1 2027</span><div><h3>Consistencia interna y estructura factorial</h3><p>Análisis sobre el baseline de MAMA-LE8. Hipótesis previa: correlación moderada con LE8. Si fuera muy alta, el índice no aportaría información nueva y habría que rediseñarlo.</p></div></li>
      <li><span class="when">Q2–Q3 2027</span><div><h3>Recalibración empírica de ponderaciones</h3><p>Si los pesos empíricos difieren de 36/33/31, adoptamos los empíricos y lo documentamos como versión 2.0 del índice.</p></div></li>
      <li><span class="when">2029 +</span><div><h3>Validez predictiva</h3><p>Seguimiento longitudinal contra eventos cardiovasculares incidentes. Es la única etapa que habilita a reclamar valor pronóstico.</p></div></li>
    </ol>
  </div>
</section>

<section class="band band-alt">
  <div class="wrap">
    <div class="head rv"><p class="eyebrow">Producto</p><h2>Plataforma</h2></div>
    <ol class="tl rv">
      <li><span class="when">En curso</span><div><h3>Índice EPA en producción</h3><p>Motor de puntuación sobre Medplum, con las reglas de seguridad clínica como requisito bloqueante de despliegue.</p></div></li>
      <li><span class="when">2026</span><div><h3>Canal conversacional en WhatsApp</h3><p>Captura de outcomes reportados por la paciente en español rioplatense, con persistencia directa como recursos FHIR.</p></div></li>
      <li><span class="when">2026</span><div><h3>Módulo de cardio-oncología</h3><p>En desarrollo junto al Hospital Municipal de Oncología Marie Curie.</p></div></li>
      <li><span class="when">2027</span><div><h3>Longevity Passport</h3><p>Credencial verificable W3C sobre FHIR DocumentReference: la usuaria se lleva su historia cardiovascular en formato portable y verificable.</p></div></li>
    </ol>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="head rv">
      <p class="eyebrow">Infraestructura de IA</p>
      <h2>Investigación federada</h2>
      <p class="lede">El objetivo no es entrenar modelos con datos centralizados. Es entrenar sin
      mover los datos de su jurisdicción de origen.</p>
    </div>
    <div class="cards rv">
      <div class="card"><div class="kicker">Prioridad 1</div><h3>Aprendizaje federado entre sitios FAC</h3><p>Entrenar modelos a través de los sitios sin que los datos de las pacientes salgan de cada institución.</p></div>
      <div class="card"><div class="kicker">Prioridad 1</div><h3>Analítica sobre FHIR</h3><p>Procesamiento acelerado para generación de evidencia de mundo real a partir del repositorio FAVALORO.</p></div>
      <div class="card"><div class="kicker">Prioridad 1</div><h3>Transcripción de voz en español</h3><p>Para el canal conversacional: que una mujer pueda reportar sus síntomas hablando, no escribiendo.</p></div>
      <div class="card"><div class="kicker">12–24 meses</div><h3>Modelo clínico en español</h3><p>Ajuste fino de un modelo de lenguaje para terminología clínica en español rioplatense.</p></div>
      <div class="card"><div class="kicker">Regional</div><h3>Expansión LatAm</h3><p>México y California como primeros mercados, con FAVALORO como columna de investigación federada regional.</p></div>
      <div class="card"><div class="kicker">Abierto</div><h3>Lo que todavía no sabemos</h3><p>Hay decisiones de arquitectura sin cerrar. Cuando se cierren, esta página se actualiza.</p></div>
    </div>
  </div>
</section>

<section class="band band-alt">
  <div class="wrap">
    <div class="callout callout-info rv" style="max-width:80ch">
      <p><b>Sobre las declaraciones a futuro.</b> Este roadmap describe planes e intenciones a la
      fecha de publicación. No constituye un compromiso contractual ni una oferta de inversión.
      Las prioridades pueden cambiar según los resultados de validación clínica, la disponibilidad
      de financiamiento y el contexto regulatorio.</p>
    </div>
  </div>
</section>
""" + CTA)

# ═══════════════════════════════════════════════════════════════
# 5 · INTEGRACIONES
# ═══════════════════════════════════════════════════════════════
PAGES["integraciones.html"] = dict(
    title="Integraciones", active="estandares",
    desc="Wearables, laboratorios, sistemas de historia clínica y API FHIR R4. Cómo se conecta EPA Bienestar con el resto del ecosistema de salud.",
    body=phero(
        "Integraciones", "Estándares en salud digital",
        "Interoperar no es una función. Es la arquitectura.",
        "Todo lo que entra a la plataforma se guarda como un recurso FHIR R4 con su código LOINC "
        "o SNOMED CT. Un sistema externo puede leer nuestros datos sin traducción intermedia.",
        "Endpoint FHIR",
        [("Estándar", "HL7 FHIR R4"), ("Base", "api.epa-bienestar.com.ar"),
         ("Terminología", "LOINC · SNOMED CT"), ("Región", "AWS Local Zone Buenos Aires"),
         ("Auth", "OAuth 2.0 · SMART on FHIR")]) + """
<section class="band">
  <div class="wrap">
    <div class="head rv"><p class="eyebrow">Fuentes de datos</p><h2>De dónde vienen las mediciones</h2></div>
    <div class="cards rv">
      <div class="card"><div class="kicker">Wearables</div><h3>openwearables.io</h3><p>Integración con Oura, Apple Watch y Google Fit. Alimenta la dimensión Equilibrio: regularidad del sueño, variabilidad de la frecuencia cardíaca y actividad.</p></div>
      <div class="card"><div class="kicker">Domiciliario</div><h3>Presión arterial</h3><p>Series de mediciones domiciliarias, protocolo de siete días. Es el insumo de la variabilidad de presión, que es la señal más específica de la transición.</p></div>
      <div class="card"><div class="kicker">Laboratorio</div><h3>Perfil bioquímico</h3><p>Lípidos, ApoB, glucemia, HbA1c, función renal y lipoproteína(a). Ingresa con código LOINC desde el inicio.</p></div>
      <div class="card"><div class="kicker">Conversacional</div><h3>WhatsApp Business</h3><p>Captura de síntomas y cuestionarios validados en español rioplatense. Cada respuesta se guarda como QuestionnaireResponse.</p></div>
      <div class="card"><div class="kicker">Clínico</div><h3>Historia clínica</h3><p>Intercambio bidireccional con sistemas de historia clínica que hablen FHIR. Sin exportaciones manuales.</p></div>
      <div class="card"><div class="kicker">Portal</div><h3>Autogestión</h3><p>La usuaria carga y consulta sus propios datos desde el portal, y puede llevárselos cuando quiera.</p></div>
    </div>
  </div>
</section>

<section class="band band-alt">
  <div class="wrap">
    <div class="head rv"><p class="eyebrow">Para equipos técnicos</p><h2>Cómo se modelan los datos</h2></div>
    <div class="tbl-wrap rv">
      <table class="tbl">
        <thead><tr><th>Qué se mide</th><th>Recurso FHIR</th><th>Código</th></tr></thead>
        <tbody>
          <tr><td>Presión arterial sistólica</td><td>Observation</td><td><code>LOINC 8480-6</code></td></tr>
          <tr><td>Duración del sueño</td><td>Observation</td><td><code>LOINC 93832-4</code></td></tr>
          <tr><td>Índice de masa corporal</td><td>Observation</td><td><code>LOINC 39156-5</code></td></tr>
          <tr><td>Colesterol LDL calculado</td><td>Observation</td><td><code>LOINC 13457-7</code></td></tr>
          <tr><td>Lipoproteína(a) molar</td><td>Observation</td><td><code>LOINC 43583-4</code></td></tr>
          <tr><td>Puntaje total Life's Essential 8</td><td>Observation</td><td><code>LOINC 96607-7</code></td></tr>
          <tr><td>Estratificación de riesgo</td><td>RiskAssessment</td><td><code>epa-dim-precision</code></td></tr>
          <tr><td>Cuestionarios de la paciente</td><td>QuestionnaireResponse</td><td><code>epa-mrs</code></td></tr>
          <tr><td>Historia familiar</td><td>FamilyMemberHistory</td><td><code>SNOMED CT</code></td></tr>
          <tr><td>Índice EPA compuesto</td><td>Observation</td><td><code>epa-index-total</code></td></tr>
        </tbody>
      </table>
    </div>
    <div class="callout callout-info rv" style="margin-top:26px;max-width:80ch">
      <p><b>Cuando no existe código estándar, lo decimos.</b> STRAW+10, los subcomponentes derivados
      y los puntajes compuestos usan un sistema de códigos local publicado, con texto descriptivo.
      Es práctica FHIR válida y preferible a forzar un código incorrecto.</p>
    </div>
    <div class="rv" style="margin-top:26px">
      <a class="btn btn-solid" href="https://app.epa-bienestar.com.ar">Documentación para desarrolladores</a>
    </div>
  </div>
</section>
""" + CTA)

# ═══════════════════════════════════════════════════════════════
# 6 · ENGAGEMENT
# ═══════════════════════════════════════════════════════════════
PAGES["engagement.html"] = dict(
    title="Experiencias y desafíos", active=None,
    desc="Cómo diseñamos la adherencia: el determinante conductual pesa 36 %, y es el más modificable. Plan Bienestar 100 Días®, MEPA-Express y SBAE.",
    body=phero(
        "Experiencias y desafíos", "Adherencia",
        "El 36 % del resultado depende del comportamiento.",
        "Es el determinante de mayor peso y también el único que una persona puede cambiar esta "
        "semana. Toda nuestra mecánica de adherencia se apoya en ese número.") + """
<section class="band">
  <div class="wrap prose rv">
    <h3>Por qué cien días</h3>
    <p><strong>Plan Bienestar 100 Días®</strong> no dura cien días por marketing. Es la ventana
    mínima en la que un cambio conductual sostenido produce un desplazamiento medible en las
    métricas de Life's Essential 8, y suficientemente corta como para que una persona la
    visualice completa desde el día uno.</p>
    <p>El resultado del plan se mide con <strong>Δ-EPA</strong>: la diferencia del índice entre el
    día 0 y el día 100. Excluimos deliberadamente la dimensión Precisión de ese cálculo, porque
    Lp(a) es fija y el estadio menopáusico solo avanza. Incluirla penalizaría a la paciente
    simplemente por envejecer.</p>
  </div>
</section>

<section class="band band-alt">
  <div class="wrap">
    <div class="head rv"><p class="eyebrow">Instrumentos</p><h2>Herramientas adaptadas, no traducidas</h2></div>
    <div class="cards rv">
      <div class="card"><div class="kicker">Nutrición</div><h3>MEPA-Express</h3><p>Tamizaje dietario de ocho ítems adaptado al patrón alimentario argentino. Una traducción literal de un cuestionario mediterráneo no sirve acá.</p></div>
      <div class="card"><div class="kicker">Actividad</div><h3>SBAE</h3><p>Sesiones breves acumuladas de ejercicio. Diseñado para agendas reales: la evidencia sostiene que la acumulación importa más que la sesión larga.</p></div>
      <div class="card"><div class="kicker">Sueño</div><h3>Regularidad antes que duración</h3><p>Trabajamos sobre la consistencia del horario, no sobre alcanzar ocho horas. La regularidad predice mejor los resultados.</p></div>
      <div class="card"><div class="kicker">Síntomas</div><h3>Menopause Rating Scale</h3><p>Once ítems en tres subescalas. Reportamos las subescalas por separado porque la distribución orienta la intervención.</p></div>
      <div class="card"><div class="kicker">Ánimo</div><h3>Seguimiento integrado</h3><p>Ánimo y ansiedad se miden con instrumentos validados y forman parte del índice, no de un módulo aparte.</p></div>
      <div class="card"><div class="kicker">Social</div><h3>Comunidad</h3><p>El determinante social pesa 24 %. Los grupos de acompañamiento no son un extra: son una intervención sobre ese porcentaje.</p></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap prose rv">
    <h3>Qué evitamos deliberadamente</h3>
    <p>Hay mecánicas de adherencia que funcionan a corto plazo y hacen daño a mediano plazo.
    No las usamos:</p>
    <ul>
      <li><strong>No hay rachas que se rompen.</strong> Perder una racha genera abandono, no motivación.</li>
      <li><strong>No hay comparación entre usuarias.</strong> Los rankings públicos de peso o actividad son un riesgo conocido en salud femenina.</li>
      <li><strong>No usamos culpa como palanca.</strong> Los mensajes no reprochan; describen y proponen el siguiente paso.</li>
      <li><strong>No mostramos el número cuando el número hace daño.</strong> En la banda de riesgo más alta del índice, la usuaria ve la derivación clínica, no el puntaje.</li>
    </ul>
  </div>
</section>
""" + CTA)

# ═══════════════════════════════════════════════════════════════
# 7 · PREVENCIÓN / SEGUIMIENTO
# ═══════════════════════════════════════════════════════════════
PAGES["prevencion.html"] = dict(
    title="Seguimiento", active=None,
    desc="Cómo funciona el seguimiento longitudinal: bandas de riesgo, reglas de escalamiento clínico y derivación a la red de la Federación Argentina de Cardiología.",
    body=phero(
        "Seguimiento", "Prevención",
        "Un índice sin escalamiento clínico es un número suelto.",
        "El seguimiento no termina en un puntaje. Cada banda de riesgo tiene una acción asociada, "
        "un plazo y un responsable identificado.") + """
<section class="band">
  <div class="wrap">
    <div class="head rv"><p class="eyebrow">Bandas</p><h2>Qué pasa según el resultado</h2></div>
    <div class="tbl-wrap rv">
      <table class="tbl">
        <thead><tr><th style="width:14%">Índice EPA</th><th style="width:26%">Lectura clínica</th><th>Acción</th></tr></thead>
        <tbody>
          <tr><td><strong>85 – 100</strong></td><td>Transición gobernada</td><td>Mantener el plan. Reevaluación a 90 días.</td></tr>
          <tr><td><strong>70 – 84</strong></td><td>Favorable con margen</td><td>Plan Bienestar 100 Días® en intensidad estándar.</td></tr>
          <tr><td><strong>55 – 69</strong></td><td>Intermedia</td><td>Plan intensificado y consulta cardiológica programada.</td></tr>
          <tr><td><strong>40 – 54</strong></td><td>En riesgo</td><td>Derivación a cardiólogo de la red FAC dentro de 30 días.</td></tr>
          <tr><td><strong>Menos de 40</strong></td><td>Alto riesgo</td><td class="yes">Derivación prioritaria dentro de 7 días. No se muestra el número a la paciente sin acompañamiento clínico.</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="band band-alt">
  <div class="wrap">
    <div class="head rv">
      <p class="eyebrow">Seguridad clínica</p>
      <h2>Reglas que interrumpen el sistema</h2>
      <p class="lede">Hay situaciones en las que calcular un puntaje sería lo incorrecto. En esos
      casos el sistema se detiene y notifica a una persona.</p>
    </div>
    <div class="tbl-wrap rv">
      <table class="tbl">
        <thead><tr><th style="width:38%">Situación</th><th>Respuesta</th></tr></thead>
        <tbody>
          <tr><td>Indicio de ideación suicida en un cuestionario</td><td class="yes">Se interrumpe el cuestionario, no se muestra puntaje, se despliegan recursos de crisis y se notifica al equipo clínico en menos de 15 minutos. Requiere acuse de recibo de una persona identificada.</td></tr>
          <tr><td>Presión arterial en rango de crisis</td><td>Alerta inmediata e indicación de consulta sin demora.</td></tr>
          <tr><td>Presión elevada sostenida en tres mediciones</td><td>Derivación dentro de 72 horas.</td></tr>
          <tr><td>Glucemia en ayunas muy elevada</td><td>Derivación dentro de 7 días.</td></tr>
          <tr><td>Lipoproteína(a) muy elevada</td><td>Aviso al cardiólogo tratante y recomendación de tamizaje familiar en cascada.</td></tr>
          <tr><td>Mención de dolor torácico en el canal conversacional</td><td class="yes">Respuesta de emergencia inmediata. No se puntúa nada.</td></tr>
        </tbody>
      </table>
    </div>
    <div class="callout callout-warn rv" style="margin-top:26px;max-width:80ch">
      <p><b>El escalamiento no se automatiza a una respuesta de chatbot.</b> Una paciente que
      reporta ideación suicida no debe recibir un puntaje: debe recibir una persona. Si el equipo
      clínico no acusa recibo dentro de la hora, la alerta escala al contacto secundario.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap prose rv">
    <h3>Seguimiento del cierre</h3>
    <p>Una derivación emitida no es una derivación cumplida. Cuando el sistema genera una derivación
    prioritaria y no registra la consulta correspondiente a los catorce días, el caso escala al
    coordinador clínico. El circuito se cierra o se explica; no queda abierto en silencio.</p>
    <h3>Para profesionales</h3>
    <p>El equipo de salud accede al panel de seguimiento con la trazabilidad completa de cada dato
    de entrada. Puede reconstruir cualquier puntaje desde los valores crudos.</p>
    <p><a href="https://seguimiento.epa-bienestar.com.ar">Ir al panel de seguimiento →</a> ·
    <a href="modelo_de_atencion.html">Ver el modelo de atención →</a></p>
  </div>
</section>
""" + CTA)

# ═══════════════════════════════════════════════════════════════
# 8 · MODELO DE ATENCIÓN
# ═══════════════════════════════════════════════════════════════
PAGES["modelo_de_atencion.html"] = dict(
    title="Modelo de atención", active="modelo",
    desc="Cómo trabaja el equipo de salud de EPA Bienestar: complemento del médico tratante, nunca reemplazo. Roles, alcance y límites explícitos.",
    body=phero(
        "Modelo de atención", "Cómo trabajamos",
        "Complementamos al equipo médico. No lo reemplazamos.",
        "Esta distinción no es diplomacia: define qué hacemos, qué no hacemos y dónde termina "
        "nuestra responsabilidad.") + """
<section class="band">
  <div class="wrap">
    <div class="cards cards-2 rv">
      <div class="card">
        <div class="kicker">Sí hacemos</div>
        <h3>Nuestro alcance</h3>
        <p>Evaluación estructurada de salud cardiovascular con el marco Life's Essential 8.</p>
        <p>Seguimiento longitudinal de variabilidad fisiológica y síntomas reportados.</p>
        <p>Educación y acompañamiento sobre los determinantes modificables.</p>
        <p>Detección de señales que ameritan consulta y derivación a la red cardiológica.</p>
        <p>Entrega de información estructurada e interoperable al médico tratante.</p>
      </div>
      <div class="card">
        <div class="kicker">No hacemos</div>
        <h3>Nuestros límites</h3>
        <p>No diagnosticamos ninguna condición médica.</p>
        <p>No indicamos, suspendemos ni ajustamos medicación.</p>
        <p>No interpretamos electrocardiogramas ni estudios de imagen.</p>
        <p>No atendemos urgencias. Ante una emergencia hay que llamar al servicio de emergencias.</p>
        <p>No sustituimos la evaluación de un profesional de la salud.</p>
      </div>
    </div>
  </div>
</section>

<section class="band band-alt">
  <div class="wrap">
    <div class="head rv"><p class="eyebrow">Recorrido</p><h2>Cómo es el proceso</h2></div>
    <ol class="tl rv">
      <li><span class="when">Paso 1</span><div><h3>Evaluación inicial</h3><p>Diez minutos. Devuelve el punto de partida con el marco Life's Essential 8 y define el grupo de vida correspondiente.</p></div></li>
      <li><span class="when">Paso 2</span><div><h3>Línea de base ampliada</h3><p>Incorporación de laboratorio, mediciones domiciliarias y dispositivos. Acá se calcula el primer Índice EPA, siempre acompañado de su nivel de completitud.</p></div></li>
      <li><span class="when">Paso 3</span><div><h3>Plan Bienestar 100 Días®</h3><p>Plan personalizado según grupo de vida, perfil de riesgo y carga sintomática. Con seguimiento continuo.</p></div></li>
      <li><span class="when">Paso 4</span><div><h3>Monitoreo y escalamiento</h3><p>Las reglas de seguridad clínica corren antes que cualquier cálculo. Si una señal lo amerita, el sistema se detiene y notifica a una persona.</p></div></li>
      <li><span class="when">Paso 5</span><div><h3>Cierre y reevaluación</h3><p>Se calcula el Δ-EPA a 100 días y se comparte el informe estructurado con el médico tratante.</p></div></li>
    </ol>
  </div>
</section>

<section class="band">
  <div class="wrap prose rv">
    <h3>La relación con tu médico</h3>
    <p>Si ya tenés cardiólogo, ginecólogo o clínico de cabecera, el rol de EPA es <strong>darles
    mejor información entre consulta y consulta</strong>. Un médico ve a su paciente unas pocas
    veces al año; nosotros aportamos lo que pasa en el medio, en formato estándar y trazable.</p>
    <p>Si no tenés especialista, podemos conectarte con la red de la Federación Argentina de
    Cardiología: 38 sociedades federadas distribuidas en 24 provincias.</p>
    <h3>Quién ve tus datos</h3>
    <p>Vos, siempre. El equipo de salud de EPA en la medida necesaria para el seguimiento. Los
    profesionales que vos autorices explícitamente. Nadie más.
    <a href="politica_de_privacidad.html">Ver la política de privacidad →</a></p>
  </div>
</section>
""" + CTA)

# ═══════════════════════════════════════════════════════════════
# 9 · ENLACES / PROGRAMAS
# ═══════════════════════════════════════════════════════════════
PAGES["enlaces.html"] = dict(
    title="Programas", active="programa",
    desc="Programa Mujer, Plan Bienestar 100 Días®, MAMA-LE8 y Programa Residentes FRICCAR. Todos los programas de EPA Bienestar IA.",
    body=phero(
        "Programas", "Programa Mujer y más",
        "Cuatro etapas. Una misma infraestructura.",
        "Entramos por la transición menopáusica, porque es el momento en que el riesgo "
        "cardiovascular femenino se vuelve visible. Desde ahí vamos hacia atrás y hacia adelante.") + """
<section class="band">
  <div class="wrap">
    <div class="grp rv">
      <article class="grp-c"><div class="grp-l">A</div><div class="age">18 – 30</div><h3>Crecimiento y desarrollo</h3><p>Establecer hábitos cardiovasculares que duran toda la vida, durante la etapa académica y los primeros años profesionales.</p></article>
      <a class="grp-c" href="embarazo.html" style="text-decoration:none;color:inherit"><div class="grp-l">B</div><div class="age">28 – 44</div><h3>Maternidad planificada</h3><p>Preparación preconcepcional, seguimiento cardio-obstétrico y recuperación posparto.</p><p style="font-family:var(--f-mono);font-size:10.5px;letter-spacing:.11em;text-transform:uppercase;color:var(--teal);margin-top:12px">Ver el programa →</p></a>
      <a class="grp-c is-focus" href="menopausia.html" style="text-decoration:none;color:inherit"><span class="tag">Foco 2026</span><div class="grp-l">C</div><div class="age">45 – 65</div><h3>Transición menopáusica</h3><p>El punto de inflexión cardiovascular. Donde el Índice EPA se aplica primero y donde se concentra la validación clínica.</p><p style="font-family:var(--f-mono);font-size:10.5px;letter-spacing:.11em;text-transform:uppercase;color:var(--plum);margin-top:12px">Ver el programa →</p></a>
      <article class="grp-c"><div class="grp-l">D</div><div class="age">65 +</div><h3>Envejecimiento activo</h3><p>Prevención secundaria, función física y comunidad. Abuelas, emprendedoras, viajeras.</p></article>
    </div>
  </div>
</section>

<section class="band band-alt">
  <div class="wrap">
    <div class="head rv"><p class="eyebrow">Programas</p><h2>Todo lo que está en marcha</h2></div>
    <div class="cards rv">
      <a class="card" href="https://info.epa-bienestar.com.ar/"><div class="kicker">Producto principal</div><h3>Plan Bienestar 100 Días®</h3><p>El programa de intervención personalizado. Cien días con seguimiento continuo y medición de resultado mediante Δ-EPA.</p></a>
      <a class="card" href="bienestar_con_datos.html#indice"><div class="kicker">Instrumento</div><h3>Índice EPA</h3><p>Equilibrio, Precisión y Armonía. Tres capas que Life's Essential 8 no tiene.</p></a>
      <a class="card" href="https://info.epa-bienestar.com.ar/evaluacion-inicial.php"><div class="kicker">Gratuito</div><h3>Evaluación inicial</h3><p>Diez minutos para conocer tu punto de partida con el marco Life's Essential 8. Sin costo.</p></a>
      <a class="card" href="programa/residentes/index.html"><div class="kicker">Profesionales</div><h3>Programa Residentes · FRICCAR</h3><p>Factores de riesgo cardiovascular de los residentes y cardiólogos argentinos. ¿Cómo se cuidan los que cuidan?</p></a>
      <a class="card" href="embarazo.html"><div class="kicker">Grupo B</div><h3>Embarazo y corazón</h3><p>El embarazo es una prueba de esfuerzo cardiovascular. Antes, durante y después: qué medir y por qué importa décadas más tarde.</p></a>
      <div class="card"><div class="kicker">Investigación</div><h3>MAMA-LE8</h3><p>Cohorte prospectiva en tres sitios de la Federación Argentina de Cardiología. Es la base de validación del Índice EPA.</p></div>
      <div class="card"><div class="kicker">En desarrollo</div><h3>Cardio-oncología</h3><p>Módulo específico para pacientes oncológicas, junto al Hospital Municipal de Oncología Marie Curie.</p></div>
    </div>
  </div>
</section>
""" + CTA)

# ═══════════════════════════════════════════════════════════════
# 10 · PROGRAMA RESIDENTES (subcarpeta, depth=2)
# ═══════════════════════════════════════════════════════════════
PAGES["programa/residentes/index.html"] = dict(
    title="Programa Residentes · FRICCAR", active=None, depth=2,
    desc="FRICCAR: factores de riesgo cardiovascular de los residentes y cardiólogos argentinos. ¿Cómo se cuidan los que cuidan?",
    body=phero(
        '<a href="../../enlaces.html">Programas</a><span>/</span>Residentes',
        "FRICCAR", "¿Cómo se cuidan los que cuidan?",
        "Factores de riesgo cardiovascular de los residentes y cardiólogos argentinos. "
        "Guardias, turnos rotativos y sueño fragmentado son exactamente el perfil de exposición "
        "que estudiamos en nuestras pacientes.", depth=2) + """
<section class="band">
  <div class="wrap prose rv">
    <h3>Por qué este programa</h3>
    <p>El personal de salud en formación acumula una combinación de exposiciones poco frecuente:
    privación crónica de sueño, irregularidad extrema del ritmo circadiano, alimentación
    desorganizada por disponibilidad y una carga de estrés sostenida durante años.</p>
    <p>Es, casi punto por punto, el perfil de variabilidad fisiológica que el Índice EPA fue
    diseñado para detectar. Y es una población que rara vez se mide a sí misma.</p>

    <h3>Qué mide FRICCAR</h3>
    <ul>
      <li>Perfil de riesgo cardiovascular con el marco Life's Essential 8.</li>
      <li>Regularidad del ritmo sueño-vigilia durante ciclos de guardia.</li>
      <li>Variabilidad de la frecuencia cardíaca contra el basal propio de cada participante.</li>
      <li>Carga de estrés percibido y salud mental.</li>
      <li>Comparación entre residentes y cardiólogos con años de ejercicio.</li>
    </ul>

    <h3>Participación</h3>
    <p>La participación es voluntaria y los datos individuales son confidenciales. Los resultados
    se reportan de forma agregada. Todo protocolo pasa por evaluación de un Comité de Ética en
    Investigación antes de comenzar.</p>
    <p>Si sos residente o cardiólogo y querés participar,
    <a href="https://docs.google.com/forms/d/e/1FAIpQLSeqeXaSt2gi3CbaCO1xVIIRwdxittwh5AYaSoj8VuLSQ4OMOg/viewform">escribinos</a>
    o agendá una conversación en
    <a href="https://www.calendly.com/epabienestar/entrevistas">Calendly</a>.</p>
  </div>
</section>

<section class="band band-alt">
  <div class="wrap">
    <div class="callout callout-info rv" style="max-width:80ch">
      <p><b>Un apunte sobre reciprocidad.</b> Pedimos a los profesionales de la salud que confíen
      en nuestra plataforma para sus pacientes. Nos parece razonable ofrecerles primero la misma
      herramienta para ellos mismos.</p>
    </div>
  </div>
</section>
""" + CTA)

# ═══════════════════════════════════════════════════════════════
# 11 · POLÍTICA DE PRIVACIDAD
# ═══════════════════════════════════════════════════════════════
_PRIV_SECS = [
    ("responsable", "Responsable del tratamiento", """
    <p>EPA Bienestar IA, con domicilio en Húsares 2248, CP 1428, Ciudad Autónoma de Buenos Aires,
    Argentina, es responsable del tratamiento de los datos personales recogidos a través de sus
    plataformas. Contacto: <a href="mailto:hola@epa-bienestar.com">hola@epa-bienestar.com</a>.</p>"""),
    ("marco", "Marco legal aplicable", """
    <p>El tratamiento se rige por la <strong>Ley 25.326</strong> de Protección de Datos Personales
    y su reglamentación, la <strong>Ley 26.529</strong> de Derechos del Paciente, Historia Clínica
    y Consentimiento Informado, y la <strong>Ley 25.506</strong> de Firma Digital cuando corresponde.
    La base de datos se encuentra <strong>inscripta en el Registro Nacional de Bases de Datos</strong> de la Agencia de Acceso a la Información Pública (AAIP). La constancia de inscripción puede verificarse en el <a href="https://www.argentina.gob.ar/aaip/datospersonales/reclama/20205419935--RL-2023-154634293-APN-DNPDP#AAIP" target="_blank" rel="noopener">registro público de la AAIP</a>.</p>"""),
    ("datos", "Qué datos tratamos", """
    <p>Tratamos las siguientes categorías de datos:</p>
    <ul>
      <li><strong>Identificación y contacto:</strong> nombre, fecha de nacimiento, correo electrónico, teléfono.</li>
      <li><strong>Datos de salud (dato sensible):</strong> mediciones clínicas, resultados de laboratorio, síntomas reportados, respuestas a cuestionarios validados y antecedentes familiares.</li>
      <li><strong>Datos de dispositivos:</strong> métricas de actividad, sueño y frecuencia cardíaca provenientes de los wearables que la persona decida conectar.</li>
      <li><strong>Datos de uso:</strong> registros técnicos de acceso a la plataforma.</li>
    </ul>
    <p>Los datos de salud son <strong>datos sensibles</strong> en los términos del artículo 2 de la
    Ley 25.326 y reciben el nivel de protección más alto previsto por esa norma.</p>"""),
    ("finalidad", "Para qué los usamos", """
    <ul>
      <li>Calcular la evaluación cardiovascular y el Índice EPA.</li>
      <li>Brindar seguimiento longitudinal y ejecutar las reglas de seguridad clínica.</li>
      <li>Facilitar la derivación a profesionales de la salud cuando corresponde.</li>
      <li>Mejorar la plataforma mediante análisis agregados.</li>
      <li>Cumplir obligaciones legales y requerimientos de autoridad competente.</li>
    </ul>
    <p><strong>No vendemos datos personales.</strong> No cedemos datos de salud identificables a
    terceros con fines comerciales o publicitarios.</p>"""),
    ("consentimiento", "Consentimiento", """
    <p>El tratamiento de datos de salud requiere <strong>consentimiento libre, expreso e informado</strong>,
    otorgado por escrito o por medio equivalente. El consentimiento se solicita de forma separada
    para cada finalidad y puede revocarse en cualquier momento sin efecto retroactivo sobre los
    tratamientos ya realizados.</p>
    <p>La participación en protocolos de investigación requiere un consentimiento adicional y
    específico, evaluado previamente por un Comité de Ética en Investigación.</p>"""),
    ("investigacion", "Uso en investigación", """
    <p>Los datos pueden utilizarse con fines de investigación clínica y epidemiológica únicamente
    en forma <strong>disociada o anonimizada</strong>, o bien de forma identificable cuando exista
    consentimiento específico y aprobación de un Comité de Ética en Investigación.</p>
    <p>En los estudios de aprendizaje federado, los datos <strong>no salen de la institución de
    origen</strong>: lo que se comparte son parámetros de modelo, no registros de pacientes.</p>"""),
    ("donde", "Dónde se almacenan", """
    <p>La infraestructura se aloja en <strong>AWS Local Zone Buenos Aires</strong>. Los datos de las
    pacientes argentinas permanecen en territorio argentino. Cualquier transferencia internacional
    se realiza únicamente hacia jurisdicciones con nivel de protección adecuado o mediante
    garantías contractuales, y siempre con notificación previa.</p>"""),
    ("seguridad", "Medidas de seguridad", """
    <ul>
      <li>Cifrado en tránsito y en reposo.</li>
      <li>Control de acceso por rol y registro de auditoría de cada consulta a datos de salud.</li>
      <li>Trazabilidad de origen (Provenance) en cada recurso clínico.</li>
      <li>Revisión periódica de seguridad con socio especializado.</li>
    </ul>
    <p>Ningún sistema es invulnerable. Ante un incidente que afecte datos personales, notificamos
    a las personas afectadas y a la autoridad de control conforme a la normativa vigente.</p>"""),
    ("plazos", "Cuánto tiempo los conservamos", """
    <p>Los datos de historia clínica se conservan por los plazos que fija la Ley 26.529. El resto
    de los datos se conserva mientras exista relación con la persona usuaria y por los plazos
    legales aplicables posteriores. Cumplidos esos plazos, se eliminan o anonimizan de forma
    irreversible.</p>"""),
    ("derechos", "Tus derechos", """
    <p>Podés ejercer en cualquier momento los derechos de <strong>acceso, rectificación,
    actualización, supresión y portabilidad</strong> de tus datos, escribiendo a
    <a href="mailto:hola@epa-bienestar.com">hola@epa-bienestar.com</a>. La respuesta se brinda en
    los plazos que establece la Ley 25.326.</p>
    <p>La portabilidad se entrega en formato estándar HL7 FHIR R4: tus datos son tuyos y te los
    podés llevar en un formato que otro sistema pueda leer.</p>
    <p>La Agencia de Acceso a la Información Pública, en su carácter de órgano de control de la
    Ley 25.326, tiene la atribución de atender denuncias y reclamos por incumplimiento de las
    normas de protección de datos personales.</p>"""),
    ("cookies", "Cookies y analítica", """
    <p>Usamos cookies y herramientas de analítica —Google Analytics 4— para entender qué
    contenidos resultan útiles y dónde se traba la navegación. Concretamente:</p>
    <ul>
      <li><strong>No hacemos publicidad ni remarketing.</strong> El almacenamiento publicitario
      está deshabilitado por configuración, no solo por política: las señales de Google y la
      personalización de anuncios están desactivadas en el código.</li>
      <li><strong>No enviamos datos de salud a la analítica.</strong> Ninguna respuesta a un
      cuestionario, ningún síntoma marcado y ninguna medición clínica sale hacia Google Analytics
      ni hacia ningún tercero. Los datos clínicos viven exclusivamente en nuestra infraestructura
      en Argentina.</li>
      <li><strong>La dirección IP se anonimiza.</strong></li>
      <li><strong>Podés desactivar la analítica</strong> desde el aviso que aparece en tu primera
      visita. La preferencia queda guardada en tu navegador.</li>
    </ul>
    <p>También usamos almacenamiento local para recordar preferencias de visualización, como el
    modo claro u oscuro. Ese dato no sale de tu dispositivo.</p>"""),
    ("menores", "Personas menores de edad", """
    <p>Las plataformas de EPA Bienestar IA están dirigidas a personas mayores de 18 años. No
    recogemos datos de personas menores de edad de forma deliberada. Si detectamos que se cargaron
    datos de una persona menor sin la autorización correspondiente, los eliminamos.</p>"""),
    ("cambios", "Cambios en esta política", """
    <p>Si modificamos esta política de forma sustancial, lo comunicamos por los canales de contacto
    registrados con antelación razonable a su entrada en vigencia.</p>"""),
]

_PRIV_TOC = "\n".join(f'        <li><a href="#{i}">{t}</a></li>' for i, t, _ in _PRIV_SECS)
_PRIV_BODY = "\n".join(f'    <h3 id="{i}">{t}</h3>{c}' for i, t, c in _PRIV_SECS)

PAGES["politica_de_privacidad.html"] = dict(
    title="Política de privacidad", active=None,
    desc="Cómo trata EPA Bienestar IA tus datos personales y de salud, bajo Ley 25.326 y Ley 26.529.",
    body=phero("Política de privacidad", "Legales", "Política de privacidad",
               "Tus datos de salud son datos sensibles y los tratamos como tales. "
               "Esta página explica qué recogemos, para qué, dónde vive y cómo lo controlás.") + f"""
<section class="band">
  <div class="wrap legal-grid">
    <nav class="toc" aria-label="Contenido de la página">
      <h4>Contenido</h4>
      <ol>
{_PRIV_TOC}
      </ol>
    </nav>
    <div class="prose">
    <div class="callout callout-warn" style="margin-bottom:34px">
      <p><b>Documento pendiente de revisión legal.</b> Esta versión es un texto base preparado
      por el equipo de producto sobre el marco normativo argentino. Debe ser revisado y validado
      por asesoría legal antes de considerarse definitivo.</p>
    </div>
    <p class="mono" style="color:var(--muted)">Última actualización: agosto de 2026</p>
{_PRIV_BODY}
    </div>
  </div>
</section>
""")

# ═══════════════════════════════════════════════════════════════
# 12 · CONDICIONES DEL SERVICIO
# ═══════════════════════════════════════════════════════════════
_TOS_SECS = [
    ("objeto", "Objeto", """
    <p>Estas condiciones regulan el acceso y uso de las plataformas de EPA Bienestar IA, incluidos
    el portal de la usuaria, el canal conversacional, la evaluación inicial y el Plan Bienestar
    100 Días®. El uso de las plataformas implica la aceptación de estas condiciones.</p>"""),
    ("naturaleza", "Naturaleza del servicio", """
    <div class="callout callout-warn" style="margin:18px 0">
      <p><b>Esto no es un servicio de urgencias ni sustituye la atención médica.</b>
      Ante síntomas de urgencia —dolor de pecho, dificultad respiratoria, pérdida de conciencia,
      debilidad súbita de un lado del cuerpo— hay que llamar al servicio de emergencias o acudir
      a una guardia. No uses esta plataforma para eso.</p>
    </div>
    <p>EPA Bienestar IA ofrece una herramienta de <strong>apoyo a la decisión clínica y
    acompañamiento en prevención</strong>. En particular, el servicio:</p>
    <ul>
      <li><strong>No emite diagnósticos médicos.</strong></li>
      <li><strong>No indica, suspende ni ajusta tratamientos farmacológicos.</strong></li>
      <li><strong>No interpreta electrocardiogramas ni estudios de imagen.</strong></li>
      <li><strong>No sustituye la evaluación de un profesional de la salud matriculado.</strong></li>
    </ul>"""),
    ("indice", "Sobre el Índice EPA", """
    <p>El Índice EPA es un instrumento compuesto en <strong>etapa de validación</strong>. Los
    instrumentos que lo integran están validados individualmente en la literatura científica,
    pero las ponderaciones, los cortes de puntuación y la diferencia mínima clínicamente
    importante son propuestos por EPA y <strong>aún no fueron validados empíricamente</strong>.</p>
    <p>El índice no tiene valor predictivo establecido sobre eventos cardiovasculares. No debe
    utilizarse como único fundamento de ninguna decisión clínica.</p>"""),
    ("cuenta", "Cuenta y uso responsable", """
    <ul>
      <li>Debés ser mayor de 18 años para crear una cuenta.</li>
      <li>La información que cargues debe ser veraz. Los resultados dependen de la calidad del dato de entrada.</li>
      <li>Sos responsable de mantener la confidencialidad de tus credenciales.</li>
      <li>No está permitido usar la plataforma para cargar datos de terceros sin su consentimiento.</li>
      <li>No está permitido el acceso automatizado no autorizado ni la extracción masiva de datos.</li>
    </ul>"""),
    ("profesionales", "Uso por profesionales de la salud", """
    <p>Los profesionales que accedan al panel de seguimiento mantienen la responsabilidad clínica
    plena sobre sus pacientes. La información que provee la plataforma es un insumo adicional y
    no desplaza el criterio profesional ni las obligaciones que impone el ejercicio de la
    profesión.</p>"""),
    ("terceros", "Servicios de terceros", """
    <p>Algunas funciones dependen de servicios de terceros, como la integración con dispositivos
    wearables o el canal de mensajería. La disponibilidad y las condiciones de esos servicios se
    rigen por sus propios términos. No respondemos por interrupciones ajenas a nuestra
    infraestructura.</p>"""),
    ("propiedad", "Propiedad intelectual", """
    <p>PLAN BIENESTAR 100 DÍAS® es marca registrada del Dr. Alejandro Sergio D'Alessandro para EPA
    Bienestar IA. Life's Essential 8™ y PREVENT™ son marcas de la American Heart Association,
    referenciadas con fines científicos y sin implicar patrocinio.</p>
    <p>Los datos de salud de cada persona le pertenecen a esa persona. EPA Bienestar IA los trata
    en los términos de la <a href="politica_de_privacidad.html">política de privacidad</a>.</p>"""),
    ("disponibilidad", "Disponibilidad y cambios", """
    <p>Procuramos mantener el servicio disponible de forma continua, pero puede haber
    interrupciones por mantenimiento o causas de fuerza mayor. Podemos modificar, suspender o
    discontinuar funciones, avisando con antelación razonable cuando el cambio sea sustancial.</p>"""),
    ("responsabilidad", "Limitación de responsabilidad", """
    <p>Dentro de los límites que permite la legislación argentina, EPA Bienestar IA no responde por
    decisiones clínicas tomadas exclusivamente sobre la base de la información de la plataforma,
    sin intervención de un profesional de la salud. Nada en estas condiciones limita
    responsabilidades que la ley declare indisponibles.</p>"""),
    ("baja", "Baja del servicio", """
    <p>Podés dar de baja tu cuenta en cualquier momento escribiendo a
    <a href="mailto:hola@epa-bienestar.com">hola@epa-bienestar.com</a>. Antes de la baja podés
    solicitar la portabilidad de tus datos en formato HL7 FHIR R4.</p>"""),
    ("ley", "Ley aplicable y jurisdicción", """
    <p>Estas condiciones se rigen por la legislación de la República Argentina. Para toda
    controversia, las partes se someten a los tribunales ordinarios competentes de la Ciudad
    Autónoma de Buenos Aires, sin perjuicio de los fueros que resulten irrenunciables para la
    persona usuaria en su carácter de consumidora.</p>"""),
]

_TOS_TOC = "\n".join(f'        <li><a href="#{i}">{t}</a></li>' for i, t, _ in _TOS_SECS)
_TOS_BODY = "\n".join(f'    <h3 id="{i}">{t}</h3>{c}' for i, t, c in _TOS_SECS)

PAGES["condiciones_del_servicio.html"] = dict(
    title="Condiciones del servicio", active=None,
    desc="Condiciones de uso de las plataformas de EPA Bienestar IA, alcance del servicio y límites explícitos.",
    body=phero("Condiciones del servicio", "Legales", "Condiciones del servicio",
               "Qué ofrecemos, qué no, y bajo qué reglas. Escrito para que se entienda, "
               "no para que no se lea.") + f"""
<section class="band">
  <div class="wrap legal-grid">
    <nav class="toc" aria-label="Contenido de la página">
      <h4>Contenido</h4>
      <ol>
{_TOS_TOC}
      </ol>
    </nav>
    <div class="prose">
    <div class="callout callout-warn" style="margin-bottom:34px">
      <p><b>Documento pendiente de revisión legal.</b> Esta versión es un texto base preparado
      por el equipo de producto. Debe ser revisado y validado por asesoría legal antes de
      considerarse definitivo.</p>
    </div>
    <p class="mono" style="color:var(--muted)">Última actualización: agosto de 2026</p>
{_TOS_BODY}
    </div>
  </div>
</section>
""")


# ═══════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════
# 13 · LANDING GRUPO C — menopausia (página de conversión)
# ═══════════════════════════════════════════════════════════════
_ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
          'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h13M13 6l6 6-6 6"/></svg>')

_TRANSLATION = [
    ("Te despertás a las 3 y no volvés a dormirte",
     "Fragmentación del sueño. La regularidad del ritmo sueño-vigilia predice riesgo cardiovascular mejor que la cantidad de horas."),
    ("La ropa te queda distinta aunque la balanza no se mueva",
     "Redistribución de grasa hacia el abdomen. Ocurre con peso estable, y la cintura importa más que el índice de masa corporal."),
    ("Sofocos que aparecen sin aviso",
     "Los síntomas vasomotores moderados a severos se asocian a un perfil de riesgo cardiovascular menos favorable."),
    ("Te sentís más irritable o con menos paciencia",
     "El ánimo forma parte del cuadro clínico de la transición, no es un tema aparte ni un problema de carácter."),
    ("Tu último análisis dio el colesterol más alto que siempre",
     "Durante la transición el colesterol LDL suele subir entre un 10 % y un 15 %, aun sin cambios en la alimentación."),
    ("El médico te dijo que tenés la presión &laquo;un poquito alta&raquo;",
     "Antes de que el promedio suba, lo que aumenta es la variabilidad. Es la señal más temprana y la que casi nunca se mide."),
]
_TR_ROWS = "\n".join(
    f'      <div class="tr2-row"><div class="tr2-felt">{f}</div>'
    f'<div class="tr2-arrow">{_ARROW}</div><div class="tr2-real">{r}</div></div>'
    for f, r in _TRANSLATION)

_RECOG = [
    "Dormís peor que antes", "Sofocos o sudoración nocturna",
    "Cambió la forma de tu cuerpo", "Más cansancio del habitual",
    "Cambios en el ánimo o la ansiedad", "Tu última presión dio elevada",
    "Colesterol o glucemia en alza", "Antecedentes cardíacos en tu familia",
    "Tu menopausia empezó antes de los 45", "Todavía no te hiciste un chequeo cardiovascular",
]
_RECOG_ITEMS = "\n".join(
    f'      <label><input type="checkbox" class="rc" /><span>{t}</span></label>' for t in _RECOG)

_FAQ = [
    ("¿Necesito tener síntomas para hacer la evaluación?", """
      <p>No. De hecho, varias de las cosas que medimos —cómo varía tu presión, cómo se comporta
      tu colesterol, tu lipoproteína(a)— no producen ningún síntoma. Esa es exactamente la razón
      para medirlas.</p>"""),
    ("¿Tengo que dejar a mi ginecóloga o a mi cardiólogo?", """
      <p>No, y preferimos que no. Programa Mujer es un complemento del equipo médico, nunca un
      reemplazo. Nuestro rol es darles mejor información entre consulta y consulta: un profesional
      te ve unas pocas veces al año, y nosotros aportamos lo que pasa en el medio, en un formato
      estándar que su sistema puede leer.</p>
      <p>Si todavía no tenés especialista, podemos conectarte con la red de la Federación Argentina
      de Cardiología.</p>"""),
    ("Estoy haciendo terapia hormonal. ¿Puedo igual?", """
      <p>Sí. El programa es compatible con cualquier tratamiento que estés haciendo. Nosotros no
      indicamos, suspendemos ni ajustamos medicación: esa decisión es de tu médica o médico, con
      tu historia clínica completa a la vista. Lo que sí hacemos es medir cómo evolucionás, y esa
      información le sirve a quien te trata.</p>"""),
    ("¿Necesito un reloj inteligente?", """
      <p>Ayuda, pero no es obligatorio. Si tenés Oura, Apple Watch o Google Fit, los conectás y
      enriquecen la dimensión de variabilidad. Si no tenés, el índice se calcula igual con las
      señales disponibles y te mostramos con qué nivel de completitud lo estamos haciendo.</p>
      <p>Somos explícitos sobre esto porque depender de dispositivos introduce un sesgo
      socioeconómico. Preferimos declararlo antes que disimularlo.</p>"""),
    ("¿Qué es la lipoproteína(a) y por qué la piden?", """
      <p>Es una partícula que determina tu genética y que casi no cambia a lo largo de la vida.
      Eleva el riesgo cardiovascular de forma independiente del colesterol, y se mide
      <strong>una sola vez en la vida</strong>: hecho el análisis, no hace falta repetirlo nunca.</p>
      <p>Está muy poco pedida en Argentina. Es probablemente el estudio con mejor relación entre
      lo que cuesta y lo que informa, y por eso lo incorporamos.</p>"""),
    ("¿Cuánto cuesta?", """
      <p>La evaluación inicial es gratuita y no pide datos de pago. Toma unos diez minutos y te
      devuelve tu punto de partida con el marco Life's Essential 8 de la American Heart Association.</p>
      <p>Si después querés seguir con el Plan Bienestar 100 Días®, las condiciones te las contamos
      al final de la evaluación, sin compromiso.</p>"""),
    ("¿Qué pasa con mis datos?", """
      <p>Son tuyos. Viven en servidores en Argentina, bajo la Ley 25.326, con la base inscripta en
      el Registro Nacional de Bases de Datos de la AAIP. No los vendemos ni los cedemos a terceros
      con fines comerciales.</p>
      <p>Podés pedir que te los entreguemos en formato estándar y llevártelos a otro sistema, o
      pedir que los borremos.
      <a href="politica_de_privacidad.html">Leer la política de privacidad completa →</a></p>"""),
    ("¿Esto me va a decir que baje de peso?", """
      <p>No es el enfoque. El determinante de mayor peso es el comportamiento —36 %—, y trabajamos
      sobre sueño, actividad, alimentación y estrés porque mueven marcadores cardiovasculares, no
      porque haya un número en la balanza que alcanzar.</p>
      <p>En antropometría miramos la trayectoria de la cintura, no el índice de masa corporal,
      porque durante la transición la grasa se redistribuye con peso estable. Y no vendemos
      suplementos ni planes de descenso rápido.</p>"""),
]
_FAQ_ITEMS = "\n".join(
    f'    <details><summary>{q}</summary><div class="ans">{a}\n    </div></details>'
    for q, a in _FAQ)

PAGES["menopausia.html"] = dict(
    title="Menopausia y corazón", active=None, cls="pg-c",
    desc="Durante la transición menopáusica cambia tu riesgo cardiovascular, y casi nadie te lo cuenta. Evaluación inicial gratuita con el marco Life's Essential 8 de la AHA.",
    body="""<section class="phero">
  <div class="wrap">
    <p class="crumb"><a href="index.html">Inicio</a><span>/</span><a href="enlaces.html">Programas</a><span>/</span>Menopausia</p>
    <p class="eyebrow">Mujeres de 45 a 65 · Grupo C</p>
  </div>
  <div class="wrap phero-grid" style="margin-top:6px">
    <div>
      <h1 style="max-width:23ch">Te dijeron que era la menopausia. También es tu corazón.</h1>
      <p class="lede" style="max-width:56ch">Los sofocos y el insomnio son la parte visible. Al mismo
      tiempo, en silencio, cambia tu perfil cardiovascular. Esta es la etapa en que conviene mirarlo
      —y es la que casi nunca se mira.</p>
      <div class="hero-cta">
        <a class="btn btn-solid" data-cta="hero" href="https://info.epa-bienestar.com.ar/evaluacion-inicial.php">Hacer mi evaluación · gratis</a>
        <a class="btn btn-ghost" href="#como">Ver cómo funciona</a>
      </div>
    </div>
    <aside class="card-fx">
      <h4>La evaluación inicial</h4>
      <div class="fx-row"><span class="k">Cuánto dura</span><span class="v">10 minutos</span></div>
      <div class="fx-row"><span class="k">Cuánto cuesta</span><span class="v">Gratis</span></div>
      <div class="fx-row"><span class="k">Datos de pago</span><span class="v">No se piden</span></div>
      <div class="fx-row"><span class="k">Marco clínico</span><span class="v">AHA Life&#39;s Essential 8™</span></div>
      <div class="fx-row"><span class="k">Tus datos</span><span class="v">Servidores en Argentina</span></div>
      <div class="fx-row"><span class="k">Suplementos</span><span class="v">No vendemos</span></div>
    </aside>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="head rv">
      <p class="eyebrow">La traducción</p>
      <h2>Lo que sentís tiene una explicación clínica</h2>
      <p class="lede">No estás imaginando cosas y no es solo cuestión de hormonas. Cada síntoma de
      la izquierda tiene un correlato medible a la derecha.</p>
    </div>
    <div class="tr2 rv">
      <div class="tr2-hd"><div>Lo que sentís</div><div></div><div>Lo que está pasando</div></div>
""" + _TR_ROWS + """
    </div>
    <p class="mono rv" style="color:var(--muted);margin-top:16px">
      Describe hallazgos frecuentes durante la transición menopáusica. No es un diagnóstico
      ni reemplaza una consulta médica.
    </p>
  </div>
</section>

<section class="band band-alt">
  <div class="wrap">
    <div class="head rv">
      <p class="eyebrow">El dato incómodo</p>
      <h2>Las mujeres temen al cáncer. Las mata el corazón.</h2>
    </div>
    <div class="gap-grid rv">
      <div class="gap-cell">
        <div class="num">62 %</div>
        <h3>Cree que el cáncer es su principal amenaza</h3>
        <p>Es lo que se conversa, lo que se chequea y lo que aparece en las campañas.</p>
      </div>
      <div class="gap-cell is-teal">
        <div class="num">27,3 %</div>
        <h3>De las muertes de mujeres son cardiovasculares</h3>
        <p>Primera causa de muerte femenina, por encima de todos los cánceres combinados.</p>
      </div>
      <div class="gap-cell is-teal">
        <div class="num">36 %</div>
        <h3>Del resultado depende de lo que hacés</h3>
        <p>Es el factor de mayor peso y el único que podés empezar a mover esta semana.</p>
      </div>
    </div>
    <div class="callout rv" style="margin-top:30px;max-width:78ch">
      <p><b>Un detalle que suele pasarse por alto:</b> si tu menopausia empezó antes de los 45 años,
      eso se considera un factor que aumenta el riesgo cardiovascular y merece una evaluación
      específica. Vale la pena mencionárselo a tu médica o médico aunque no te lo pregunten.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="head rv">
      <p class="eyebrow">Reconocimiento</p>
      <h2>¿Te suena alguna de estas?</h2>
      <p class="lede">Marcá lo que estés viviendo. No es un test ni un puntaje: es una forma de
      ordenar lo que te está pasando antes de la evaluación.</p>
    </div>
    <div class="recog rv" id="recog">
""" + _RECOG_ITEMS + """
    </div>
    <div class="recog-out rv" id="recog-out" hidden>
      <p><b>Marcaste <span class="n" id="rc-n">0</span> de 10.</b> <span id="rc-msg"></span></p>
      <p style="margin-top:14px">
        <a class="btn btn-solid" data-cta="reconocimiento" href="https://info.epa-bienestar.com.ar/evaluacion-inicial.php">Empezar mi evaluación</a>
      </p>
    </div>
  </div>
</section>

<section class="band band-alt">
  <div class="wrap">
    <div class="head rv">
      <p class="eyebrow">Qué medimos</p>
      <h2>Tres preguntas, en vez de un número suelto</h2>
      <p class="lede">La mayoría de las apps te dan un puntaje y te dejan sola con él. Nosotros
      separamos tres cosas que no son lo mismo.</p>
    </div>
    <div class="dims rv">
      <article class="dim dim-e">
        <div class="dim-hd"><span class="dim-ltr">E</span></div>
        <h3>Equilibrio</h3>
        <p class="q">Qué hace tu cuerpo</p>
        <p>Cómo se comportan tu presión, tu sueño y tu ritmo a lo largo de las semanas. Nos importa
        la <strong>estabilidad</strong>, no un valor aislado del día que fuiste al médico.</p>
      </article>
      <article class="dim dim-p">
        <div class="dim-hd"><span class="dim-ltr">P</span></div>
        <h3>Precisión</h3>
        <p class="q">Qué dice tu riesgo</p>
        <p>Tu mapa estructural: laboratorio, antecedentes familiares, en qué punto de la transición
        estás y <strong>lipoproteína(a)</strong>, un análisis que se hace una sola vez en la vida
        y que casi nadie pide.</p>
      </article>
      <article class="dim dim-a">
        <div class="dim-hd"><span class="dim-ltr">A</span></div>
        <h3>Armonía</h3>
        <p class="q">Qué sentís vos</p>
        <p>Tus síntomas, tu sueño percibido, tu ánimo. Con instrumentos validados, respondidos por
        WhatsApp en dos minutos. <strong>Lo que reportás cuenta en el resultado.</strong></p>
      </article>
    </div>
  </div>
</section>

<section class="band" id="como">
  <div class="wrap">
    <div class="head rv"><p class="eyebrow">Cómo funciona</p><h2>De la evaluación al plan</h2></div>
    <ol class="tl rv">
      <li><span class="when">10 minutos</span><div><h3>Evaluación inicial gratuita</h3><p>Sin datos de pago. Te devuelve tu punto de partida con el marco Life's Essential 8 de la American Heart Association.</p></div></li>
      <li><span class="when">Primer mes</span><div><h3>Línea de base</h3><p>Sumás laboratorio, tomas de presión en casa y —si tenés— tu reloj o anillo. Acá se calcula tu primer Índice EPA, siempre acompañado de cuán completo está.</p></div></li>
      <li><span class="when">100 días</span><div><h3>Plan Bienestar 100 Días®</h3><p>Un plan armado para tu etapa, tu perfil de riesgo y tus síntomas. Con seguimiento continuo, no con una consulta y chau.</p></div></li>
      <li><span class="when">Si hace falta</span><div><h3>Derivación</h3><p>Si aparece una señal que amerita consulta, te lo decimos y te conectamos con la red de la Federación Argentina de Cardiología.</p></div></li>
      <li><span class="when">Día 100</span><div><h3>Resultado medido</h3><p>Cuánto se movió tu índice, en qué dimensión, y un informe estructurado para tu médica o médico.</p></div></li>
    </ol>
  </div>
</section>

<section class="band band-alt">
  <div class="wrap">
    <div class="head rv"><p class="eyebrow">Confianza</p><h2>Lo que no vas a encontrar acá</h2></div>
    <div class="cards rv">
      <div class="card"><h3>No vendemos suplementos</h3><p>Ni pastillas, ni polvos, ni fórmulas milagrosas para la menopausia. No tenemos nada que colocarte.</p></div>
      <div class="card"><h3>No diagnosticamos</h3><p>Ni indicamos, suspendemos o cambiamos tu medicación. Eso le corresponde a tu profesional tratante.</p></div>
      <div class="card"><h3>No competimos con tu médica</h3><p>Trabajamos para que llegue mejor informada a tu consulta, no para ocupar su lugar.</p></div>
      <div class="card"><h3>No hay rachas ni rankings</h3><p>Nada de competir con otras usuarias ni perder una racha por faltar un día. Eso genera abandono, no salud.</p></div>
      <div class="card"><h3>No usamos la culpa</h3><p>Los mensajes describen y proponen el paso siguiente. No te reprochan nada.</p></div>
      <div class="card"><h3>No prometemos lo que no sabemos</h3><p>El Índice EPA está en validación clínica y lo decimos en todas partes. Todavía no podemos afirmar que prediga eventos.</p></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="head rv"><p class="eyebrow">Preguntas frecuentes</p><h2>Lo que suelen preguntarnos</h2></div>
    <div class="faq rv" style="max-width:80ch">
""" + _FAQ_ITEMS + """
    </div>
  </div>
</section>

<section class="band band-ink cta-fin">
  <div class="wrap rv">
    <p class="eyebrow" style="justify-content:center">Diez minutos</p>
    <h2>Lo que no se conoce, no se previene.</h2>
    <p class="lede">La evaluación inicial es gratuita, no pide datos de pago y te dice dónde estás
    parada hoy. Es el punto de partida de todo lo demás.</p>
    <div class="row">
      <a class="btn btn-signal" data-cta="cierre" href="https://info.epa-bienestar.com.ar/evaluacion-inicial.php">Hacer mi evaluación inicial</a>
      <a class="btn btn-ghost" style="border-color:rgba(255,255,255,.32);color:#fff" href="https://wa.me/5491169315830?text=Hola,%20quiero%20consultar%20sobre%20el%20Programa%20Mujer%20para%20menopausia.">Preguntar por WhatsApp</a>
    </div>
  </div>
</section>

<script>
/* Reconocimiento: agrupa lo que la persona marcó y sugiere el paso siguiente.
   No puntúa, no estratifica y no guarda nada. Es una ayuda para ordenar,
   deliberadamente distinta de un test de autodiagnóstico. */
(function () {
  var boxes = document.querySelectorAll("#recog .rc");
  var out = document.getElementById("recog-out");
  var n = document.getElementById("rc-n");
  var msg = document.getElementById("rc-msg");
  if (!boxes.length || !out) return;
  function upd() {
    var c = 0;
    boxes.forEach(function (b) { if (b.checked) c++; });
    if (!c) { out.hidden = true; return; }
    out.hidden = false;
    n.textContent = c;
    msg.textContent = c <= 2
      ? "Son cosas frecuentes en esta etapa. La evaluación inicial te muestra qué hay detrás y qué conviene medir."
      : c <= 5
      ? "Varias de estas se relacionan entre sí. Verlas juntas, y no de a una, es justamente lo que hace la evaluación."
      : "Es un conjunto que merece una mirada cardiovascular ordenada. Empezá por la evaluación y, si hace falta, te conectamos con un profesional.";
  }
  boxes.forEach(function (b) { b.addEventListener("change", upd); });
})();
</script>
""")


# ═══════════════════════════════════════════════════════════════
# 14 · LANDING GRUPO B — embarazo y corazón (Corazón de Mamá)
# ═══════════════════════════════════════════════════════════════
_APO = [
    ("Preeclampsia",
     "Aproximadamente el doble de riesgo cardiovascular a lo largo de la vida, y un riesgo "
     "particularmente elevado de insuficiencia cardíaca. Justifica seguimiento cardiológico "
     "aunque la presión se haya normalizado."),
    ("Hipertensión gestacional",
     "Mayor probabilidad de desarrollar hipertensión crónica en los años siguientes. Conviene "
     "control de presión anual desde el posparto, no recién a los cincuenta."),
    ("Diabetes gestacional",
     "Riesgo aumentado de diabetes tipo 2 y de enfermedad cardiovascular. Se recomienda "
     "reevaluación metabólica después del parto y de forma periódica."),
    ("Parto prematuro",
     "Se asocia a mayor riesgo cardiovascular materno posterior, con independencia de si hubo "
     "hipertensión durante el embarazo."),
    ("Bajo peso para la edad gestacional",
     "También se asocia a un perfil de riesgo cardiovascular materno menos favorable a largo plazo."),
    ("Cardiomiopatía periparto",
     "Requiere seguimiento cardiológico específico y condiciona la planificación de embarazos "
     "posteriores. Es una indicación clara de consulta especializada."),
]
_APO_ROWS = "\n".join(
    f'      <div class="apo-row"><div class="apo-ev">{e}</div><div class="apo-rk">{r}</div></div>'
    for e, r in _APO)

_FAQ_B = [
    ("¿Esto es un servicio de fertilidad?", """
      <p>No. No tratamos infertilidad, no hacemos seguimiento de ovulación ni acompañamos
      tratamientos de reproducción asistida. Nuestro campo es la <strong>salud cardiovascular</strong>
      de la mujer, y el embarazo nos interesa porque es el momento en que el sistema cardiovascular
      se pone a prueba y revela información que sirve para el resto de la vida.</p>"""),
    ("Estoy embarazada ahora. ¿Puedo empezar igual?", """
      <p>Sí. El seguimiento durante el embarazo es compatible con tu control obstétrico y está
      pensado para complementarlo, no para superponerse. Lo que hacemos es ordenar tus señales
      cardiovasculares y avisar cuando algo amerita que lo consultes con tu obstetra.</p>
      <p>Si estás en el primer trimestre y todavía no tuviste tu primera consulta obstétrica, esa
      es la prioridad. Nosotros venimos después.</p>"""),
    ("Tuve preeclampsia hace cinco años. ¿Sirve igual empezar ahora?", """
      <p>Sirve especialmente. El riesgo cardiovascular asociado a un evento adverso del embarazo
      no vence: se despliega a lo largo de décadas. Cinco años después es un momento perfectamente
      razonable para hacer la evaluación que probablemente no te ofrecieron en el posparto.</p>
      <p>Y si tenés los registros de ese embarazo —cifras de presión, análisis, epicrisis— traelos.
      Son datos clínicos valiosos que casi nadie vuelve a mirar.</p>"""),
    ("¿Reemplaza a mi obstetra?", """
      <p>De ninguna manera. Tu obstetra conduce el embarazo. Nosotros aportamos una lectura
      cardiovascular estructurada entre consulta y consulta, en un formato estándar que su sistema
      puede leer. Si hay una señal de alarma, la conversación es con tu obstetra, no con nosotros.</p>"""),
    ("Estoy amamantando. ¿Hay algo que no pueda hacer?", """
      <p>Nada de lo que hacemos interfiere con la lactancia: medimos, acompañamos y educamos.
      No indicamos medicación ni suplementos. Las recomendaciones de actividad y alimentación
      contemplan el período de lactancia y sus requerimientos.</p>"""),
    ("¿Y si no pienso tener hijos?", """
      <p>La evaluación cardiovascular te sirve igual, y bastante. Si estás entre los 28 y los 44
      años, es la mejor edad para establecer tu línea de base: conocer tu lipoproteína(a), tu
      perfil de riesgo y tus antecedentes familiares mientras hay tiempo de sobra para actuar.</p>
      <p>Este grupo se llama así porque la maternidad es un evento cardiovascular relevante para
      quienes la atraviesan, no porque sea un requisito para entrar.</p>"""),
    ("¿Cuánto cuesta?", """
      <p>La evaluación inicial es gratuita y no pide datos de pago. Si después querés seguir con
      el Plan Bienestar 100 Días®, te contamos las condiciones al final, sin compromiso.</p>"""),
    ("¿Qué pasa con mis datos?", """
      <p>Son tuyos. Viven en servidores en Argentina, bajo la Ley 25.326, con la base inscripta en
      el Registro Nacional de Bases de Datos de la AAIP. No los vendemos ni los cedemos con fines
      comerciales, y podés llevártelos o pedir que los borremos.
      <a href="politica_de_privacidad.html">Leer la política completa →</a></p>"""),
]
_FAQ_B_ITEMS = "\n".join(
    f'    <details><summary>{q}</summary><div class="ans">{a}\n    </div></details>'
    for q, a in _FAQ_B)

PAGES["embarazo.html"] = dict(
    title="Embarazo y corazón", active=None, cls="pg-b",
    desc="El embarazo es una prueba de esfuerzo cardiovascular y casi nadie te da el resultado. Preeclampsia, diabetes gestacional y parto prematuro predicen tu riesgo futuro. Evaluación inicial gratuita.",
    body="""<section class="phero">
  <div class="wrap">
    <p class="crumb"><a href="index.html">Inicio</a><span>/</span><a href="enlaces.html">Programas</a><span>/</span>Embarazo</p>
    <p class="eyebrow">Mujeres de 28 a 44 · Grupo B</p>
  </div>
  <div class="wrap phero-grid" style="margin-top:6px">
    <div>
      <h1 style="max-width:22ch">El embarazo es una prueba de esfuerzo. Casi nadie te da el resultado.</h1>
      <p class="lede" style="max-width:56ch">Durante nueve meses tu sistema cardiovascular trabaja
      al límite. Cómo respondió a esa exigencia dice mucho sobre tu salud de los próximos treinta
      años. Es información clínica valiosa, y casi siempre se pierde.</p>
      <div class="hero-cta">
        <a class="btn btn-solid" data-cta="hero" href="https://info.epa-bienestar.com.ar/evaluacion-inicial.php">Hacer mi evaluación · gratis</a>
        <a class="btn btn-ghost" href="#momentos">Ver los tres momentos</a>
      </div>
    </div>
    <aside class="card-fx">
      <h4>La evaluación inicial</h4>
      <div class="fx-row"><span class="k">Cuánto dura</span><span class="v">10 minutos</span></div>
      <div class="fx-row"><span class="k">Cuánto cuesta</span><span class="v">Gratis</span></div>
      <div class="fx-row"><span class="k">Sirve si estás</span><span class="v">Antes, durante o después</span></div>
      <div class="fx-row"><span class="k">Marco clínico</span><span class="v">AHA Life&#39;s Essential 8™</span></div>
      <div class="fx-row"><span class="k">Fertilidad</span><span class="v">No es nuestro campo</span></div>
      <div class="fx-row"><span class="k">Tus datos</span><span class="v">Servidores en Argentina</span></div>
    </aside>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="head rv">
      <p class="eyebrow">La curva</p>
      <h2>Lo que le pasa a tu corazón en un embarazo</h2>
      <p class="lede">El volumen sanguíneo aumenta entre un 40 % y un 50 %. El corazón bombea más,
      más rápido y durante meses. Después del parto, la carga baja —pero la información que dejó
      ese período casi nunca se recoge.</p>
    </div>

    <figure class="arc rv" style="margin:0">
      <figcaption class="arc-top">
        <span>Carga cardiovascular a lo largo del embarazo</span>
        <span>Esquemático</span>
      </figcaption>
      <div class="arc-body">
        <svg id="arc-svg" viewBox="0 0 720 290" role="img"
             aria-label="Curva esquemática de la carga cardiovascular. Parte de una línea de base en la preconcepción, asciende de forma sostenida durante el embarazo hasta un pico alrededor de las semanas 28 a 32, cae tras el parto y desciende gradualmente durante el posparto sin volver de inmediato al punto de partida. La zona del posparto está marcada como ventana de seguimiento que habitualmente no se utiliza."></svg>
      </div>
      <div class="arc-foot">
        <div class="arc-cell">
          <div class="k">Antes</div>
          <div class="t">La ventana de mayor palanca</div>
          <p>Optimizar el perfil cardiovascular antes de concebir mejora el embarazo y la trayectoria posterior. Casi nunca se hace.</p>
        </div>
        <div class="arc-cell">
          <div class="k">Durante</div>
          <div class="t">La prueba de esfuerzo</div>
          <p>El pico de carga llega alrededor de las semanas 28 a 32. Ahí es donde suelen aparecer las señales.</p>
        </div>
        <div class="arc-cell is-gap">
          <div class="k">Después</div>
          <div class="t">La ventana que se cierra</div>
          <p>Toda la atención pasa al bebé. El control cardiovascular materno es el que más se pierde.</p>
        </div>
      </div>
    </figure>
  </div>
</section>

<section class="band band-alt">
  <div class="wrap">
    <div class="head rv">
      <p class="eyebrow">El resultado que no te dieron</p>
      <h2>Si algo de esto pasó en tu embarazo, tu corazón lo registró</h2>
      <p class="lede">Estos eventos están reconocidos como factores que aumentan el riesgo
      cardiovascular a lo largo de la vida. Salís del sanatorio, la presión se normaliza, y la
      información desaparece del expediente.</p>
    </div>
    <div class="apo rv">
      <div class="apo-hd"><div>Lo que pasó en tu embarazo</div><div>Lo que significa para tu corazón</div></div>
""" + _APO_ROWS + """
    </div>
    <div class="callout callout-warn rv" style="margin-top:28px;max-width:80ch">
      <p><b>Esto no es un diagnóstico ni una condena.</b> Es información de estratificación: que
      un evento aumente el riesgo poblacional no determina lo que va a pasar con vos. Lo que sí
      hace es cambiar qué conviene medir, con qué frecuencia y desde qué edad. Saberlo a los 35
      es una ventaja enorme sobre enterarse a los 60.</p>
    </div>
  </div>
</section>

<section class="band" id="momentos">
  <div class="wrap">
    <div class="head rv">
      <p class="eyebrow">Tres momentos</p>
      <h2>Sirve en cualquiera de los tres</h2>
      <p class="lede">No hace falta estar planificando para que esto tenga sentido. Cada etapa
      tiene su propia oportunidad.</p>
    </div>
    <div class="mom rv">
      <article class="mom-c mom-1">
        <div class="when2">Antes de concebir</div>
        <h3>Preconcepción</h3>
        <p>Es la ventana de mayor rendimiento y la más desaprovechada. Lo que se corrige acá mejora
        el embarazo <em>y</em> tu trayectoria de las próximas décadas.</p>
        <ul>
          <li>Línea de base cardiovascular completa</li>
          <li>Lipoproteína(a), una sola vez en la vida</li>
          <li>Presión, lípidos y glucemia antes del embarazo</li>
          <li>Antecedentes familiares ordenados</li>
          <li>Plan de optimización previo a la concepción</li>
        </ul>
      </article>
      <article class="mom-c mom-2">
        <div class="when2">Durante el embarazo</div>
        <h3>Seguimiento</h3>
        <p>Complementa tu control obstétrico. Ordena las señales cardiovasculares y te avisa cuándo
        conviene consultar, sin superponerse con tu obstetra.</p>
        <ul>
          <li>Registro de presión domiciliaria estructurado</li>
          <li>Señales de alarma explicadas en claro</li>
          <li>Sueño y actividad adaptados al trimestre</li>
          <li>Informe legible para tu equipo obstétrico</li>
          <li>Derivación cardiológica si hace falta</li>
        </ul>
      </article>
      <article class="mom-c mom-3">
        <div class="when2">Después del parto</div>
        <h3>Posparto</h3>
        <p>La etapa que más se descuida. Si tuviste un evento adverso, este es el momento de dejarlo
        registrado y armar el seguimiento que va a servirte durante décadas.</p>
        <ul>
          <li>Registro formal de lo que pasó en el embarazo</li>
          <li>Control de presión en las semanas posteriores</li>
          <li>Reevaluación metabólica si hubo diabetes gestacional</li>
          <li>Recuperación cardiovascular progresiva</li>
          <li>Plan de vigilancia a largo plazo</li>
        </ul>
      </article>
    </div>
  </div>
</section>

<section class="band band-ink">
  <div class="wrap">
    <div class="head rv">
      <p class="eyebrow">Corazón de Mamá</p>
      <h2>No estamos solos en esto</h2>
      <p class="lede">La salud cardiovascular materna es una prioridad regional declarada. La
      iniciativa Corazón de Mamá reúne a la Sociedad Interamericana de Cardiología, la American
      Heart Association y la Federación Argentina de Cardiología alrededor de este problema.</p>
      <p class="lede">Nuestro aporte es convertir una campaña de concientización anual en un
      programa de evaluación y seguimiento que funcione todo el año, con datos estructurados que
      sirvan también para investigación.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="head rv">
      <p class="eyebrow">Qué medimos</p>
      <h2>Tres preguntas, en vez de un número suelto</h2>
    </div>
    <div class="dims rv">
      <article class="dim dim-e">
        <div class="dim-hd"><span class="dim-ltr">E</span></div>
        <h3>Equilibrio</h3>
        <p class="q">Qué hace tu cuerpo</p>
        <p>Cómo se comportan tu presión, tu sueño y tu ritmo semana a semana. En el embarazo la
        <strong>tendencia</strong> importa más que cualquier medición aislada de consultorio.</p>
      </article>
      <article class="dim dim-p">
        <div class="dim-hd"><span class="dim-ltr">P</span></div>
        <h3>Precisión</h3>
        <p class="q">Qué dice tu riesgo</p>
        <p>Acá entran los eventos de tus embarazos previos, junto con laboratorio, antecedentes
        familiares y <strong>lipoproteína(a)</strong>. Tu historia obstétrica es un dato
        cardiovascular, no solo obstétrico.</p>
      </article>
      <article class="dim dim-a">
        <div class="dim-hd"><span class="dim-ltr">A</span></div>
        <h3>Armonía</h3>
        <p class="q">Qué sentís vos</p>
        <p>Síntomas, sueño percibido y ánimo, respondidos por WhatsApp en dos minutos. El posparto
        es un período de alta carga emocional y <strong>eso también se mide</strong>.</p>
      </article>
    </div>
  </div>
</section>

<section class="band band-alt">
  <div class="wrap">
    <div class="head rv"><p class="eyebrow">Confianza</p><h2>Lo que no vas a encontrar acá</h2></div>
    <div class="cards rv">
      <div class="card"><h3>No somos fertilidad</h3><p>No tratamos infertilidad ni acompañamos reproducción asistida. Nuestro campo es cardiovascular.</p></div>
      <div class="card"><h3>No reemplazamos a tu obstetra</h3><p>Tu obstetra conduce el embarazo. Nosotros aportamos la lectura cardiovascular entre consultas.</p></div>
      <div class="card"><h3>No somos una app de embarazo</h3><p>No contamos semanas ni comparamos el tamaño del bebé con frutas. Hay apps excelentes para eso.</p></div>
      <div class="card"><h3>No diagnosticamos</h3><p>Ni indicamos, suspendemos ni ajustamos medicación. Eso le corresponde a tu equipo tratante.</p></div>
      <div class="card"><h3>No vendemos suplementos</h3><p>Ni prenatales, ni fórmulas, ni nada. No tenemos nada que colocarte.</p></div>
      <div class="card"><h3>No usamos la culpa</h3><p>Un evento adverso en el embarazo no es algo que hiciste mal. Es información, y la tratamos así.</p></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="head rv"><p class="eyebrow">Preguntas frecuentes</p><h2>Lo que suelen preguntarnos</h2></div>
    <div class="faq rv" style="max-width:80ch">
""" + _FAQ_B_ITEMS + """
    </div>
  </div>
</section>

<section class="band band-ink cta-fin">
  <div class="wrap rv">
    <p class="eyebrow" style="justify-content:center">Diez minutos</p>
    <h2>Lo que no se conoce, no se previene.</h2>
    <p class="lede">Estés planificando, embarazada o con hijos grandes, la evaluación inicial te
    dice dónde estás parada hoy. Es gratuita y no pide datos de pago.</p>
    <div class="row">
      <a class="btn btn-signal" data-cta="cierre" href="https://info.epa-bienestar.com.ar/evaluacion-inicial.php">Hacer mi evaluación inicial</a>
      <a class="btn btn-ghost" style="border-color:rgba(255,255,255,.32);color:#fff" href="https://wa.me/5491169315830?text=Hola,%20quiero%20consultar%20sobre%20salud%20cardiovascular%20y%20embarazo.">Preguntar por WhatsApp</a>
    </div>
  </div>
</section>

<script>
/* Arco cardiovascular del embarazo. Esquemático y deliberadamente sin
   eje Y numérico: comunica la forma de la curva y la ventana posparto
   desaprovechada, no valores hemodinámicos concretos. */
(function () {
  var svg = document.getElementById("arc-svg");
  if (!svg) return;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var W = 720, H = 290, T = 26, B = 54, L = 14, R = 14;
  var xPre = 118, xBirth = 486;            // fin de preconcepción · parto
  var yBase = 206, yPeak = 84, yEnd = 168; // línea de base · pico · posparto

  var curve =
    "M" + L + " " + yBase +
    " L" + xPre + " " + yBase +
    " C" + (xPre + 78) + " " + (yBase - 14) +
    " "  + (xPre + 150) + " " + (yPeak + 62) +
    " "  + 322 + " " + (yPeak + 26) +
    " C" + 372 + " " + (yPeak + 2) +
    " "  + 402 + " " + yPeak +
    " "  + 432 + " " + yPeak +
    " L" + xBirth + " " + (yPeak + 10) +
    " C" + (xBirth + 20) + " " + (yPeak + 66) +
    " "  + (xBirth + 74) + " " + (yEnd - 22) +
    " "  + (W - R) + " " + yEnd;

  var g = "";
  g += '<rect class="arc-zone" x="' + L + '" y="' + T + '" width="' + (xPre - L) + '" height="' + (H - T - B) + '" rx="3"/>';
  g += '<rect class="arc-gap"  x="' + xBirth + '" y="' + T + '" width="' + (W - R - xBirth) + '" height="' + (H - T - B) + '" rx="3"/>';
  g += '<line class="arc-base" x1="' + L + '" y1="' + yBase + '" x2="' + (W - R) + '" y2="' + yBase + '"/>';
  g += '<path class="arc-fill" d="' + curve + " L" + (W - R) + " " + (H - B) + " L" + L + " " + (H - B) + ' Z"/>';
  g += '<path class="arc-curve" id="arc-line" d="' + curve + '"/>';
  g += '<line class="arc-birth" x1="' + xBirth + '" y1="' + T + '" x2="' + xBirth + '" y2="' + (H - B) + '"/>';

  g += '<text class="arc-lbl" x="' + (L + 6) + '" y="' + (H - 34) + '">PRECONCEPCIÓN</text>';
  g += '<text class="arc-lbl" x="' + (xPre + 8) + '" y="' + (H - 34) + '">SEMANA 0</text>';
  g += '<circle cx="440" cy="' + yPeak + '" r="3.4" fill="var(--signal)"/>';
  g += '<line class="arc-birth" x1="440" y1="' + (yPeak - 8) + '" x2="440" y2="' + (yPeak - 26) + '"/>';
  g += '<text class="arc-note" x="440" y="' + (yPeak - 34) + '" text-anchor="middle">Pico de carga</text>';
  g += '<text class="arc-lbl" x="440" y="' + (yPeak - 50) + '" text-anchor="middle">SEMANAS 28–32</text>';
  g += '<text class="arc-lbl" x="' + (xBirth - 8) + '" y="' + (H - 34) + '" text-anchor="end">PARTO</text>';
  g += '<text class="arc-lbl" x="' + (W - R) + '" y="' + (H - 34) + '" text-anchor="end">POSPARTO · 12 MESES</text>';
  g += '<text class="arc-lbl" x="' + (L + 6) + '" y="' + (yBase + 16) + '">línea de base</text>';
  g += '<text class="arc-note" x="' + (xBirth + 14) + '" y="' + (T + 20) + '">Ventana de seguimiento</text>';
  g += '<text class="arc-lbl" x="' + (xBirth + 14) + '" y="' + (T + 36) + '">HABITUALMENTE NO SE USA</text>';
  g += '<text class="arc-note" x="' + (xPre + 14) + '" y="' + (yBase - 8) + '">Volumen sanguíneo +40–50 %</text>';

  svg.innerHTML = g;

  if (reduce) return;
  var p = document.getElementById("arc-line"), len = p.getTotalLength();
  p.style.strokeDasharray = len;
  p.style.strokeDashoffset = len;
  p.style.transition = "stroke-dashoffset 2s cubic-bezier(.36,.86,.34,1) .2s";
  requestAnimationFrame(function () {
    requestAnimationFrame(function () { p.style.strokeDashoffset = 0; });
  });
})();
</script>
""")


if __name__ == "__main__":
    total = 0
    for path, cfg in PAGES.items():
        d = cfg.get("depth", 0)
        n = write(path, layout(path, cfg["title"], cfg["desc"], cfg["body"],
                               depth=d, active=cfg.get("active"), cls=cfg.get("cls", "")))
        total += n
        print(f"  {path:42s} {n:>7,} bytes")
    print(f"\n{len(PAGES)} páginas · {total:,} bytes")
