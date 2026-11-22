FROM debian:bookworm-slim AS builder
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN curl -fsSL -o model.llamafile https://huggingface.co/Mozilla/TinyLlama-1.1B-Chat-v1.0-llamafile/resolve/main/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.llamafile && \
    chmod +x model.llamafile

FROM debian:bookworm-slim
RUN useradd --create-home --uid 1000 appuser
WORKDIR /app
COPY --from=builder --chown=appuser:appuser /build/model.llamafile /app/model.llamafile
USER appuser
ENV HOME=/tmp
EXPOSE 8080
ENTRYPOINT ["/bin/bash", "/app/model.llamafile"]
CMD ["--server", "--nobrowser", "--host", "0.0.0.0", "--port", "8080"]
