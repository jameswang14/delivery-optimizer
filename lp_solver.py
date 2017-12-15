import numpy as np
from haversine import haversine
import cvxpy as cvx
def dot(x,y):
    return sum([ xx*yy for xx,yy in zip(x,y) ]) + 0.

def solve_min_cost(drivers, requests):
    n_d = len(drivers)
    n_r = len(requests)
    if n_d <= 1 or n_r <= 1:
        return None
        
    dist = [[haversine(d.pos, r.store_pos) + haversine(r.store_pos, r.pos) for r in requests] for d in drivers]
    c = np.asarray(dist)
    x = cvx.Variable((n_d, n_r), integer=True)
    objective = cvx.Minimize(dot(c,x))
    constraints = [
            x <= 1,
            x >= 0,
            cvx.cumsum(x) <= 1,
            cvx.cumsum(x, axis=1) <= 1,
            cvx.sum(x) == min(n_r, n_d)
        ]
    p = cvx.Problem(objective, constraints)
    p.solve(solver=cvx.ECOS_BB)
    x_val = np.around(x.value).astype(int)

    return x_val
    
