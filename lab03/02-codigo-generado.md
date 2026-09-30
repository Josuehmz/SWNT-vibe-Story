---
documento: Código generado + validación
lab: 3
componente: C11 - API Generar Cuento
entregable: 2
---

# Entregable 2 — Código generado y validación

## 2.1 Primera versión generada (con el prompt inicial)

El prompt inicial produjo un endpoint FastAPI funcional, pero **incompleto** frente a la
especificación. Fragmento representativo de esa primera versión:

```python
# v1 — generada con el prompt inicial (tiene huecos, ver validación)
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"],  # ← CORS abierto
                   allow_methods=["*"], allow_headers=["*"])

class StoryResponse(BaseModel):
    story_id: str; title: str; character_name: str; pages: list

@app.post("/api/v1/generate-story")
async def generate_story(drawing: UploadFile = File(...)):
    if drawing.content_type not in ("image/png", "image/jpeg"):
        raise HTTPException(400, "Invalid file type")   # ← mensaje en inglés
    data = await drawing.read()
    result = await run_pipeline(data)                   # ← sin timeout → sin 504
    return result                                       # ← no valida 5MB, no valida vacío
                                                        # ← no descarta 'data' (privacidad)
```

## 2.2 Validación contra los criterios de aceptación (v1)

| # | Criterio / RNF | v1 | Motivo |
|---|----------------|----|--------|
| CA-1 | Archivo > 5 MB → 400 | ❌ | No hay comprobación de tamaño. |
| CA-2 | Pipeline lento → 504 | ❌ | No hay `asyncio.wait_for`; un pipeline colgado nunca corta. |
| CA-3 | Petición válida → 200 con 3 páginas | ⚠️ | Funciona, pero `pages` no está tipado (`list` genérico). |
| RNF-Seguridad | No almacenar el dibujo (HU-05) | ❌ | Los bytes no se descartan explícitamente. |
| RNF-Seguridad | CORS restringido | ❌ | `allow_origins=["*"]`. |
| Regla | Imagen vacía → 400 | ❌ | No se valida. |
| Extra | Errores claros en español | ❌ | Mensajes en inglés. |
| Extra | Pruebas unitarias | ❌ | No se generaron. |

**Conclusión:** el prompt inicial acertó la forma (FastAPI, endpoint, modelo de salida) pero
falló en las **reglas medibles**. Se refina el prompt (ver `03-prompt-refinado.md`).

## 2.3 Versión final (tras el prompt refinado)

Código completo y **ejecutable con pruebas que pasan** en [`codigo/`](codigo/):

- [`codigo/main.py`](codigo/main.py) — endpoint con las 4 reglas, timeout→504, privacidad
  (`del image_bytes` en `finally`), CORS por lista, límites como configuración inyectable.
- [`codigo/test_main.py`](codigo/test_main.py) — 7 pruebas, una por criterio/RNF.
- [`codigo/README.md`](codigo/README.md) — cómo ejecutar y probar.

Resultado de las pruebas:

```text
$ pytest -q
.......                                                              [100%]
7 passed in 1.57s
```
