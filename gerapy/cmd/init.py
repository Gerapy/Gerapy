import os
from os.path import join

PROJECTS_FOLDER = 'projects'

def init(folder):
    if not folder:
        folder = 'gerapy'
    # execute path
    execute_path = os.getcwd()
    folder_path = join(execute_path, folder)
    # make folder dir, default to gerapy
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    
    # make dir of project
    os.chdir(folder_path)
    projects_folder = join(folder_path, PROJECTS_FOLDER)
    if not os.path.exists(projects_folder):
        os.mkdir(projects_folder)
