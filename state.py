import views

class State:

    app_path: str
    users_json_path: str
    users_data_path: str
    admin_list: list

    username = None

    user_home: str
    user_json_path: str
    user_data: dict
    current_story_home: str

    view: views.View
    running: bool

    view_stack = []

    def run(self, option):
        self.view.run(option)

    def prompt(self):
        return self.view.prompt()

