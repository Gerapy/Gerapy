def scrapyd_url(ip, port):
    url = 'http://{ip}:{port}'.format(ip=ip, port=port)
    return url
