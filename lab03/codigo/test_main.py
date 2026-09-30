"""Pruebas unitarias de C11 — API Generar Cuento.

Cada prueba mapea a un criterio de aceptación o a un RNF de la especificación.
El pipeline se sustituye por dobles (mocks) para no llamar a servicios de IA.
"""
import asyncio

import pytest
from fastapi.testclient import TestClient

import main
from main import Settings, StoryPageOut, StoryResponse, StoryGenerationError, app, get_pipeline, get_settings

client = TestClient(app)


def _fake_story() -> StoryResponse:
    return StoryResponse(
        story_id="abc-123",
        title="La aventura del dragón azul",
        character_name="Dragón",
        pages=[
            StoryPageOut(text=f"Página {i}", image_url=f"https://cdn/img{i}.png", audio_url=None)
            for i in range(1, 4)
        ],
    )


@pytest.fixture(autouse=True)
def _clean_overrides():
    yield
    app.dependency_overrides.clear()


def _override_pipeline(fn):
    app.dependency_overrides[get_pipeline] = lambda: fn


def _override_settings(**kwargs):
    app.dependency_overrides[get_settings] = lambda: Settings(**kwargs)


# ── Criterio: archivo > 5 MB → 400 ──────────────────────────────────────────────
def test_imagen_demasiado_grande_devuelve_400():
    _override_settings(max_upload_bytes=10)  # límite pequeño para no cargar 6 MB reales
    files = {"drawing": ("d.png", b"x" * 11, "image/png")}
    r = client.post("/api/v1/generate-story", files=files)
    assert r.status_code == 400
    assert "Máximo 5MB" in r.json()["detail"]


# ── Criterio: tipo no permitido → 400 ───────────────────────────────────────────
def test_tipo_no_permitido_devuelve_400():
    files = {"drawing": ("d.txt", b"hola", "text/plain")}
    r = client.post("/api/v1/generate-story", files=files)
    assert r.status_code == 400
    assert "PNG o JPEG" in r.json()["detail"]


# ── Regla: imagen vacía → 400 ───────────────────────────────────────────────────
def test_imagen_vacia_devuelve_400():
    files = {"drawing": ("d.png", b"", "image/png")}
    r = client.post("/api/v1/generate-story", files=files)
    assert r.status_code == 400
    assert "vacía" in r.json()["detail"]


# ── Criterio: petición válida → 200 con 3 páginas ───────────────────────────────
def test_peticion_valida_devuelve_3_paginas():
    async def ok(_: bytes) -> StoryResponse:
        return _fake_story()

    _override_pipeline(ok)
    files = {"drawing": ("d.png", b"\x89PNG fake", "image/png")}
    r = client.post("/api/v1/generate-story", files=files)
    assert r.status_code == 200
    body = r.json()
    assert len(body["pages"]) == 3
    assert body["title"]


# ── Criterio: pipeline lento → 504 ──────────────────────────────────────────────
def test_pipeline_lento_devuelve_504():
    async def slow(_: bytes) -> StoryResponse:
        await asyncio.sleep(0.5)
        return _fake_story()

    _override_settings(pipeline_timeout_seconds=0.1)
    _override_pipeline(slow)
    files = {"drawing": ("d.png", b"\x89PNG fake", "image/png")}
    r = client.post("/api/v1/generate-story", files=files)
    assert r.status_code == 504


# ── RNF fiabilidad: fallo del pipeline → 500 sin filtrar detalles ───────────────
def test_fallo_pipeline_devuelve_500():
    async def boom(_: bytes) -> StoryResponse:
        raise StoryGenerationError("detalle interno que no debe salir")

    _override_pipeline(boom)
    files = {"drawing": ("d.png", b"\x89PNG fake", "image/png")}
    r = client.post("/api/v1/generate-story", files=files)
    assert r.status_code == 500
    assert "detalle interno" not in r.json()["detail"]


def test_health():
    assert client.get("/health").json() == {"status": "ok"}
