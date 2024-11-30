import dearpygui.dearpygui as dpg
import threading
import time
import importlib

import Simulator
Sim = Simulator.Simulator
reload_sim = Simulator.reload_sim

def reload():
    reload_sim()

def run_simulation(sender, data):

    # Получаем параметры симуляции из GUI
    sim_time = dpg.get_value("sim_time_input")
    sim_dt = dpg.get_value("sim_time_dt")
    # Можете добавить другие параметры
    trajectory = [[9.5,9.5]]

    # Создаем экземпляр симулятора
    simulator = Sim(sim_time=sim_time, trajectory=trajectory)  # добавьте другие параметры, если необходимо

    # Отображаем результаты на графиках
    with dpg.window(label="Path Results", pos=(250,0)):
        with dpg.plot(label="Path Plot", height=400, width=400):
            dpg.add_plot_legend()
            x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="X")
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Y")
            path_series = dpg.add_line_series(simulator.X_array, simulator.Y_array, label="Path", parent=y_axis)
            for point in simulator.walls:
                x_coordinates = []
                y_coordinates = []

                x_coordinates.append(point[0][0])
                y_coordinates.append(point[1][0])

                x_coordinates.append(point[0][1])
                y_coordinates.append(point[1][1])
                series_id = dpg.add_line_series(x_coordinates, y_coordinates, parent=y_axis)

            dpg.set_axis_limits(x_axis, 0, 11)
            dpg.set_axis_limits(y_axis, 0, 11)

    with dpg.window(label="Heading Control Results", pos=(700,0)):
        with dpg.plot(label="Heading Control Plot", height=200, width=400):
            dpg.add_plot_legend()
            x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="Time, s")
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Heading angle, rad")
            heading_series = dpg.add_line_series(simulator.time_array, simulator.heading_array, label="Heading", parent=y_axis)
            heading_control_series = dpg.add_line_series(simulator.time_array, simulator.heading_control_array, label="Heading Control", parent=y_axis)
            dpg.set_axis_limits(x_axis, 0, sim_time)
            dpg.set_axis_limits(y_axis, -3.16, 3.16)

    with dpg.window(label="Speed Control Results", pos=(700,250)):
        with dpg.plot(label="Speed Control Plot", height=200, width=400):
            dpg.add_plot_legend()
            x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="Time, s")
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Speed, m/s")
            speed_series = dpg.add_line_series(simulator.time_array, simulator.speed_array, label="Speed", parent=y_axis)
            dpg.set_axis_limits(x_axis, 0, sim_time)
            dpg.set_axis_limits(y_axis, 0, 5)

    with dpg.window(label="Speed Control Results", pos=(700,500)):
        with dpg.plot(label="Speed Control Plot", height=200, width=400):
            dpg.add_plot_legend()
            x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="Time, s")
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Coordinat, m/s")
            x_series = dpg.add_line_series(simulator.time_array, simulator.X_array, label="x coordinate", parent=y_axis)
            y_series = dpg.add_line_series(simulator.time_array, simulator.Y_array, label="y coordinate", parent=y_axis)
            dpg.set_axis_limits(x_axis, 0, sim_time)
            dpg.set_axis_limits(y_axis, -20, 40)

    # Запускаем симуляцию
    while not simulator.check_simulation_done():
        simulator.measure()
        simulator.calculate_target_data()
        simulator.calculate_control()
        simulator.check_target()
        if (not simulator.move()):
            break
        simulator.accumulate_data()

        dpg.set_value(path_series, [simulator.X_array, simulator.Y_array])
        dpg.set_value(heading_series, [simulator.time_array, simulator.heading_array])
        dpg.set_value(heading_control_series, [simulator.time_array, simulator.heading_control_array])
        dpg.set_value(speed_series, [simulator.time_array, simulator.speed_array])
        dpg.set_value(x_series, [simulator.time_array, simulator.X_array])
        dpg.set_value(y_series, [simulator.time_array, simulator.Y_array])
        time.sleep(sim_dt)

def start_simulation(sender, data):
    simulation_thread = threading.Thread(target=run_simulation, args=(sender, data))
    simulation_thread.start()

# Создаем GUI
dpg.create_context()

with dpg.window(label="Simulator Configuration", width=250, height=120):
    dpg.add_input_float(tag="sim_time_input", label="Simulation Time", default_value=200.0)
    dpg.add_input_float(tag="sim_time_dt", label="Simulation speed", default_value=0.001)
    # Можете добавить другие элементы управления для настройки параметров симуляции
    dpg.add_button(label="Start Simulation", callback=start_simulation)
    dpg.add_button(label="Reload controls", callback=reload)

dpg.create_viewport(title='Simulator', width=1000, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
