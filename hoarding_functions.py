
def post_design(wind_zone, post_height, k_factor_variable, return_corners, pressure, horizontal_udl):
    width = int(input(wind_zone + " post width (in mm): "))
    depth = int(input(wind_zone + " post depth (in mm): "))
    timber_grade_input = None
    while True:
        if (timber_grade_input == "c16") or (timber_grade_input == "c24"):
            break
        else:
            timber_grade_input = input("Timber grade (C16 or C24): ").casefold()
    timber_grade = {"c16": 7.42, "24": 10.50}
    timber_grade = timber_grade.get(str(timber_grade))
    print("Yay it worked!")


# height = 2.4
# r_corners = True
# peak_pressure = 0.4
# k_factor = 1
#
# B = True
# C16 = True
#
#
# post_design()


def interpolation_bs5975(height, km, town_country):
    km = float(km)
    height = float(height)

    if town_country == "town":
        shore_distance_list = (2, 10, 100)

        tab_16 = ((1.07, 1.01, 0.94),
                  (1.32, 1.25, 1.17),
                  (1.54, 1.44, 1.35),
                  (1.72, 1.62, 1.50),
                  (2.33, 2.20, 2.04),
                  (2.81, 2.65, 2.48),
                  (2.99, 2.83, 2.64),
                  (3.40, 3.24, 3.01),
                  (3.68, 3.62, 3.39),
                  (3.98, 3.98, 3.80))
    else:
        shore_distance_list = (0.1, 2, 10, 100)

        tab_16 = ((1.90, 1.60, 1.50, 1.40),
                  (2.15, 1.84, 1.73, 1.62),
                  (2.31, 2.03, 1.90, 1.78),
                  (2.43, 2.18, 2.05, 1.90),
                  (2.82, 2.65, 2.50, 2.32),
                  (3.07, 3.02, 2.85, 2.67),
                  (3.20, 3.15, 2.98, 2.78),
                  (3.42, 3.43, 3.27, 3.04),
                  (3.68, 3.68, 3.62, 3.39),
                  (3.98, 3.98, 3.98, 3.80))

    height_list = (2, 3, 4, 5, 10, 15, 20, 30, 50, 100)

    low_x = 0
    high_x = 1
    u = 0
    k = None  # index position in list i.e. k = 2 --> 10
    m = False
    while True:
        if km in shore_distance_list:
            for e in shore_distance_list:
                if km == e:
                    k = u
                    m = True
                else:
                    u += 1
            break
        elif (km > shore_distance_list[low_x]) and (km < shore_distance_list[high_x]):
            break
        elif km < shore_distance_list[0]:
            k = 0  # changed value for test
            m = True
            break
        elif km > shore_distance_list[-1]:
            k = len(shore_distance_list) - 1
            m = True
            break
        else:
            low_x += 1
            high_x += 1

    x = km
    x1 = shore_distance_list[low_x]
    x2 = shore_distance_list[high_x]
    interpolation_list = []

    # interpolate or take list entries depending on input number

    if not m:  # if m == False
        for t in range(0, 10):
            y1 = tab_16[t][low_x]
            y2 = tab_16[t][high_x]
            y = y1 + (((x - x1) / (x2 - x1)) * (y2 - y1))
            interpolation_list.append(y)
    else:
        for t in range(0, 10):
            interpolation_list.append(tab_16[t][k])

    # ------------------------------------------------------------------------------------------------------
    # height list interpolation

    low_y = 0
    high_y = 1
    u = 0
    k = None  # index position in list i.e. k = 2 --> 10
    m = False
    while True:
        if height in height_list:
            for e in height_list:
                if height == e:
                    k = u
                    m = True
                else:
                    u += 1
            break
        elif (height > height_list[low_y]) and (height < height_list[high_y]):
            break
        elif height < height_list[0]:
            k = 0  # changed value for test
            m = True
            break
        elif height > height_list[-1]:
            k = len(height_list) - 1
            m = True
            break
        else:
            low_y += 1
            high_y += 1

    # r = 0
    x = height
    x1 = height_list[low_y]
    x2 = height_list[high_y]

    # interpolate or take list entries depending on input number

    if not m:  # if m == False
        y1 = interpolation_list[low_y]
        y2 = interpolation_list[high_y]
        y = y1 + (((x - x1) / (x2 - x1)) * (y2 - y1))
        r = y
    else:
        r = interpolation_list[k]

    print("Interpolated " + town_country + " exposure factor: " + str(round(r, 3)))
    return r


def wind_bs5975(height):
    return_period = None
    while True:
        if (return_period == "1") or (return_period == "2") or (return_period == "50"):
            break
        else:
            return_period = input("Return period (1, 2 or 50 years): ")

    p_factor = {"1": 0.79, "2": 0.83, "50": 1.00}
    p_factor = p_factor.get(return_period)

    town_country = None
    while True:
        if (town_country == "town") or (town_country == "t"):
            town = True
            break
        elif (town_country == "country") or (town_country == "c"):
            town = False
            break
        else:
            town_country = input("Town or country: ").casefold()

    distance_shore = input("Distance to shoreline (in km): ")

    if town:  # if town == true
        exposure_factor = interpolation_bs5975(height, distance_shore, town_country)
    else:
        exposure_factor = interpolation_bs5975(height, distance_shore, town_country)

    basic_wind_velocity = float(input("Basic wind velocity (Vb,map): "))
    topographical_factor = float(input("Topographical factor (Twind): "))
    altitude = float(input("Site altitude (in metres): "))
    air_density = 1.225

    s_wind = topographical_factor * basic_wind_velocity * (1 + (altitude / 1000))
    peak_pressure_bs5975 = 0.5 * air_density * (p_factor ** 2) * (exposure_factor ** 2) * (s_wind ** 2) * (10 ** -3)
    return peak_pressure_bs5975, p_factor, town_country, distance_shore, exposure_factor, basic_wind_velocity,\
        topographical_factor, altitude, s_wind
