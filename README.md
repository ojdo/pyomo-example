# Hello Pandas + Pyomo examples

This is a minimum example that demonstrates how Pandas and Pyomo (< version 4) are combined to yield a mathematical optimisation model.

The example is a [Minimum-cost flow problem](https://en.wikipedia.org/wiki/Minimum-cost_flow_problem) formulation of the task to find the [Bacon number](https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon#Bacon_numbers) of a given actor/actress within the given [social graph](https://en.wikipedia.org/wiki/Social_graph) of Hollywood actors.

## What is it about?

Technically, the example shows how to convert the conceptually simpler, self-contained `bacon.mod` (GNU MathProg problem, including dat) into a more complex triplet of input data (`input.xlsx`), model formulation and helper functions (`bacon.py`) and a run script (`runme.py`).


## Requirements

 - Python 2.7 ([Anaconda](https://www.continuum.io/downloads))
 - Pandas (included in Anaconda)
 - Coopr 3.5.8787: `pip install coopr=3.5.8787`
 

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
