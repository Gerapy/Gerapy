from os.path import join
from gerapy.server.core.parser import get_start_requests, get_follow_requests_and_items


def parse(args):
    project_path = join(args.dir, args.project)
    if args.start:
        results = get_start_requests(project_path, args.spider)
        print('results', results)
        return results
    else:
        results = get_follow_requests_and_items(project_path, 'quotes', args)
        print('results', results)
        return results
