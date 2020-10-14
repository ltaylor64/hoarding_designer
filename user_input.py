import hoarding_functions

print("-" * 50, "\nTemporary Site Hoarding Designer v0.0.0", "\n", "-" * 50, sep="")

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
      "\nLow --> Low traffic areas (0.37kN/m)\nNone --> No public access (0.0kN/m)", sep="")

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

peak_pressure_bs5975 = hoarding_functions.wind_bs5975(height)

# print("Peak velocity pressure = " + str(peak_pressure_bs5975) + "kN/m^2")
print("BS5975 peak velocity pressure = " + str(round(peak_pressure_bs5975, 2)) + "kN/m^2")
print()

# post design
zone_b = "Zone B"
return_corners = True

# functions.post_design(zone_b, height, k_factor, return_corners, peak_pressure, h_udl)


# post_spacing_B = int(input("Zone B post spacing (in m): "))
# post_width_B = int(input("Zone B post width (in mm): "))
# post_depth_B = int(input("Zone B post depth (in mm): "))
# post_grade_B = input("Zone B post grade (C16 or C24): ")
# return_corners = True
