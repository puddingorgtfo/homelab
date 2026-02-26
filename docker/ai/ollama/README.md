# Ollama + Open WebUI

Two services in one compose stack:

- **Ollama** — local LLM server. Downloads and runs open-source language models
  (Llama 3, Mistral, Gemma, Phi, etc.) on the local GPU or CPU.
- **Open WebUI** — ChatGPT-style chat interface that connects to Ollama.

## Ports

| Port | Purpose |
|------|---------|
| 11434 | Ollama API |
| 8080 | Open WebUI |

## Configuration

| Variable | Description |
|----------|-------------|
| `WEBUI_SECRET_KEY` | Secret key for Open WebUI session signing |
| `OLLAMA_BASE_URL` | URL Open WebUI uses to reach Ollama (`http://ollama:11434`) |
| `OLLAMA_KEEP_ALIVE` | How long to keep a model loaded in memory (e.g. `24h`) |

## Notes

- **GPU**: Ollama uses Nvidia GPU passthrough for fast inference. The compose file includes
  a `reservations.devices` block for this. Remove it if no Nvidia GPU is available (falls
  back to CPU, much slower).
- **Models**: Pull a model with:
  ```bash
  docker exec -it ollama ollama pull llama3.2
  docker exec -it ollama ollama pull mistral
  ```
  List available models: https://ollama.com/library
- **Storage**: Models are stored on the NAS at `/mnt/nas/ollama/models` — they can be
  several GB each. The NAS mount prevents filling the boot disk.
- Ollama is also accessible to other tools via its API at `http://<host>:11434`.
- **Ollama docs**: https://ollama.com/
- **Open WebUI docs**: https://docs.openwebui.com/
