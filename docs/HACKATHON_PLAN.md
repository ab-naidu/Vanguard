# Hackathon plan — 48 hours (scale up/down)

**Product direction (default):** Field / ops copilot — turn **site photos + vendor PDF/screenshots + short note** into **structured work order + BOM + risk flags**, using **Gemma 4** (multimodal + function calling). Adjust names if you pick another persona.

**Repo status:** Day 0 narrative in **[JUDGE_ONE_PAGER.md](./JUDGE_ONE_PAGER.md)**. Vertical slice: `scripts/run_work_order.py`, `streamlit_app.py`, `vanguard/pipeline.py`.

---

## Day 0 — Before coding (~2 hours)

| Step | Output | Default (edit if needed) |
|------|--------|---------------------------|
| Pick one persona | Who suffers weekly | **Field technician / small contractor ops lead** |
| Pick one workflow | One sentence | **Photos + PDF → work order + parts list + risk notes** |
| Define 3 success metrics | Measurable | **(1) Time to ticket** ↓ **(2) Missing-part / wrong-SKU errors** ↓ **(3) Every field has source** (image # / page hint) |
| Write 1-page judge story | Problem → payer → why now → demo | One pager: *SMB fleet maintenance; office manager “pays” in time; phones already have photos; demo = 90s upload → JSON → approve* |

**Judge story outline (fill names):**

1. **Pain:** WhatsApp + camera roll + PDF quotes; re-keying into CMMS/spreadsheet; errors on part numbers.
2. **Who pays:** Ops manager / owner (labor + mistakes).
3. **Why now:** Gemma 4 vision + long context + native tools = one flow without a fragile chain of OCR + LLM + manual merge.
4. **Demo script (3 min):** See Day 2 afternoon.

---

## Day 1 — Morning: vertical slice (MVP)

**Goal:** Upload **3–5 images** + optional **short text** → **structured JSON** via **function calling** (or strict JSON schema if your stack uses that).

**Suggested tool / function names (implement as your API expects):**

- `create_work_order` — title, site_id, priority, summary, due_hint
- `extract_bom` — line items: sku_or_description, qty, unit, confidence
- `flag_hazards` — hazards: type, severity, evidence_ref (e.g. `image:2`)

**Model path**

- Instruction-tuned Gemma 4 variant.
- **`enable_thinking=False`** for snappy demos unless the track scores reasoning explicitly.

**Multimodal**

- **Media before text** (Gemma 4 guidance).
- **Image token budget:** default **280**; **560 / 1120** only for OCR-heavy pages or fine print.

**Definition of done (morning)**

- [x] One end-to-end path: UI or notebook → model → parsed JSON displayed. *(CLI + Streamlit + `vanguard` pipeline)*
- [ ] One happy-path demo asset set (your own photos/PDFs, no copyright issues). *(add files under `sample_assets/` — not committed)*

---

## Day 1 — Afternoon: “why us” (pick **two** only)

| Feature | What judges see | Effort hint |
|---------|-----------------|-------------|
| **A — Evidence mode** | Each JSON field links to `source: image #n` or `pdf page p` (short phrase OK) | Prompt + post-process validation |
| **B — Human-in-the-loop** | Editable form from JSON; **diff** vs model output before “commit” | UI + state |
| **C — Long-context lane** | Long pasted spec + one diagram; model grounds answers in attached text | One tab or mode in UI |

**Pick two:** **A + B** is usually strongest for trust + “real product.” Use **C** if the brief emphasizes documents.

---

## Day 2 — Morning: reliability + safety

- [ ] **Guardrails:** No PII in logs; redact or hash filenames if needed.
- [ ] **Positioning:** Not “medical/legal advice” unless rules allow; **disclaimer** in UI + slides.
- [ ] **Eval mini-set:** **10** fixed cases (your screenshots); run before every demo; note pass/fail.
- [ ] **Fallbacks:** Crop image; optional user caption if vision low confidence.

---

## Day 2 — Afternoon: demo packaging

1. **Live demo (3 minutes):** (1) **Pain** in one sentence → (2) **Upload** images + note → (3) **Structured output** + **one action** (e.g. export JSON, mock “create ticket”) → (4) **One limitation** honestly.
2. **Backup:** 60–90s screen recording if Wi‑Fi or API fails.
3. **Repo README:** Setup, **which Gemma variant**, hardware/API **costs**, **known failure modes**.

---

## 48-hour hour grid (compress if shorter)

| Hours | Focus |
|------|--------|
| 0–2 | Day 0 doc + repo skeleton + sample assets |
| 2–6 | Inference path + chat template + first JSON |
| 6–10 | Upload UI or notebook polish + error handling |
| 10–14 | Feature A or B (first “why us”) |
| 14–18 | Second “why us” + styling |
| 18–22 | Eval set + fix top 3 failures |
| 22–26 | Sleep + buffer |
| 26–30 | Safety copy + disclaimers + no PII |
| 30–34 | Slides + diagram |
| 34–38 | Demo rehearsal ×3 |
| 38–42 | README + video backup |
| 42–48 | Final rehearsal + submission checklist |

---

## Team split (3–4 people)

| Role | Focus |
|------|--------|
| PM / narrative | Persona, rubric mapping, deck, demo script |
| Full-stack | Upload UI, API, persistence, auth stub |
| ML / integration | Gemma prompts, templates, tool schemas, image pipeline |
| Design / QA | Demo data, latency, edge cases, recording |

---

## Pitch slides (order)

1. Problem + who feels it weekly  
2. Today’s workaround (spreadsheets / chat chaos)  
3. Your flow (**simple diagram**)  
4. Live demo  
5. Why **Gemma 4** (only claims you **actually** use: multimodal, tools, context)  
6. Safety / limitations  
7. Next 30 days (pilot, integrations, data)  

---

## Submission checklist

- [ ] Repo public / link submitted  
- [ ] README: run instructions + model ID + secrets pattern (no real keys)  
- [ ] License for your code; respect Gemma / dataset licenses  
- [ ] Demo path works on a **clean** machine or container notes  

---

## References

- [Gemma Cookbook](https://github.com/google-gemma/cookbook)  
- [Gemma 4 model card](https://ai.google.dev/gemma/docs/core/model_card_4) (modalities, thinking tokens, image budgets)  
