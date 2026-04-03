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

### Real inference

Default dev model id is **`google/gemma-3-4b-it`** (set **`VANGUARD_MODEL_ID`** for Gemma 4, e.g. `google/gemma-4-26B-A4B-it` — needs large GPU / Kaggle).

```bash
python scripts/run_work_order.py --images sample_assets/a.jpg sample_assets/b.jpg --note "Replace seal" -o out.json
```

### Streamlit demo

```bash
streamlit run streamlit_app.py
```

Use **Mock mode** in the sidebar if you have no GPU.

## Model notes

| Model | Role |
|--------|------|
| `google/gemma-3-4b-it` | Default for smaller GPUs / local dev |
| `google/gemma-4-26B-A4B-it` | Hackathon target when you have the hardware or Kaggle |

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
