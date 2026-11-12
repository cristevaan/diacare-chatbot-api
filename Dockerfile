FROM python:3.14-slim
ENV PYTHONUNBUFFERED=1 HF_HOME=/root/.cache/huggingface
WORKDIR /app

COPY requirements.txt .
# torch versi CPU saja — image tidak perlu wheel CUDA (ratusan MB)
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch
RUN pip install --no-cache-dir -r requirements.txt

# Index dibangun di layer terpisah: perubahan kode aplikasi (main.py, api/)
# tidak memicu embed ulang seluruh PDF
COPY rag/ ./rag/
COPY docs/ ./docs/
RUN python -m rag.pipeline

COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
