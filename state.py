import views

class State:
    username: str
    userdata: dict
    user_home: str

    admin_list: list

    current_story: str

    view: views.View
    running: bool

    app_path: str
    users_json_path: str
    users_data_path: str

    def run(self, option):
        self.view.run(option)

    def prompt(self):
        return self.view.prompt()

