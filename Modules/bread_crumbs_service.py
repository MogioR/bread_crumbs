import random
import time
import copy

# Import containers
import os
import sys
API_PATH = os.getenv("API_PATH")
if API_PATH is None or API_PATH == '':
    API_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(str(API_PATH))
from api_objects.container import BaseContainer

MAX_PER_MINUTE = 30
TIMEOUT = 60


class BreadCrumbsService:
    def __init__(self, base_container: BaseContainer):
        self.base_container = base_container
        self.all_first_containers = base_container.get_containers(level_mode=True, level=1)
        self.crumbs = dict()
        self.all_containers = base_container.get_containers()

    def generate(self, path: str = ''):
        domains = {}

        for container in self.all_first_containers:
            self.generate_crumbs(container, domains, '/', [])

        # for key in domains.keys():
        #     with open(path + key, "w", encoding='utf-8') as write_file:
        #         json.dump(domains[key], write_file, ensure_ascii=False, indent=4)
        #
        # with open('crumbs.json', "w", encoding='utf-8') as write_file:
        #     json.dump(self.crumbs, write_file, ensure_ascii=False, indent=4)

    def upload(self):
        for container in self.crumbs.keys():
            container.stat_bread_crumbs.bread_crumbs = True
            try:
                pass
                self.base_container.post_breadcrumbs(container.id, self.crumbs[container])
            except:
                print('Error upload for', + container.id)

        self.base_container.save()

    def generate_crumbs(self, container, domains: dict, parent_path: str, current_crumb: list):
        if len(container.anchor_name) > 0:
            name = random.choice(container.anchor_name)
        elif container.extract_name is not None:
            name = container.extract_name
        else:
            name = container.name

        if container.domain not in domains.keys():
            domains[container.domain] = []

        crumb = copy.deepcopy(current_crumb)

        if len(crumb) > 0:
            crumb[-1]['path @optional'] = parent_path
            # crumb = crumb[1:]
            crumb.append({'name': name})
            # crumb.insert(0, {'debug_id': container.id, 'debug_path': container.path})
            self.crumbs[container] = crumb

            domains[container.domain].append(crumb)
        else:
            # crumb.insert(0, {'debug_id': container.id, 'debug_path': container.path})
            crumb.append({'name': name})

        if container.id in self.base_container.base_parents.keys():
            for child in self.base_container.base_parents[container.id]:
                self.generate_crumbs(child, domains, container.path, crumb)