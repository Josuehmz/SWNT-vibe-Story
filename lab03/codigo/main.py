"""C11 — API Generar Cuento (StoryDraw).

Endpoint único que recibe el dibujo de un niño, lo valida, ejecuta el pipeline de
IA con un límite de tiempo y devuelve el cuento generado. El dibujo NUNCA se
persiste: se usa en memoria y se descarta al terminar la petición.

Ejecutar:  uvicorn main:app --reload
Probar:    pytest -q
"""
from __future__ import annotations

import asyncio
import logging
from functools import lru_cache
from typing import Awaitable, Callable

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_settings import BaseSettings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("storydraw.api")


# ── Configuración (RNF: CORS restringido, límites como parámetros) ──────────────
class Settings(BaseSettings):
    max_upload_bytes: int = 5 * 1024 * 1024          # 5 MB
    pipeline_timeout_seconds: float = 85.0           # 5 s bajo el timeout de 90 s del cliente
    cors_origins: str = "http://localhost:3000"      # lista separada por comas

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


# ── Contrato de salida (debe coincidir con el cliente Flutter) ──────────────────
class StoryPageOut(BaseModel):
    text: str
    image_url: str
    audio_url: str | None = None


class StoryResponse(BaseModel):
    story_id: str
    title: str
    character_name: str
    pages: list[StoryPageOut]


# ── Errores de dominio del pipeline ─────────────────────────────────────────────
class StoryGenerationError(Exception):
    """Fallo controlado del pipeline de generación."""


# El pipeline real se inyecta como dependencia para poder sustituirlo en pruebas.
Pipeline = Callable[[bytes], Awaitable[StoryResponse]]


async def _default_pipeline(image_bytes: bytes) -> StoryResponse:  # pragma: no cover
    # En producción aquí se llama a run_pipeline() (visión → guion → ilustración/voz → nube).
    raise StoryGenerationError("Pipeline no configurado")


def get_pipeline() -> Pipeline:
    return _default_pipeline


# ── App ─────────────────────────────────────────────────────────────────────────
_ALLOWED_TYPES = ("image/png", "image/jpeg")

app = FastAPI(title="StoryDraw API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins_list,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/api/v1/generate-story", response_model=StoryResponse)
async def generate_story_endpoint(
    drawing: UploadFile = File(...),
    settings: Settings = Depends(get_settings),
    pipeline: Pipeline = Depends(get_pipeline),
) -> StoryResponse:
    # Regla 1: solo PNG/JPEG.
    if drawing.content_type not in _ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Solo se aceptan imágenes PNG o JPEG")

    image_bytes = await drawing.read()
    try:
        # Regla 2: no vacío.
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Imagen vacía")
        # Regla 3: tamaño máximo.
        if len(image_bytes) > settings.max_upload_bytes:
            raise HTTPException(status_code=400, detail="Imagen demasiado grande. Máximo 5MB")

        # Regla 4: pipeline con timeout → 504.
        try:
            return await asyncio.wait_for(
                pipeline(image_bytes), timeout=settings.pipeline_timeout_seconds
            )
        except asyncio.TimeoutError:
            logger.warning("El pipeline superó %.0fs", settings.pipeline_timeout_seconds)
            raise HTTPException(status_code=504, detail="El pipeline tardó demasiado. Intenta de nuevo.")
        except StoryGenerationError:
            logger.exception("Fallo controlado del pipeline")
            raise HTTPException(status_code=500, detail="Error generando el cuento. Intenta de nuevo.")
        except HTTPException:
            raise
        except Exception:  # noqa: BLE001
            logger.exception("Error inesperado en el pipeline")
            raise HTTPException(status_code=500, detail="Error generando el cuento. Intenta de nuevo.")
    finally:
        # Regla 5 (privacidad HU-05): el dibujo del niño se descarta; nunca se persiste.
        del image_bytes
