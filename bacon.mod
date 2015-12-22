set actor;
set movie;
set plays_in within actor cross movie;

set plays_with within actor cross actor := setof{
    (a1, m) in plays_in, (a2, m) in plays_in: a1 <> a2
} (a1, a2); 

## alternative syntax
#set plays_with within actor cross actor := { 
#    a1 in actor, a2 in actor: 
#    a1 <> a2 and exists{m in movie} (
#        (a1, m) in plays_in and 
#        (a2, m) in plays_in
#    ) 
#};

param sink_source{actor}, default 0;

var flow{actor, actor} >= 0;

minimize obj: sum{a1 in actor, a2 in actor} flow[a1, a2];

s.t. flow_conservation{a in actor}:
    sum{p in actor: (p, a) in plays_with} flow[p, a] -
    sum{s in actor: (a, s) in plays_with} flow[a, s] +
    sink_source[a] = 0;

solve;

printf "Distance: %i\n", obj;
printf{a1 in actor, a2 in actor : flow[a1,a2] <> 0}: "%s -> %s\n", a1, a2; 

data;

# source: http://www.behindthename.com/random/
set actor := "Lakeshia Westerberg" 
             "Rajab Heintze"
             "Oceanus Yap"
             "Tiger Probert" 
             "Kevin Bacon";

# source: http://moviebooknamegenerator.blogspot.de/
set movie := "The fast brat of Paris"
             "The young fly"
             "The red beard"
             "Farm of ribbons";
set plays_in := ("Lakeshia Westerberg", "The fast brat of Paris") 
                    ("Oceanus Yap", "The fast brat of Paris") 
                ("Lakeshia Westerberg", "The young fly") 
                    ("Rajab Heintze", "The young fly") 
                ("Rajab Heintze", "The red beard") 
                    ("Oceanus Yap", "The red beard") 
                    ("Tiger Probert", "The red beard") 
                ("Tiger Probert", "Farm of ribbons") 
                    ("Kevin Bacon", "Farm of ribbons");

param sink_source := ["Lakeshia Westerberg"] 1, 
                     ["Kevin Bacon"] -1;       

end;
