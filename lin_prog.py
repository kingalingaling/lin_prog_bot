import pulp as p
  
def lin_prog(cost_a, cost_b, profit_a, profit_b, budget, item_a='Item A', item_b='Item B', soln='Maximize'):
    # Create a LP Minimization problem
    if soln == 'Maximize':
        Lp_prob = p.LpProblem('Problem', p.LpMaximize)
    else:
        Lp_prob = p.LpProblem('Problem', p.LpMinimize)
        
    # Create problem Variables 
    x = p.LpVariable(item_a, lowBound = 0)   # Create a variable x >= 0
    y = p.LpVariable(item_b, lowBound = 0)   # Create a variable y >= 0
    # Objective Function
    Lp_prob += profit_a * x + profit_b * y   
    # Constraints:
    Lp_prob += cost_a * x + cost_b * y <= 500
    Lp_prob += x + y <= int(budget/max(cost_a, cost_b))
  
    # Display the problem
    #print(Lp_prob)
  
    status = Lp_prob.solve()   # Solver
    #print(p.LpStatus[status])   # The solution status
    
    # Printing the final solution
    return p.value(x), p.value(y), p.value(Lp_prob.objective)