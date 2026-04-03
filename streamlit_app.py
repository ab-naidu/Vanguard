"""
Vanguard demo UI: streamlit run streamlit_app.py
Requires: pip install -r requirements.txt
"""

from __future__ import annotations

import io
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from PIL import Image

from vanguard.pipeline import generate_work_order_json, load_processor_and_model

DEFAULT_MODEL = os.environ.get("VANGUARD_MODEL_ID", "google/gemma-3-4b-it")


@st.cache_resource
def cached_model(model_id: str):
    return load_processor_and_model(model_id)


def main() -> None:
    st.set_page_config(page_title="Vanguard Field Copilot", layout="wide")
    st.title("Vanguard Field Copilot")
    st.caption("Gemma multimodal → work order + BOM + hazards (demo). Not for production safety decisions.")

    with st.sidebar:
        model_id = st.text_input("Hugging Face model id", value=DEFAULT_MODEL)
        mock = st.checkbox("Mock mode (no GPU / no download)", value=False)
        max_new = st.slider("max_new_tokens", 256, 4096, 2048, 256)

    files = st.file_uploader("Site photos / screenshots", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True)
    note = st.text_area("Technician note", placeholder="e.g. Replace pump at Building C; vendor quote attached.")

    if st.button("Generate JSON", type="primary"):
        if mock:
            from vanguard.mock_data import MOCK_WORK_ORDER_RESULT

            data = MOCK_WORK_ORDER_RESULT
            raw = json.dumps(data)
            st.session_state["result"] = data
            st.session_state["raw"] = raw
        else:
            if not files:
                st.warning("Add at least one image, or enable Mock mode.")
                return
            images = [Image.open(io.BytesIO(f.getvalue())).convert("RGB") for f in files]
            with st.spinner("Loading model & generating…"):
                processor, model = cached_model(model_id)
                data, raw = generate_work_order_json(
                    processor, model, images, note, max_new_tokens=max_new
                )
            st.session_state["result"] = data
            st.session_state["raw"] = raw

    if "result" in st.session_state:
        st.subheader("Structured output")
        st.json(st.session_state["result"])
        st.download_button(
            "Download JSON",
            data=json.dumps(st.session_state["result"], indent=2),
            file_name="vanguard_work_order.json",
            mime="application/json",
        )
        with st.expander("Raw model tail (debug)"):
            st.code(st.session_state.get("raw", "")[:8000])


if __name__ == "__main__":
    main()
