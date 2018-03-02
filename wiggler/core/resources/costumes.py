from wiggler.common.resource import Resource

class Costume(Resource):
    pass

class Wardrobe(object):

    def __init__(self, costumes_ids):
        self.active = None
        self.costumes_ids = []
        self.costumes = {}
        for asset_id in self.costumes_ids:
            self.add(asset_id)

        try:
            self.active = self.costumes[self.costumes_list[0]]
        except IndexError:
            pass

    def add(self, asset_id, position=None, make_active=False):
        costume = Costume(asset_id)
        self.costumes[asset_id] = costume
        if position is not None:
            self.costumes_ids.insert(position, asset_id)
        else:
            self.costumes_list.append(asset_id)
        if make_active:
            self.set_active(asset_id)

    def remove(self, asset_id):
        del(self.costumes[asset_id])
        self.costumes_ids.remove(asset_id)
        if self.active == asset_id:
            act_index = self.costumes_ids.index(asset_id)
            if act_index < len(self.costumes_ids - 1):
                act_index += 1
            else:
                act_index -= 1
            try:
                self.active == self.costumes_ids[act_index]
            except IndexError:
                self.active = None

    def set_active(self, asset_id):
        self.active = asset_id

    def get_active_costume(self, asset_id):
        return self.costumes[self.active]

    def get_active(self):
        return self.active


