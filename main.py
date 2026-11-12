import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from api.routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("diacare")

app = FastAPI(
    title="Diacare Chatbot API",
    description="Chatbot diabetes melitus tipe 2 berbasis RAG (pedoman PNPK/Kemenkes).",
)
app.include_router(router)


@app.exception_handler(Exception)
async def unhandled_handler(request, exc):
    logger.exception("unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Terjadi kesalahan internal."})
