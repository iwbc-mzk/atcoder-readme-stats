from typing import Union, Literal, Optional
from abc import ABC, abstractmethod

from src.themes import Theme, THEMES

Auto = Literal["auto"]


class Card(ABC):
    def __init__(
        self,
        width: Union[int, Auto] = "auto",
        height: Union[int, Auto] = "auto",
        viewbox_width: Optional[int] = 450,
        viewbox_height: Optional[int] = 200,
        theme: Optional[Theme] = THEMES["default"],
    ) -> None:
        self._width = width
        self._height = height
        self._viewbox_width = viewbox_width
        self._viewbox_height = viewbox_height
        self._theme = theme

    @abstractmethod
    def _render_title(self):
        ...

    @abstractmethod
    def _render_body(self):
        ...

    def _styles(self) -> str:
        return ""

    def render(self):
        style = f"""
            #svg-body {{
                margin: 0;
                font-family: {self._theme.font_family};
                color: {self._theme.text_color};
                height: {self._viewbox_height}px;
                width: {self._viewbox_width}px;
            }}
             #card {{
                width: {self._viewbox_width - 2}px;
                height: {self._viewbox_height - 2}px;
                
                display: flex;
                position: relative;
                background-color: {self._theme.background_color};

                border: 1px solid rgb(228, 226, 226);
                border-radius: 10px;
            }}
            #card-body {{
                margin: 20px;
                width: {self._viewbox_width - 40}px;
                height: {self._viewbox_height - 40}px;
                display: flex;
                flex-direction: column;
            }}
            #title-container {{
                height: 20%;
            }}
            #body-container {{
                height: 80%;
            }}
        """

        style += self._styles()

        return f"""
            <svg version="1.1" 
                viewBox="0 0 {self._viewbox_width} {self._viewbox_height}"
                xmlns="http://www.w3.org/2000/svg"
                {f'width="{self._width}"' if type(self._width) == int else ""}
                {f'height="{self._height}"' if type(self._height) == int else ""}
            >
                <foreignObject width="{self._viewbox_width}" height="{self._viewbox_height}" requiredExtensions="http://www.w3.org/1999/xhtml">
                    <body id="svg-body" xmlns="http://www.w3.org/1999/xhtml">
                        <div id="card">
                            <div id="card-body">
                                <div id="title-container">
                                    {self._render_title()}
                                </div>
                                <div id="body-container">
                                    {self._render_body()}
                                </div>
                            </div>
                        </div>
                        <style id="main-style">{style}</style>
                    </body>
                </foreignObject>
            </svg>
        """
