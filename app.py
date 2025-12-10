import base64

import torch
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class OcrRequest(BaseModel):
    image_data: str  # Base64 encoded image data


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/ocr")
async def ocr_endpoint(ocr_request: OcrRequest):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    doctr_model = ocr_predictor(pretrained=True, detect_language=True)
    doctr_model = doctr_model.to(device)
    image_bytes = base64.b64decode(ocr_request.image_data)
    doc = DocumentFile.from_images([image_bytes])
    result = doctr_model(doc)

    lines: list[str] = []
    for page in result.pages:
        for block in page.blocks:
            for line in block.lines:
                text = " ".join([word.value for word in line.words])
                lines.append(text)

    extract_text = "\n".join(lines)
    return {"extracted_text": extract_text}
