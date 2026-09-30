---
documento: Prompt inicial (Vibe Coding)
lab: 3
componente: C11 - API Generar Cuento
entregable: 1
---

# Entregable 1 — Prompt inicial usado en Vibe Coding

Componente elegido del Mapa de Componentes (Lab 2): **C11 · API Generar Cuento** (tipo Servicio,
módulo M5). Es el más autocontenido y el más fácil de validar contra sus criterios de aceptación.

> Prompt pegado en la herramienta de vibe coding, con los campos rellenados desde la
> especificación `02-especificaciones/C11-api-generar-cuento.md` del Lab 2.

```text
Quiero que generes el código de un componente llamado: API Generar Cuento
Tipo: Servicio (backend)
Lenguaje/Framework preferido: Python con FastAPI

Especificación del componente:
- Propósito: Exponer el único endpoint que recibe el dibujo de un niño, lo valida,
  ejecuta un pipeline de IA y devuelve el cuento generado.
- Entradas: petición multipart/form-data, campo "drawing" con una imagen PNG o JPEG.
- Salidas: JSON StoryResponse { story_id, title, character_name, pages[] }, donde cada
  página tiene { text, image_url, audio_url (opcional) }.
- Reglas de negocio:
  1) Solo se aceptan imágenes PNG o JPEG.
  2) El tamaño máximo es 5 MB.
  3) El pipeline tiene un límite de tiempo; si se excede, error de timeout.
  4) El dibujo del niño no se debe almacenar en el servidor.
- Flujo principal (máx. 5 pasos):
  1) Recibe el archivo. 2) Valida tipo y tamaño. 3) Ejecuta el pipeline con timeout.
  4) Devuelve StoryResponse. 5) Libera el dibujo.
- RNF clave: rendimiento < 90 s; seguridad (CORS y no registrar el dibujo);
  errores claros para el cliente.
- Criterios de aceptación:
  - Dado un archivo de 6 MB, cuando se envía, entonces responde 400.
  - Dado un pipeline que excede el tiempo límite, cuando corre, entonces responde 504.
  - Dada una petición válida, cuando termina, entonces responde 200 con 3 páginas.

Requerimientos adicionales para el código:
- Código modular y comentado.
- Buenas prácticas de FastAPI.
- Pruebas unitarias básicas incluidas.
- Documentación mínima (README corto con instrucciones de ejecución).
```
