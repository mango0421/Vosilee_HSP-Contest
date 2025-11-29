# embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np

_model = None

def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("jhgan/ko-sroberta-multitask")
    return _model

def get_embedding(text: str) -> np.ndarray:
    """
    문장을 벡터로 바꿔주는 함수
    - text: 공백 제거된 한국어 문장
    - return: L2 정규화된 numpy 벡터
    """
    model = _get_model()
    emb = model.encode(text, normalize_embeddings=True)
    return np.array(emb)
