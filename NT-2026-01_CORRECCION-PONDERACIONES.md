# Nota técnica NT-2026-01
## Corrección de las ponderaciones del Índice EPA

**Para:** Dr. Alejandro Barbagelata (MD, FAHA, FSCAI) — Asesor Médico Principal
Ing. María Paula Bonomini — Directora, Laboratorio de IA, ITBA

**De:** Dr. Alejandro S. D'Alessandro — CEO y Co-Fundador, EPA Bienestar IA

**Fecha:** Agosto de 2026
**Asunto:** Corrección de un error heredado en las ponderaciones del Índice EPA
**Adjunto:** `INDICE-EPA_SPEC_v1.1` (especificación técnica actualizada)
**Acción requerida:** revisión y conformidad antes del panel Delphi con el Comité de Mujer de FAC

---

## Resumen

Detectamos un **error aritmético heredado** en los porcentajes del modelo de determinantes de
salud que sustentan las ponderaciones del Índice EPA. El error no es nuestro en origen —
proviene de la primera versión publicada de la metodología de GoInvo, que sus autores
rectificaron pocas semanas después— pero **estuvo incorporado en toda nuestra documentación
desde el comienzo**.

Ya lo comenté verbalmente con el Dr. Barbagelata usando los valores corregidos. Esta nota
formaliza el hallazgo, cuantifica su impacto y deja registro escrito de la corrección.

**Las ponderaciones pasan de 38 / 32 / 30 a 36 / 33 / 31.**

---

## 1. Qué se encontró

Nuestra documentación calculaba el promedio del determinante conductual así:

```
Comportamiento: (50 + 38 + 40 + 39 + 36 + 45 + 30) / 6 = 46,33
```

Son **siete valores de fuente divididos por seis**. La suma de los siete es 278; el promedio
correcto es 278 / 7 = 39,71.

Ese cálculo es idéntico al publicado en la **versión 1 de la metodología de GoInvo
(26 de julio de 2017)**. La página de metodología vigente conserva esa línea con una nota al
pie que consigna que un error de cálculo original en 'Comportamiento' fue rectificado y que
los valores subsiguientes se actualizaron. Nuestros documentos quedaron anclados a la versión
previa a esa corrección.

Un segundo indicio estaba a la vista y no lo advertimos: nuestra propia normalización
declaraba un total de **100,4 %**. Una normalización correcta suma exactamente 100. Ese
excedente era el error señalándose solo.

---

## 2. Valores vigentes

GoInvo revisó la metodología en **v2 (30 ago 2017)**, reduciendo de siete a cinco las fuentes
utilizadas para el determinante conductual, y confirmó los mismos resultados en **v3
(15 nov 2018)**, que es la versión actual.

| Determinante | Nuestra documentación | Valor vigente |
|---|---:|---:|
| Comportamiento individual | 38 % | **36 %** |
| Circunstancias sociales | 23 % | **24 %** |
| Genética y biología | 21 % | **22 %** |
| Cuidado médico | 11 % | **11 %** |
| Ambiente físico | 7 % | **7 %** |

El póster oficial en español —traducido por Roberto Laureles y publicado en abril de 2020—
consigna 36 / 24 / 22 / 11 / 7. **El póster siempre estuvo bien; lo que estaba mal era nuestra
transcripción de la metodología.**

---

## 3. Ponderaciones del Índice EPA

La derivación no cambia de lógica, solo de insumos:

| Dimensión | Derivación | Antes | Ahora |
|---|---|---:|---:|
| **E — Equilibrio** | Comportamiento | 38 % | **36 %** |
| **P — Precisión** | Genética + Cuidado médico | 32 % | **33 %** |
| **A — Armonía** | Social + Ambiente | 30 % | **31 %** |
| | | 100 % | **100 %** |

Fórmula actualizada:

```
Índice EPA  =  0,36 · E  +  0,33 · P  +  0,31 · A
```

El divisor de reescalado del Δ-EPA a 100 días pasa de 0,68 a **0,67** (= 0,36 + 0,31),
manteniéndose la exclusión deliberada de la dimensión P del cálculo del delta.

---

## 4. Magnitud del impacto

**Esta es la pregunta central, y la respuesta es tranquilizadora.**

El desplazamiento del índice para un mismo perfil está **analíticamente acotado**:

```
Δ  =  EPA(v1.1) − EPA(v1.0)  =  −0,02 · E  +  0,01 · P  +  0,01 · A
```

Como cada dimensión está acotada en el intervalo [0, 100], el desplazamiento **máximo teórico
es de ±2,0 puntos** sobre una escala de 0 a 100. Es exactamente cero cuando las tres
dimensiones tienen el mismo valor.

Simulación sobre 200.000 perfiles sintéticos (μ = 68, σ = 16 por dimensión):

| Métrica | Valor |
|---|---:|
| Desplazamiento medio | −0,001 puntos |
| Desvío estándar | 0,385 puntos |
| Rango observado | −1,45 a +1,55 |
| Casos con desplazamiento superior a 1,0 punto | 0,75 % |
| **Casos que cambian de banda clínica** | **2,09 %** |

**Consecuencias operativas:**

- **No corresponde reevaluar pacientes.** El cambio afecta a aproximadamente 1 de cada 48
  evaluaciones, y únicamente a las que ya se encontraban dentro de dos puntos de un umbral
  de banda.
- **No se invalidan los datos ya recolectados**, siempre que cada recurso `Observation`
  declare la versión del motor que lo generó. Esa regla ya estaba en la especificación
  (§10.2) y ahora se vuelve indispensable.
- **No se recalculan índices históricos.** Se emiten recursos nuevos con el tag
  `epa-index-v1.1`; los anteriores conservan `epa-index-v1.0`.

---

## 5. Problema de atribución, y su corrección

Nuestra documentación describía la metodología —enumerando OMS, NEJM, Health Affairs,
Institute of Medicine, JAMA, DHHS y Universidad de Wisconsin— **sin acreditar a los autores
del modelo**.

El trabajo está publicado bajo licencia Creative Commons Attribution 4.0, que exige
atribución. La omisión era, estrictamente, un incumplimiento de los términos de la licencia.

A partir de v1.1, toda referencia debe incluir:

> Choi, E., & Sonin, J. (2019). *Determinants of Health.* GoInvo. CC BY 4.0.
> https://www.goinvo.com/vision/determinants-of-health

Y **especificar la versión de metodología utilizada** (v3, 15 nov 2018).

---

## 6. Lecciones que incorporamos al proceso

1. **Toda constante numérica heredada debe tener fuente, versión y fecha de verificación.**
   El modelo de GoInvo fue revisado tres veces entre 2017 y 2018. Copiar un número sin
   registrar de qué versión proviene es una deuda técnica que vence en el peor momento posible.

2. **Una normalización que no suma 100 es un error, no un redondeo.** Nuestro 100,4 % estuvo
   publicado durante meses.

3. **Se verifica la fuente antes de cada publicación**, no solo al inicio del proyecto. Queda
   incorporado como paso obligatorio previo a someter el paper conceptual.

4. **La trazabilidad del error es un activo.** La especificación v1.1 incluye una fe de erratas
   (§0) que documenta el origen, la magnitud y la corrección. Un revisor que compare una
   presentación de comienzos de 2026 con la publicación de 2027 va a encontrar la explicación
   escrita, en lugar de una discrepancia sin justificar.

---

## 7. Lo que este hallazgo **no** cambia

- **La arquitectura conceptual del índice permanece intacta.** Tres dimensiones —varianza
  fisiológica, riesgo estructural y outcomes reportados por la paciente— con tres fuentes de
  datos y tres clases de recursos FHIR.
- **La tesis central se sostiene:** Life's Essential 8 mide niveles; la transición menopáusica
  es un fenómeno de varianza. Eso no depende de ningún porcentaje.
- **El estado de validación es el mismo que antes.** Las ponderaciones siguen siendo
  **derivadas conceptualmente y no validadas empíricamente** en nuestra población. Corregir un
  error aritmético no las convierte en validadas.
- **El plan de recalibración empírica sobre MAMA-LE8 no se modifica** (§12.2, Etapa 3). Si los
  pesos empíricos difieren de 36 / 33 / 31, se adoptan los empíricos y se documenta como v2.0.

---

## 8. Consultas concretas al comité

**Al Dr. Barbagelata (revisión clínica):**

1. ¿Confirma que 36 / 33 / 31 es la base adecuada para presentar ante el Comité de
   Enfermedades Cardiovasculares en la Mujer de FAC en el panel Delphi?
2. ¿Corresponde incluir la fe de erratas en el material que circule a los miembros del comité,
   o alcanza con dejarla en la especificación técnica? Mi inclinación es incluirla: llegar con
   el error propio ya documentado fortalece la posición en vez de debilitarla.
3. ¿Ve algún inconveniente en el criterio de no reevaluar pacientes, dado el 2,09 % de cambio
   de banda?

**A la Ing. Bonomini (revisión metodológica):**

1. ¿Considera adecuada la simulación de 200.000 perfiles con μ = 68 y σ = 16, o prefiere que
   la rehagamos sobre la distribución empírica del baseline de MAMA-LE8 cuando esté disponible?
2. Dado que los pesos van a recalibrarse empíricamente en la Etapa 3, ¿tiene sentido sostener
   la derivación desde el modelo de determinantes, o convendría declararlos directamente como
   **priors informados** sujetos a actualización? La segunda opción es más honesta desde lo
   estadístico; la primera es más comunicable ante instituciones.
3. ¿Corresponde pre-registrar las ponderaciones actuales antes de la Etapa 2, para evitar
   cualquier sospecha de ajuste posterior a los datos?

---

## 9. Estado de los entregables

| Entregable | Estado |
|---|---|
| `INDICE-EPA_SPEC_v1.1` (MD · DOCX · PDF) | ✅ Actualizado, con fe de erratas §0 |
| Sitio web público | ✅ Actualizado a 36 / 24 / 22 / 11 / 7 y 36 / 33 / 31 |
| Atribución CC BY a Choi & Sonin | ✅ Incorporada en especificación y sitio |
| Motor de scoring en Medplum | ⏳ Pendiente: actualizar constantes y tag a `epa-index-v1.1` |
| Material para panel Delphi de FAC | ⏳ Pendiente: sujeto a conformidad de esta nota |
| Materiales para inversores | ⏳ Pendiente de revisión: verificar toda mención a "38 %" |

---

*EPA Bienestar IA · Húsares 2248, CP 1428, CABA, Argentina · Documento confidencial de uso interno y comité científico.*
