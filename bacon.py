try:
    # Example for Python 2.7 with Coopr 3.5.8787
    import coopr.pyomo as pyomo
except ImportError:
    # Pyomo 4
    import pyomo.environ as pyomo
import pandas as pd

def read_excel(filename):
    """Read special Excel spreadsheet to input dict. 
    
    Args:
        filename: path to a spreadsheet file
        
    Returns
        dict of DataFrames, to be passed to create_model()
    """
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
    """Create Pyomo ConcreteModel
    """
    m = pyomo.ConcreteModel()
    m.name = 'BACON'
    m.data = data
    
    # pre-processing
    social_network = get_social_network(m.data['actor-film']) 
        
    # SETS
    # elementary sets, e.g.
    #    actor = {'Actor A', 'Actor B', 'Actor C'}
    #    film = {'Film 1', 'Film 2', 'Film 3', 'Film 4'}
    m.actor = pyomo.Set(initialize=m.data['actor'].index.unique())
    m.film = pyomo.Set(initialize=m.data['film'].index.unique())
    
    # tuple sets, e.g.
    #   plays_in = {('Actor A', 'Film 2'), ...}
    #   plays_with = {('Actor A', 'Actor B'), ...}
    m.plays_in = pyomo.Set(within=m.actor * m.film,
                           initialize=m.data['actor-film'].index)

    m.plays_with = pyomo.Set(within=m.actor * m.actor,
                             initialize=social_network)

    # PARAMS
    # not needed in this way of doing things. Instead, one can simply use the
    # DataFrames directly within the constraint function. See fc_rule and 
    # how it accesses the `sink-source` column from input.xlsx.
    
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


# OBJECTIVE
def obj_rule(m):
    return pyomo.summation(m.flow)  # == short for sum{a1,a2} flow[a1,a2]



# CONSTRAINTS
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




# HELPER FUNCTIONS
def get_social_network(actor_film_table):
    social_network = []  # list of (actor, actor) pairs together in a film
    for film, group in actor_film_table.reset_index().groupby('Film'):
        all_actors = group['Actor'].unique()
        
        for a1, a2 in pd.MultiIndex.from_product([all_actors, all_actors]):
            if a1 != a2:  # only  include distinct
                social_network.append((a1, a2))
    return social_network
