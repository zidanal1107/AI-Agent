import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen2.5:3b"


def llm(prompt: str, model: str = DEFAULT_MODEL, timeout: float = 30.0) -> str:
    """Mengirim prompt ke Ollama dan mengembalikan teks responsnya."""
    if not prompt.strip():
        raise ValueError("Prompt tidak boleh kosong.")

    body = json.dumps(
        {"model": model, "prompt": prompt, "stream": False}
    ).encode("utf-8")
    request = Request(
        OLLAMA_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise RuntimeError(f"Ollama mengembalikan HTTP {error.code}.") from error
    except URLError as error:
        raise RuntimeError(
            "Tidak dapat terhubung ke Ollama. Pastikan layanan Ollama sudah berjalan."
        ) from error
    except TimeoutError as error:
        raise RuntimeError("Permintaan ke Ollama melewati batas waktu.") from error
    except json.JSONDecodeError as error:
        raise RuntimeError("Respons Ollama bukan JSON yang valid.") from error

    answer = payload.get("response")
    if not isinstance(answer, str):
        raise RuntimeError("Respons Ollama tidak memiliki teks jawaban.")
    return answer
