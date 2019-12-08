import argparse
import yaml
import sys
import os
from afctl import __version__
from afctl.utils import Utility

class Parser():


    def setup_parser(self):
        self.parser = argparse.ArgumentParser(description="A CLI tool to make deployment of airflow projects faster")
        self.parser.add_argument("-v", "--version", action='version', version=__version__)
        new_parser = self.parser.add_subparsers()
        sub_parser = new_parser.add_parser("init", help="Create a boilerplate code for your airflow project")
        sub_parser.set_defaults(func=self.create_project)
        sub_parser.add_argument("-n", "--name", help="Name of your airflow project", required=True)
        sub_parser.add_argument("-p", "--plugin", help="Add plugin to your project", choices=self.plugins, required=True)
        sub_parser = new_parser.add_parser("list", help="Get list of operators, sensors, plugins, hooks.")
        sub_parser.set_defaults(func=self.list)
        sub_parser.add_argument("type", choices=self.choices)
        return self.parser

    def create_project(self, args):
        pwd = os.getcwd()
        main_dir = [os.path.join(pwd, args.name)]
        sub_files = ['requirements.txt', 'setup.py', '.gitignore']
        sub_dir = [args.name]
        sub_dir_files = ['__init__.py', 'command_line.py', 'parser.py', 'meta.yml']

        if os.path.exists(main_dir[0]):
            self.parser.error("Project already exists.")

        print("Initializing new project...")

        # Create parent dir
        os.mkdir(main_dir[0])

        # Create sub files
        Utility.create_files(main_dir, sub_files)

        # Create sub dir
        Utility.create_dirs(main_dir, sub_dir)

        # Create sub dir files
        package_dir = ["{}/{}".format(main_dir[0], args.name)]
        Utility.create_files(package_dir, sub_dir_files)

        print("New project initialized successfully.")

    def list(self, args):
        print("Available {} :".format(args.type))
        vals = eval("self.{}".format(args.type))
        print('\n'.join(map(str, vals)))

    def __init__(self):
        try:
            with open("{}/{}".format(os.path.dirname(os.path.abspath(__file__)), 'meta.yml')) as file:
                self.data = yaml.full_load(file)

            self.choices = [k for k in self.data]
            self.operators = self.data['operators'].split(' ')
            self.hooks = self.data['hooks'].split(' ')
            self.sensors = self.data['sensors'].split(' ')
            self.plugins = self.data['plugins'].split(' ')
        except:
            sys.exit(3)
