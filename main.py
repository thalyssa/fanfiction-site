import os
import json
import state
import views
import users

option: str = ''
state = state.State()
view = views.InitView(state)
state.running = True
state.view = view

APP_PATH = os.getcwd()
USERS_JSON_PATH = os.path.join(APP_PATH, 'users.json')
state.users_json_path = USERS_JSON_PATH

if not os.path.isfile(USERS_JSON_PATH):
    users_data = {
        'users': {
            'admin': {
                'email': 'admin@admin.com',
                'pass': '12345',
            }
        }
    }
    with open(USERS_JSON_PATH, 'w') as file:
        json.dump(users_data, file)

while state.running:
    option = state.prompt()
    state.run(option)

print("Até logo <3!")
