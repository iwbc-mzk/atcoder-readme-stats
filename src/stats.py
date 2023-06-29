from src.model import UserData


class StatsCard:
    def __init__(self, userdata: UserData) -> None:
        self._userdata = userdata

    def render(self):
        return f"""
            <svg width="400" height="300" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
                <foreignObject width="400" height="300" requiredExtensions="http://www.w3.org/1999/xhtml">
                    <body xmlns="http://www.w3.org/1999/xhtml">
                        <p>{self._userdata.rating}</p>
                    </body>
                </foreignObject>
            </svg>
        """
