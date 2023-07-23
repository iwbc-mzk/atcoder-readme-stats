from src.cards.card import Card


class ErrorCard(Card):
    def __init__(self, message: str, secondary_message: str) -> None:
        self._message = message
        self._secondary_message = secondary_message

        super().__init__(height=150, viewbox_height=150, width=600, viewbox_width=600)

    @property
    def message(self) -> str:
        return self._message

    @property
    def secondary_message(self) -> str:
        return self._secondary_message

    def _render_title(self):
        return f"""
            <div id="title">Something went wrong!</div>
        """

    def _render_body(self):
        return f"""
            <div id="error-message-container">
                <p id="error-message">
                    <span id="main-message">{self._message}</span>
                    <br />
                    <span id="secondary-message">{self._secondary_message}</span>
                </p>
            </div>
        """

    def _styles(self):
        return f"""
            #title {{
                color: {self._theme.title_color};
                font-size: 20px;
                font-weight: 600;
                height: 30%;
            }}
            #error-message-container {{
                display: flex;
                align-items: center;
                height: 70%;
            }}
            #error-message {{
                line-height: 18px;
                margin: 0px
            }}
            #main-message {{
                color: {self._theme.text_color};
                font-size: 18px;
                font-weight: 500;
            }}
            #secondary-message {{
                color: {self._theme.text_color};
                opacity: 0.7;
                font-size: 14px;
            }}
        """
