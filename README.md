# Hello Pandas + Pyomo examples

This is a minimum example that demonstrates how Pandas and Pyomo (< version 4) are combined to yield a mathematical optimisation model.

The example is a [Minimum-cost flow problem](https://en.wikipedia.org/wiki/Minimum-cost_flow_problem) formulation of the task to find the [Bacon number](https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon#Bacon_numbers) of a given actor/actress within the given [social graph](https://en.wikipedia.org/wiki/Social_graph) of Hollywood actors.

## What is it about?

Technically, the example shows how to convert the conceptually simpler, self-contained `bacon.mod` (GNU MathProg problem, including dat) into a more complex triplet of input data (`input.xlsx`), model formulation and helper functions (`bacon.py`) and a run script (`runme.py`).


## Requirements

 - Python 2.7 or 3.5 ([Anaconda](https://www.continuum.io/downloads))
 - Pandas (included in Anaconda)
 - **Either (old)**: Coopr 3.5.8787 (`pip install coopr=3.5.8787`) **or (new)** Pyomo 4 (`pip install pyomo`)
 - GLPK

 
## How to run

### Setup

    git clone https://github.com/ojdo/pyomo-3-example.git
    cd pyomo-3-example

### MathProg example (`bacon.mod`)

    glpsol -m bacon.mod
    
### Pyomo example (everything else in the folder)

    python runme.py
    
For a better learning experience, one can also launch `ipython` and execute the lines of `runme.py` step by step, inspecting the created objects with one eye on the [Pyomo Online Documentation](https://software.sandia.gov/downloads/pub/pyomo/PyomoOnlineDocs.html):

    import coopr.environ
    from coopr.opt.base import SolverFactory
    import bacon
    
    data = bacon.read_excel('input.xlsx')
    model = bacon.create_model(data)
    prob = model.create()
    optim = SolverFactory('glpk')
    result = optim.solve(prob, tee=True)
    prob.load(result)

All the work happens in the functions defined within `bacon.py`.
    

## Copyright

Copyright (C) 2015  ojdo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
