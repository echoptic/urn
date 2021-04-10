import os

dir = os.getcwd()

blueprints = []

# list all folders and append them to blueprints[]
dir_content = os.listdir(dir)
# ignore pycache folder
dir_content.remove('__pycache__')

# ignore all files and folders that have a . in them
for folder in dir_content:
    if not '.' in folder:
        blueprints.append(folder)
        

def update_blueprints():
    # what will be written in app.py
    app_content = ['from flask import Flask\n\n','application=Flask(__name__)\n', "if __name__ == '__main__':\n\tapplication.run()"]
    for blueprint in blueprints:
        app_content.insert(1, f'from {blueprint}.{blueprint} import {blueprint}\n')
        app_content.insert(-1, f'application.register_blueprint({blueprint})\n')
    
    # write in app.py
    with open('app.py', 'w') as f:
        for content in app_content:
            f.write(content)
        f.close()
        print('Updated app.py')