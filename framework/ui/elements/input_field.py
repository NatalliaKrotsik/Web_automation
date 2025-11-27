from framework.ui.core.base_element import BaseElement


class InputField(BaseElement):
    def __init__(self, page, selector):
        super().__init__(page, selector)
    
    def clear(self) -> None:
        self.locator.fill("")
    
    def _type(self, text: str) -> None:
        self.locator.fill(text)
    
    def clear_and_type(self, text: str) -> None:
        self.clear()
        self.type(text)