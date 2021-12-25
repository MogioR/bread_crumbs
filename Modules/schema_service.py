import random
import time

from api_objects.container import BaseContainer


class SchemaService:
    def __init__(self, base_container: BaseContainer):
        self.base_container = base_container
        self.all_containers = base_container.get_containers()
        self.schema = dict()

    def generate(self, path: str = ''):
        domains = {}

        for container in self.all_containers:
            if container.domain not in domains.keys():
                domains[container.domain] = []

            domains[container.domain].append(
                {
                    'position': container.level,
                    '@id': 'https//' + container.domain + container.path,
                    'name': random.choice(container.anchor_name) if len(container.anchor_name) > 0 else container.name
                }
            )
            self.schema[container.id] = {
                    'position': container.level,
                    '@id': 'https//' + container.domain + container.path,
                    'name': random.choice(container.anchor_name) if len(container.anchor_name) > 0 else container.name
                }

        # for key in domains.keys():
        #     with open(path+key, "w", encoding='utf-8') as write_file:
        #         json.dump(domains[key], write_file, ensure_ascii=False, indent=4)

    def upload(self):
        # TODO: upload for schema service
        pass
        # for id_ in self.schema.keys():
        #     self.base_container.pos(id_, self.crumbs[id_])
