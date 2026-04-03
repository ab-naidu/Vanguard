# Vanguard

Field / ops copilot prototype: **photos + short note → structured JSON** (work order, BOM, hazards) using **Gemma** multimodal models via Hugging Face `transformers`.

- **Judge one-pager:** [docs/JUDGE_ONE_PAGER.md](docs/JUDGE_ONE_PAGER.md)  
- **48h plan:** [docs/HACKATHON_PLAN.md](docs/HACKATHON_PLAN.md)

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

**Hugging Face:** Gemma weights are gated. Accept the license on the model page, then:

```bash
huggingface-cli login
# or set HF_TOKEN for CI
```

### Mock run (no GPU, no download)

```bash
python scripts/run_work_order.py --mock -o out.json
```

### PyTorch with CUDA (laptop GPU)

Install a **CUDA** build of PyTorch that matches your driver (see [pytorch.org](https://pytorch.org/get-started/locally/)). Example (adjust CUDA version):

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
```

Then reinstall other deps from `requirements.txt` if needed. Confirm GPU: `python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"`.

### Real inference

Default model id is **`google/gemma-3-4b-it`**. For a **Gemma 4** hackathon demo on GPU, set **`VANGUARD_MODEL_ID`** (and use a recent `transformers`):

```bash
set VANGUARD_MODEL_ID=google/gemma-4-e4b-it
python scripts/run_work_order.py --images sample_assets\a.jpg --note "Replace seal" -o out.json
```

### GPU: laptop vs Kaggle (rough guide)

VRAM is approximate; quantization, batch size, and context length change fit.

| Where | Typical GPU | Good Gemma 4 picks |
|--------|-------------|-------------------|
| **Kaggle notebook** | Often **T4 ~16 GB** | **`google/gemma-4-e2b-it`** or **`google/gemma-4-e4b-it`**; upgrade `transformers`; use short context for demo. |
| **Laptop 8–12 GB** | RTX 3060 laptop, etc. | **`google/gemma-4-e2b-it`** or stay on **`gemma-3-4b-it`** if downloads or VRAM bite. |
| **Laptop 16–24 GB** | RTX 4080 laptop, etc. | **`google/gemma-4-e4b-it`**; try **26B A4B** only if you add **4-bit** / aggressive offload (not in this repo by default). |
| **Desktop 24+ GB** | RTX 3090/4090, etc. | **`google/gemma-4-26B-A4B-it`** is realistic for many setups; **`gemma-4-31B-it`** needs more headroom. |

**Kaggle tips:** Turn on the **GPU** accelerator, put **`HF_TOKEN`** in notebook secrets, `pip install -U transformers`, clone or copy `vanguard/` + `scripts/` into the notebook, and run the same pipeline. Expect session time limits — keep `max_new_tokens` moderate.

### Streamlit demo

```bash
streamlit run streamlit_app.py
```

Use **Mock mode** in the sidebar if you have no GPU.

## Model notes

| Model | Role |
|--------|------|
| `google/gemma-3-4b-it` | Default in code; smallest friction if Gemma 4 + latest `transformers` is painful |
| `google/gemma-4-e2b-it` / `google/gemma-4-e4b-it` | **Gemma 4** on **Kaggle T4** or **12–16 GB** laptop GPUs |
| `google/gemma-4-26B-A4B-it` | MoE “hero” model when you have **~24 GB+** VRAM (or quantize) |

Use **`enable_thinking=False`** in code for faster demos unless the track scores reasoning. Image order is **images first**, then text (see [Gemma 4 model card](https://ai.google.dev/gemma/docs/core/model_card_4)).

## Known limitations

- Outputs are **assistive**; humans must validate safety and compliance.
- **No PII** in demo logs; avoid real people’s data in screenshots.
- JSON parsing assumes the model returns a single object; brittle outputs may need retry logic.
- **Gemma 4** may require a newer `transformers` than Gemma 3; upgrade with `pip install -U transformers`.

## Tests

```bash
pip install pytest
pytest tests/
```

## License

Your app code: add a license you choose. Gemma weights are under Google’s Gemma terms on Hugging Face.
