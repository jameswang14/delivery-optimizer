class Request:
    def __init__(self, pos, time, store_pos):
        self.pos = pos
        self.init_time = time
        self.store_pos = store_pos
        self.assigned_time = -1
        self.fulfill_time = -1
        

