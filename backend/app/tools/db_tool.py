from app.services.storage import JsonStorage


class DBTool:
    def __init__(self) -> None:
        self.storage = JsonStorage()
