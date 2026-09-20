# rag-learning

Scratch space for learning retrieval-augmented generation, starting with embeddings.

| File | What it does |
|------|--------------|
| `sentence-transformers.ipynb` | Encodes a handful of sentences with `all-MiniLM-L6-v2`, then plots the cosine-similarity matrix — first over all 384 dimensions, then over a random slice of them, to show that individual dimensions aren't independently meaningful. |

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (used for dependency and Python management)
- Python 3.14 — `uv` will download it for you if it isn't installed

## Setup

```powershell
cd rag-learning
uv sync
```

This creates `.venv/` and installs `sentence-transformers`, `matplotlib`, and `ipykernel`.

## Running the notebook

### Option A — VS Code (no extra packages)

1. Open `sentence-transformers.ipynb`.
2. Click the kernel picker in the top right → **Select Another Kernel** → **Python Environments** → the `.venv` in this folder (`.venv\Scripts\python.exe`).
3. Run cells with `Shift+Enter`.

The Jupyter and Python extensions handle the server themselves, so `uv sync` is all the setup you need.

### Option B — JupyterLab in the browser

`uv sync` installs `ipykernel` (the kernel) but **not** a notebook server, so `jupyter lab` won't work out of the box. Either run it ad hoc:

```powershell
uv run --with jupyterlab jupyter lab
```

or add it to the project permanently:

```powershell
uv add --dev jupyterlab
uv run jupyter lab
```

Either way, JupyterLab prints a `http://localhost:8888/lab?token=...` URL and usually opens your browser. Open `sentence-transformers.ipynb` from the file list; the default `Python 3 (ipykernel)` kernel is the project `.venv`, since `uv run` launches Jupyter from inside it.

Stop the server with `Ctrl+C` twice in the terminal.

## First run is slow

The first execution of cell 1 downloads the `all-MiniLM-L6-v2` weights (~90 MB) from Hugging Face into your user cache (`~\.cache\huggingface`). Later runs load from that cache and need no network.

## Troubleshooting

**Kernel doesn't appear, or Jupyter picks the wrong Python.** Register the project venv as a named kernel:

```powershell
uv run python -m ipykernel install --user --name rag-learning --display-name "rag-learning"
```

Then pick **rag-learning** from the kernel menu.

**`ModuleNotFoundError: No module named 'sentence_transformers'`.** The notebook is attached to a different interpreter than `.venv`. Check which one it's using from inside the notebook:

```python
import sys; print(sys.executable)
```

It should point at this folder's `.venv\Scripts\python.exe`.

**Environment drifted or got corrupted.** `.venv/` is gitignored and disposable — delete it and re-run `uv sync`.
