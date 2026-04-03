MOCK_WORK_ORDER_RESULT = {
    "work_order": {
        "title": "Mock pump inspection",
        "site_id": "SITE-MOCK-1",
        "priority": "medium",
        "summary": "Replace seal; verify pressure per note.",
        "due_hint": "End of week",
        "source_refs": ["image:1"],
    },
    "bom": {
        "line_items": [
            {
                "sku_or_description": "MECH-SEAL-100",
                "qty": 1,
                "unit": "ea",
                "confidence": 0.5,
                "source_refs": ["image:1"],
            }
        ]
    },
    "hazards": [
        {
            "type": "rotating_equipment",
            "severity": "medium",
            "evidence_ref": "image:1",
        }
    ],
}
