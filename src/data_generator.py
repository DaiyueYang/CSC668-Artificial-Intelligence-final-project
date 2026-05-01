import os

import numpy as np
import pandas as pd

CATEGORY_PROFILES = {
    "museum": {
        "cost": (15, 35),
        "duration": (60, 150),
        "open": (9, 10),
        "close": (16, 18),
        "score_bias": 1.5,
    },
    "park": {
        "cost": (0, 10),
        "duration": (45, 120),
        "open": (7, 8),
        "close": (19, 21),
        "score_bias": 1.0,
    },
    "restaurant": {
        "cost": (10, 30),
        "duration": (45, 90),
        "open": (11, 12),
        "close": (21, 23),
        "score_bias": 0.5,
    },
    "landmark": {
        "cost": (0, 15),
        "duration": (30, 60),
        "open": (8, 9),
        "close": (18, 20),
        "score_bias": 2.0,
    },
    "market": {
        "cost": (0, 5),
        "duration": (30, 75),
        "open": (8, 9),
        "close": (14, 16),
        "score_bias": 0.0,
    },
    "entertainment": {
        "cost": (25, 80),
        "duration": (120, 240),
        "open": (10, 11),
        "close": (21, 23),
        "score_bias": 1.0,
    },
}

_NAMES = {
    "museum": ["City History Museum", "Modern Art Gallery", "Science Center",
               "War Memorial Museum", "Natural History Museum"],
    "park": ["Riverside Park", "Zen Garden", "Botanical Garden",
             "Hilltop Park", "Lakeside Park"],
    "restaurant": ["Fusion Kitchen", "Harbor Grill", "Noodle House",
                   "Rooftop Bistro", "Street Food Alley"],
    "landmark": ["Skyline Tower", "Old Cathedral", "Victory Bridge",
                 "Lighthouse Point", "Clock Tower"],
    "market": ["Old Town Market", "Night Bazaar", "Flower Market",
               "Craft Market", "Spice Market"],
    "entertainment": ["Adventure World", "City Aquarium", "Comedy Theater",
                      "Escape Room Center", "Concert Hall"],
}


def _time_str(hour: int, minute: int = 0) -> str:
    return f"{hour:02d}:{minute:02d}"


def generate_attractions(
    n: int = 30,
    map_size: float = 20.0,
    n_clusters: int = 4,
    seed: int = 42,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    categories = list(CATEGORY_PROFILES.keys())

    cat_list = [categories[i % len(categories)] for i in range(n)]
    rng.shuffle(cat_list)

    margin = map_size * 0.15
    cluster_centres = rng.uniform(margin, map_size - margin, size=(n_clusters, 2))
    cluster_ids = rng.integers(0, n_clusters, size=n)

    xs, ys = [], []
    for i in range(n):
        cx, cy = cluster_centres[cluster_ids[i]]
        x = np.clip(rng.normal(cx, 2.5), 0, map_size)
        y = np.clip(rng.normal(cy, 2.5), 0, map_size)
        xs.append(round(float(x), 1))
        ys.append(round(float(y), 1))

    records = []
    cat_counters: dict[str, int] = {c: 0 for c in categories}

    for i in range(n):
        cat = cat_list[i]
        profile = CATEGORY_PROFILES[cat]

        name_idx = cat_counters[cat] % len(_NAMES[cat])
        name = _NAMES[cat][name_idx]
        if cat_counters[cat] >= len(_NAMES[cat]):
            name += f" {cat_counters[cat] - len(_NAMES[cat]) + 2}"
        cat_counters[cat] += 1

        cost = round(float(rng.uniform(*profile["cost"])), 0)
        duration = int(rng.integers(profile["duration"][0] // 15,
                                    profile["duration"][1] // 15 + 1)) * 15

        open_h = int(rng.integers(profile["open"][0], profile["open"][1] + 1))
        close_h = int(rng.integers(profile["close"][0], profile["close"][1] + 1))

        base_score = rng.uniform(1.0, 8.0) + profile["score_bias"]
        score = round(float(np.clip(base_score, 1.0, 10.0)), 1)

        records.append({
            "attraction_id": i,
            "name": name,
            "category": cat,
            "x": xs[i],
            "y": ys[i],
            "cost": cost,
            "visit_duration": duration,
            "opening_time": _time_str(open_h),
            "closing_time": _time_str(close_h),
            "priority_score": score,
        })

    return pd.DataFrame(records)


def generate_travel_time_matrix(
    attractions: pd.DataFrame,
    hotel_x: float = 10.0,
    hotel_y: float = 10.0,
    speed_kmh: float = 30.0,
) -> pd.DataFrame:
    ids = list(attractions["attraction_id"])
    xs = list(attractions["x"])
    ys = list(attractions["y"])

    labels = ["hotel"] + ids
    all_x = [hotel_x] + xs
    all_y = [hotel_y] + ys

    n = len(labels)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt((all_x[i] - all_x[j]) ** 2 +
                           (all_y[i] - all_y[j]) ** 2)
            minutes = round(dist / speed_kmh * 60, 1)
            matrix[i][j] = minutes
            matrix[j][i] = minutes

    return pd.DataFrame(matrix, index=labels, columns=labels)


def save_attractions_csv(
    attractions: pd.DataFrame,
    path: str = "data/attractions.csv",
) -> str:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    attractions.to_csv(path, index=False)
    return path


def save_travel_matrix_csv(
    travel_matrix: pd.DataFrame,
    path: str = "data/travel_matrix.csv",
) -> str:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    travel_matrix.to_csv(path, index_label="from")
    return path


def save_dataset(
    attractions: pd.DataFrame,
    travel_matrix: pd.DataFrame,
    data_dir: str = "data",
) -> tuple[str, str]:
    a_path = save_attractions_csv(
        attractions, os.path.join(data_dir, "attractions.csv")
    )
    m_path = save_travel_matrix_csv(
        travel_matrix, os.path.join(data_dir, "travel_matrix.csv")
    )
    return a_path, m_path
