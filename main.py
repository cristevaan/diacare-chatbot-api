import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from api.routes import router
from rag.pipeline import get_vectorstore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("diacare")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("membuka index RAG...")
    get_vectorstore()
    logger.info("index RAG siap")
    yield

app = FastAPI(
    title="Diacare Chatbot API",
    description="Chatbot diabetes melitus tipe 2 berbasis RAG (pedoman PNPK/Kemenkes).",
    lifespan=lifespan,
)
app.include_router(router)


@app.exception_handler(Exception)
async def unhandled_handler(request, exc):
    logger.exception("unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Terjadi kesalahan internal."})
