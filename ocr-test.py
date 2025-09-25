import sys, torch
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

MODEL_ID = "microsoft/trocr-base-handwritten"
device = "cuda" if torch.cuda.is_available() else "cpu"

processor = TrOCRProcessor.from_pretrained(MODEL_ID)
model = VisionEncoderDecoderModel.from_pretrained(MODEL_ID).to(device).eval()

@torch.inference_mode()
def recognize(path: str) -> str:
    img = Image.open(path).convert("RGB")
    pixel_values = processor(images=img, return_tensors="pt").pixel_values.to(device)
    generated_ids = model.generate(pixel_values, max_new_tokens=128)
    text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
    return text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ocr_cli.py <image_path>")
        sys.exit(1)
    text = recognize(sys.argv[1])
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(text)           # <-- prints to your terminal/console
