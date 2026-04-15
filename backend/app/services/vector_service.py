from collections import Counter
from functools import lru_cache
from math import sqrt


class VectorService:
    def embed_text(self, text: str) -> Counter[str]:
        tokens = [token.strip(".,()[]").lower() for token in text.split()]
        return Counter(token for token in tokens if token)

    def cosine_similarity(self, left_text: str, right_text: str) -> float:
        left = self.embed_text(left_text)
        right = self.embed_text(right_text)
        if not left or not right:
            return 0.0
        shared = set(left) & set(right)
        numerator = sum(left[token] * right[token] for token in shared)
        left_norm = sqrt(sum(value * value for value in left.values()))
        right_norm = sqrt(sum(value * value for value in right.values()))
        if left_norm == 0 or right_norm == 0:
            return 0.0
        return numerator / (left_norm * right_norm)


@lru_cache
def get_vector_service() -> VectorService:
    return VectorService()
