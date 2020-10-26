import math

# def post_design(wind_zone, post_height, k_factor_variable, return_corners, pressure, horizontal_udl):
#     width = int(input(wind_zone + " post width (in mm): "))
#     depth = int(input(wind_zone + " post depth (in mm): "))
#     timber_grade_input = None
#     while True:
#         if (timber_grade_input == "c16") or (timber_grade_input == "c24"):
#             break
#         else:
#             timber_grade_input = input("Timber grade (C16 or C24): ").casefold()
#     timber_grade = {"c16": 7.42, "24": 10.50}
#     timber_grade = timber_grade.get(str(timber_grade))
#     print("Yay it worked!")


def interpolation(height, km, x_axis_distance_list, y_axis_height_list, table_figures_list):
    height = float(height)
    low_x = 0
    high_x = 1
    u = 0
    k = None  # index position in list i.e. k = 2 --> 10
    m = False
    while True:
        if km in x_axis_distance_list:
            for e in x_axis_distance_list:
                if km == e:
                    k = u
                    m = True
                else:
                    u += 1
            break
        elif (km > x_axis_distance_list[low_x]) and (km < x_axis_distance_list[high_x]):
            break
        elif km < x_axis_distance_list[0]:
            k = 0  # changed value for test
            m = True
            break
        elif km > x_axis_distance_list[-1]:
            k = len(x_axis_distance_list) - 1
            m = True
            break
        else:
            low_x += 1
            high_x += 1

    x = km
    x1 = x_axis_distance_list[low_x]
    x2 = x_axis_distance_list[high_x]
    interpolation_list = []

    # interpolate or take list entries depending on input number

    if not m:  # if m == False
        for t in range(0, len(table_figures_list)):
            y1 = table_figures_list[t][low_x]
            y2 = table_figures_list[t][high_x]
            y = y1 + (((x - x1) / (x2 - x1)) * (y2 - y1))
            interpolation_list.append(y)
    else:
        for t in range(0, len(table_figures_list)):
            interpolation_list.append(table_figures_list[t][k])

    # ------------------------------------------------------------------------------------------------------
    # height list interpolation

    low_y = 0
    high_y = 1
    print(height)
    print(y_axis_height_list)
    u = 0
    k = None  # index position in list i.e. k = 2 --> 10
    m = False
    while True:
        if height in y_axis_height_list:
            for e in y_axis_height_list:
                if height == e:
                    k = u
                    m = True
                else:
                    u += 1
            break
        elif (height > y_axis_height_list[low_y]) and (height < y_axis_height_list[high_y]):
            break
        elif height < y_axis_height_list[0]:
            k = 0  # changed value for test
            m = True
            break
        elif height > y_axis_height_list[-1]:
            k = len(y_axis_height_list) - 1
            m = True
            break
        else:
            low_y += 1
            high_y += 1

    # r = 0
    x = height
    x1 = y_axis_height_list[low_y]
    x2 = y_axis_height_list[high_y]

    # interpolate or take list entries depending on input number

    if not m:  # if m == False
        y1 = interpolation_list[low_y]
        y2 = interpolation_list[high_y]
        y = y1 + (((x - x1) / (x2 - x1)) * (y2 - y1))
        interpolated_result = y
    else:
        interpolated_result = interpolation_list[k]

    return interpolated_result


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
    distance_shore = float(distance_shore)

    shore_distance_list_town = (2, 10, 100)

    tab_16_town = ((1.07, 1.01, 0.94),
                   (1.32, 1.25, 1.17),
                   (1.54, 1.44, 1.35),
                   (1.72, 1.62, 1.50),
                   (2.33, 2.20, 2.04),
                   (2.81, 2.65, 2.48),
                   (2.99, 2.83, 2.64),
                   (3.40, 3.24, 3.01),
                   (3.68, 3.62, 3.39),
                   (3.98, 3.98, 3.80))

    shore_distance_list_country = (0.1, 2, 10, 100)

    tab_16_country = ((1.90, 1.60, 1.50, 1.40),
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

    if town:  # if town == true
        exposure_factor = interpolation(height, distance_shore, shore_distance_list_town, height_list, tab_16_town)
        # exposure_factor = interpolation_bs5975(height, distance_shore, town_country)
    else:
        exposure_factor = interpolation(height, distance_shore, shore_distance_list_country, height_list,
                                        tab_16_country)
        # exposure_factor = interpolation_bs5975(height, distance_shore, town_country)

    basic_wind_velocity = float(input("Basic wind velocity (Vb,map): "))
    topographical_factor = float(input("Topographical factor (Twind): "))
    altitude = float(input("Site altitude (in metres): "))
    air_density = 1.225

    s_wind = topographical_factor * basic_wind_velocity * (1 + (altitude / 1000))
    peak_pressure_bs5975 = 0.5 * air_density * (p_factor ** 2) * (exposure_factor ** 2) * (s_wind ** 2) * (10 ** -3)
    print("Peak dynamic pressure = " + str(round(peak_pressure_bs5975, 3)))
    return peak_pressure_bs5975, p_factor, town_country, distance_shore, exposure_factor, basic_wind_velocity,\
        topographical_factor, altitude, s_wind


def wind_bs6399(height):
    building_type_factor = None
    while True:
        if (building_type_factor == "0.5") or (building_type_factor == "1") or (building_type_factor == "2") or \
                (building_type_factor == "4") or (building_type_factor == "8"):
            break
        else:
            building_type_factor = input("Building type factor; Kb (0.5, 1, 2, 4 or 8): ")
    building_type_factor = float(building_type_factor)

    dynamic_augmentation_factor = (building_type_factor * ((float(height) / 0.1) ** 0.75)) / \
                                  (800 * math.log10(float(height) / 0.1))
    print("Dynamic augmentation factor, Cr = " + str(round(dynamic_augmentation_factor, 2)))

    basic_wind_velocity = float(input("Basic wind velocity (Vb,map): "))

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

    hr = float(height)  # maximum height of building above ground level

    # Tables for fetch factor (Sc), turbulence factor (St), fetch adjustment factor (Tc) & turbulence adjustment
    # factor (Tt). Factors are then interpolated using the interpolation() function.

    effective_height = (2, 5, 10, 15, 20, 30, 50, 100, 200, 300)

    upwind_sea_to_site = (0.1, 0.3, 1, 3, 10, 30, 100)

    upwind_town_edge_to_site = (0.1, 0.3, 1, 3.0, 10, 30)

    sc_table = ((0.873, 0.840, 0.812, 0.792, 0.774, 0.761, 0.723),
                (1.06, 1.02, 0.990, 0.966, 0.944, 0.928, 0.882),
                (1.21, 1.17, 1.13, 1.10, 1.07, 1.06, 1.00),
                (1.28, 1.25, 1.21, 1.18, 1.15, 1.13, 1.08),
                (1.32, 1.31, 1.27, 1.23, 1.21, 1.19, 1.13),
                (1.39, 1.39, 1.35, 1.31, 1.28, 1.26, 1.20),
                (1.47, 1.47, 1.46, 1.42, 1.39, 1.36, 1.30),
                (1.59, 1.59, 1.59, 1.57, 1.54, 1.51, 1.43),
                (1.74, 1.74, 1.74, 1.73, 1.70, 1.67, 1.59),
                (1.84, 1.84, 1.84, 1.83, 1.82, 1.78, 1.70))

    st_table = ((0.203, 0.215, 0.215, 0.215, 0.215, 0.215, 0.215),
                (0.161, 0.179, 0.192, 0.192, 0.192, 0.192, 0.192),
                (0.137, 0.154, 0.169, 0.175, 0.178, 0.178, 0.178),
                (0.131, 0.141, 0.156, 0.167, 0.171, 0.171, 0.171),
                (0.127, 0.132, 0.145, 0.157, 0.163, 0.164, 0.166),
                (0.120, 0.122, 0.132, 0.145, 0.155, 0.159, 0.159),
                (0.112, 0.113, 0.117, 0.125, 0.135, 0.145, 0.149),
                (0.097, 0.100, 0.100, 0.100, 0.110, 0.120, 0.132),
                (0.075, 0.075, 0.075, 0.078, 0.083, 0.093, 0.111),
                (0.065, 0.065, 0.065, 0.067, 0.068, 0.080, 0.092))

    tc_table = ((0.695, 0.653, 0.619, 0.596, 0.576, 0.562),
                (0.846, 0.795, 0.754, 0.725, 0.701, 0.684),
                (0.929, 0.873, 0.828, 0.796, 0.770, 0.751),
                (0.969, 0.911, 0.863, 0.831, 0.803, 0.783),
                (0.984, 0.935, 0.886, 0.853, 0.824, 0.804),
                (0.984, 0.965, 0.915, 0.880, 0.851, 0.830),
                (0.984, 0.984, 0.947, 0.912, 0.881, 0.859),
                (0.984, 0.984, 0.984, 0.948, 0.917, 0.894),
                (0.984, 0.984, 0.984, 0.980, 0.947, 0.924),
                (0.984, 0.984, 0.984, 0.984, 0.964, 0.940))

    tt_table = ((1.92, 1.93, 1.93, 1.93, 1.93, 1.93),
                (1.41, 1.60, 1.63, 1.63, 1.63, 1.63),
                (1.16, 1.34, 1.50, 1.52, 1.52, 1.52),
                (1.04, 1.22, 1.38, 1.47, 1.47, 1.47),
                (1.00, 1.17, 1.35, 1.44, 1.45, 1.45),
                (1.00, 1.06, 1.21, 1.33, 1.43, 1.43),
                (1.00, 1.00, 1.12, 1.24, 1.38, 1.42),
                (1.00, 1.00, 1.00, 1.14, 1.28, 1.38),
                (1.00, 1.00, 1.00, 1.07, 1.19, 1.31),
                (1.00, 1.00, 1.00, 1.04, 1.14, 1.24))

    if town:  # if town == True
        ho = float(input("Average height of surrounding building rooftops (in metres): "))
        xo = float(input("Upwind spacing of surrounding buildings (in metres): "))
        if xo <= ho:
            hd = 0.8 * ho
        elif (xo > (2 * ho)) and (xo < (6 * xo)):
            hd = (1.2 * ho) - (0.2 * xo)
        else:  # xo >= 6ho
            hd = 0

        # determine effective height of building
        he1 = hr - hd
        he2 = 0.4 * hr
        if he1 >= he2:
            he = he1
        else:
            he = he2

        print("Topography not considered in calculation!")
        altitude = float(input("Site altitude (in metres): "))
        sa = 1 + (0.001 * altitude)
        direction_factor = float(input("Direction factor; Sd: "))
        seasonal_factor = float(input("Seasonal factor; Ss: "))

        return_period = None
        while True:
            if (return_period == "1") or (return_period == "2") or (return_period == "50"):
                break
            else:
                return_period = input("Return period (1, 2 or 50 years): ")

        p_factor = {"1": 0.79, "2": 0.83, "50": 1.00}
        p_factor = p_factor.get(return_period)
        print("Probability factor = " + str(p_factor))

        site_wind_speed = basic_wind_velocity * sa * direction_factor * seasonal_factor * p_factor
        print("Site wind speed = " + str(round(site_wind_speed, 3)))
        upwind_distance_sea = float(input("Upwind distance from sea to site; dsea (in km): "))
        upwind_distance_town = float(input("Upwind distance from edge of town to site; dsite (in km): "))

        interpolated_sc = interpolation(he, upwind_distance_sea, upwind_sea_to_site, effective_height, sc_table)
        interpolated_st = interpolation(he, upwind_distance_sea, upwind_sea_to_site, effective_height, st_table)
        interpolated_tc = interpolation(he, upwind_distance_town, upwind_town_edge_to_site, effective_height,
                                        tc_table)
        interpolated_tt = interpolation(he, upwind_distance_town, upwind_town_edge_to_site, effective_height,
                                        tt_table)

        print("Interpolated fetch factor; Sc: " + str(round(interpolated_sc, 3)))
        print("Interpolated turbulence factor; St: " + str(round(interpolated_st, 3)))
        print("Interpolated fetch adjustment factor; Tc: " + str(round(interpolated_tc, 3)))
        print("Interpolated turbulence adjustment factor; Tt: " + str(round(interpolated_tt, 3)))

        terrain_building_factor = interpolated_sc * interpolated_tc * (1 + (3.44 * interpolated_st * interpolated_tt))
        print("Terrain and building factor: " + str(terrain_building_factor))
        effective_wind_speed = site_wind_speed * terrain_building_factor
        print("Effective wind speed: " + str(effective_wind_speed))
        dynamic_pressure = 0.613 * (effective_wind_speed ** 2)
        print("Dynamic pressure = " + str(round(dynamic_pressure, 3)) + "kN/m^2")
    else:
        upwind_distance_town = 0
        interpolated_tc = 0
        interpolated_tt = 0
        ho = 0
        xo = 0
        hd = 0
        he = height  # effective height of building equal to actual height
        print("Topography not considered in calculation!")
        altitude = float(input("Site altitude (in metres): "))
        sa = 1 + (0.001 * altitude)
        direction_factor = float(input("Direction factor; Sd: "))
        seasonal_factor = float(input("Seasonal factor; Ss: "))

        return_period = None
        while True:
            if (return_period == "1") or (return_period == "2") or (return_period == "50"):
                break
            else:
                return_period = input("Return period (1, 2 or 50 years): ")

        p_factor = {"1": 0.79, "2": 0.83, "50": 1.00}
        p_factor = p_factor.get(return_period)
        print("Probability factor = " + str(p_factor))

        site_wind_speed = basic_wind_velocity * sa * direction_factor * seasonal_factor * p_factor
        print("Site wind speed = " + str(round(site_wind_speed, 3)))

        upwind_distance_sea = float(input("Upwind distance from sea to site; dsea (in km): "))
        interpolated_sc = interpolation(he, upwind_distance_sea, upwind_sea_to_site, effective_height, sc_table)
        interpolated_st = interpolation(he, upwind_distance_sea, upwind_sea_to_site, effective_height, st_table)
        print()
        print("Interpolated fetch factor; Sc: " + str(round(interpolated_sc, 3)))
        print("Interpolated turbulence factor; St: " + str(round(interpolated_st, 3)))
        terrain_building_factor = interpolated_sc * (1 + (3.44 * interpolated_st))
        print("Terrain and building factor: " + str(round(terrain_building_factor, 3)))
        effective_wind_speed = site_wind_speed * terrain_building_factor
        print("Effective wind speed: " + str(round(effective_wind_speed, 3)))
        dynamic_pressure = 0.613 * (effective_wind_speed ** 2)
        print("Dynamic pressure = " + str(round(dynamic_pressure, 3)) + "kN/m^2")
    return p_factor, town, upwind_distance_sea, upwind_distance_town, \
        basic_wind_velocity, altitude, height, building_type_factor, dynamic_augmentation_factor, he, hd, sa, \
        interpolated_sc, interpolated_st, interpolated_tc, interpolated_tt, ho, xo, terrain_building_factor, \
        effective_wind_speed, direction_factor, seasonal_factor, site_wind_speed, dynamic_pressure


def wind_print_bs5975(doc_name, wind_pressure, probability_factor, town_country, shore_distance, exposure_factor,
                      basic_wind_velocity, topographical_factor, altitude, s_wind):
    file = doc_name
    text = "Surface Wind Load (BS 5975):\n\n"
    text += "Probability factor; cprob = " + str(probability_factor) + "\n"
    text += "Site in town or country = " + town_country + "\n"
    text += "Distance from shoreline = " + str(shore_distance) + "km\n"
    text += "Combined exposure factor; ce = " + str(exposure_factor) + "\n"
    text += "Basic wind velocity; vb,map = " + str(basic_wind_velocity) + "\n"
    text += "Topographical factor; Twind = " + str(topographical_factor) + "\n"
    text += "Site altitude; A = " + str(altitude) + "m\n"
    text += "Air density; Ad = 1.225kg/m^3\n\n"
    text += "Swind = Twind * vb,map * (1 + (A / 1000)) = " + str(s_wind) + "\n\n"
    text += "Peak velocity pressure; qb = 0.5 * Ad * (cprob)^2 * (ce)^2 * (Swind)^2 = " + str(wind_pressure) + "kN/m^2"
    file.write(text)


def wind_print_bs6399(doc_name, probability_factor, town, shore_distance, town_edge_distance,
                      basic_wind_speed, altitude, height, building_type_factor, dynamic_augmentation_factor,
                      effective_height_of_building, displacement_height, site_altitude_factor, fetch_factor,
                      turbulence_factor, fetch_adjustment_factor, turbulence_adjustment_factor, average_height_rooftops,
                      spacing_surrounding_buildings, terrain_building_factor, effective_wind_speed, direction_factor,
                      seasonal_factor, site_wind_speed, dynamic_pressure):
    # Look into town_country == "town". This may break as will also accept "t". Change to town == True instead.
    file = doc_name
    text = "Surface Wind Load (BS 6399):\n\n"
    text += "Actual height of building above ground; H = " + str(height) + "\n"
    text += "Building type factor; Kb = " + str(building_type_factor) + "\n"
    text += "Dynamic augmentation factor: \n"
    text += "\tCr = (Kb * (H / ho)^0.75) / (800 * log(H / ho)) = " + str(round(dynamic_augmentation_factor, 3)) + "\n"
    text += "Maximum height of building above ground level; Hr = " + str(height) + "\n"
    if town:
        text += "Site in town or country = town\n"
        text += "Average height of roof tops of surrounding buildings; Ho = " + str(average_height_rooftops) + "\n"
        text += "Upwind spacing of surrounding buildings; Xo = " + str(spacing_surrounding_buildings) + "\n"
        text += "Displacement height:\n"
        text += "\tif (Xo <= 2Ho) then Hd = 0.8Ho\n"
        text += "\tif (2Ho < Xo < 6Ho) then Hd = (1.2Ho - 0.2Xo)\n"
        text += "\tif (Xo >= 6Ho) then Hd = 0\n"
        text += "\tHd = " + str(round(displacement_height, 3)) + "\n"
        text += "Effective height of building:\n"
        text += "\tHe = maximum of (Hr - Hd) & 0.4Hr = " + str(round(effective_height_of_building, 3)) + "\n"
        text += "Basic wind speed; Vb = " + str(basic_wind_speed) + "m/s\n"
        text += "Site altitude; Sa = " + str(altitude) + "m\n"
        text += "Site altitude factor = 1 + (0.001 * Sa) = " + str(site_altitude_factor) + "\n"
        text += "Direction factor; Sd = " + str(direction_factor) + "\n"
        text += "Seasonal factor; Ss = " + str(seasonal_factor) + "\n"
        text += "Probability factor; Sp = " + str(probability_factor) + "\n"
        text += "Site wind speed; Vs = Vb * Sa * Sd * Ss * Sp = " + str(round(site_wind_speed, 3)) + "m/s\n"
        text += "Upwind distance from sea to site; dsea = " + str(shore_distance) + "km\n"
        text += "Upwind distance from edge of town to site; dtown = " + str(town_edge_distance) + "km\n"
        text += "Table 22 fetch factor; Sc = " + str(round(fetch_factor, 3)) + "\n"
        text += "Table 22 turbulence factor; St = " + str(round(turbulence_factor, 3)) + "\n"
        text += "Table 23 fetch adjustment factor; Tc = " + str(round(fetch_adjustment_factor, 3)) + "\n"
        text += "Table 23 turbulence adjustment factor; Tt = " + str(round(turbulence_adjustment_factor, 3)) + "\n"
        text += "Terrain and building factor; Sb = Sc * Tc * (1 + 3.44 * St * Tt) = " \
                + str(round(terrain_building_factor, 3)) + "\n"
        text += "Effective wind speed; Ve = Vs * Sb = " + str(round(effective_wind_speed, 2)) + "m/s\n"
        text += "Dynamic pressure; qs = 0.613kg/m^3 * Ve^2 * 10^-3 = " \
                + str(round((dynamic_pressure * (10 ** -3)), 3)) + "kN/m^2\n"
    else:  # site in country
        text += "Site in town or country = country\n"
        text += "Effective height of building; He = Hr = " + str(effective_height_of_building) + "m\n"
        text += "Basic wind speed; Vb = " + str(basic_wind_speed) + "m/s\n"
        text += "Site altitude; Sa = " + str(altitude) + "m\n"
        text += "Site altitude factor = 1 + (0.001 * Sa) = " + str(site_altitude_factor) + "\n"
        text += "Direction factor; Sd = " + str(direction_factor) + "\n"
        text += "Seasonal factor; Ss = " + str(seasonal_factor) + "\n"
        text += "Probability factor; Sp = " + str(probability_factor) + "\n"
        text += "Site wind speed; Vs = Vb * Sa * Sd * Ss * Sp = " + str(round(site_wind_speed, 3)) + "m/s\n"
        text += "Upwind distance from sea to site; dsea = " + str(shore_distance) + "km\n"
        text += "Table 22 fetch factor; Sc = " + str(round(fetch_factor, 3)) + "\n"
        text += "Table 22 turbulence factor; St = " + str(round(turbulence_factor, 3)) + "\n"
        text += "Terrain and building factor; Sb = Sc * (1 + 3.44 * St) = " + str(round(terrain_building_factor, 3)) \
                + "\n"
        text += "Effective wind speed; Ve = Vs * Sb = " + str(round(effective_wind_speed, 3)) + "m/s\n"
        text += "Dynamic pressure; qs = 0.613kg/m^3 * Ve^2 * 10^-3 = " \
                + str(round((dynamic_pressure * (10 ** -3)), 3)) + "kN/m^2\n"
    file.write(text)
