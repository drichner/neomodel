import re
from py2neo import neo4j
from .exception import UniqueProperty, DataInconsistencyError

camel_to_upper = lambda x: "_".join(word.upper() for word in re.split(r"([A-Z][0-9a-z]*)", x)[1::2])
upper_to_camel = lambda x: "".join(word.title() for word in x.split("_"))


class CustomBatch(neo4j.WriteBatch):

    def __init__(self, graph, index_name, node='(unsaved)'):
        super(CustomBatch, self).__init__(graph)
        self.index_name = index_name
        self.node = node





    def _check_for_conflicts(self, results, requests):
        for i, r in enumerate(results):
            if r.status == 200:
                raise DataInconsistencyError(requests[i], self.index_name, self.node)


def _legacy_conflict_check(cls, node, props):
    for key, value in props.items():
        if key in cls._class_properties() and cls.get_property(key).unique_index:
                results = cls.index.__index__.get(key, value)
                if len(results):
                    if isinstance(node, (int,)):  # node ref
                        raise UniqueProperty(key, value, cls.index.name)
                    elif hasattr(node, 'id') and results[0].id != node.id:
                        raise UniqueProperty(key, value, cls.index.name, node)
