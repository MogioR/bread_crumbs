from Modules.schema_service import SchemaService
from Modules.bread_crumbs_service import BreadCrumbsService

# Import containers
import os
import sys
API_PATH = os.getenv("API_PATH")
if API_PATH is None or API_PATH == '':
    API_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(str(API_PATH))
from api_objects.container import BaseContainer


if __name__ == '__main__':
    base_container = BaseContainer()
    base_container.load()

    schema_generator = SchemaService(base_container)
    schema_generator.generate('Schemas/')
    schema_generator.upload()

    bread_crumbs_generator = BreadCrumbsService(base_container)
    bread_crumbs_generator.generate('Bread_crumbs/')
    bread_crumbs_generator.upload()
