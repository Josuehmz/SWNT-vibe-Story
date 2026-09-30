---
id: C11
nombre: API Generar Cuento
tipo: Servicio
modulo: M5
mvp: true
historias: [HU-02, HU-05]
endpoint: POST /api/v1/generate-story
---

# Especificación del Componente: API Generar Cuento

**Tipo:** Servicio (backend)
**Historias de usuario relacionadas:** HU-02, HU-05

## Propósito
Exponer el único endpoint que recibe el dibujo, lo valida, ejecuta el pipeline con un límite
de tiempo y devuelve el cuento; garantizando que el dibujo **no se persista** en el servidor.

## Entradas
- Petición `multipart/form-data`, campo `drawing`: imagen `PNG` o `JPEG`, tamaño ≤ 5 MB.

## Salidas
- `StoryResponse` (`story_id`, `title`, `character_name`, `pages[]`), donde cada página tiene
  `text`, `image_url` y `audio_url` (opcional).
- Error HTTP tipificado: `400` (validación), `500` (fallo interno), `504` (timeout).

## Reglas de negocio
- Rechaza contenido que no sea PNG/JPEG (400), imagen vacía (400) o mayor a 5 MB (400).
- El pipeline se ejecuta con timeout de 85 s (5 s de margen bajo los 90 s del cliente) → 504 si se excede.
- Al finalizar, los bytes del dibujo se **descartan** de memoria; no se guardan ni se registran.

## Flujo principal (máx. 5 pasos)
1. Recibe el archivo del formulario.
2. Valida tipo de contenido y tamaño.
3. Ejecuta el pipeline con espera máxima de 85 s.
4. Devuelve `StoryResponse` (200).
5. Libera de memoria el dibujo.

## Requisitos no funcionales (RNF)
- **Rendimiento:** responder en < 90 s en el caso normal.
- **Seguridad:** CORS restringido a la lista de orígenes permitidos; el dibujo no se registra ni almacena; los errores no exponen detalles internos.
- **Accesibilidad:** mensajes de error claros y accionables para el cliente ("Imagen demasiado grande. Máximo 5MB").

## Criterios de aceptación
- **Dado** un archivo de 6 MB, **cuando** se envía al endpoint, **entonces** responde `400` con "Imagen demasiado grande".
- **Dado** un pipeline que supera los 85 s, **cuando** se ejecuta, **entonces** responde `504`.
- **Dada** una petición válida con un PNG, **cuando** el pipeline termina, **entonces** responde `200` con una lista `pages` de longitud 3.
