import numpy as np
import cvxpy as cvx
from Deliveryman import Deliveryman 
x_bound = (-122.460281, -122.400213)
y_bound = (37.749058, 37.802265)
# bounding box (cw from northwest): (37.756720, -122.445502), (37.808680, -122.409081)
np.random.seed(0)
num_deliverymen = 150
a_r = 5.0
num_stores = 20
num_requests = 20

delivery_positions = zip( ((x_bound[1] - x_bound[0]) * np.random.ranf(num_deliverymen) + x_bound[0] ),
                            ((y_bound[1] - y_bound[0]) * np.random.ranf(num_deliverymen) + y_bound[0] ))

deliverymen = [Deliveryman(p) for p in delivery_positions]

store_positions = [(-122.437987, 37.774938), (-122.422714, 37.79344), (-122.419367, 37.756737)]

if num_stores > 3:
    store_positions = store_positions + zip( ((x_bound[1] - x_bound[0]) * np.random.ranf(num_stores-3) + x_bound[0] ),
                            ((y_bound[1] - y_bound[0]) * np.random.ranf(num_stores-3) + y_bound[0] ))

request_positions = zip( ((x_bound[1] - x_bound[0]) * np.random.ranf(num_requests) + x_bound[0] ),
                            ((y_bound[1] - y_bound[0]) * np.random.ranf(num_requests) + y_bound[0] ))


