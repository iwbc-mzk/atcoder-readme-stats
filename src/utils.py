def get_rating_color(rating: int) -> str:
    color = "#000000"
    colors = {
        400: "#808080",
        800: "#ba5f17",
        1200: "#008000",
        1600: "#00C0C0",
        2000: "#4169e1",
        2400: "#C0C000",
        2800: "#FF8000",
        10000: "#FF0000",
    }
    for r, c in colors.items():
        if rating < r:
            color = c
            break

    return color
