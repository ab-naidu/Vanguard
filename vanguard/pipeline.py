from __future__ import annotations

import inspect
import logging
import os
from typing import Any

import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoProcessor

from vanguard.json_extract import extract_json_object
from vanguard.prompts import SYSTEM_PROMPT, USER_TASK_TEMPLATE

logger = logging.getLogger(__name__)


def _model_load_kwargs() -> dict[str, Any]:
    use_cuda = torch.cuda.is_available()
    torch_dtype = torch.bfloat16 if use_cuda else torch.float32
    kw: dict[str, Any] = {"torch_dtype": torch_dtype}
    if use_cuda:
        kw["device_map"] = "auto"
    return kw


def load_processor_and_model(model_id: str):
    token = os.environ.get("HF_TOKEN")
    processor = AutoProcessor.from_pretrained(model_id, token=token)
    load_kw = _model_load_kwargs()
    try:
        from transformers import AutoModelForImageTextToText

        model = AutoModelForImageTextToText.from_pretrained(model_id, token=token, **load_kw)
    except Exception as e:
        logger.warning("AutoModelForImageTextToText failed (%s); trying AutoModelForCausalLM.", e)
        model = AutoModelForCausalLM.from_pretrained(model_id, token=token, **load_kw)
    if not load_kw.get("device_map"):
        model = model.to("cpu")
    model.eval()
    return processor, model


def build_messages(images: list[Image.Image], note: str) -> list[dict[str, Any]]:
    user_content: list[dict[str, Any]] = []
    for img in images:
        user_content.append({"type": "image", "image": img})
    user_content.append(
        {
            "type": "text",
            "text": USER_TASK_TEMPLATE.format(note=note.strip() or "(none)", n_images=len(images)),
        }
    )
    return [
        {"role": "system", "content": [{"type": "text", "text": SYSTEM_PROMPT}]},
        {"role": "user", "content": user_content},
    ]


def _apply_chat_template(processor, messages: list[dict], enable_thinking: bool | None) -> dict:
    kwargs: dict[str, Any] = {
        "add_generation_prompt": True,
        "tokenize": True,
        "return_dict": True,
        "return_tensors": "pt",
    }
    sig = inspect.signature(processor.apply_chat_template)
    if enable_thinking is not None and "enable_thinking" in sig.parameters:
        kwargs["enable_thinking"] = enable_thinking
    return processor.apply_chat_template(messages, **kwargs)


def _move_batch_to_model(batch: dict, model: torch.nn.Module) -> dict:
    device = next(model.parameters()).device
    dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
    out: dict[str, Any] = {}
    for k, v in batch.items():
        if isinstance(v, torch.Tensor):
            if v.is_floating_point():
                out[k] = v.to(device=device, dtype=dtype)
            else:
                out[k] = v.to(device=device)
        else:
            out[k] = v
    return out


def generate_work_order_json(
    processor,
    model,
    images: list[Image.Image],
    note: str,
    *,
    max_new_tokens: int = 2048,
    enable_thinking: bool = False,
    temperature: float = 1.0,
    top_p: float = 0.95,
    top_k: int = 64,
) -> tuple[dict[str, Any], str]:
    messages = build_messages(images, note)
    inputs = _apply_chat_template(processor, messages, enable_thinking)
    inputs = _move_batch_to_model(inputs, model)
    input_len = inputs["input_ids"].shape[-1]

    gen_kw: dict[str, Any] = {
        **inputs,
        "max_new_tokens": max_new_tokens,
        "do_sample": True,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
    }

    with torch.inference_mode():
        out = model.generate(**gen_kw)

    raw = processor.decode(out[0][input_len:], skip_special_tokens=False)

    if hasattr(processor, "parse_response"):
        try:
            parsed = processor.parse_response(raw)
            if isinstance(parsed, dict) and "text" in parsed:
                raw = parsed.get("text", raw)
        except Exception:
            pass

    data = extract_json_object(raw)
    return data, raw
