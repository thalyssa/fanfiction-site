import users
import views


class State:
    user: users.User
    view: views.View
    running: bool
    users_json_path: str

    def run(self, option):
        self.view.run(option)

    def prompt(self):
        return self.view.prompt()

