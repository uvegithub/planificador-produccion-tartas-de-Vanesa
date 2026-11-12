from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router

app = FastAPI(
    title="Planificador de Producción de Tartas",
    description="API para planificar procesos de producción.",
    version="1.0.0",
)

app.include_router(router)

FRONTEND_DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"
INDEX_HTML = FRONTEND_DIST / "index.html"

if (FRONTEND_DIST / "assets").is_dir():
    app.mount(
        "/assets",
        StaticFiles(directory=FRONTEND_DIST / "assets"),
        name="assets",
    )


@app.get("/")
async def root():
    if INDEX_HTML.is_file():
        return FileResponse(INDEX_HTML)

    return {"message": "API funcionando correctamente"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/{full_path:path}")
async def frontend_fallback(full_path: str):
    if full_path == "api" or full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Ruta de API no encontrada")

    requested_file = (FRONTEND_DIST / full_path).resolve()

    if FRONTEND_DIST.resolve() in requested_file.parents and requested_file.is_file():
        return FileResponse(requested_file)

    if INDEX_HTML.is_file():
        return FileResponse(INDEX_HTML)

    raise HTTPException(status_code=404, detail="Recurso no encontrado")