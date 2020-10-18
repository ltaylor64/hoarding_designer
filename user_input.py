import hoarding_functions


def wind_print_bs5975(wind_pressure, probability_factor, town_country, shore_distance, exposure_factor,
                      basic_wind_velocity, topographical_factor, altitude, s_wind):
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


file = open("Temporary Hoarding Calculation Pack.txt", "w")

print("-" * 50, "\nTemporary Site Hoarding Designer v0.0.1", "\n", "-" * 50, sep="")

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
      "method used once both have been calculated. BS 5950 method ---BROKEN---")
print()
print("BS 5975 Wind Loading Method:")

peak_pressure_bs5975, p_factor_bs5975, town_country_bs5975, distance_shore_bs5975, exposure_factor_bs5975, \
    basic_wind_velocity_bs5975, topographical_factor_bs5975, altitude_bs5975, s_wind_bs5975, \
    = hoarding_functions.wind_bs5975(height)

print("BS5975 peak velocity pressure = " + str(round(peak_pressure_bs5975, 2)) + "kN/m^2")
print()

choose_wind = None
while True:
    if (choose_wind == "1") or (choose_wind == "2"):
        if choose_wind == "1":
            wind_print_bs5975(peak_pressure_bs5975, p_factor_bs5975, town_country_bs5975, distance_shore_bs5975,
                              exposure_factor_bs5975, basic_wind_velocity_bs5975, topographical_factor_bs5975,
                              altitude_bs5975, s_wind_bs5975)
            break
        else:
            # wind_print_bs5950()
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
