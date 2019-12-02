import os
import json
import state
import views


option: str = ''
state = state.State()
view = views.InitView(state)
state.view = view

while option != 'q':
    option = state.prompt()
    state.run(option)

print("Até logo <3!")