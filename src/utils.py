def get_rating_color(rating: int) -> str:
    color = "black"
    colors = {
        400: "#E7E7E7",
        800: "#804000",
        1200: "#418141",
        1600: "#00C0C0",
        2000: "#0000FF",
        2400: "#C0C000",
        2800: "#FF8000",
        10000: "#FF0000",
    }
    for r, c in colors.items():
        if rating < r:
            color = c
            break

    return color
