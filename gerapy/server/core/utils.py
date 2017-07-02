import os
import fnmatch

IGNORES = ['.git/', '*.pyc', '.DS_Store', '.idea/']


def scrapyd_url(ip, port):
    url = 'http://{ip}:{port}'.format(ip=ip, port=port)
    return url


def log_url(ip, port, project, spider, job):
    url = 'http://{ip}:{port}/logs/{project}/{spider}/{job}.log'.format(ip=ip, port=port, project=project,
                                                                        spider=spider, job=job)
    return url


def merge(path, file):
    return '{0}/{1}'.format(path, file)


def ignored(ignores, path, file):
    file_name = merge(path, file)
    for ignore in ignores:
        if '/' in ignore and ignore.rstrip('/') in file_name:
            return True
        if fnmatch.fnmatch(file_name, ignore):
            return True
        if file == ignore:
            return True
    return False


def get_tree(path, ignores=IGNORES):
    result = []
    for file in os.listdir(path):
        if os.path.isdir(merge(path, file)):
            if not ignored(ignores, path, file):
                children = get_tree(merge(path, file), ignores)
                if children:
                    result.append({
                        'label': file,
                        'children': children,
                        'path': path
                    })
        else:
            if not ignored(ignores, path, file):
                result.append({'label': file, 'path': path})
    return result
