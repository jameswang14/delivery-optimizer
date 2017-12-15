import numpy as np
import math
from haversine import haversine
epsilon = .01
mph = 10.0
mps =  mph / 60 / 60 
dist_to_miles = 53.3880 # approximate ratio of distance to miles based on haversine

def dist(x1, x2): 
    return np.hypot( (x1[0]-x2[0]), (x1[1]-x2[1]))

class Deliveryman:
    def __init__(self, pos):
        self.pos = pos
        self.req = None
        self.picked_up = False
        self.total_cost = 0
    def move(self, t):
        if not self.req:
            return

        destination = self.req.store_pos
        if self.picked_up:
            destination = self.req.pos

        angle = np.arctan((destination[1]-self.pos[1])/(destination[0]-self.pos[0]))
        old_dist = dist(self.pos, destination) * dist_to_miles

        if old_dist <= epsilon:
            if not self.picked_up: # reached store
                self.picked_up = True
            else:                   # reached customer
                self.req.fulfill_time = t
                self.picked_up = False
                self.req = None
            return

        new_dist = old_dist - mps
        if self.picked_up:
            self.total_cost += (old_dist-new_dist)*3
        if destination[0]<self.pos[0]:
            new_x = destination[0] + np.cos(angle)*new_dist/dist_to_miles
            new_y = destination[1] + np.sin(angle)*new_dist/dist_to_miles    
        else:
            new_x = destination[0] - np.cos(angle)*new_dist/dist_to_miles
            new_y = destination[1] - np.sin(angle)*new_dist/dist_to_miles
        self.pos = (new_x, new_y)

        