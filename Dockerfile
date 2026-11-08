FROM python:3.12-slim
WORKDIR /app
COPY agent.py app.py ./
COPY static ./static
COPY data ./data
RUN useradd --create-home appuser
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=2)"
CMD ["python", "app.py"]
