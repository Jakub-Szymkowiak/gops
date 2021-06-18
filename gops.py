import numpy as np
from scipy.optimize import linprog

# we try to stick to the notation used in "Computer Solution to the GOPS"

# number of cards used to play 
N = 6

# no point in running N > 6
if N > 6:
	N = 6

# initial state of the game
init_state = {
    "V": list(range(1,N+1)), # cards in player one's hand
    "Y": list(range(1,N+1)), # cards in player two's hand
    "P": list(range(1,N+1))  # cards in the deck
}

# we keep track of already calcualted arrangements of cards
calculated = set()
results = dict()

# convert state to string, so we can use it as a key in a hashmap
# we want to use the fact that f(V,Y,P) = f(Y,V,P)
# this is why why need the symmetric variant 
def state_string (state, symmetric = False):
    if symmetric == False:
        return "V" + str(state["V"]) + "Y" + str(state["Y"]) + "P" + str(state["P"])
    else:
        return  "Y" + str(state["Y"]) + "V" + str(state["V"]) + "P" + str(state["P"])

def f (state):
    # if there are no cards then return 0
    # we also use the fact that f(V,V,P) = 0
    if not state["P"] or state["V"] == state["Y"]:
        return 0

    state_str = state_string(state)

    # checking if the arrangment was consdered before
    if state_str in calculated:
        return results[state_str]
    else:
        state_str_symm = state_string(state, symmetric=True)
        if state_str_symm in calculated:
            return results[state_str_symm]
        else:
            calculated.add(state_str)

            s = 0
            for k in range(0, len(state["P"])):
                s += f_k(state, k)

            val = 1/len(state["P"])*s 
            results[state_str] = val
            return val
        

def f_k (state, k): 
    return calc_game_value(create_payoff_matrix(state, k))[0]

def new_state (state, i, j, k):
    return {
        "V": state["V"][:i] + state["V"][i+1:],
        "Y": state["Y"][:j] + state["Y"][j+1:],
        "P": state["P"][:k] + state["P"][k+1:]
    }

def create_payoff_matrix(state, k):
    # formula for a single element X_ij of the matrix
    x = lambda i, j: state["P"][k]*np.sign(state["V"][i]-state["Y"][j]) + f(new_state(state, i, j, k))

    n = len(state["P"])

    # filling the matrix
    X = np.empty(shape=(n,n))
    for i in range(0,n):
        for j in range(0,n):
            X[i,j] = x(i,j)
    
    return X

# solving the matrix game
def calc_game_value (X):
    n = X.shape[0]

    # we need to transpose the array
    X = np.transpose(X)

    # the inequilty constraint matrix is negative
    # because we need to change the inequilty sign
    X = np.append(-X, np.ones(shape=(n,1)), axis=1)

    # inequilty constraint vector
    bub = [0]*n

    # the coefficients of the objective function are negative
    # because scipy.optimize.linprog always solves the minimization problem
    # and we need to maximize
    c = [0]*n 
    c.append(-1)
    c = np.array(c)

    # our only equilty constraint is that the sum of the coefficients is equal to one
    # because we are looking for a probability distribution
    Aeq = [1]*n 
    Aeq.append(0)
    Aeq = np.array(Aeq)
    Aeq = Aeq.reshape(1,n+1)

    beq = 1

    # every coefficient except for the value of the game must be nonnegative
    bounds = [(0,None)]*n 
    bounds.append((None,None))

    result = linprog(c, A_ub=X, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=bounds)

    # we have to change the sign of the optimal value
    # because the sign of the objective function has been flipped before
    return (-result.fun, result.x[:-1])

# calculates strategy for a given upcard
def first_move_strategy (upcard):
    upcard -= 1
    M = create_payoff_matrix(init_state, upcard)
    return calc_game_value(M)[1]

# construct the results table
table = np.empty(shape=(N,N))
for i in init_state["P"]:
    table[:,i-1] = first_move_strategy(i)

# and print it
np.set_printoptions(precision=4, suppress=True)
print(table)

# save results to "gopsN.csv"
np.savetxt(f"gops{N}.csv", table, delimiter=",")