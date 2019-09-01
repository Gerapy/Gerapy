from os.path import join, exists
from os import makedirs, getcwd
from gerapy.settings import PROJECTS_FOLDER


def init(folder):
    """
    init workspace
    :param folder:
    :return:
    """
    # execute path
    execute_path = getcwd()
    folder_path = join(execute_path, folder)
    # make folder dir, default to gerapy
    exists(folder_path) or makedirs(folder_path)
    
    # make dir of project
    projects_folder = join(folder_path, PROJECTS_FOLDER)
    exists(projects_folder) or makedirs(projects_folder)
