from sys import argv
import os
import shutil
import configparser

# this is for update command
cwd = os.getcwd()
blueprints = []
# list all folders and append them to blueprints[]
dir_content = os.listdir(cwd)
# ignore pycache folder
if '__pycache__' in dir_content:
    dir_content.remove('__pycache__')

# ignore all files and folders that have a . in them
for folder in dir_content:
    if not '.' in folder:
        blueprints.append(folder)
        
def update_blueprints():
    # what will be written in app.py
    app_content = ['from flask import Flask\n\n','application=Flask(__name__)\n', "if __name__ == '__main__':\n\tapplication.run(debug=True)"]
    for blueprint in blueprints:
        app_content.insert(1, f'from {blueprint}.{blueprint} import {blueprint}\n')
        app_content.insert(-1, f'application.register_blueprint({blueprint})\n')
    
    # write in app.py
    with open('app.py', 'w') as f:
        for content in app_content:
            f.write(content)
        f.close()
        print('Updated app.py')


# CONFIG
if 'urn.ini' in dir_content:
    config = configparser.ConfigParser()
    config.read('urn.ini')
    settings = config['SETTINGS']
    auto_update = settings['AutoUpdateApp']


if len(argv) < 2:
    print('Not enough arguments given.')
    quit()

# fix error for name = argv[2] out of range when running update command
# should be changed later
elif len(argv) > 2:
    name = argv[2]
    dir = f'./{name}/'

# excluding f'{name}'.py and templates/index.html because they will be written after
file_list = [
    '__init__.py',
    f'static/css/{name}.css',
    f'static/js/{name}.js',
]


def write_html():
    with open(dir + f'/templates/{name}.html', 'w') as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/%s.css') }}">
    <title>Document</title>
</head>
<body>
    %s
    <script defer src="{{ url_for('static', filename='js/%s.js') }}"></script>
</body>
</html>''' % name)

# this is the most important file in the blueprint
def write_blueprint():
    with open(dir + f'/{name}.py', 'w') as f:
        f.write(f"""from flask import Blueprint, render_template

{name} = Blueprint('{name}', __name__, template_folder='templates')

@{name}.route('/', defaults={{'{name}': 'index'}})
@{name}.route('/<{name}>')
def show({name}):
    return render_template(f'{{{name}}}.html')""")



def create_file(file_name):
    open(dir + file_name, 'w')


def create_folder(folder_name):
    os.makedirs(name + folder_name)


def create_blueprint():
    try:
        try:

            # create all folders
            create_folder('/templates')
            create_folder('/static/js')
            create_folder('/static/css')
            create_folder('/static/img')

            # create all files that are in file_list[]
            for file in file_list:
                create_file(file)
            
            write_blueprint()
            write_html()


        # if blueprint with the same name already exists
        except FileExistsError:
            print(f"Folder with the name '{name}' already exists. Do you wan't to owerwrite it?")
            prompt = input('(y/N)\n')
            if prompt == 'y':
                shutil.rmtree(name)
                create_blueprint()


        # Ask to initialize git repozitory
        if not os.path.exists('.git'):
            print("This folder isn't a git repository. Do you want to initialize it?")
            prompt = input('(y/N)\n')
            if prompt == 'y':
                os.system('git init')
                if not os.path.exists('.gitignore'):
                    with open('.gitignore', 'w') as f:
                        f.write('__pycache__\n')

    except KeyboardInterrupt:
        pass


if argv[1] == 'create':
    create_blueprint()

    # for some reason this isnt updating the last one but the one
    if auto_update == 'yes':
            update_blueprints()

elif argv[1] == 'update':
    update_blueprints()
