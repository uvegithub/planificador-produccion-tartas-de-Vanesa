from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="Planificador de Producción de Tartas",
    description="API para planificar procesos de producción.",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "API funcionando correctamente"}


@app.get("/health")
async def health():
    return {"status": "ok"}