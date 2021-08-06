import cellpylib as cpl
import time

# Glider
start_time = time.time()
cellular_automaton = cpl.init_simple2d(60, 60)
cellular_automaton[:, [28,29,30,30], [30,31,29,31]] = 1

# Blinker
cellular_automaton[:, [40,40,40], [15,16,17]] = 1

# Light Weight Space Ship (LWSS)
cellular_automaton[:, [18,18,19,20,21,21,21,21,20], [45,48,44,44,44,45,46,47,48]] = 1

# evolve the cellular automaton for 60 time steps
cellular_automaton = cpl.evolve2d(cellular_automaton, timesteps=60, neighbourhood='Moore',
                                  apply_rule=cpl.game_of_life_rule)
print("time to compute 60x60, 60 steps, 3 objects: ",str(time.time()-start_time),"s")


# Glider
start_time = time.time()
cellular_automaton = cpl.init_simple2d(60, 60)
cellular_automaton[:, [28,29,30,30], [30,31,29,31]] = 1

# Blinker
cellular_automaton[:, [40,40,40], [15,16,17]] = 1

# Blinker
cellular_automaton[:, [40,40,40], [15,16,17]] = 1

# Blinker
cellular_automaton[:, [40,40,40], [5,6,7]] = 1

# Blinker
cellular_automaton[:, [40,40,40], [25,26,27]] = 1

# Light Weight Space Ship (LWSS)
cellular_automaton[:, [18,18,19,20,21,21,21,21,20], [45,48,44,44,44,45,46,47,48]] = 1

# Light Weight Space Ship (LWSS)
cellular_automaton[:, [29,28,29,30,31,31,31,31,30], [45,48,44,44,44,45,46,47,48]] = 1

# Light Weight Space Ship (LWSS)
cellular_automaton[:, [39,38,39,40,41,41,41,41,40], [45,48,44,44,44,45,46,47,48]] = 1

# evolve the cellular automaton for 60 time steps
cellular_automaton = cpl.evolve2d(cellular_automaton, timesteps=60, neighbourhood='Moore',
                                  apply_rule=cpl.game_of_life_rule)
print("time to compute 60x60, 60 steps, more objects: ",str(time.time()-start_time),"s")


# Glider
start_time = time.time()
cellular_automaton = cpl.init_simple2d(60, 60)
cellular_automaton[:, [28,29,30,30], [30,31,29,31]] = 1

# Blinker
cellular_automaton[:, [40,40,40], [15,16,17]] = 1

# Light Weight Space Ship (LWSS)
cellular_automaton[:, [18,18,19,20,21,21,21,21,20], [45,48,44,44,44,45,46,47,48]] = 1

# evolve the cellular automaton for 60 time steps
cellular_automaton = cpl.evolve2d(cellular_automaton, timesteps=600, neighbourhood='Moore',
                                  apply_rule=cpl.game_of_life_rule)
print("increased length by x10")
print("time to compute 60x60, 600 steps, 3 objects: ",str(time.time()-start_time),"s")

# Glider
start_time = time.time()
cellular_automaton = cpl.init_simple2d(190, 190)
cellular_automaton[:, [28,29,30,30], [30,31,29,31]] = 1

# Blinker
cellular_automaton[:, [40,40,40], [15,16,17]] = 1

# Light Weight Space Ship (LWSS)
cellular_automaton[:, [18,18,19,20,21,21,21,21,20], [45,48,44,44,44,45,46,47,48]] = 1

# evolve the cellular automaton for 60 time steps
cellular_automaton = cpl.evolve2d(cellular_automaton, timesteps=60, neighbourhood='Moore',
                                  apply_rule=cpl.game_of_life_rule)
print("increased size by x10")
print("time to compute 190x190, 60 steps, 3 objects: ",str(time.time()-start_time),"s")



cpl.plot2d_animate(cellular_automaton)
