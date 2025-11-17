from framework.ui.core.base_element import BaseElement


class Button(BaseElement):
    def __init__(self, page, selector):
        super().__init__(page, selector)
    
    def get_button_locator_and_click_around(self):

        button_box = self.selector.bounding_box()

        offsets = [
            (-5, -5),
            (button_box["width"] + 5, -5),
            (-5, button_box["height"] + 5),
            (button_box["width"] + 5, button_box["height"] + 5),
            (-5, button_box["height"] // 2),
            (button_box["width"] + 5, button_box["height"] // 2),
            (button_box["width"] // 2, -5),
            (button_box["width"] // 2, button_box["height"] + 5),
        ]

        for offset in offsets:
            x_offset = button_box["x"] + offset[0]
            y_offset = button_box["y"] + offset[1]

            self.base_page.mouse.move(x_offset, y_offset)
            self.base_page.mouse.click(x_offset, y_offset)