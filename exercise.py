import math

previous_angular_rate = 0

def calculate_target_data(x1, y1, x2, y2, heading):

    distanse = 1

    # Угол между направлением робота и конечной точкой
    heading_diff = math.atan2((y2-y1),(x2-x1))-heading

    return [heading_diff, distanse]

def calculate_control(heading_diff, distanse, distances):
    left_dist, front_dist, right_dist = distances

    min_distR = right_dist - left_dist
    min_distL = left_dist - right_dist

    if right_dist > 1 and left_dist > 1:
        # Если возможен поворот
        angular_rate = 2 * heading_diff
        velocity = front_dist / 2

    elif min_distR > 0.3:
        # Если робот слишком близко к левой стороне
        angular_rate = -abs(min_distR) * 0.5
        velocity = front_dist * 0.3

    elif min_distL > 0.2:
        # Если робот слишком близко к правой стенке
        angular_rate = abs(min_distR) * 0.5
        velocity = front_dist * 0.3

    else:
        # Если достаточное расстояние до всех стенок
        angular_rate = 0
        velocity = front_dist * 0.4

    if left_dist > 1 and front_dist > 1 and right_dist < 1:
        # Условие если есть путь вперед и налево
        angular_rate = -right_dist * 0.3
        velocity = front_dist * 0.4
    elif right_dist > 1 and front_dist > 1 and left_dist < 1:
        # Условие если есть путь вперед и направо
        angular_rate = left_dist * 0.3
        velocity = front_dist * 0.4
    if front_dist < 0.3:
        # Условие если робот слишком близко подъехал к передней стенке
        angular_rate = 3 * heading_diff
        velocity = 0
    return velocity, angular_rate

def check_target_reached(x1, y1, x2, y2):
    if math.sqrt((x2 - x1)**2 + (y2 - y1)**2) < 0.5:
        # Дошли ли до точки
        print('Закрой симуляцию, если я дошел хотя бы 8 из 10 раз')
        print('На единицу ниже не смотри вообще')
        return True
    else:
        print('Ща')
        return False