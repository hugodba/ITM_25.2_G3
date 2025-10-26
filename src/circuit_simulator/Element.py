class Element:
    """Base class for circuit elements."""
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
       return f"Element: {self.name}"
