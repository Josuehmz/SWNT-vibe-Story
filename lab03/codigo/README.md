# C11 · API Generar Cuento — código

Implementación del componente **C11** (StoryDraw) generada y refinada con vibe coding
durante el Laboratorio 3.

## Requisitos
- Python 3.11+

## Instalación
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate   |   Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar la API
```bash
uvicorn main:app --reload
# Documentación interactiva: http://localhost:8000/docs
```

## Probar
```bash
pytest -q
```
Salida esperada: `7 passed`.

## Endpoint
`POST /api/v1/generate-story` — `multipart/form-data`, campo `drawing` (PNG/JPEG ≤ 5 MB).
Devuelve `StoryResponse { story_id, title, character_name, pages[] }`.

## Configuración (variables de entorno)
| Variable | Por defecto | Descripción |
|----------|-------------|-------------|
| `MAX_UPLOAD_BYTES` | `5242880` (5 MB) | Tamaño máximo del dibujo. |
| `PIPELINE_TIMEOUT_SECONDS` | `85` | Límite de tiempo del pipeline (→ 504). |
| `CORS_ORIGINS` | `http://localhost:3000` | Orígenes permitidos, separados por comas. |

> El pipeline de IA real (visión → guion → ilustración/voz → nube) se inyecta con la
> dependencia `get_pipeline`; aquí se deja un stub para poder ejecutar y probar el endpoint
> de forma aislada. El dibujo del niño **no se persiste**: se descarta al terminar la petición.
