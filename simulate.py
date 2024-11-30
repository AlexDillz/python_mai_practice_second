from Simulator import Simulator


simulation_done = False
sim_time = 200
trajectory = [[9.5,9.5]]

main_simulator = Simulator(sim_time, trajectory)

while not simulation_done:
    main_simulator.measure()
    main_simulator.calculate_target_data()
    main_simulator.calculate_control()
    if (not main_simulator.move()):
        break
    main_simulator.check_target()
    main_simulator.accumulate_data()
    simulation_done = main_simulator.check_simulation_done()

main_simulator.plot_main_data()
