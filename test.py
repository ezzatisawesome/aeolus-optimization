from atmos1976 import density
import math


# CONSTANTS
R_reenty = 6455 # km
R_earth = 6371 # km
earth_mu = 3.9860043543609598e5 # km^3/s^2
g0 = 9.80665 # m/s^2


def calculate_mass_prop(delta_v, isp, sc_mass):
    return math.exp(delta_v / (isp * g0 / 1000)) * sc_mass - sc_mass

def simulate(altitude):
    coefficient_drag = 2.2 # -
    sma = altitude + 6371 # km
    sc_cross_sectional_area = 28 # m^2
    sc_dry_mass = 1300 # kg
    mission_lifepsan = 3.45 # years
    isp = 200 # s

    # Intermediate variables
    orbital_velocity = math.sqrt(earth_mu / sma) # km/s
    atmospheric_density = density(sma - R_earth) # kg/km^3

    # Deorbit delta-v
    V_reentry = math.sqrt(earth_mu / R_reenty) # km/s
    delta_v_deorbit = V_reentry - orbital_velocity # km/s

    # Maintenance delta-v
    orbit_period = 2 * math.pi * math.sqrt(sma ** 3 / earth_mu)
    orbits_per_year = 365 * 24 * 60 * 60 / orbit_period # orbits / year
    delta_v_lost_drag = (math.pi * (coefficient_drag * sc_cross_sectional_area / sc_dry_mass) * atmospheric_density * (sma*1000) * (orbital_velocity*1000)) / 1000 # km/rev
    delta_v_maintenance = delta_v_lost_drag * orbits_per_year * mission_lifepsan # km

    # Propellant mass
    delta_v_total = delta_v_deorbit + delta_v_maintenance # km
    mass_prop_total = math.exp(delta_v_total / (isp * g0 / 1000)) * sc_dry_mass - sc_dry_mass
    mass_prop_deorbit = math.exp(delta_v_deorbit / (isp * g0 / 1000)) * sc_dry_mass - sc_dry_mass
    mass_prop_maintenance = math.exp(delta_v_maintenance / (isp * g0 / 1000)) * sc_dry_mass - sc_dry_mass

    return mass_prop_total, mass_prop_deorbit, mass_prop_maintenance, atmospheric_density


if __name__ == "__main__":
    for i in range(200, 990, 10):
        print("Altitude: ", i)
        mass_prop_total, mass_prop_deorbit, mass_prop_maintenance, atmospheric_density = simulate(i)

        print("Total Prop: ", mass_prop_total)
        print("Mass prop Deorbit: ", mass_prop_deorbit)
        print("Mass prop Maintenance: ", mass_prop_maintenance)
        print("Atmospheric Density: ", atmospheric_density)