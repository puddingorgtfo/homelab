# AI

Local large language model inference.

## Services

| Service | Description | Port |
|---------|-------------|------|
| [Ollama](ollama/) | Local LLM runner — download and run open-source models (Llama, Mistral, Gemma, etc.) | 11434 (API) |
| Open WebUI | Chat UI for Ollama models (runs in same compose stack) | 8080 |

## Notes

- Ollama uses GPU passthrough (Nvidia) for fast inference. If no GPU is available, it
  falls back to CPU (much slower).
- Models are stored on the NAS under `/mnt/nas/ollama/models` — they can be several GB each.
- Open WebUI provides a ChatGPT-style interface. It connects to Ollama at `http://ollama:11434`
  on the internal Docker network.
- Pull a model with: `docker exec -it ollama ollama pull llama3.2`
- The `OLLAMA_KEEP_ALIVE=24h` setting keeps loaded models in memory for 24 hours to avoid
  slow cold-start times.
