import user
import views


class State:
    user: user.User
    view: views.View
    option: str

    def run(self, option):
        self.view.run(option)

    def prompt(self):
        return self.view.prompt()

