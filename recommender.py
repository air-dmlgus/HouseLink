"""HouseLink portfolio reconstruction: synthetic-area recommendations and clustering."""
from __future__ import annotations

import csv
import math
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "data" / "sample_areas.csv"
FEATURES = ("safety", "education", "medical")
PROFILES = {
    "balanced": {"safety": 0.4, "education": 0.3, "medical": 0.3},
    "safety": {"safety": 0.7, "education": 0.15, "medical": 0.15},
    "education": {"safety": 0.15, "education": 0.7, "medical": 0.15},
    "medical": {"safety": 0.15, "education": 0.15, "medical": 0.7},
}


def load_areas(path: str | Path = DATA_PATH) -> list[dict]:
    """Load demonstration data. Scores are illustrative, NOT real area assessments."""
    with open(path, encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))
    if not rows:
        raise ValueError("지역 데이터가 비어 있습니다.")
    result = []
    for row in rows:
        district = row["district"].strip()
        if not district:
            raise ValueError("지역명이 필요합니다.")
        area = {"district": district}
        for feature in FEATURES:
            value = float(row[feature])
            if not math.isfinite(value) or not 0 <= value <= 100:
                raise ValueError(f"{district}: {feature} 점수는 0~100이어야 합니다.")
            area[feature] = value
        result.append(area)
    return result


def recommend(areas: list[dict], profile: str = "balanced") -> list[dict]:
    """Weighted ranking across three demo dimensions, descending by score."""
    if profile not in PROFILES:
        raise ValueError(f"지원하지 않는 선호도: {profile}")
    weights = PROFILES[profile]
    ranked = []
    for area in areas:
        score = sum(area[name] * weight for name, weight in weights.items())
        ranked.append({**area, "score": round(score, 1)})
    return sorted(ranked, key=lambda row: (-row["score"], row["district"]))


def cluster_areas(areas: list[dict], k: int = 3, max_iter: int = 50) -> list[int]:
    """Small dependency-free K-Means demonstration (cluster IDs are NOT quality grades)."""
    if not areas or not 1 <= k <= len(areas):
        raise ValueError("k는 1부터 지역 개수 사이여야 합니다.")
    points = [tuple(float(area[key]) / 100 for key in FEATURES) for area in areas]

    def squared_distance(a, b):
        return sum((x - y) ** 2 for x, y in zip(a, b))

    # Deterministic farthest-first initialization for repeatable demonstrations.
    centers = [points[0]]
    while len(centers) < k:
        candidate = max(
            range(len(points)),
            key=lambda i: (min(squared_distance(points[i], c) for c in centers), -i),
        )
        centers.append(points[candidate])

    labels = [-1] * len(points)
    for _ in range(max_iter):
        new_labels = [
            min(range(k), key=lambda i: squared_distance(point, centers[i]))
            for point in points
        ]
        if new_labels == labels:
            break
        labels = new_labels
        updated = []
        for idx in range(k):
            members = [point for point, label in zip(points, labels) if label == idx]
            updated.append(
                tuple(sum(column) / len(members) for column in zip(*members))
                if members else centers[idx]
            )
        centers = updated
    return labels
