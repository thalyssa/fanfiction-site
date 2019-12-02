import os
import json
import state
import views

option = ''
state = state.State()
view = views.InitView(state)
state.running = True
state.view = view

APP_PATH = os.getcwd()
state.app_path = APP_PATH

USERS_JSON_PATH = os.path.join(APP_PATH, 'users.json')
state.users_json_path = USERS_JSON_PATH

USERS_DATA_PATH = os.path.join(APP_PATH, 'users')
state.users_data_path = USERS_DATA_PATH

if not os.path.isdir(USERS_DATA_PATH):
    os.mkdir(USERS_DATA_PATH)

if not os.path.isfile(USERS_JSON_PATH):

    users_data = {
        'admins': ['admin'],
        'users': ['admin'],
    }

    admin_data = {
                'email': 'admin@admin.com',
                'pass': '12345',
            }

    with open(USERS_JSON_PATH, 'w') as file:
        json.dump(users_data, file)

    admin_data_path = os.path.join(USERS_DATA_PATH, 'admin')

    if not os.path.isdir(admin_data_path):
        os.mkdir(admin_data_path)

    admin_json_file_path = os.path.join(admin_data_path, 'user_data.json')
    with open(admin_json_file_path, 'w') as file:
        json.dump(admin_data, file)

while state.running:
    option = state.prompt()
    state.run(option)

print("Até logo <3!")
