FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install uv && uv sync --no-dev

COPY src/ ./src/
COPY data/ ./data/
COPY faiss_index/ ./faiss_index/

# Port Chainlit
EXPOSE 8000
CMD ["uv", "run", "chainlit", "run", "src/interface.py", "--host", "0.0.0.0", "--port", "8000"]