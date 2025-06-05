"""牌解析ロジックを提供するモジュール"""

from mahjong.shanten import Shanten
from src.dahitter.config import TILE_KIND_COUNT, MAX_TILE_DUPLICATE


def convert_hand_to_34(hand: list[str]) -> list[int]:
    """牌名リストを34種形式へ変換する"""
    result = [0] * TILE_KIND_COUNT
    for pai in hand:
        if pai[0] == "m":
            idx = int(pai[1]) - 1
        elif pai[0] == "p":
            idx = 9 + int(pai[1]) - 1
        elif pai[0] == "s":
            idx = 18 + int(pai[1]) - 1
        elif pai[0] == "z":
            idx = 27 + int(pai[1]) - 1
        else:
            continue
        result[idx] += 1
    return result

def name_to_34(name: str) -> int:
    """牌名から34インデックスを取得する"""
    if name[0] == "m":
        return int(name[1]) - 1
    elif name[0] == "p":
        return 9 + int(name[1]) - 1
    elif name[0] == "s":
        return 18 + int(name[1]) - 1
    elif name[0] == "z":
        return 27 + int(name[1]) - 1
    return -1

def tile34_to_name(idx: int) -> str:
    """34形式のインデックスを牌名に変換する"""
    if 0 <= idx < 9:
        return f"m{idx + 1}"
    if 9 <= idx < 18:
        return f"p{idx - 8}"
    if 18 <= idx < 27:
        return f"s{idx - 17}"
    if 27 <= idx < TILE_KIND_COUNT:
        return f"z{idx - 26}"
    return "?"

def calc_ukeire34(hand34: list[int], shanten_val: int) -> tuple[list[int], int]:
    """受け入れ牌一覧と残り枚数の合計を求める"""
    ukeire_tiles = []
    shanten_instance = Shanten()
    for i in range(TILE_KIND_COUNT):
        if hand34[i] >= MAX_TILE_DUPLICATE:
            continue
        temp = hand34[:]
        temp[i] += 1
        s = shanten_instance.calculate_shanten(temp)
        if s < shanten_val:
            ukeire_tiles.append(i)
    ukeire_count = sum(MAX_TILE_DUPLICATE - hand34[i] for i in ukeire_tiles)
    return ukeire_tiles, ukeire_count

def estimate_ryoukei_score(ukeire_tiles: list[int]) -> float:
    if len(ukeire_tiles) <= 1:
        return 0.0
    ukeire_tiles = sorted(ukeire_tiles)
    ryoukei_count = 0
    for i in range(1, len(ukeire_tiles)):
        if abs(ukeire_tiles[i] - ukeire_tiles[i - 1]) == 1:
            ryoukei_count += 1
    return ryoukei_count / (len(ukeire_tiles) - 1)

def analyze_hand_with_ukeire(hand: list[str]) -> tuple[int, list[dict]]:
    """
    打牌候補ごとの受け入れを計算し、スコア付きで返す。
    - 向聴が下がる → +10000
    - 受け入れ枚数 → *100
    - 受け入れ牌の種類数 → *10
    - 良形スコア（両面など） → *5
    """
    shanten = Shanten()
    candidates = []

    hand34 = convert_hand_to_34(hand)
    base_shanten = shanten.calculate_shanten(hand34)

    for i, pai in enumerate(hand):
        idx = name_to_34(pai)
        if idx == -1:
            continue

        if hand34[idx] == 0:
            continue

        hand34[idx] -= 1
        new_shanten = shanten.calculate_shanten(hand34)
        ukeire_tiles, ukeire_count = calc_ukeire34(hand34, new_shanten)
        ukeire_types = len(set(ukeire_tiles))
        ryoukei_score = estimate_ryoukei_score(ukeire_tiles)

        score = (
            (base_shanten - new_shanten) * 10000 +
            ukeire_count * 100 +
            ukeire_types * 10 +
            ryoukei_score * 5
        )

        candidates.append({
            "index": i,
            "pai": pai,
            "shanten": new_shanten,
            "ukeire": ukeire_count,
            "ukeire_tiles": ukeire_tiles,
            "ukeire_types": ukeire_types,
            "ryoukei_score": round(ryoukei_score, 3),
            "score": score,
        })

        hand34[idx] += 1

    # 最良打をマーク
    if candidates:
        max_score = max(c["score"] for c in candidates)
        for c in candidates:
            c["recommended"] = c["score"] == max_score

    return base_shanten, sorted(candidates, key=lambda x: -x["score"])
