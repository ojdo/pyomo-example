# Example for Python 2.7 with Coopr.Pyomo (i.e. Pyomo before version 4)
# 
import coopr.pyomo as pyomo
import pandas as pd


def read_excel(filename):
    with pd.ExcelFile(filename) as xls:
        actor = xls.parse('Actor').set_index('Name')
        film = xls.parse('Film').set_index('Title')
        actor_film = xls.parse('Actor-Film').set_index(['Actor', 'Film'])
        
    data = {
        'actor': actor,
        'film': film,
        'actor-film': actor_film}

    return data


def create_model(data):
    m = pyomo.ConcreteModel()
    m.name = 'BACON'
    
    # allow referencing the input DataFrames from within the model object.
    # Technical reason: within the constraint rule functions, one then could
    # simply access the attribute values using `m.actor.loc[name, 'age']`
    # http://pandas.pydata.org/pandas-docs/stable/10min.html#selection-by-label
    m.data = data
    
    # pre-processing
    # (actually, this should be moved to a dedicated function and then only be
    # called from here. But, I'm lazy..)
    
    social_network = []  # list of (actor, actor) pairs together in a film
    for film, group in m.data['actor-film'].reset_index().groupby('Film'):
        all_actors = group['Actor'].unique()
        
        for a1, a2 in pd.MultiIndex.from_product([all_actors, all_actors]):
            if a1 != a2:  # only  include distinct
                social_network.append((a1, a2))
    
    # GAMS-like stuff ahead
    # (actually, this could/should might be better be split as well once it
    # gets to length of an urbs-style model)
    
    # SETS
    # elementary sets, e.g.
    #    actor = {'Actor A', 'Actor B', 'Actor C'}
    #    film = {'Film 1', 'Film 2', 'Film 3', 'Film 4'}
    #
    # Nothing interesting here, just copying the index
    # labels (i.e. actor names and film titles) into pyomo Set objects
    m.actor = pyomo.Set(initialize=m.data['actor'].index.unique())
    m.film = pyomo.Set(initialize=m.data['film'].index.unique())
    
    # tuple sets
    m.plays_in = pyomo.Set(within=m.actor * m.film,
                           initialize=m.data['actor-film'].index)

    m.plays_with = pyomo.Set(within=m.actor * m.actor,
                             initialize=social_network)

    # PARAMS
    # not needed in this way of doing things. Instead, one can simply use the
    # DataFrames directly within the constraint function without having copied
    # around the values
    
    # VARIABLES
    m.flow = pyomo.Var(m.actor, m.actor,  # domain (actor1, actor2)
                       within=pyomo.NonNegativeReals)  # flow >= 0
    
    
    # OBJECTIVE
    m.obj = pyomo.Objective(rule=obj_rule,  # cf. `def obj_rule` below
                            sense=pyomo.minimize)  # or up or down?
    
    # CONSTRAINTS
    m.flow_conservation = pyomo.Constraint(m.actor,  # forall a in m.actor 
                                           rule=fc_rule)  # this must hold
    
    return m

# the rule functions must be placed outside the create_model function, so that
# pickling (storing) the whole model works automagically works

# OBJECTIVE RULE FUNCTION
def obj_rule(m):
    return pyomo.summation(m.flow)  # == short for sum{a1,a2} flow[a1,a2]
    
def fc_rule(m, a):  # a == actor (from the `forall a in m.actor` line above)
    flow_balance = 0
    for (a1, a2) in m.plays_with:
        if a1 == a:
            flow_balance += m.flow[a1, a2]
        if a2 == a:
            flow_balance -= m.flow[a1, a2]
    
    # HA, finally an example for accessing a parameter value!
    flow_balance += m.data['actor'].loc[a, 'sink-source']
    
    return flow_balance == 0
