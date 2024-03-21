from vkwave.bots import (
    Keyboard, ButtonColor
)
KS = Keyboard()
KS.add_text_button("Начать", ButtonColor.SECONDARY, payload={"command":"start"})

KSTART = Keyboard()
KSTART.add_text_button(
    text="получить помощь", 
    color=ButtonColor.POSITIVE, 
    payload={"command": "help"}
)
KSTART.add_row()
KSTART.add_link_button(text="Вступить в СООПР", link="https://google.com")
KSTART.add_link_button(text="Справка", link="https://google.com")
