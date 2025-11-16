FISH_POOLS = {
    "Comum": {
        "chance":100, # 60% de chance de cair nesta pool
        "emoji": "🐟",
        "peixes": {
            "Sardinha": {"min_size": float(10), "max_size": float(25), "valor": 5},
            "Tilápia": {"min_size": float(20), "max_size": float(40), "valor": 8},
            "Pacu": {"min_size": float(15), "max_size": float(30), "valor": 6},
        }
    }
}

POOLS = list(FISH_POOLS.keys())
CHANCES = [FISH_POOLS[pool]["chance"] for pool in POOLS]