# ocr_adapter.py
from typing import Any

class HandwritingOCR:
    def __init__(self, weights_path: str | None = None, device: str = "cpu"):
        self.model: Any = None
        self.device = device
        self.weights_path = weights_path

    def load(self):
        """
        TODO: load your model weights here.
        e.g., self.model = torch.jit.load(self.weights_path, map_location=self.device).eval()
        or     self.model = tf.saved_model.load(self.weights_path)
        """
        pass

    def _preprocess(self, img_bgr):
        """
        Typical steps for handwriting:
        - convert to grayscale
        - optional denoise (median/gaussian)
        - contrast normalize (CLAHE)
        - binarize/adaptive threshold if your model expects it
        - resize/normalize to model’s input size
        - (optional) deskew if needed
        Return: tensor/array in the exact format your model expects.
        """
        return img_bgr  # TODO: replace

    def _infer(self, x):
        """
        Run the model’s forward pass and return raw logits/sequences.
        - Torch: with torch.no_grad(): logits = self.model(x)
        - TF: logits = self.model(x, training=False)
        """
        return None  # TODO: replace

    def _decode(self, logits):
        """
        Convert model outputs to text.
        - CTC: greedy or beam search decode
        - Seq2seq: argmax tokens -> string
        Return: string
        """
        return ""  # TODO: replace

    def recognize(self, img_bgr) -> str:
        x = self._preprocess(img_bgr)
        logits = self._infer(x)
        text = self._decode(logits)
        return text.strip()
