import hoarding_functions

test = "test2.txt"

# file = open("Temporary Hoarding Calculation Pack.txt", "w")
file = open(test, "w")

print("-" * 50, "\nTemporary Site Hoarding Designer v0.0.3", "\n", "-" * 50, sep="")

# Project details
# project_name = input("Project name: ")
# client_name = input("Client name: ")
# job_number = input("Job number: ")
# temp_ref = input("Temporary works reference: ")
# designer_initials = input("Designer initials: ")
# checker_initials = input("Checker initials: ")
# approver_initials = input("Approver initials: ")
# add_L1 = input("First line of address: ")
# add_L2 = input("Second line of address: ")
# add_L3 = input("Third line of address: ")
# add_L4 = input("Fourth line of address: ")
# add_L5 = input("Post code: ")
# print()

# Loading details
height = float(input("Hoarding height (in metres): "))

print()
print("Crowd loading examples: \nHigh --> Stadium (1.5kN/m)\nMedium --> High traffic areas (0.74kN/m)"
      "\nLow --> Low traffic areas (0.37kN/m)\nNone --> No public access (0.0kN/m)\n", sep="")

crowd_load = None
while True:
    if (crowd_load == "high") or (crowd_load == "medium") or (crowd_load == "low") or (crowd_load == "none"):
        break
    else:
        crowd_load = input("Crowd loading severity (high, medium, low, none): ").casefold()

h_udl = {"high": 1.5, "medium": 0.74, "low": 0.37, "none": 0}
h_udl = h_udl.get(crowd_load)
print("\nProgramme calculates wind load using two separate methods (BS 5975 & BS 5950). User to decide upon "
      "method used once both have been calculated")
print()

print("BS 5975 Wind Loading Method:")

peak_pressure_bs5975, p_factor_bs5975, town_country_bs5975, distance_shore_bs5975, exposure_factor_bs5975, \
    basic_wind_velocity_bs5975, topographical_factor_bs5975, altitude_bs5975, s_wind_bs5975, \
    = hoarding_functions.wind_bs5975(height)

print()
print("BS 6399 Wind Loading Method:")

p_factor_bs6399, town_bs6399, upwind_distance_sea_bs6399, upwind_distance_town_bs6399, basic_wind_velocity_bs6399, \
    altitude_bs6399, height_bs6399, building_type_factor_bs6399, dynamic_augmentation_factor_bs6399, \
    effective_height_bs6399, displacement_height_bs6399, site_altitude_factor_bs6399, interpolated_sc_bs6399, \
    interpolated_st_bs6399, interpolated_tc_bs6399, interpolated_tt_bs6399, average_height_rooftops_bs6399, \
    spacing_surrounding_buildings_bs6399, terrain_building_factor_bs6399, effective_wind_speed_bs6399, \
    direction_factor_bs6399, seasonal_factor_bs6399, site_wind_speed_bs6399, dynamic_pressure_bs6399 \
    = hoarding_functions.wind_bs6399(height)

# Choose whether BS5975 method or BS6399 method used for calculations

print()
print("BS 5975 peak velocity pressure (1) = " + str(round(peak_pressure_bs5975, 3)) + "kN/m^2")
print("BS 6399 peak velocity pressure (2) = " + str(round(dynamic_pressure_bs6399, 3)) + "kN/m^2")
print()

choose_wind = None
while True:
    if (choose_wind == "1") or (choose_wind == "2"):
        if choose_wind == "1":
            hoarding_functions.wind_print_bs5975(file, peak_pressure_bs5975, p_factor_bs5975, town_country_bs5975,
                                                 distance_shore_bs5975, exposure_factor_bs5975,
                                                 basic_wind_velocity_bs5975, topographical_factor_bs5975,
                                                 altitude_bs5975, s_wind_bs5975)
            print()
            print("Peak velocity pressure = " + str(round(peak_pressure_bs5975, 3)) + "kN/m^2")
            peak_velocity_pressure = peak_pressure_bs5975
            break
        else:
            hoarding_functions.wind_print_bs6399(file, p_factor_bs6399, town_bs6399, upwind_distance_sea_bs6399,
                                                 upwind_distance_town_bs6399, basic_wind_velocity_bs6399,
                                                 altitude_bs6399, height_bs6399, building_type_factor_bs6399,
                                                 dynamic_augmentation_factor_bs6399, effective_height_bs6399,
                                                 displacement_height_bs6399, site_altitude_factor_bs6399,
                                                 interpolated_sc_bs6399, interpolated_st_bs6399, interpolated_tc_bs6399,
                                                 interpolated_tt_bs6399, average_height_rooftops_bs6399,
                                                 spacing_surrounding_buildings_bs6399, terrain_building_factor_bs6399,
                                                 effective_wind_speed_bs6399, direction_factor_bs6399,
                                                 seasonal_factor_bs6399, site_wind_speed_bs6399,
                                                 dynamic_pressure_bs6399)
            print()
            print("Peak velocity pressure = " + str(round(dynamic_pressure_bs6399, 3)) + "kN/m^2")
            peak_velocity_pressure = dynamic_pressure_bs6399
            break
    else:
        choose_wind = input("Wind calculation choice between BS 5975 & BS 6399 (BS 5975 = 1; BS 6399 = 2): ")

print()
length = float(input("Length of wall in metres (if wall returns around corner, choose the longer length): "))
k_factor = hoarding_functions.k_reduction_factor(height, length)

return_corners = input("Design hoarding with or without return corners (1 = w/ return corners; "
                       "2 = w/o return corners) = ")

if return_corners == "2":
    cp_b = 2.1
    cp_c = 1.7
    cp_d = 1.2
else:
    cp_b = 1.8
    cp_c = 1.4
    cp_d = 1.2

# Load case checks. Load cases evaluated on a per metre width basis.
zone_b_lc1 = (peak_velocity_pressure * 1 * cp_b * (height ** 2)) / 2
zone_b_lc2 = ((0.2 * 1 * cp_b * (height ** 2)) / 2) + (h_udl * 1 * 1.1)
if zone_b_lc1 > zone_b_lc2:
    load_case_b = "LC1"
    peak_pressure_b = peak_velocity_pressure
    h_udl_b = 0
    k_factor_b = k_factor
else:
    load_case_b = "LC2"
    peak_pressure_b = 0.2
    h_udl_b = h_udl
    k_factor_b = 1
zone_c_lc1 = (peak_velocity_pressure * 1 * cp_c * (height ** 2)) / 2
zone_c_lc2 = ((0.2 * 1 * cp_c * (height ** 2)) / 2) + (h_udl * 1 * 1.1)
if zone_c_lc1 > zone_c_lc2:
    load_case_c = "LC1"
    peak_pressure_c = peak_velocity_pressure
    h_udl_c = 0
    k_factor_c = k_factor
else:
    load_case_c = "LC2"
    peak_pressure_c = 0.2
    h_udl_c = h_udl
    k_factor_c = 1
zone_d_lc1 = (peak_velocity_pressure * 1 * cp_d * (height ** 2)) / 2
zone_d_lc2 = ((0.2 * 1 * cp_d * (height ** 2)) / 2) + (h_udl * 1 * 1.1)
if zone_d_lc1 > zone_d_lc2:
    load_case_d = "LC1"
    peak_pressure_d = peak_velocity_pressure
    h_udl_d = 0
    k_factor_d = k_factor
else:
    load_case_d = "LC2"
    peak_pressure_d = 0.2
    h_udl_d = h_udl
    k_factor_d = 1

# Post design
zone_b = "B"
post_width_b, post_depth_b, post_timber_grade_b = hoarding_functions.post_design(height, k_factor_b, return_corners,
                                                                                 zone_b, h_udl_b, load_case_b,
                                                                                 peak_pressure_b)
zone_c = "C"
post_width_c, post_depth_c, post_timber_grade_c = hoarding_functions.post_design(height, k_factor_c, return_corners,
                                                                                 zone_c, h_udl_c, load_case_c,
                                                                                 peak_pressure_c)
zone_d = "D"
post_width_d, post_depth_d, post_timber_grade_d = hoarding_functions.post_design(height, k_factor_d, return_corners,
                                                                                 zone_d, h_udl_d, load_case_d,
                                                                                 peak_pressure_d)

# Rail design
rail_width_b, rail_depth_b, rail_timber_grade_b = hoarding_functions.rail_design(height, k_factor_b, return_corners,
                                                                                 zone_b, h_udl_b, load_case_b,
                                                                                 peak_pressure_b)
rail_width_d, rail_depth_d, rail_timber_grade_d = hoarding_functions.rail_design(height, k_factor_d, return_corners,
                                                                                 zone_d, h_udl_d, load_case_d,
                                                                                 peak_pressure_d)





# Note under post design print function whether LC1 or LC2 used


file.close()
