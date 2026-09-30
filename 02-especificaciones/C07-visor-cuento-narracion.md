---
id: C07
nombre: Visor de Cuento con Narración
tipo: UI
modulo: M3
mvp: true
historias: [HU-03, HU-04]
componentes_relacionados: [C08]
---

# Especificación del Componente: Visor de Cuento con Narración

**Tipo:** UI (con apoyo del Servicio de Audio, C08)
**Historias de usuario relacionadas:** HU-03, HU-04

## Propósito
Mostrar el cuento página a página y narrarlo en voz alta, para que un niño que aún no lee pueda
disfrutarlo por sí mismo.

## Entradas
- `StoryEntity` (páginas con texto, imagen y `audio_url` opcional).
- Gestos de avanzar / retroceder y control de reproducción (play/pausa).

## Salidas
- Render de cada página (imagen + texto).
- Reproducción de la narración de la página activa.

## Reglas de negocio
- Si la página tiene `audio_url`, se ofrece reproducción; si es `null`, se muestra solo texto e
  imagen (sin control de audio roto).
- Al cambiar de página se detiene el audio de la página anterior.
- Al terminar la última página, se muestra la pantalla de celebración.

## Flujo principal (máx. 5 pasos)
1. Abre la primera página del cuento.
2. Reproduce (u ofrece) su narración.
3. El niño avanza a la siguiente página.
4. Se detiene el audio previo y suena el de la nueva página.
5. Al finalizar, muestra la pantalla de celebración.

## Requisitos no funcionales (RNF)
- **Rendimiento:** transición entre páginas en < 300 ms.
- **Seguridad:** solo consume URLs entregadas por el backend; no expone datos del niño.
- **Accesibilidad:** controles grandes, alto contraste, texto legible; la lectura no exige saber leer (audio).

## Criterios de aceptación
- **Dada** una página con `audio_url`, **cuando** se abre, **entonces** su narración se puede reproducir.
- **Dada** una página con `audio_url = null`, **cuando** se abre, **entonces** se muestra sin control de audio y sin error.
- **Dado** que el niño avanza de página, **cuando** empieza la nueva narración, **entonces** la narración anterior ya se detuvo.
