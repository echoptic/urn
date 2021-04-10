from sys import argv
import os
import shutil
import configparser

from update_app import update_blueprints

# read config file
config = configparser.ConfigParser()
config.read('urn.ini')
default = config['DEFAULT']
auto_update = default['AutoUpdateApp']


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
    'static/css/style.css',
    'static/js/script.js',
]


def write_html():
    with open(dir + f'/templates/{name}.html', 'w') as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <title>Document</title>
</head>
<body>
    %s
    <script defer src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>''' % name)

# this is the most important file in the blueprint
def write_blueprint():
    with open(dir + f'/{name}.py', 'w') as f:
        f.write(f"""from flask import Blueprint, render_template

{name} = Blueprint('{name}', __name__, template_folder='templates')

@{name}.route('/', defaults={{'page': 'index'}})
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
