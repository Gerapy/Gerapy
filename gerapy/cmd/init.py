import os
from gerapy.server.core.utils import merge

PROJECTS_FOLDER = 'projects'


def init(folder):
    if not folder:
        folder = 'gerapy'
    # 执行路径
    execute_path = os.getcwd()
    folder_path = merge(execute_path, folder)
    # 创建folder，默认gerapy
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    
    # 创建projects文件夹，存放scrapy项目
    os.chdir(folder_path)
    projects_folder = merge(folder_path, PROJECTS_FOLDER)
    if not os.path.exists(projects_folder):
        os.mkdir(projects_folder)
