from gui.keyboards.constructors import Row, Button

class ProgrammRow(list):
    def __init__(self, data: list) -> None:
        super().__init__()
        programm_id = data[0]
        programm_name = data[1]
        self.extend(Row(Button(text=f"{programm_name}", callback_data=f"menu.progs.id_{programm_id}")))
        
        
class UserRow(list):
    def __init__(self, data: list) -> None:
        super().__init__()
        user_id = data[0]
        access_level = data[1]
        self.extend(
            Row(
                Button(text=f"id {user_id}"),
                Button(text="-", callback_data=f"menu.opts.access.minus_id_{user_id}"),
                Button(text=f"{access_level}"),
                Button(text=f"+", callback_data=f"menu.opts.access.plus_id_{user_id}")
            )
        )