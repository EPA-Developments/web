# Nota técnica NT-2026-02
## Redenominación de la dimensión A del Índice EPA: Armonía → Autonomía

**Para:** Dr. Alejandro Barbagelata (MD, FAHA, FSCAI) — Asesor Médico Principal
Ing. María Paula Bonomini — Directora, Laboratorio de IA, ITBA

**De:** Equipo de Producto — EPA Bienestar IA (borrador para conformidad y firma del
Dr. Alejandro S. D'Alessandro)

**Fecha:** Octubre de 2026
**Asunto:** Cambio de nombre y de definición de la dimensión A, sin cambios de cálculo
**Adjunto:** `INDICE-EPA_SPEC_v1.2` (especificación técnica actualizada) ·
`fhir/CodeSystem-epa-index.json`
**Acción requerida:** revisión clínica de la nueva definición y de los puntos abiertos (§6)
antes de usar el término en material para el comité o para pacientes

---

## Resumen

La dimensión A del Índice EPA pasa a llamarse **Autonomía** (antes **Armonía**). La sigla
pública del sitio ya dice *Equilibrio · Precisión · Autonomía* desde octubre de 2026; esta
nota alinea la especificación con ese cambio y deja registro escrito de qué se modificó.

**Es un cambio de denominación y de definición, no de cálculo.** La ponderación (31 %), los
subcomponentes A1–A5, sus pesos, sus cortes, la fórmula del índice y los códigos FHIR quedan
exactamente como en la v1.1.

---

## 1. Qué cambia

| Elemento | Antes (v1.1) | Ahora (v1.2) |
|---|---|---|
| Nombre de la dimensión A | Armonía | **Autonomía** |
| Definición operacional | Carga sintomática, calidad de vida y capacidad de acción reportadas por la propia paciente, mediante instrumentos validados | Lo mismo, **como base para que decida sobre su salud junto a su equipo médico** (automanejo y decisión compartida) |
| Frase de síntesis | "Armonía es lo que la mujer siente." | "Autonomía es lo que la mujer siente y decide, junto a su equipo médico." |
| `display` FHIR del código `epa-dim-armonia` | No había recurso `CodeSystem` publicado | **"Autonomía"**, con el nombre anterior como `designation` |
| Componente de automanejo y decisión compartida | No existía | **A6, propuesto, sin ponderar** (§4) |
| Título del documento de especificación | Decía "v1.0" aunque el documento era la v1.1 | Corregido: "v1.2" |

## 2. Qué NO cambia

| Elemento | Estado |
|---|---|
| Ponderación de A | **31 %** |
| A1 MRS (30 %) · A2 VMS (25 %) · A3 PSQI (20 %) · A4 PHQ-9 + GAD-7 (15 %) · A5 Autoeficacia (10 %) | Mismos instrumentos, pesos y tablas de corte |
| Fórmula del índice, Δ-EPA, completitud EPA-C, reglas de bloqueo | Sin cambios |
| Reglas de seguridad clínica (§8, incluida la del ítem 9 del PHQ-9) | Sin cambios |
| Códigos `epa-dim-armonia` y `epa-bot-armonia` | **No se renombran** |
| Versión del motor de scoring | Sigue siendo `epa-index-v1.1` |

**Por qué no se renombran los códigos.** Un código FHIR es un identificador, no una
etiqueta. Las `Observation` ya emitidas con `epa-dim-armonia`, las consultas de §9.6 y
cualquier integración que filtre por ese código dejarían de encontrar los datos. La práctica
correcta es mantener el `code`, actualizar `display` y `definition`, y conservar el nombre
anterior como `designation`.

**Por qué no cambia la versión del motor.** El tag `epa-index-vX.Y` identifica el
resultado numérico. Como ningún número cambia, emitir un tag nuevo generaría una ruptura
artificial en las series longitudinales sin ningún beneficio. No hay nada que recalcular ni
pacientes que reevaluar.

## 3. Motivo

- **Coherencia con la comunicación pública.** El sitio ya presenta la sigla como
  *Equilibrio · Precisión · Autonomía*, con el mensaje "Autonomía para decidir sobre tu
  salud, junto a tu equipo médico". La especificación no puede usar otro nombre.
- **El nombre anterior describía un estado, no un rol.** "Armonía" sugería un equilibrio
  emocional a alcanzar. "Autonomía" pone el foco en la paciente como protagonista de las
  decisiones sobre su salud, sin quitarle lugar al equipo médico.
- **La dimensión ya tenía el germen.** A5 (autoeficacia y activación) y la definición
  operacional ("capacidad de acción") ya apuntaban en esta dirección.

## 4. Componente propuesto: A6 — Automanejo y decisión compartida

| Aspecto | Definición |
|---|---|
| Estado | **Propuesto. Sin ponderar. Pendiente de validación clínica y psicométrica.** No entra en el puntaje de A, ni en EPA-C, ni en las reglas de bloqueo. No se emiten `Observation`. |
| Constructo | Capacidad de la paciente para manejar su plan de cuidado y participar en las decisiones sobre su salud junto a su equipo médico |
| Instrumento candidato | La escala propia de EPA ya prevista en A5, ampliada con ítems de decisión compartida a definir por el comité |
| Validación | La misma que ya exige A5: psicométrica (§12.2) y contra PAM-13 en un submuestreo de MAMA-LE8. **Hoy la escala propia no está validada.** |
| Código FHIR | No se asigna hasta que exista una definición aprobada |

**Sobre PAM-13.** No se adopta como instrumento del índice. Patient Activation Measure es
propiedad de **Insignia Health** y su uso requiere licencia y autorización previa. Esto vale
también para el submuestreo de validación: usar PAM-13 como referencia en MAMA-LE8 exige
gestionar la autorización antes de recolectar datos.

## 5. Impacto en FHIR R4

- Se publica en el repositorio el primer recurso de terminología:
  `fhir/CodeSystem-epa-index.json`.
  - `url`: `https://epa-bienestar.com.ar/fhir/CodeSystem/epa-index` (la misma URI canónica
    que declara §10.1 de la especificación).
  - `version`: `1.2`; `status`: `draft`; `date`: `2026-10-17`.
  - `content`: `fragment`, porque contiene solo las tres dimensiones y no todos los códigos
    de `epa-index`.
  - Concepto `epa-dim-armonia`: `display` = "Autonomía"; `designation` = "Armonía" con uso
    SNOMED CT `900000000000013009` (*Synonym*).
- Validado como CodeSystem FHIR 4.0.1.
- No había ValueSets ni ConceptMaps en el repositorio, así que no hubo `display` copiados
  que actualizar.
- Los nombres de los bots (`epa-bot-armonia`) son identificadores de despliegue en Medplum
  y no forman parte del CodeSystem. Se mantienen.
- **Pendiente fuera de este repositorio:** cargar el CodeSystem en FAVALORO
  (`https://api.epa-bienestar.com.ar/fhir/R4`) y revisar si el motor escribe un `display`
  en las `Observation` de dimensión A. Las nuevas deberían decir "Autonomía"; las
  existentes no se modifican.

## 6. Puntos abiertos para los revisores

**Al Dr. Barbagelata (revisión clínica):**

1. ¿Está de acuerdo con la nueva definición operacional de A, o prefiere que la v1.2 la
   deje igual a la v1.1 y que "Autonomía" quede solo como nombre?
2. ¿A6 debe ser un componente separado o una ampliación de A5? Ambos miden constructos
   cercanos (activación, autoeficacia, participación en decisiones).
3. Riesgo de comunicación: el nombre "Autonomía" promete más de lo que A mide hoy, que son
   resultados reportados por la paciente. ¿Alcanza con la advertencia de §00 de la
   especificación, o conviene revisar los textos para pacientes?

**A la Ing. Bonomini (revisión metodológica):**

1. La correspondencia de A con los determinantes *Circunstancias sociales* (24 %) y
   *Ambiente físico* (7 %) ya era de alineación conceptual. ¿El nuevo nombre la debilita al
   punto de tener que declararlo en publicaciones?
2. Si A6 llega a ponderarse, ¿se recalibra dentro del 31 % de A o se reabre el reparto
   entre dimensiones? Cualquiera de las dos opciones exige nueva versión del motor.

---

## 7. Estado de los entregables

| Entregable | Estado |
|---|---|
| `INDICE-EPA_SPEC_v1.2` (MD) | ✅ Creada; la v1.1 se conserva sin modificar |
| `fhir/CodeSystem-epa-index.json` | ✅ Creado y validado (FHIR 4.0.1) |
| Sitio web público | ✅ Sigla actualizada en octubre de 2026 |
| `LEEME.md` | ✅ Apunta a la v1.2 y a esta nota |
| Especificación en DOCX / PDF | ⏳ Pendiente: regenerar desde la v1.2 |
| CodeSystem cargado en FAVALORO | ⏳ Pendiente |
| `display` en el motor de scoring | ⏳ Pendiente de revisión |
| Validación de A6 | ⏳ Pendiente: sujeta a los puntos de §6 |

---

*EPA Bienestar IA · Húsares 2248, CP 1428, CABA, Argentina · Documento confidencial de uso interno y comité científico.*
