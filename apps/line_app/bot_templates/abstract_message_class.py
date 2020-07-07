import json
from abc import ABC


class AbstractLineMessage(ABC):

    def __init__(self, object_instance):
        self.object_instance = object_instance

    def render(self):
        return {
            'hello': 'world'
        }

    def get_json(self):
        return json.dumps(self.render(self.object_instance))
