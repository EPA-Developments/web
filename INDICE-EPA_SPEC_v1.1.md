# ÍNDICE EPA™ — Especificación Técnica v1.0

## Equilibrio · Precisión · Armonía
### Un índice compuesto de salud cardiovascular femenina para la transición menopáusica

---

**Documento:** `EPA-SPEC-IDX-001`
**Versión:** 1.1 (Draft para revisión científica)
**Fecha:** Agosto 2026
**Cambio respecto de v1.0:** corrección de las ponderaciones. Ver §0 — Fe de erratas.
**Autor técnico:** Equipo de Producto — EPA Bienestar IA
**Revisión clínica pendiente:** Dr. Alejandro Barbagelata (MD, FAHA, FSCAI) · Comité de Enfermedades Cardiovasculares en la Mujer, FAC
**Revisión metodológica pendiente:** María Paula Bonomini — ITBA AI Lab
**Backend de referencia:** FAVALORO — Medplum self-hosted, `https://api.epa-bienestar.com.ar/fhir/R4`
**Clasificación:** Confidencial — Uso interno y comité científico

---

## 0. FE DE ERRATAS — v1.0 → v1.1

**Qué se corrigió.** Las ponderaciones de las tres dimensiones del Índice EPA derivan del
modelo de determinantes de salud de GoInvo. La v1.0 de esta especificación utilizó valores
tomados de la **versión 1 de la metodología de GoInvo (26 de julio de 2017)**, que contenía
un error aritmético que la propia GoInvo rectificó semanas más tarde.

El error: el promedio del determinante conductual se calculó dividiendo **siete valores de
fuente por seis**.

```
Publicado en v1:   (50 + 38 + 40 + 39 + 36 + 45 + 30) / 6 = 46,33   ← incorrecto
Correcto:          (50 + 38 + 40 + 39 + 36 + 45 + 30) / 7 = 39,71
```

La nota al pie de la metodología de GoInvo consigna que un error de cálculo original en
'Comportamiento' fue rectificado y que los valores subsiguientes se actualizaron.

Un segundo indicio estaba a la vista en la propia v1.0: la normalización declaraba un total
de **100,4 %**. Una normalización correcta suma exactamente 100.

**Valores vigentes** (GoInvo v2, 30 ago 2017; confirmados sin cambios en v3, 15 nov 2018):

| Determinante | v1.0 (incorrecto) | v1.1 (vigente) |
|---|---:|---:|
| Comportamiento individual | 38 % | **36 %** |
| Circunstancias sociales | 23 % | **24 %** |
| Genética y biología | 21 % | **22 %** |
| Cuidado médico | 11 % | **11 %** |
| Ambiente físico | 7 % | **7 %** |

**Ponderaciones del índice resultantes:**

| Dimensión | v1.0 | v1.1 |
|---|---:|---:|
| E — Equilibrio | 38 % | **36 %** |
| P — Precisión | 32 % | **33 %** |
| A — Armonía | 30 % | **31 %** |

### 0.1 Magnitud del impacto

El desplazamiento del índice ante un mismo perfil está **analíticamente acotado**:

```
Δ  =  EPA(v1.1) − EPA(v1.0)  =  −0,02 · E  +  0,01 · P  +  0,01 · A
```

Como cada dimensión está acotada en [0, 100], el desplazamiento máximo posible es
**±2,0 puntos** sobre una escala de 0 a 100. Es exactamente cero cuando las tres dimensiones
tienen el mismo valor.

Simulación sobre 200.000 perfiles sintéticos (μ = 68, σ = 16 por dimensión):

| Métrica | Valor |
|---|---:|
| Desplazamiento medio | −0,001 puntos |
| Desvío estándar | 0,385 puntos |
| Rango observado | −1,45 a +1,55 |
| Casos con desplazamiento mayor a 1,0 punto | 0,75 % |
| **Casos que cambian de banda clínica** | **2,09 %** |

**Interpretación.** La corrección no altera materialmente la estratificación. Afecta a
aproximadamente 1 de cada 48 evaluaciones, y únicamente a las que ya se encontraban dentro
de dos puntos de un umbral de banda. **No obliga a reevaluar pacientes** ni invalida los datos
recolectados bajo v1.0, siempre que cada `Observation` declare la versión del motor que la
generó (§10.2).

### 0.2 Por qué se documenta en lugar de corregirse en silencio

Un índice que cambia sus pesos sin dejar registro es irreproducible. Esta sección existe para
que cualquier revisor pueda reconstruir por qué los valores de una presentación de comienzos
de 2026 difieren de los de una publicación de 2027. **La trazabilidad del error forma parte
de la credibilidad del instrumento**, no es una concesión.

### 0.3 Atribución

El modelo de determinantes empleado es obra de terceros y se utiliza bajo licencia
Creative Commons Attribution 4.0:

> Choi, E., & Sonin, J. (2019). *Determinants of Health.* GoInvo. CC BY 4.0.
> https://www.goinvo.com/vision/determinants-of-health

La v1.0 describía la metodología sin acreditar a sus autores. **Eso constituía un
incumplimiento de los términos de la licencia**, no solamente una omisión de cortesía. Toda
referencia futura —sitio web, presentaciones institucionales, publicaciones— debe incluir la
cita completa y **especificar la versión de metodología utilizada** (actualmente v3,
15 nov 2018).

---

## TABLA DE CONTENIDOS

0. [Fe de erratas — v1.0 → v1.1](#0-fe-de-erratas--v10--v11)
1. [Fundamento y brecha que cubre](#1-fundamento-y-brecha-que-cubre)
2. [Arquitectura del índice y ponderaciones](#2-arquitectura-del-índice-y-ponderaciones)
3. [Dimensión E — Equilibrio](#3-dimensión-e--equilibrio-36-)
4. [Dimensión P — Precisión](#4-dimensión-p--precisión-33-)
5. [Dimensión A — Armonía](#5-dimensión-a--armonía-31-)
6. [Cómputo del índice compuesto](#6-cómputo-del-índice-compuesto)
7. [Completitud, confianza y reglas de no reporte](#7-completitud-confianza-y-reglas-de-no-reporte)
8. [Reglas de seguridad clínica y escalamiento](#8-reglas-de-seguridad-clínica-y-escalamiento)
9. [Esquema FHIR R4](#9-esquema-fhir-r4)
10. [CodeSystem y ValueSets locales](#10-codesystem-y-valuesets-locales)
11. [Arquitectura de cómputo en Medplum](#11-arquitectura-de-cómputo-en-medplum)
12. [Validación científica y plan de publicación](#12-validación-científica-y-plan-de-publicación)
13. [Limitaciones declaradas](#13-limitaciones-declaradas)
14. [Anexo A — Tabla LOINC consolidada](#anexo-a--tabla-loinc-consolidada)

---

## 1. FUNDAMENTO Y BRECHA QUE CUBRE

### 1.1 El problema con medir solo niveles

Life's Essential 8™ (AHA, *Circulation* 2022) es el estándar de oro para cuantificar salud cardiovascular. Su diseño es deliberadamente transversal: cada uno de los ocho componentes se puntúa a partir de **un valor puntual** (una presión arterial, un LDL, una glucemia, horas de sueño autorreportadas).

Ese diseño es apropiado para vigilancia poblacional. Es insuficiente para la **transición menopáusica**, por tres razones fisiológicas:

**a) La menopausia es un fenómeno de varianza, no de nivel.**
La perimenopausia se caracteriza por variabilidad extrema de estradiol y FSH antes de que cualquier valor medio se desplace. Los efectos cardiovasculares acompañan ese patrón: la variabilidad de la presión arterial visita-a-visita aumenta antes de que la PA media suba; la fragmentación del sueño precede a la reducción de la duración total del sueño; la variabilidad glucémica se deteriora antes de que la HbA1c cruce umbral. **Un LE8 tomado en dos visitas puede ser idéntico mientras la fisiología subyacente se desestabiliza.**

**b) La variabilidad es predictora independiente de eventos.**
La variabilidad de la presión arterial visita-a-visita predice ACV y eventos coronarios de forma independiente de la PA media. La irregularidad del ritmo sueño-vigilia predice mortalidad de forma independiente —y más fuerte— que la duración del sueño. Ninguna de estas señales entra en LE8.

**c) LE8 no tiene voz de la paciente.**
Los síntomas vasomotores, la calidad de sueño percibida, el ánimo y la carga sintomática urogenital no aparecen en el score. Sin embargo, la carga de síntomas vasomotores moderados-severos se asocia a peor perfil de riesgo cardiovascular y es el determinante principal de adherencia a cualquier plan de intervención. **Un score que ignora lo que la mujer siente no puede predecir si la mujer va a sostener el plan.**

### 1.2 Qué agrega el Índice EPA

El Índice EPA **no reemplaza a LE8: lo envuelve**. LE8 aporta la base de niveles y sigue reportándose de forma independiente (LOINC 96607-7). El Índice EPA agrega dos capas que LE8 no tiene:

| Capa | Pregunta que responde | Fuente de datos | Novedad |
|---|---|---|---|
| **E — Equilibrio** | ¿Qué hace el cuerpo *a lo largo del tiempo*? | Wearables continuos (openwearables.io) + monitoreo domiciliario | Varianza y trayectoria, no nivel |
| **P — Precisión** | ¿Qué dice el riesgo *estructural*? | Laboratorio + estadificación clínica | Lp(a) + STRAW+10 + potenciadores sexo-específicos |
| **A — Armonía** | ¿Qué siente y reporta *la mujer*? | PROs validados vía WhatsApp/Kapso | Outcome reportado por la paciente, ausente en LE8 |

**Formulación en una línea:**
> Equilibrio es lo que el cuerpo hace. Precisión es lo que el riesgo dice. Armonía es lo que la mujer siente.
> Objetivo → predictivo → subjetivo, en un solo índice interoperable.

### 1.3 Población objetivo y alcance de validez

- **Población índice (v1.0):** mujeres de 40 a 65 años en cualquier estadio STRAW+10 de −2 a +2. Corresponde al **Grupo C** de la segmentación EPA, extendido hacia abajo para capturar perimenopausia temprana.
- **Fuera de alcance en v1.0:** Grupos A (18–30), B (28–44) y D (65+). El marco conceptual es extensible pero los cortes de scoring **no** son transferibles sin recalibración; se documentarán en especificaciones separadas.
- **Uso previsto:** herramienta de estratificación y seguimiento longitudinal de apoyo a la decisión clínica. **No es un dispositivo diagnóstico.** No sustituye evaluación médica ni la decisión de un profesional.

---

## 2. ARQUITECTURA DEL ÍNDICE Y PONDERACIONES

### 2.1 Ponderación de las tres dimensiones

Las ponderaciones **no son arbitrarias**: derivan por alineación conceptual del Modelo de Determinantes de Salud adoptado por EPA Bienestar IA.

| Determinante | Peso | Dimensión EPA que lo captura predominantemente |
|---|---:|---|
| Comportamiento individual | 36 % | **E — Equilibrio** (sueño, actividad, peso, adherencia reflejada en fisiología) |
| Genética y biología | 22 % | **P — Precisión** |
| Cuidado médico | 11 % | **P — Precisión** |
| Circunstancias sociales | 24 % | **A — Armonía** |
| Ambiente físico | 7 % | **A — Armonía** |

*Fuente:* Choi, E., & Sonin, J. (2019). *Determinants of Health.* GoInvo. CC BY 4.0.
Metodología v3 (15 nov 2018), que confirma los valores calculados en v2 (30 ago 2017).

**Ponderaciones resultantes:**

| Dimensión | Peso | Derivación |
|---|---:|---|
| **E — Equilibrio** | **36 %** | Comportamiento (36 %) |
| **P — Precisión** | **33 %** | Genética (22 %) + Cuidado médico (11 %) |
| **A — Armonía** | **31 %** | Social (24 %) + Ambiente (7 %) |
| **Total** | **100 %** | |

> **Nota metodológica obligatoria.** La correspondencia entre determinante y dimensión es de **alineación conceptual, no de identidad estricta**. La carga de síntomas vasomotores (dimensión A) es biológica, no social; la variabilidad glucémica (dimensión E) tiene componente genético. La derivación se utiliza para fundamentar el peso relativo con un criterio externo, publicado y reproducible, en lugar de una asignación de juicio experto. **Esta justificación debe declararse explícitamente en cualquier publicación.** Los pesos son candidatos a recalibración empírica una vez disponibles los datos de MAMA-LE8 (ver §12).

### 2.2 Estructura jerárquica

```
ÍNDICE EPA (0–100)
│
├── E — EQUILIBRIO ......................... 36 %
│   ├── E1  Variabilidad de presión arterial ....... 25 % de E
│   ├── E2  Regularidad del sueño (SRI) ............ 25 % de E
│   ├── E3  HRV nocturna (desvío del basal) ........ 20 % de E
│   ├── E4  Trayectoria antropométrica (cintura) ... 20 % de E
│   └── E5  Variabilidad glucémica ................. 10 % de E
│
├── P — PRECISIÓN .......................... 33 %
│   ├── P1  Lipoproteína(a) ........................ 20 % de P
│   ├── P2  Riesgo a 10 años (PREVENT / PCE) ....... 30 % de P
│   ├── P3  Estadio STRAW+10 + edad de menopausia .. 20 % de P
│   ├── P4  Historia familiar de ECV prematura ..... 10 % de P
│   └── P5  Perfil aterogénico (ApoB / no-HDL) ..... 20 % de P
│
└── A — ARMONÍA ............................ 31 %
    ├── A1  Menopause Rating Scale (MRS) ........... 30 % de A
    ├── A2  Carga de síntomas vasomotores .......... 25 % de A
    ├── A3  Calidad de sueño percibida (PSQI) ...... 20 % de A
    ├── A4  Ánimo y ansiedad (PHQ-9 + GAD-7) ....... 15 % de A
    └── A5  Autoeficacia / activación .............. 10 % de A
```

Cada subcomponente se puntúa **0–100**. Cada dimensión es la media ponderada de sus subcomponentes. El índice es la media ponderada de las tres dimensiones.

**Convención de dirección:** en todos los casos, **100 = mejor, 0 = peor**. Los instrumentos cuya escala nativa es inversa (MRS, PSQI, PHQ-9, GAD-7, riesgo a 10 años) se invierten explícitamente en las tablas de corte.

---

## 3. DIMENSIÓN E — EQUILIBRIO (36 %)

**Definición operacional:** grado de estabilidad fisiológica de la paciente a lo largo del tiempo, medido como dispersión y deriva, no como nivel absoluto.

**Ventana de observación estándar:** 28 días móviles. Ventana mínima aceptable: 14 días. Ventana para trayectoria antropométrica: 12 meses (mínimo 6 meses con ≥3 mediciones).

### E1 — Variabilidad de presión arterial (25 % de E)

**Métrica:** desvío estándar de la presión arterial sistólica sobre mediciones domiciliarias seriadas (protocolo mínimo: 7 días consecutivos, 2 mediciones matutinas + 2 vespertinas). Métrica secundaria cuando el número de mediciones lo permite: *average real variability* (ARV).

```
SD(PAS) = raíz[ (1/(n−1)) · Σ (PASᵢ − media)² ]
ARV     = (1/(n−1)) · Σ |PASᵢ₊₁ − PASᵢ|
```

| SD PAS (mmHg) | Puntaje E1 | Interpretación |
|---|---:|---|
| < 8 | 100 | Estabilidad óptima |
| 8 – < 11 | 80 | Estabilidad conservada |
| 11 – < 14 | 60 | Variabilidad incipiente |
| 14 – < 18 | 35 | Variabilidad significativa |
| ≥ 18 | 0 | Inestabilidad hemodinámica |

**Requisito mínimo de datos:** ≥ 12 mediciones válidas en la ventana. Con < 12, E1 se marca como no computable.

**LOINC:** `85354-9` (panel de PA) · `8480-6` (PAS) · `8462-4` (PAD) · derivado: código local `epa-bpv-sd`

---

### E2 — Regularidad del sueño (25 % de E)

**Métrica:** *Sleep Regularity Index* (SRI), 0–100 nativo. Probabilidad porcentual de que la paciente se encuentre en el mismo estado (sueño/vigilia) en dos momentos separados exactamente por 24 horas, promediada sobre la ventana.

```
SRI = −100 + [ 200 / (M · (N−1)) ] · Σ Σ δ(s(i,j), s(i+1,j))
```

donde $s$ es el estado sueño/vigilia por época y $\delta$ es la delta de Kronecker.

**Justificación de selección:** SRI predice mortalidad por todas las causas de forma independiente y con mayor magnitud de efecto que la duración del sueño. LE8 puntúa duración; SRI captura la señal que LE8 pierde.

| SRI | Puntaje E2 | Interpretación |
|---|---:|---|
| ≥ 85 | 100 | Ritmo altamente regular |
| 75 – < 85 | 80 | Regularidad adecuada |
| 65 – < 75 | 55 | Irregularidad leve |
| 55 – < 65 | 30 | Irregularidad marcada |
| < 55 | 0 | Ritmo circadiano desorganizado |

**Requisito mínimo de datos:** ≥ 14 noches con ≥ 80 % de cobertura de época. Con < 14 noches, se sustituye por métrica de respaldo (SD del horario de inicio del sueño) y se marca la confianza como reducida.

**Fuente:** openwearables.io — Oura, Apple Watch, Google Fit.
**LOINC:** `93832-4` (duración del sueño, contexto) · derivado: código local `epa-sri`

---

### E3 — HRV nocturna: desvío del basal personal (20 % de E)

**Métrica:** rMSSD nocturna media de 7 días, expresada como **z-score contra el basal personal** de la paciente (definido como la media y el desvío de los primeros 28 días de registro válido, o de la ventana de 90 días previa si existe).

```
z  =  [ rMSSD medio de 7 noches  −  μ(basal) ]  /  σ(basal)
```

**Justificación de selección:** los valores normativos poblacionales de HRV carecen de utilidad clínica por su enorme dispersión interindividual (edad, condición física, medicación, dispositivo). El basal personal es la única referencia interpretable. Esta decisión también **reduce el sesgo por dispositivo**, ya que cada paciente es su propio control.

| z-score | Puntaje E3 | Interpretación |
|---|---:|---|
| ≥ −0.5 | 100 | Tono autonómico estable o mejorado |
| −0.5 a > −1.0 | 80 | Dentro de variación esperable |
| −1.0 a > −1.5 | 55 | Descenso sostenido — revisar contexto |
| −1.5 a > −2.0 | 30 | Descenso marcado |
| ≤ −2.0 | 0 | Desvío severo del basal |

**Requisito mínimo de datos:** basal establecido (≥ 21 noches válidas) + ≥ 5 noches en la ventana de evaluación. Sin basal establecido, E3 no es computable y se redistribuye su peso (§7.2).

**LOINC:** `80404-7` ⚠ (SD de intervalo R-R) · derivado: código local `epa-hrv-zscore`

---

### E4 — Trayectoria antropométrica (20 % de E)

**Métrica:** cambio en circunferencia de cintura a 12 meses (o pendiente anualizada si la ventana es de 6–11 meses).

**Justificación de selección:** la redistribución adiposa visceral es la firma antropométrica de la transición menopáusica y ocurre **con IMC estable**. Usar IMC como única medida antropométrica en esta población es un error de diseño: se pierde la señal más específica del período. La cintura se reporta como componente primario; el IMC se conserva para compatibilidad con LE8.

| Δ cintura 12 meses | Puntaje E4 |
|---|---:|
| ≤ −2 cm | 100 |
| > −2 a ≤ 0 cm | 90 |
| > 0 a ≤ +2 cm | 70 |
| > +2 a ≤ +4 cm | 45 |
| > +4 a ≤ +6 cm | 20 |
| > +6 cm | 0 |

**Ajuste por nivel:** si la cintura absoluta es ≥ 88 cm (umbral de riesgo cardiometabólico en mujeres), se aplica un tope máximo de 80 puntos a E4 independientemente de la trayectoria.

**Requisito mínimo de datos:** ≥ 2 mediciones separadas por ≥ 180 días.
**LOINC:** `8280-0` ⚠ (circunferencia de cintura) · `29463-7` (peso) · `39156-5` (IMC)

---

### E5 — Variabilidad glucémica (10 % de E)

**Métrica primaria (con CGM disponible):** coeficiente de variación glucémica sobre 14 días.
**Métrica de respaldo (sin CGM):** desvío estándar de glucemias en ayunas seriadas (≥ 3 mediciones en 12 meses).

| CV glucémico (CGM) | SD glucemia ayunas (mg/dL) | Puntaje E5 |
|---|---|---:|
| < 24 % | < 6 | 100 |
| 24 – < 30 % | 6 – < 10 | 80 |
| 30 – < 36 % | 10 – < 15 | 55 |
| 36 – < 42 % | 15 – < 22 | 30 |
| ≥ 42 % | ≥ 22 | 0 |

> El umbral de 36 % corresponde al consenso internacional que separa glucemia estable de inestable. Los cortes por encima y por debajo son propuestos por EPA y **requieren validación empírica**.

**LOINC:** `1558-6` (glucosa en ayunas) · `4548-4` (HbA1c, contexto) · `97507-8` ⚠ (glucosa media CGM) · derivado: código local `epa-glucose-cv`

---

## 4. DIMENSIÓN P — PRECISIÓN (33 %)

**Definición operacional:** profundidad y calidad de la estratificación de riesgo cardiovascular estructural de la paciente.

> **Nota de diseño crítica.** Esta dimensión puntúa **riesgo**, no comportamiento. Un puntaje P bajo no es responsabilidad de la paciente ni es modificable a corto plazo (Lp(a) es genéticamente determinada y esencialmente fija de por vida). Por esa razón, **P se excluye del cálculo de Δ-EPA a 100 días** (§6.3) y la comunicación al usuario debe enmarcarla explícitamente como *"tu mapa de riesgo"*, nunca como *"tu desempeño"*.

### P1 — Lipoproteína(a) (20 % de P)

**Métrica:** Lp(a) sérica. Unidad preferida **nmol/L** (molar); se acepta mg/dL con conversión documentada.

**Justificación de selección:** Lp(a) es el marcador que convierte la palabra "precisión" en un dato verificable. Es determinada genéticamente, se mide **una vez en la vida**, está recomendada para tamizaje universal al menos una vez por las principales sociedades, es un factor de riesgo causal e independiente para ECV aterosclerótica, y está **groseramente subutilizada en Argentina y México**. Es el único componente del índice con costo marginal cero después de la primera medición.

| Lp(a) nmol/L | Lp(a) mg/dL (aprox.) | Puntaje P1 | Categoría |
|---|---|---:|---|
| < 75 | < 30 | 100 | Riesgo no aumentado |
| 75 – < 125 | 30 – < 50 | 70 | Riesgo límite |
| 125 – < 250 | 50 – < 100 | 35 | Riesgo alto |
| ≥ 250 | ≥ 100 | 0 | Riesgo muy alto |

**Persistencia:** resultado válido de por vida salvo cambio de método analítico. No requiere repetición.
**LOINC:** `43583-4` ⚠ (Lp(a), moles/volumen, nmol/L — **preferido**) · `10835-7` ⚠ (Lp(a), masa/volumen, mg/dL)

---

### P2 — Riesgo cardiovascular a 10 años (30 % de P)

**Métrica primaria:** AHA PREVENT™ (2023), riesgo de ECV total a 10 años.
**Métrica de respaldo:** Pooled Cohort Equations (ASCVD, 2013) cuando falten insumos de PREVENT (eGFR, ACR).

**Justificación de selección de PREVENT sobre PCE:** PREVENT incorpora función renal y variables cardiometabólicas, no incluye raza como variable, y está calibrado sobre cohortes contemporáneas. Para una población femenina latinoamericana, la eliminación de raza como predictor y la inclusión de eGFR son mejoras materiales.

| Riesgo a 10 años | Puntaje P2 |
|---|---:|
| < 2.5 % | 100 |
| 2.5 – < 5 % | 85 |
| 5 – < 7.5 % | 65 |
| 7.5 – < 10 % | 45 |
| 10 – < 20 % | 20 |
| ≥ 20 % | 0 |

> Los cortes están desplazados hacia abajo respecto de los umbrales de decisión terapéutica clásicos (7.5 % / 20 %) porque la población índice es **femenina y en prevención primaria**, un grupo en el que el riesgo se subestima sistemáticamente. Un 7.5 % en una mujer de 52 años es un hallazgo relevante, no un valor tranquilizador.

**LOINC:** `79423-0` ⚠ (riesgo ECV 10 años, PCE) · derivado: código local `epa-prevent-10y`

---

### P3 — Estadio STRAW+10 y edad de menopausia (20 % de P)

**Componente doble.** Se puntúa el mayor riesgo de los dos.

**P3a — Estadificación STRAW+10.** El estadio no es "bueno" o "malo" en sí mismo; puntúa el grado de **turbulencia hormonal**, que es cuando la ventana de intervención es más valiosa y el riesgo se acelera.

| Estadio STRAW+10 | Descripción | Puntaje P3a |
|---|---|---:|
| −5 / −4 | Reproductivo temprano / pico | 100 |
| −3b / −3a | Reproductivo tardío | 85 |
| −2 | Transición menopáusica temprana | 55 |
| −1 | Transición menopáusica tardía | 35 |
| +1a / +1b | Posmenopausia temprana (0–2 años) | 40 |
| +1c | Posmenopausia temprana (3–6 años) | 60 |
| +2 | Posmenopausia tardía | 70 |

**P3b — Edad de menopausia (potenciador de riesgo sexo-específico).**

| Edad de menopausia final | Puntaje P3b |
|---|---:|
| ≥ 50 años | 100 |
| 45 – 49 años | 80 |
| 40 – 44 años (menopausia precoz) | 40 |
| < 40 años (insuficiencia ovárica primaria) | 0 |
| Menopausia quirúrgica < 45 años | 0 |

**P3 = mín(P3a, P3b).** Si aún no se alcanzó la menopausia final, P3 = P3a.

**Codificación:** STRAW+10 **no tiene representación LOINC**. Se implementa como CodeSystem local `epa-straw10` con mapeo a SNOMED CT donde exista concepto verificado (ver §10.3 — requiere validación contra la release vigente).

---

### P4 — Historia familiar de ECV prematura (10 % de P)

**Definición:** evento cardiovascular aterosclerótico en familiar de primer grado — hombre < 55 años, mujer < 65 años.

| Historia familiar | Puntaje P4 |
|---|---:|
| Ausente y documentada | 100 |
| Desconocida o no documentada | 60 |
| Presente, un familiar de primer grado | 30 |
| Presente, ≥ 2 familiares de primer grado | 0 |

> "Desconocida" puntúa 60, no 100. No documentar no es equivalente a ausencia de riesgo, y puntuar la ignorancia como tranquilidad es un error de diseño que se debe evitar explícitamente.

**Recurso FHIR:** `FamilyMemberHistory` (no `Observation`).

---

### P5 — Perfil aterogénico (20 % de P)

**Métrica primaria:** ApoB. **Métrica de respaldo:** colesterol no-HDL.

**Justificación:** ApoB cuenta partículas aterogénicas y supera a LDL-C como predictor, particularmente en presencia de síndrome metabólico o hipertrigliceridemia —ambos frecuentes en la transición menopáusica, donde el LDL-C puede subestimar la carga de partículas.

| ApoB (mg/dL) | No-HDL (mg/dL) | Puntaje P5 |
|---|---|---:|
| < 70 | < 100 | 100 |
| 70 – < 90 | 100 – < 130 | 80 |
| 90 – < 110 | 130 – < 160 | 55 |
| 110 – < 130 | 160 – < 190 | 30 |
| ≥ 130 | ≥ 190 | 0 |

**LOINC:** `1884-6` ⚠ (ApoB) · `43396-1` ⚠ (colesterol no-HDL) · `13457-7` (LDL calculado) · `2085-9` (HDL) · `2571-8` (triglicéridos) · `2093-3` (colesterol total)

---

## 5. DIMENSIÓN A — ARMONÍA (31 %)

**Definición operacional:** carga sintomática, calidad de vida y capacidad de acción reportadas por la propia paciente, mediante instrumentos validados.

**Canal de captura:** conversacional vía WhatsApp (Kapso Business API), en español rioplatense, con persistencia directa como `QuestionnaireResponse`.

**Cadencia:** MRS y PSQI cada 30 días. Carga VMS semanal. PHQ-9 y GAD-7 cada 30 días. Autoeficacia al inicio, día 50 y día 100.

### A1 — Menopause Rating Scale (30 % de A)

11 ítems, escala 0–4 cada uno, rango total 0–44. Tres subescalas: somato-vegetativa, psicológica, urogenital. Instrumento de dominio público, validado en español.

| MRS total | Puntaje A1 | Categoría clínica |
|---|---:|---|
| 0 – 4 | 100 | Sin síntomas o mínimos |
| 5 – 8 | 80 | Leve |
| 9 – 16 | 50 | Moderado |
| 17 – 25 | 25 | Severo |
| ≥ 26 | 0 | Muy severo |

**Se reportan además las tres subescalas por separado** como `Observation` hijas — la distribución del puntaje importa clínicamente tanto como el total, y el perfil de subescalas orienta la intervención.

**Codificación:** CodeSystem local `epa-mrs`; sin LOINC panel disponible.

---

### A2 — Carga de síntomas vasomotores (25 % de A)

**Métrica:** frecuencia media diaria de sofocos moderados a severos, sobre 7 días.

**Justificación de selección:** es el endpoint primario estándar en los ensayos regulatorios de tratamientos para síntomas vasomotores (el umbral de ≥ 7 episodios moderados-severos por día define elegibilidad en esos protocolos). Adoptar la misma métrica hace que los datos de EPA sean **directamente comparables con la evidencia regulatoria y de la industria** — un activo estratégico deliberado, no una coincidencia.

| VMS moderados-severos / 24 h | Puntaje A2 |
|---|---:|
| 0 | 100 |
| > 0 – < 2 | 85 |
| 2 – < 4 | 60 |
| 4 – < 7 | 35 |
| 7 – < 10 | 15 |
| ≥ 10 | 0 |

**Codificación:** código local `epa-vms-daily-freq`.

---

### A3 — Calidad de sueño percibida — PSQI (20 % de A)

19 ítems autoadministrados, puntaje global 0–21.

**Nota de diseño:** A3 (percepción) y E2 (regularidad objetiva) son deliberadamente independientes. **La discordancia entre ambos es información clínica de primer orden**: sueño objetivamente regular con PSQI alto sugiere insomnio paradójico o carga psicológica; sueño objetivamente irregular con PSQI bajo sugiere falta de conciencia del problema y baja probabilidad de adherencia a intervención de higiene del sueño. El motor debe **reportar la discordancia explícitamente** cuando |E2 − A3| > 35 puntos.

| PSQI global | Puntaje A3 |
|---|---:|
| ≤ 5 | 100 |
| 6 – 8 | 75 |
| 9 – 11 | 50 |
| 12 – 15 | 25 |
| ≥ 16 | 0 |

⚠ **PSQI tiene restricciones de licencia para uso comercial.** Verificar términos con la Universidad de Pittsburgh antes de despliegue en producción. Alternativa de dominio público si la licencia resulta prohibitiva: Insomnia Severity Index (ISI) o Escala de Somnolencia de Epworth, con recalibración de cortes.

---

### A4 — Ánimo y ansiedad (15 % de A)

**Componente compuesto:** PHQ-9 (depresión) y GAD-7 (ansiedad), promediados.

| PHQ-9 | Puntaje | | GAD-7 | Puntaje |
|---|---:|---|---|---:|
| 0 – 4 | 100 | | 0 – 4 | 100 |
| 5 – 9 | 75 | | 5 – 9 | 75 |
| 10 – 14 | 50 | | 10 – 14 | 50 |
| 15 – 19 | 25 | | ≥ 15 | 25 |
| ≥ 20 | 0 | | | |

**A4 = (puntaje PHQ-9 + puntaje GAD-7) / 2**

🔴 **El ítem 9 del PHQ-9 (ideación suicida) dispara una regla de seguridad obligatoria — ver §8.1. No se puede desplegar A4 en producción sin esa regla implementada y probada.**

**LOINC:** `44261-6` (PHQ-9 puntaje total) · `70274-6` (GAD-7 puntaje total) · `44260-8` ⚠ (PHQ-9 ítem 9)

---

### A5 — Autoeficacia y activación (10 % de A)

**Métrica:** escala breve de autoeficacia en salud cardiovascular, 6 ítems, escala Likert 1–5, rango 6–30. Instrumento propio de EPA, **pendiente de validación psicométrica** (ver §12.2).

| Puntaje bruto (6–30) | Puntaje A5 |
|---|---:|
| 26 – 30 | 100 |
| 21 – 25 | 75 |
| 16 – 20 | 50 |
| 11 – 15 | 25 |
| 6 – 10 | 0 |

> Se evaluó Patient Activation Measure (PAM-13) como alternativa validada. **Se descartó para v1.0 por costo de licencia por usuario**, incompatible con un modelo freemium a escala. La escala propia debe validarse contra PAM-13 en un submuestreo de MAMA-LE8 antes de reclamar equivalencia en cualquier publicación.

---

## 6. CÓMPUTO DEL ÍNDICE COMPUESTO

### 6.1 Fórmula

```
            Σ (wᵢ · sᵢ · vᵢ)
dimensión = ────────────────      para cada una de E, P y A
              Σ (wᵢ · vᵢ)
```

donde $s$ = puntaje del subcomponente (0–100), $w$ = peso del subcomponente, $v \in \{0,1\}$ = indicador de validez del dato.

```
Índice EPA  =  0,36 · E  +  0,33 · P  +  0,31 · A
```

La normalización por $\sum w_i v_i$ implementa la **redistribución automática de peso** ante datos faltantes (§7.2).

### 6.2 Bandas interpretativas

| Índice EPA | Banda | Etiqueta clínica | Etiqueta para la paciente | Acción |
|---|---|---|---|---|
| 85 – 100 | 1 | Transición gobernada | *"Tu transición está bajo control"* | Mantener. Reevaluar a 90 días. |
| 70 – 84 | 2 | Favorable con margen | *"Vas bien, con espacio para mejorar"* | Plan Bienestar 100 Días®, intensidad estándar. |
| 55 – 69 | 3 | Intermedia | *"Hay señales que conviene atender"* | Plan intensificado + consulta cardiológica programada. |
| 40 – 54 | 4 | En riesgo | *"Necesitás acompañamiento clínico"* | Derivación a cardiólogo de red FAC dentro de 30 días. |
| < 40 | 5 | Alto riesgo | *(sin etiqueta numérica al usuario)* | **Derivación prioritaria dentro de 7 días.** Ver §8.3. |

> **Regla de comunicación.** En la banda 5 **no se muestra el número a la paciente**. Se muestra el mensaje de derivación y el mecanismo de contacto. Un score de 31/100 comunicado sin acompañamiento clínico produce daño sin beneficio.

### 6.3 Δ-EPA: el endpoint de Plan Bienestar 100 Días®

```
ΔEPA(100)  =  [ 0,36 · E(d100) + 0,31 · A(d100) ]  −  [ 0,36 · E(d0) + 0,31 · A(d0) ]
```

**La dimensión P se excluye deliberadamente del Δ.** Lp(a) es fija, la historia familiar es fija, el estadio STRAW+10 solo avanza. Incluir P en el delta contaminaría el endpoint con drift no atribuible a la intervención y **penalizaría a las pacientes simplemente por avanzar en la transición**.

$\Delta\text{EPA}_{100}$ se reescala a base 100 dividiendo por **0,67** (= 0,36 + 0,31). En v1.0 el divisor era 0,68.

**Diferencia mínima clínicamente importante (MCID) propuesta: +5.0 puntos.**
⚠ Este valor es una **hipótesis de diseño, no un hallazgo**. Debe establecerse empíricamente mediante método de anclaje (correlación con mejora global autorreportada) sobre datos de MAMA-LE8 antes de usarse como endpoint en cualquier publicación o material dirigido a inversores.

---

## 7. COMPLETITUD, CONFIANZA Y REGLAS DE NO REPORTE

### 7.1 Índice de completitud (EPA-C)

```
EPA-C(dim)  =  [ Σ (wᵢ · vᵢ) / Σ wᵢ ] × 100
```

Se computa y se persiste por dimensión y global. **Se reporta siempre junto al índice, nunca por separado.**

| EPA-C global | Nivel de confianza | Presentación |
|---|---|---|
| ≥ 85 % | Alta | Índice completo, sin advertencia |
| 65 – < 85 % | Media | Índice + banda de incertidumbre visible |
| 50 – < 65 % | Baja | Índice marcado como **orientativo**; no usable para decisión clínica |
| < 50 % | No reportable | **No se emite índice.** Se emiten los subcomponentes disponibles. |

### 7.2 Reglas de redistribución y de bloqueo

**Redistribución.** Un subcomponente con $v=0$ se excluye del numerador y del denominador; su peso se redistribuye proporcionalmente entre los subcomponentes válidos de la misma dimensión. **La redistribución nunca cruza dimensiones.**

**Reglas de bloqueo (el índice no se emite si):**

| # | Condición | Fundamento |
|---|---|---|
| B1 | Completitud de E < 50 % | Sin ≥ 2 señales de variabilidad, "Equilibrio" carece de contenido |
| B2 | P2 no computable (sin riesgo a 10 años) | P2 es el ancla obligatoria de la dimensión de riesgo |
| B3 | Completitud de A < 40 % | Sin MRS o sin VMS, "Armonía" no representa a la paciente |
| B4 | Antigüedad del dato más reciente > 90 días | El índice es longitudinal por definición |
| B5 | Edad fuera del rango 40–65 | Fuera del alcance de validez v1.0 (§1.3) |

**Cuando se dispara una regla de bloqueo**, el sistema emite un `Observation` con `status: registered` y `dataAbsentReason`, más una `Task` de recolección de datos dirigida al canal correspondiente (Kapso, portal, o laboratorio).

---

## 8. REGLAS DE SEGURIDAD CLÍNICA Y ESCALAMIENTO

> Esta sección es de **implementación obligatoria previa a cualquier despliegue**. Ningún componente del índice puede activarse en producción sin estas reglas probadas y con evidencia de prueba archivada.

### 8.1 Ideación suicida (PHQ-9, ítem 9)

**Disparador:** respuesta ≥ 1 al ítem 9 del PHQ-9.

**Acción inmediata y no diferible:**
1. **Interrumpir el flujo de scoring.** No mostrar el índice. No continuar el cuestionario.
2. Mostrar mensaje de contención y recursos de crisis vigentes en Argentina.
3. Generar `Flag` FHIR con `status: active`, `category: safety`, prioridad urgente.
4. Notificar al equipo clínico designado en **menos de 15 minutos** vía canal redundante (no solo email).
5. Registrar `Communication` con el acuse del equipo clínico.

**El escalamiento no se automatiza a una respuesta de chatbot.** Un ser humano identificado debe recibir la alerta y acusar recibo. Si el acuse no ocurre en 60 minutos, escalar al contacto secundario.

### 8.2 Valores fisiológicos críticos

| Parámetro | Umbral | Acción |
|---|---|---|
| PAS ≥ 180 o PAD ≥ 110 mmHg | Cualquier medición | Alerta urgente + instrucción de consulta inmediata |
| PAS ≥ 160 o PAD ≥ 100 mmHg | Sostenido ≥ 3 mediciones | Alerta + derivación en 72 h |
| Glucemia en ayunas ≥ 200 mg/dL | Cualquier medición | Derivación en 7 días |
| Lp(a) ≥ 250 nmol/L | Cualquier medición | Notificación al cardiólogo tratante + consejo de tamizaje en cascada familiar |
| PHQ-9 total ≥ 20 | Cualquier evaluación | Derivación a salud mental en 7 días |
| Dolor torácico reportado en canal conversacional | Cualquier mención | Respuesta de emergencia inmediata, sin scoring |

### 8.3 Banda 5 del índice (< 40)

Derivación prioritaria dentro de 7 días a la red FAC. Generación automática de `ServiceRequest` con prioridad `urgent` y `CarePlan` con `intent: order`. Seguimiento activo del cierre de la derivación: si no hay `Encounter` vinculado a los 14 días, se escala al coordinador clínico.

### 8.4 Límites declarados del sistema

El motor **no**: diagnostica, indica ni ajusta medicación, interpreta electrocardiogramas, ni sustituye evaluación médica. Todo output al usuario incluye esta declaración. Toda salida dirigida a profesional incluye la trazabilidad completa de datos de entrada (`Provenance`).

---

## 9. ESQUEMA FHIR R4

### 9.1 Modelo de recursos

```
Patient (Grupo C)
│
├── Observation [epa-index-composite] ················ ÍNDICE EPA
│   │   code: epa-index-total | valueQuantity: 0–100
│   │   component: banda, EPA-C, nivel de confianza
│   │
│   ├── hasMember → Observation [epa-dim-equilibrio]
│   │                └── hasMember → E1…E5
│   ├── hasMember → Observation [epa-dim-precision]
│   │                └── derivedFrom → RiskAssessment
│   └── hasMember → Observation [epa-dim-armonia]
│                    └── derivedFrom → QuestionnaireResponse ×5
│
├── Device (openwearables.io) ──derivedFrom──▶ E2, E3
├── FamilyMemberHistory ────────derivedFrom──▶ P4
├── Provenance (por cada Observation derivada)
├── Flag (reglas de seguridad §8)
└── CarePlan [Plan Bienestar 100 Días®] ──addresses──▶ Índice EPA
```

**Principio de diseño:** cada `Observation` derivada declara su linaje completo mediante `derivedFrom` y `Provenance`. Un auditor —o un revisor de una publicación— debe poder reconstruir el índice desde los datos crudos sin acceso al código.

### 9.2 Observation compuesta — Índice EPA

```json
{
  "resourceType": "Observation",
  "meta": {
    "profile": ["https://epa-bienestar.com.ar/fhir/StructureDefinition/epa-index-composite"],
    "tag": [{ "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-engine",
              "code": "epa-index-v1.1" }]
  },
  "identifier": [{
    "system": "https://epa-bienestar.com.ar/fhir/identifier/epa-index",
    "value": "EPA-IDX-2026-08-16-79679343"
  }],
  "status": "final",
  "category": [{
    "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                 "code": "survey", "display": "Survey" }]
  }],
  "code": {
    "coding": [{
      "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-index",
      "code": "epa-index-total",
      "display": "Índice EPA — puntaje compuesto de salud cardiovascular en transición menopáusica"
    }],
    "text": "Índice EPA total"
  },
  "subject": { "reference": "Patient/[uuid]" },
  "effectiveDateTime": "2026-08-16T10:00:00-03:00",
  "issued": "2026-08-16T10:00:12-03:00",
  "performer": [{ "reference": "Device/epa-scoring-engine-v1" }],
  "valueQuantity": { "value": 63.2, "unit": "puntos", "system": "http://unitsofmeasure.org", "code": "{score}" },
  "interpretation": [{
    "coding": [{ "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-band",
                 "code": "band-3", "display": "Intermedia" }]
  }],
  "component": [
    { "code": { "coding": [{ "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-index",
                             "code": "epa-completeness", "display": "Índice de completitud (EPA-C)" }] },
      "valueQuantity": { "value": 88.0, "unit": "%", "system": "http://unitsofmeasure.org", "code": "%" } },
    { "code": { "coding": [{ "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-index",
                             "code": "epa-confidence", "display": "Nivel de confianza" }] },
      "valueCodeableConcept": { "coding": [{
        "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-confidence",
        "code": "high", "display": "Alta" }] } },
    { "code": { "coding": [{ "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-index",
                             "code": "epa-delta-100d", "display": "Δ-EPA a 100 días" }] },
      "valueQuantity": { "value": 5.7, "unit": "puntos", "system": "http://unitsofmeasure.org", "code": "{score}" } }
  ],
  "hasMember": [
    { "reference": "Observation/[uuid-equilibrio]" },
    { "reference": "Observation/[uuid-precision]" },
    { "reference": "Observation/[uuid-armonia]" }
  ],
  "derivedFrom": [
    { "reference": "Observation/[uuid-le8-score]", "display": "LE8 total (LOINC 96607-7)" }
  ],
  "note": [{
    "text": "Calculo: 0,36 x 68,5 (E) + 0,33 x 58,5 (P) + 0,31 x 62,0 (A) = 63,19 -> 63,2. Motor epa-index-v1.1."
  }]
}
```

### 9.3 Recurso 1 — `Observation` para dimensión E (Equilibrio)

```json
{
  "resourceType": "Observation",
  "meta": { "profile": ["https://epa-bienestar.com.ar/fhir/StructureDefinition/epa-dim-equilibrio"] },
  "status": "final",
  "category": [{ "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                              "code": "vital-signs" }] }],
  "code": {
    "coding": [{ "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-index",
                 "code": "epa-dim-equilibrio",
                 "display": "Dimensión E — Equilibrio (variabilidad fisiológica)" }]
  },
  "subject": { "reference": "Patient/[uuid]" },
  "effectivePeriod": { "start": "2026-07-19T00:00:00-03:00", "end": "2026-08-16T00:00:00-03:00" },
  "valueQuantity": { "value": 68.5, "unit": "puntos", "system": "http://unitsofmeasure.org", "code": "{score}" },
  "device": { "reference": "Device/openwearables-oura-gen4-[uuid]" },
  "component": [
    { "code": { "coding": [
        { "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-index", "code": "epa-bpv-sd",
          "display": "Variabilidad de PA sistólica (SD, 7 días)" },
        { "system": "http://loinc.org", "code": "8480-6", "display": "Systolic blood pressure" }] },
      "valueQuantity": { "value": 9.4, "unit": "mm[Hg]", "system": "http://unitsofmeasure.org", "code": "mm[Hg]" },
      "interpretation": [{ "text": "E1 = 80" }] },

    { "code": { "coding": [{ "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-index",
                             "code": "epa-sri", "display": "Sleep Regularity Index" }] },
      "valueQuantity": { "value": 71.2, "unit": "%", "system": "http://unitsofmeasure.org", "code": "%" },
      "interpretation": [{ "text": "E2 = 55" }] },

    { "code": { "coding": [{ "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-index",
                             "code": "epa-hrv-zscore", "display": "HRV nocturna — z-score vs basal personal" }] },
      "valueQuantity": { "value": -0.72, "unit": "SD", "system": "http://unitsofmeasure.org", "code": "1" },
      "interpretation": [{ "text": "E3 = 80" }] },

    { "code": { "coding": [
        { "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-index", "code": "epa-waist-delta-12m",
          "display": "Cambio de circunferencia de cintura a 12 meses" },
        { "system": "http://loinc.org", "code": "8280-0", "display": "Waist circumference" }] },
      "valueQuantity": { "value": 2.5, "unit": "cm", "system": "http://unitsofmeasure.org", "code": "cm" },
      "interpretation": [{ "text": "E4 = 45" }] },

    { "code": { "coding": [{ "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-index",
                             "code": "epa-glucose-cv", "display": "Coeficiente de variación glucémica" }] },
      "dataAbsentReason": { "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/data-absent-reason",
        "code": "not-performed", "display": "No realizado — sin CGM ni glucemias seriadas" }] } }
  ],
  "derivedFrom": [
    { "reference": "Observation/[uuid-bp-home-series]" },
    { "reference": "Observation/[uuid-sleep-epochs]" }
  ],
  "note": [{ "text": "E5 no computable. Peso redistribuido proporcionalmente entre E1–E4. Completitud E = 90%." }]
}
```

### 9.4 Recurso 2 — `RiskAssessment` para dimensión P (Precisión)

```json
{
  "resourceType": "RiskAssessment",
  "meta": { "profile": ["https://epa-bienestar.com.ar/fhir/StructureDefinition/epa-dim-precision"] },
  "status": "final",
  "method": {
    "coding": [{ "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-index",
                 "code": "epa-dim-precision",
                 "display": "Dimensión P — Precisión (estratificación estructural de riesgo)" }]
  },
  "code": {
    "coding": [{ "system": "http://snomed.info/sct", "code": "1231000000106",
                 "display": "Cardiovascular risk assessment" }]
  },
  "subject": { "reference": "Patient/[uuid]" },
  "occurrenceDateTime": "2026-08-16T10:00:00-03:00",
  "performer": { "reference": "Device/epa-scoring-engine-v1" },
  "basis": [
    { "reference": "Observation/[uuid-lpa]",      "display": "Lp(a) 92 nmol/L — LOINC 43583-4" },
    { "reference": "Observation/[uuid-apob]",     "display": "ApoB 84 mg/dL — LOINC 1884-6" },
    { "reference": "Observation/[uuid-straw10]",  "display": "STRAW+10: estadio -1" },
    { "reference": "FamilyMemberHistory/[uuid]",  "display": "Padre, IAM a los 51 años" },
    { "reference": "Observation/[uuid-bp-mean]" },
    { "reference": "Observation/[uuid-egfr]" }
  ],
  "prediction": [
    { "outcome": { "coding": [{ "system": "http://snomed.info/sct", "code": "266318005",
                                "display": "Cardiovascular disease" }] },
      "probabilityDecimal": 0.061,
      "whenRange": { "high": { "value": 10, "unit": "a", "system": "http://unitsofmeasure.org", "code": "a" } },
      "rationale": "AHA PREVENT™ 2023, riesgo de ECV total a 10 años. P2 = 65." }
  ],
  "note": [{
    "text": "Dimensión P = 58.5. Subcomponentes — P1 (Lp(a) 92 nmol/L): 70 · P2 (PREVENT 6.1%): 65 · P3 (STRAW+10 -1, menopausia no alcanzada): 35 · P4 (1 familiar primer grado): 30 · P5 (ApoB 84): 80. Completitud P = 100%. Potenciador sexo-específico: ninguno activo."
  }]
}
```

### 9.5 Recurso 3 — `QuestionnaireResponse` para dimensión A (Armonía)

```json
{
  "resourceType": "QuestionnaireResponse",
  "meta": { "profile": ["https://epa-bienestar.com.ar/fhir/StructureDefinition/epa-mrs-response"] },
  "questionnaire": "https://epa-bienestar.com.ar/fhir/Questionnaire/epa-mrs-es-AR",
  "status": "completed",
  "subject": { "reference": "Patient/[uuid]" },
  "authored": "2026-08-16T09:42:00-03:00",
  "author": { "reference": "Patient/[uuid]" },
  "source": { "reference": "Patient/[uuid]" },
  "extension": [{
    "url": "https://epa-bienestar.com.ar/fhir/StructureDefinition/capture-channel",
    "valueCodeableConcept": { "coding": [{
      "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-channel",
      "code": "whatsapp-kapso", "display": "WhatsApp Business API (Kapso)" }] }
  }],
  "item": [
    { "linkId": "mrs-1", "text": "Sofocos, sudoración, calores repentinos",
      "answer": [{ "valueCoding": { "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-mrs",
                                    "code": "3", "display": "Severo" } }] },
    { "linkId": "mrs-2", "text": "Molestias del corazón (palpitaciones, opresión)",
      "answer": [{ "valueCoding": { "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-mrs",
                                    "code": "1", "display": "Leve" } }] },
    { "linkId": "mrs-3", "text": "Dificultades para dormir",
      "answer": [{ "valueCoding": { "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-mrs",
                                    "code": "2", "display": "Moderado" } }] }
  ]
}
```

**`Observation` derivada del `QuestionnaireResponse`** (el `QuestionnaireResponse` guarda las respuestas crudas; el puntaje **siempre** vive en una `Observation` derivada, nunca embebido en el cuestionario):

```json
{
  "resourceType": "Observation",
  "status": "final",
  "code": { "coding": [{ "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-index",
                         "code": "epa-mrs-total", "display": "MRS — puntaje total" }] },
  "subject": { "reference": "Patient/[uuid]" },
  "effectiveDateTime": "2026-08-16T09:42:00-03:00",
  "valueQuantity": { "value": 14, "unit": "puntos", "system": "http://unitsofmeasure.org", "code": "{score}" },
  "interpretation": [{ "text": "Moderado. A1 = 50." }],
  "component": [
    { "code": { "coding": [{ "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-mrs",
                             "code": "subscale-somatovegetative" }] },
      "valueQuantity": { "value": 7, "unit": "puntos" } },
    { "code": { "coding": [{ "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-mrs",
                             "code": "subscale-psychological" }] },
      "valueQuantity": { "value": 5, "unit": "puntos" } },
    { "code": { "coding": [{ "system": "https://epa-bienestar.com.ar/fhir/CodeSystem/epa-mrs",
                             "code": "subscale-urogenital" }] },
      "valueQuantity": { "value": 2, "unit": "puntos" } }
  ],
  "derivedFrom": [{ "reference": "QuestionnaireResponse/[uuid]" }]
}
```

### 9.6 Consultas FHIR de referencia

```http
# Índice EPA más reciente de una paciente, con toda la jerarquía
GET /fhir/R4/Observation?subject=Patient/[id]
    &code=https://epa-bienestar.com.ar/fhir/CodeSystem/epa-index|epa-index-total
    &_sort=-date&_count=1&_include=Observation:has-member

# Serie longitudinal para curva Δ-EPA de 100 días
GET /fhir/R4/Observation?subject=Patient/[id]
    &code=https://epa-bienestar.com.ar/fhir/CodeSystem/epa-index|epa-index-total
    &date=ge2026-05-08&_sort=date

# Cohorte: pacientes en banda 4 o 5 sin derivación cerrada
GET /fhir/R4/Observation?code=...|epa-index-total&value-quantity=lt55
    &_has:ServiceRequest:based-on:status=active

# Inventario de completitud (conteo puro, sin traer recursos)
GET /fhir/R4/Observation?code=...|epa-index-total&_summary=count
```

---

## 10. CODESYSTEM Y VALUESETS LOCALES

### 10.1 CodeSystems a publicar en FAVALORO

| URI canónica | Contenido |
|---|---|
| `https://epa-bienestar.com.ar/fhir/CodeSystem/epa-index` | Códigos del índice y todos los subcomponentes derivados |
| `https://epa-bienestar.com.ar/fhir/CodeSystem/epa-band` | Bandas interpretativas 1–5 |
| `https://epa-bienestar.com.ar/fhir/CodeSystem/epa-confidence` | Niveles de confianza (high / medium / low / not-reportable) |
| `https://epa-bienestar.com.ar/fhir/CodeSystem/epa-straw10` | Estadios STRAW+10 (−5 … +2) |
| `https://epa-bienestar.com.ar/fhir/CodeSystem/epa-mrs` | Ítems, subescalas y niveles de respuesta de MRS |
| `https://epa-bienestar.com.ar/fhir/CodeSystem/epa-channel` | Canales de captura (whatsapp-kapso, portal, wearable, laboratorio, consultorio) |
| `https://epa-bienestar.com.ar/fhir/CodeSystem/epa-engine` | Versionado del motor de scoring |

### 10.2 Política de versionado del motor

Todo `Observation` de índice lleva `meta.tag` con la versión del motor (`epa-index-v1.1`). **Recalcular retroactivamente índices históricos con una versión nueva del motor está prohibido.** Al cambiar la versión, se emiten nuevos recursos y los antiguos conservan su tag. Sin esta regla, cualquier análisis longitudinal —y cualquier publicación derivada— es irreproducible.

### 10.3 Nota sobre SNOMED CT

Los conceptos SNOMED CT referenciados en este documento (estados menopáusicos, historia familiar de ECV, evaluación de riesgo cardiovascular) **requieren verificación contra la release internacional vigente y contra la extensión argentina antes del despliegue en producción.** No deben codificarse desde este documento sin ese paso. Donde no exista concepto verificado, se usa exclusivamente el CodeSystem local con `text` descriptivo, lo cual es práctica FHIR válida y preferible a un código incorrecto.

---

## 11. ARQUITECTURA DE CÓMPUTO EN MEDPLUM

### 11.1 Bots y disparadores

| Bot | Disparador | Responsabilidad |
|---|---|---|
| `epa-bot-equilibrio` | `Subscription` sobre ingesta de openwearables.io + `Observation` de PA | Computar E1–E5, emitir `Observation` de dimensión E |
| `epa-bot-precision` | `Subscription` sobre `Observation` de laboratorio + actualización de `Condition` | Computar P1–P5, emitir `RiskAssessment` |
| `epa-bot-armonia` | `Subscription` sobre `QuestionnaireResponse` | Puntuar PROs, emitir `Observation` derivadas, **evaluar reglas §8 antes de puntuar** |
| `epa-bot-composite` | Cron diario 06:00 ART + `Subscription` sobre las tres dimensiones | Componer el índice, evaluar completitud y bloqueos, emitir `Observation` compuesta |
| `epa-bot-safety` | `Subscription` sobre toda `Observation` y `QuestionnaireResponse` | Reglas §8. **Se ejecuta primero y puede abortar el pipeline.** |

**Stack:** TypeScript en modo estricto, logging JSON estructurado, cumplimiento FHIR R4 completo. Despliegue en AWS Local Zone Buenos Aires (soberanía de datos, Ley 25.326).

### 11.2 Orden de ejecución obligatorio

```
Ingesta de dato
    ↓
epa-bot-safety ──── ¿regla §8 disparada? ──SÍ──▶ Flag + notificación + ABORTAR pipeline
    ↓ NO
epa-bot-{equilibrio | precision | armonia}
    ↓
epa-bot-composite ── ¿regla de bloqueo §7.2? ──SÍ──▶ Observation registered + Task
    ↓ NO
Observation compuesta + actualización de CarePlan
```

**El bot de seguridad corre primero, siempre, sin excepción.** Una paciente que reporta ideación suicida no debe recibir un puntaje; debe recibir una persona.

### 11.3 Idempotencia y trazabilidad

Cada bot usa `conditional update` sobre `Observation.identifier` (formato `EPA-{DIM}-{YYYY-MM-DD}-{patientShortId}`) para garantizar idempotencia ante reintentos. Cada emisión genera un `Provenance` con `agent` = el bot, `entity` = los recursos fuente, y `signature` cuando aplique la Ley 25.506 de firma electrónica.

---

## 12. VALIDACIÓN CIENTÍFICA Y PLAN DE PUBLICACIÓN

### 12.1 Estado actual de la evidencia

**Debe declararse sin ambigüedad en todo material derivado:**

| Componente | Estado |
|---|---|
| Instrumentos individuales (MRS, PHQ-9, GAD-7, PSQI, Lp(a), PREVENT, STRAW+10, SRI) | ✅ Validados individualmente en la literatura |
| **Ponderaciones del compuesto (36/33/31)** | ⚠️ **Derivadas conceptualmente de un modelo publicado. NO validadas empíricamente en esta población.** Corregidas en v1.1 (§0). |
| **Cortes de scoring por subcomponente** | ⚠️ **Propuestos por EPA. Requieren calibración.** |
| **MCID de +5.0 puntos** | ⚠️ **Hipótesis de diseño. No es un hallazgo.** |
| Valor predictivo del índice sobre eventos CV | ❌ **No establecido.** Requiere seguimiento a ≥ 5 años. |

> Ninguna comunicación a inversores, instituciones o pacientes puede presentar el Índice EPA como validado hasta completar §12.2. Sobrevender el estado de validación es el riesgo reputacional más serio de este proyecto — y el que un due diligence técnico detecta primero.

### 12.2 Plan de validación por etapas

**Etapa 1 — Validez aparente y de contenido (Q4 2026).**
Panel Delphi con el Comité de Enfermedades CV en la Mujer de FAC (Aquieri, Crosa, Cavenago, Pages) + Dr. Barbagelata. Objetivo: consenso sobre subcomponentes y cortes. Entregable: acta de consenso con ≥ 80 % de acuerdo por ítem.

**Etapa 2 — Consistencia interna y estructura factorial (Q1 2027).**
Sobre el baseline de MAMA-LE8 (n = 100, sitios FAC Buenos Aires, Córdoba, Rosario): α de Cronbach por dimensión, análisis factorial confirmatorio de la estructura de tres dimensiones, correlación con LE8 total. **Hipótesis a priori: correlación moderada (r ≈ 0.5–0.7) con LE8.** Una correlación > 0.85 significaría que el índice no aporta información nueva y obligaría a rediseñarlo.

**Etapa 3 — Validez de constructo y recalibración de pesos (Q2–Q3 2027).**
Regresión de las tres dimensiones contra marcadores intermedios independientes (velocidad de onda de pulso, calcio coronario en submuestra). Recalibración empírica de las ponderaciones. **Si los pesos empíricos difieren materialmente de 38/32/30, se adoptan los empíricos y se documenta el cambio como v2.0.**

**Etapa 4 — Sensibilidad al cambio y MCID (Q3 2027).**
Sobre la cohorte de Plan Bienestar 100 Días®: tamaño del efecto estandarizado del Δ-EPA, MCID por método de anclaje contra escala de impresión global de cambio.

**Etapa 5 — Validez predictiva (2029+).**
Seguimiento longitudinal contra eventos CV incidentes. Único estadio que permite reclamar valor pronóstico.

### 12.3 Publicación objetivo

**Paper conceptual (someter Q1 2027):**
> *"Beyond Life's Essential 8: incorporating physiological variability and patient-reported outcomes into cardiovascular health scoring during the menopausal transition — design and rationale of the EPA Index"*

Revistas objetivo por orden: *Journal of the American Heart Association* (JAHA) · *Menopause* · *European Journal of Preventive Cardiology* · *Revista de la Federación Argentina de Cardiología* (versión en español).

**Autoría propuesta:** D'Alessandro (primer autor) · Bonomini (metodología) · Comité de Mujer FAC · Barbagelata (autor senior).

**Referencia obligatoria en el paper:** el modelo de determinantes debe citarse como
Choi, E., & Sonin, J. (2019). *Determinants of Health.* GoInvo. CC BY 4.0 — indicando la
versión de metodología empleada.

**Registro previo:** protocolo de validación en ClinicalTrials.gov u OSF **antes** de la Etapa 2. El pre-registro es lo que distingue un índice científico de un score de marketing.

### 12.4 El activo estratégico

Este índice es simultáneamente producto y **instrumento de generación de un activo de datos**. La cohorte de referencia mundial en transición menopáusica es SWAN: aproximadamente 3.300 mujeres, mayoría estadounidense, mujeres hispanas sub-representadas, diseño de hace tres décadas, sin datos continuos de wearables ni estructura interoperable.

Una cohorte latinoamericana con datos continuos de variabilidad fisiológica, PROs longitudinales y estructura FHIR R4 nativa **no existe hoy en ninguna parte del mundo**. Ese es el activo no replicable a corto plazo. El Índice EPA es el instrumento que lo construye.

---

## 13. LIMITACIONES DECLARADAS

1. **Los pesos no están validados empíricamente.** Derivan de un modelo de determinantes publicado, no de datos de esta población.
2. **Dependen de una fuente externa que puede cambiar.** El modelo de GoInvo ya fue revisado tres veces entre 2017 y 2018. Toda versión de esta especificación debe declarar qué versión de la metodología usa, y conviene revisar la fuente antes de cada publicación.
9. **Los cortes de scoring son propuestos, no calibrados.** Se basan en umbrales de la literatura donde existen y en juicio experto donde no.
3. **Sesgo de acceso a dispositivos.** La dimensión E depende de wearables y monitoreo domiciliario de PA. Esto introduce sesgo socioeconómico sistemático. La redistribución de peso (§7.2) lo mitiga parcialmente pero **no lo elimina**: las pacientes con menos recursos tendrán índices con menor completitud y menor confianza. Esto debe monitorearse activamente como métrica de equidad, no tratarse como ruido.
4. **Heterogeneidad entre dispositivos.** Oura, Apple Watch y Google Fit difieren en algoritmos de estadificación del sueño y en captura de HRV. El uso de z-score contra basal personal (E3) mitiga esto para HRV pero no para SRI. **Los cambios de dispositivo deben registrarse y romper la serie basal.**
5. **PSQI tiene restricciones de licencia comercial** (§A3). Debe resolverse antes de producción.
6. **La escala de autoeficacia (A5) no está validada psicométricamente.**
7. **Alcance limitado al Grupo C.** Los cortes no son transferibles a Grupos A, B ni D sin recalibración completa.
8. **Sin validez predictiva establecida.** No se puede afirmar que un Índice EPA más alto se asocie a menos eventos cardiovasculares. Esa afirmación requiere la Etapa 5 y no antes.

---

## ANEXO A — TABLA LOINC CONSOLIDADA

**Leyenda:** ✅ código de alta confianza · ⚠️ requiere verificación contra la release LOINC vigente antes de producción · 🔧 sin LOINC disponible, se usa CodeSystem local

| Componente | LOINC | Estado | Descripción | Unidad |
|---|---|:---:|---|---|
| **Contexto LE8** ||||
| LE8 puntaje total | `96607-7` | ✅ | Cardiovascular health score, LE8 | {score} |
| Actividad física | `68516-4` | ✅ | Physical activity | min/sem |
| Exposición a nicotina | `39240-7` | ✅ | Nicotine exposure | — |
| Duración del sueño | `93832-4` | ✅ | Sleep duration | h |
| **Dimensión E — Equilibrio** ||||
| PA panel | `85354-9` | ✅ | Blood pressure panel | — |
| PA sistólica | `8480-6` | ✅ | Systolic blood pressure | mm[Hg] |
| PA diastólica | `8462-4` | ✅ | Diastolic blood pressure | mm[Hg] |
| Variabilidad de PAS (SD) | `epa-bpv-sd` | 🔧 | Derivado | mm[Hg] |
| Sleep Regularity Index | `epa-sri` | 🔧 | Derivado | % |
| SD de intervalo R-R | `80404-7` | ⚠️ | R-R interval SD | ms |
| HRV z-score vs basal | `epa-hrv-zscore` | 🔧 | Derivado | SD |
| Peso corporal | `29463-7` | ✅ | Body weight | kg |
| Circunferencia de cintura | `8280-0` | ⚠️ | Waist circumference | cm |
| Δ cintura 12 meses | `epa-waist-delta-12m` | 🔧 | Derivado | cm |
| IMC | `39156-5` | ✅ | Body mass index | kg/m² |
| Glucosa en ayunas | `1558-6` | ✅ | Fasting glucose | mg/dL |
| Glucosa media (CGM) | `97507-8` | ⚠️ | Mean glucose, CGM | mg/dL |
| CV glucémico | `epa-glucose-cv` | 🔧 | Derivado | % |
| HbA1c | `4548-4` | ✅ | Hemoglobin A1c | % |
| **Dimensión P — Precisión** ||||
| Lp(a) molar (preferido) | `43583-4` | ⚠️ | Lipoprotein(a), moles/volume | nmol/L |
| Lp(a) másica | `10835-7` | ⚠️ | Lipoprotein(a), mass/volume | mg/dL |
| Riesgo ECV 10 años (PCE) | `79423-0` | ⚠️ | CVD 10Y risk, ACC-AHA PCE | % |
| Riesgo ECV 10 años (PREVENT) | `epa-prevent-10y` | 🔧 | Derivado — sin LOINC aún | % |
| Estadio STRAW+10 | `epa-straw10` | 🔧 | CodeSystem local | — |
| Apolipoproteína B | `1884-6` | ⚠️ | Apolipoprotein B | mg/dL |
| Colesterol no-HDL | `43396-1` | ⚠️ | Cholesterol non-HDL | mg/dL |
| LDL calculado | `13457-7` | ✅ | LDL cholesterol, calculated | mg/dL |
| HDL | `2085-9` | ✅ | HDL cholesterol | mg/dL |
| Triglicéridos | `2571-8` | ✅ | Triglyceride | mg/dL |
| Colesterol total | `2093-3` | ✅ | Cholesterol, total | mg/dL |
| Historia familiar ECV prematura | — | 🔧 | Recurso `FamilyMemberHistory` | — |
| **Dimensión A — Armonía** ||||
| MRS total | `epa-mrs-total` | 🔧 | CodeSystem local | {score} |
| MRS subescalas (×3) | `epa-mrs-subscale-*` | 🔧 | CodeSystem local | {score} |
| Frecuencia VMS diaria | `epa-vms-daily-freq` | 🔧 | Derivado | 1/d |
| PSQI global | `epa-psqi-global` | 🔧 | Sin LOINC. ⚠️ Verificar licencia | {score} |
| PHQ-9 total | `44261-6` | ✅ | PHQ-9 total score | {score} |
| PHQ-9 ítem 9 | `44260-8` | ⚠️ | PHQ-9 item 9 — **regla §8.1** | {score} |
| GAD-7 total | `70274-6` | ✅ | GAD-7 total score | {score} |
| Autoeficacia CV | `epa-selfefficacy` | 🔧 | Instrumento propio, sin validar | {score} |
| **Compuestos EPA** ||||
| Índice EPA total | `epa-index-total` | 🔧 | CodeSystem local | {score} |
| Dimensión E | `epa-dim-equilibrio` | 🔧 | CodeSystem local | {score} |
| Dimensión P | `epa-dim-precision` | 🔧 | CodeSystem local | {score} |
| Dimensión A | `epa-dim-armonia` | 🔧 | CodeSystem local | {score} |
| Completitud EPA-C | `epa-completeness` | 🔧 | CodeSystem local | % |
| Δ-EPA 100 días | `epa-delta-100d` | 🔧 | CodeSystem local | {score} |

---

## CONTROL DEL DOCUMENTO

| Versión | Fecha | Cambios | Autor |
|---|---|---|---|
| 1.0 | Agosto 2026 | Especificación inicial | Dr. A. S. D'Alessandro · Equipo de Producto EPA |
| **1.1** | **Agosto 2026** | **Corrección de ponderaciones: 38/32/30 → 36/33/31. Origen del error y análisis de impacto en §0. Atribución CC BY a Choi & Sonin incorporada.** | **Dr. A. S. D'Alessandro** |

**Aprobaciones requeridas antes de implementación:**

| Rol | Responsable | Alcance | Estado |
|---|---|---|---|
| Revisión clínica | Dr. A. Barbagelata | Cortes, reglas de seguridad, límites | ☐ Pendiente |
| Revisión metodológica | M. P. Bonomini (ITBA) | Ponderaciones, plan estadístico | ☐ Pendiente |
| Consenso Comité Mujer FAC | Aquieri · Crosa · Cavenago · Pages | Validez de contenido (Delphi) | ☐ Pendiente |
| Revisión técnica FHIR | CTO | Perfiles, bots, terminología | ☐ Pendiente |
| Ética / CEI | Comité de Ética | Uso de datos, reglas de seguridad, consentimiento | ☐ Pendiente |
| Legal | Asesoría | Ley 25.326 · 26.529 · 25.506 · licencia PSQI | ☐ Pendiente |

---

*Documento confidencial de EPA Bienestar IA. Plan Bienestar 100 Días® es marca registrada del Dr. Alejandro Sergio D'Alessandro para EPA Bienestar IA. Life's Essential 8™ y PREVENT™ son marcas de la American Heart Association, utilizadas aquí con fines de referencia científica.*
