from pydantic import BaseModel


class Theme(BaseModel):
    font_family: str
    background_color: str
    title_color: str
    text_color: str


THEMES = {
    "default": Theme(
        **{
            "font_family": '"Segoe UI", Ubuntu, Sans-Serif',
            "background_color": "white",
            "title_color": "#2f80ed",
            "text_color": "#434d58",
        }
    )
}
