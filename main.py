import types
import numpy as np
import matplotlib.pyplot as plt
import cvxpy as cvx
from Queue import Queue
from Deliveryman import Deliveryman
from Request import Request
from data import deliverymen, store_positions, x_bound, y_bound, a_r
from collections import deque
import matplotlib.animation as animation
from lp_solver import solve_min_cost
from haversine import haversine

def random_position():
    return ((x_bound[1] - x_bound[0]) * np.random.ranf(1)[0] + x_bound[0], (y_bound[1] - y_bound[0]) * np.random.ranf(1)[0] + y_bound[0] )

def plot_static(data):
    im = plt.imread("map.png")
    implot = plt.imshow(im, zorder=-1, extent=[x_bound[0], x_bound[1], y_bound[0], y_bound[1]])
    for d in data:
        plt.scatter(*zip(*d))
    plt.show()

def generate_request(t, always_create=False):
    if np.random.rand() < 1/100.0 or always_create:
        request = Request(random_position(), t, store_positions[np.random.randint(0, len(store_positions)-1)])
        return request
    return None        

def match_batch(t, assignments):
    global unassigned_requests, free_deliverymen, busy_deliverymen
    drivers_matched = []
    requests_matched = []
    for i,row in enumerate(assignments):
        for j, ele in enumerate(row):
            if ele == 1:
                request = unassigned_requests[j]
                deliveryman = free_deliverymen[i]

                request.assigned_time = t
                deliveryman.req = request
                busy_deliverymen.append(deliveryman)
                drivers_matched.append(deliveryman)
                requests_matched.append(request)
    for d in drivers_matched:
        free_deliverymen.remove(d)
    for r in requests_matched:
        unassigned_requests.remove(r)

def match(t, request, deliveryman):
    global unassigned_requests, free_deliverymen, busy_deliverymen
    request.assigned_time = t
    deliveryman.req = request
    busy_deliverymen.append(deliveryman)
    free_deliverymen.remove(deliveryman)
    unassigned_requests.remove(request)

def closest(free_deliverymen, store_pos): # todo
    min_dist = 10000000
    min_deliveryman = None
    for d in free_deliverymen:
        if haversine(d.pos, store_pos) < min_dist:
            min_dist = haversine(d.pos, store_pos)
            min_deliveryman = d
    return d

def assign(t, lp=False):
    global unassigned_requests, free_deliverymen, batch_time, batch_itr
    if lp:
        batch_itr += 1
    if lp and len(free_deliverymen) > 1 and len(unassigned_requests) > 1 and batch_itr >= batch_time:
        assignments = solve_min_cost(free_deliverymen, unassigned_requests)
        match_batch(t, assignments)
        batch_itr = 0
    
    elif not lp or (batch_itr >= batch_time and len(unassigned_requests) == 1):    
        request = unassigned_requests[0]
        deliveryman = closest(free_deliverymen, request.store_pos)
        match(t, request, deliveryman)


def step(t, scat, scat1, scat2):
    global unassigned_requests, incomplete_requests, all_requests, free_deliverymen, busy_deliverymen, all_deliverymen
    r = generate_request(t)
    print(t)
    if r: 
        unassigned_requests.append(r)
        incomplete_requests.append(r)
        all_requests.append(r)

    for d in busy_deliverymen:
        if not d.req:
            free_deliverymen.append(d)
            busy_deliverymen.remove(d)

    for r in incomplete_requests:
        if r.fulfill_time != -1:
            incomplete_requests.remove(r)

    if len(unassigned_requests) > 0 and len(deliverymen) > 0:
        assign(t, lp=True)

    for d in busy_deliverymen:
        d.move(t)

    deliveyrmen_positions = [d.pos for d in all_deliverymen]
    request_positions = [r.pos for r in incomplete_requests]
    if scat:
        scat.set_offsets(deliveyrmen_positions)
        scat2.set_offsets(request_positions)


def init_requests(n):
    global unassigned_requests, incomplete_requests
    for i in range(n):
        r = generate_request(0, True)
        unassigned_requests.append(r)
        incomplete_requests.append(r)

t = 1 * 30 * 60 # 4 hours in seconds
batch_time = 10
batch_itr = 0

unassigned_requests = deque()
incomplete_requests = []
complete_requests = []
all_requests = []
busy_deliverymen = []
free_deliverymen = deliverymen
all_deliverymen = [d for d in deliverymen]

init_requests(5)
deliveyrmen_positions = [d.pos for d in deliverymen]
fig = plt.figure()
im = plt.imread("map.png")
implot = plt.imshow(im, zorder=-1, extent=[x_bound[0], x_bound[1], y_bound[0], y_bound[1]])

scat = plt.scatter(*zip(*deliveyrmen_positions))
scat1 = plt.scatter(*zip(*store_positions))
scat2 = plt.scatter([],[])

for i in range(t):
    step(i, None, None, None)

total_cost = 0
total_wait = 0
total_revenue = 0
max_wait = 0
for r in all_requests:
    if r.fulfill_time != -1:
        total_revenue += 7
        total_wait += (r.fulfill_time - r.init_time)
        max_wait = max(r.fulfill_time - r.init_time, max_wait)

for d in all_deliverymen:
    total_cost += d.total_cost

print ("Longest Wait Time: " + str(max_wait))
print ("Total Wait Time: " + str(total_wait))
print ("Total Cost: " + str(total_cost))
print ("Total Revenue: " + str(total_revenue))
print ("Total Number of Requests: " + str(len(all_requests)))
print ("Total Number of Unfulfilled Requests: " + str(len(incomplete_requests)))

# ani = animation.FuncAnimation(fig, step, frames=range(t),
                               # fargs=(scat, scat1, scat2), interval=50)
# ani.save('busy.mp4', writer="ffmpeg")
# plt.show()
