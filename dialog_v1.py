# coding=utf-8
import json
from os.path import join, dirname
from watson_developer_cloud import DialogV1
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('datosCuentaDialogoIBM.ini')

user = config.get('datosIBM', 'user')
password = config.get('datosIBM', 'password')

dialog = DialogV1(username=user,password=password)

def creaDialogo(nombre, archivo):
    with open(join(dirname(__file__), archivo)) as dialog_file:
        return(json.dumps(dialog.create_dialog(
            dialog_file=dialog_file, name=nombre), indent=2))

#print(json.dumps(dialog.get_dialogs(), indent=2))

#print(json.dumps(dialog.get_dialog("62fb21b5-a14b-40b6-a453-80d721ca604b"), indent=2))

# CREATE A DIALOG
# creaDialogo('selene_prueba_2','guionDialogo.xml' )
         
print(json.dumps(dialog.get_dialogs(), indent=2))
dialog_id = "3e0757c5-b414-438b-9cca-321f7f5c3f89"

# with open(join(dirname(__file__), '../resources/dialog.xml') as dialog_file:
#     print(json.dumps(dialog.update_dialog(dialog_file=dialog_file, dialog_id=dialog_id), indent=2))

#print(json.dumps(dialog.get_content(dialog_id), indent=2))
#
initial_response = dialog.conversation(dialog_id)
print(json.dumps(initial_response, indent=2))

print(json.dumps(dialog.conversation(dialog_id=dialog_id,
                                      dialog_input='radio',
                                      conversation_id=initial_response['conversation_id'],
                                      client_id=initial_response['client_id']), indent=2))

# print(json.dumps(dialog.delete_dialog(dialog_id='63b0489c-cd97-45ef-8800-4e7c310eeb19'), indent=2))

# print(json.dumps(dialog.update_profile(
#     dialog_id='6250d170-41d6-468a-a697-5675578c8012', client_id=123, name_values=[{'name': 'test', 'value': 'v1'}]),
#     indent=2))
#
# print(json.dumps(dialog.get_profile(
#     dialog_id='6250d170-41d6-468a-a697-5675578c8012', client_id=123), indent=2))
