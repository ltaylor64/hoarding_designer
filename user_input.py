import hoarding_functions

test = "test2.txt"

# file = open("Temporary Hoarding Calculation Pack.txt", "w")
file = open(test, "w")

print("-" * 50, "\nTemporary Site Hoarding Designer v0.0.2", "\n", "-" * 50, sep="")

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
length = float(input("Length of wall in metres (if wall returns around corner, choose the longer length): "))
k_factor = 1
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

p_factor_bs6399, town_bs6399, upwind_distance_sea_bs6399, upwind_distance_town_bs6399, basic_wind_velocity_bs6399, altitude_bs6399, height_bs6399,\
    building_type_factor_bs6399, dynamic_augmentation_factor_bs6399, effective_height_bs6399, displacement_height_bs6399, site_altitude_factor_bs6399, interpolated_sc_bs6399, interpolated_st_bs6399, interpolated_tc_bs6399, \
    interpolated_tt_bs6399, average_height_rooftops_bs6399, spacing_surrounding_buildings_bs6399, terrain_building_factor_bs6399, \
    effective_wind_speed_bs6399, direction_factor_bs6399, seasonal_factor_bs6399, site_wind_speed_bs6399, dynamic_pressure_bs6399 = hoarding_functions.wind_bs6399(height)

# Choose whether BS5975 method or BS6399 method used for calculations

choose_wind = None
while True:
    if (choose_wind == "1") or (choose_wind == "2"):
        if choose_wind == "1":
            hoarding_functions.wind_print_bs5975(file, peak_pressure_bs5975, p_factor_bs5975, town_country_bs5975,
                                                 distance_shore_bs5975, exposure_factor_bs5975,
                                                 basic_wind_velocity_bs5975, topographical_factor_bs5975,
                                                 altitude_bs5975, s_wind_bs5975)
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
            break
    else:
        choose_wind = input("Wind calculation choice between BS 5975 & BS 5950 (BS 5975 = 1; BS 5950 = 2): ")


peak_pressure = peak_pressure_bs5975

# post design
zone_b = "Zone B"
return_corners = True

# functions.post_design(zone_b, height, k_factor, return_corners, peak_pressure, h_udl)


# post_spacing_B = int(input("Zone B post spacing (in m): "))
# post_width_B = int(input("Zone B post width (in mm): "))
# post_depth_B = int(input("Zone B post depth (in mm): "))
# post_grade_B = input("Zone B post grade (C16 or C24): ")
# return_corners = True

file.close()
