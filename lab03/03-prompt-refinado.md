---
documento: Prompt refinado
lab: 3
componente: C11 - API Generar Cuento
entregable: 3
---

# Entregable 3 — Prompt refinado con mejoras

Cada mejora del prompt corresponde a un hueco detectado en la validación de la v1
(`02-codigo-generado.md`, sección 2.2).

```text
Mejora el componente "API Generar Cuento" (Python + FastAPI) para que cumpla EXACTAMENTE
estas reglas medibles. Es la API de StoryDraw, que convierte el dibujo de un niño en un
cuento; la privacidad del dibujo es un requisito no funcional crítico.

1) Validación de entrada (todas devuelven HTTP 400 con mensaje en ESPAÑOL):
   - Si content_type no es image/png ni image/jpeg → "Solo se aceptan imágenes PNG o JPEG".
   - Si el cuerpo está vacío → "Imagen vacía".
   - Si supera 5 MB → "Imagen demasiado grande. Máximo 5MB".
   El límite de 5 MB debe ser un parámetro de configuración (no un número mágico).

2) Ejecuta el pipeline con asyncio.wait_for y un timeout configurable (por defecto 85 s,
   5 s por debajo del timeout de 90 s del cliente). Si se excede → HTTP 504
   "El pipeline tardó demasiado. Intenta de nuevo.".

3) Privacidad (HU-05): el dibujo NO se persiste. Lee los bytes, úsalos solo para el
   pipeline y descártalos en un bloque finally (del image_bytes). No los escribas en disco
   ni en logs.

4) Manejo de errores del pipeline: si lanza StoryGenerationError o cualquier excepción
   inesperada → HTTP 500 "Error generando el cuento. Intenta de nuevo." SIN filtrar el
   mensaje interno al cliente.

5) Seguridad: CORS restringido a una lista de orígenes leída de configuración
   (variable de entorno), NO allow_origins=["*"]. Métodos permitidos: GET y POST.

6) Tipado estricto de la salida: StoryResponse { story_id, title, character_name,
   pages: list[StoryPageOut] } y StoryPageOut { text, image_url, audio_url: str | None }.

7) Diseño para pruebas: inyecta el pipeline y la configuración como dependencias de FastAPI
   (Depends) para poder sustituirlos por dobles en los tests, sin llamar a servicios reales.

8) Genera pruebas unitarias con pytest y TestClient, UNA por criterio de aceptación:
   - archivo > 5 MB → 400 (usa un límite pequeño en el test para no cargar 6 MB reales)
   - tipo no permitido → 400
   - imagen vacía → 400
   - petición válida (pipeline simulado) → 200 con 3 páginas
   - pipeline lento (timeout pequeño) → 504
   - pipeline que falla → 500 y que el mensaje interno NO aparezca en la respuesta
   - /health → 200

9) Incluye un README corto con instrucciones de ejecución y de pruebas.
```

## Trazabilidad mejora → hueco corregido

| Mejora del prompt | Hueco de la v1 que corrige |
|-------------------|----------------------------|
| 1 (400 + español + límite configurable) | Falta de validación de 5 MB / vacío; mensajes en inglés |
| 2 (`wait_for` + 504) | Sin timeout → CA-2 fallaba |
| 3 (`del` en `finally`) | Privacidad HU-05 incumplida |
| 4 (500 sin filtrar) | Manejo de errores inexistente |
| 5 (CORS por lista) | `allow_origins=["*"]` |
| 6 (tipado `pages`) | `pages: list` genérico (CA-3 débil) |
| 7 (inyección de dependencias) | Código no testeable sin servicios reales |
| 8 (pytest por criterio) | Sin pruebas |
| 9 (README) | Sin documentación |
