# Vanguard — judge one-pager

**Product:** Vanguard Field Copilot — turns **site photos + vendor PDF/screenshots + a short note** into a **structured work order**, **parts list (BOM)**, and **risk flags**, with **evidence pointers** back to images.

**Persona:** Field technician / small contractor **ops lead** who closes jobs from the truck.

**Pain (weekly):** Photos and PDFs live in **camera rolls and WhatsApp**; someone **re-keys** part numbers and tasks into a spreadsheet or CMMS. That is slow, error-prone, and not auditable.

**Who pays:** The **owner / ops manager** pays in **labor hours** and **wrong-part / rework** costs.

**Why now:** **Gemma** multimodal models can **see** labels, nameplates, and quote screenshots in one pass; **long context** can carry a pasted spec alongside images; **tool-style JSON** fits CMMS and inventory APIs without a brittle OCR→LLM glue chain.

**3 success metrics**

1. **Time to ticket** — minutes → seconds from photo set to structured record.  
2. **Error reduction** — fewer wrong SKUs vs manual re-entry (spot-check on demo set).  
3. **Traceability** — each important field cites **`image:1`…`image:n`** (or page hint) so humans can verify.

**90-second demo script**

1. Show today: messy chat + spreadsheet.  
2. Upload **3 photos** + one line of context (“Replace pump at Building C”).  
3. Show **JSON**: work order + BOM + hazards with **source_refs**.  
4. **Human-in-the-loop:** tweak one field, export.  
5. **Limitation (one sentence):** Outputs are assistive; final safety and compliance decisions stay with a qualified human.

**Disclaimer:** Not medical or legal advice. Demo data must be synthetic or owned by the team; no personal data in logs.
