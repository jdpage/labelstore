import collections
import datetime
import random
import uuid

Item = collections.namedtuple("Item", ["label", "create_ts"])


class Store:
    """Simple in-memory key-value store for label items."""

    def __init__(self):
        self.items = dict()
        self.index = list()

    def clear(self):
        self.items.clear()
        self.index.clear()

    def create(self, label):
        id = uuid.uuid4().hex
        item = Item(label, datetime.datetime.now())
        self.items[id] = item
        self.index.append(id)
        return id, item

    def get_by_id(self, id):
        return self.items[id]

    def get_all(self):
        return self.items.items()

    def get_random(self):
        id = random.choice(self.index)
        return id, self.items[id]
