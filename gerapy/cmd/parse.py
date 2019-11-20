from os.path import join
from gerapy.server.core.parser import get_start_requests, get_follow_requests_and_items
import json


def parse(args):
    """
    parse result by request args
    :param args:
    :return:
    """
    project_path = join(args.dir, args.project)
    if args.start:
        results = get_start_requests(project_path, args.spider)
    else:
        results = get_follow_requests_and_items(project_path, args.spider, args)
    print(json.dumps(results, ensure_ascii=False))
