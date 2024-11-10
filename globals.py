from pygame import Vector2

SX = int((2256 * (1/1.5)) // 1)
SY = int((1504 * (1/1.5)) // 1)
FPS = 60

BG = (0, 0, 0)

def halfRound(val: float, n_digits: int = 0):
    val *= 10 ** n_digits
    result = int(val + (0.50002 if val >= 0 else -0.50002))
    return result / 10 ** n_digits if n_digits != 0 else int(result / 10)

def halfRoundV2(vec : Vector2) -> Vector2:
        return Vector2(
            gb.halfRound(vec.x, 1),
            gb.halfRound(vec.y, 1)
        )