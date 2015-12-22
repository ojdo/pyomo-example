try:
    # Coopr 3.5.8787 (old)
    import coopr.environ
    from coopr.opt.base import SolverFactory
except ImportError:
    # Pyomo 4 (new)
    import pyomo.environ
    from pyomo.opt import SolverFactory

import bacon

input_filename = 'input.xlsx'

data = bacon.read_excel(input_filename)
model = bacon.create_model(data)
prob = model.create()
optim = SolverFactory('glpk')
result = optim.solve(prob, tee=True)
prob.load(result)

# result statistics
print(result)

# all variables
prob.display()

# custom print example
for actors in prob.flow:
    if prob.flow[actors].value > 0: 
        print("{} -> {}".format(actors[0], actors[1]))

