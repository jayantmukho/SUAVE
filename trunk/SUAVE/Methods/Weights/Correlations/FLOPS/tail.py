## @ingroup Methods-Weights-Correlations-FLOPS
# tail.py
#
# Created:  May 2020, W. Van Gijseghem
# Modified:

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import numpy as np
import SUAVE
from SUAVE.Core import Units

## @ingroup Methods-Weights-Correlations-FLOPS
def tail_vertical_FLOPS(vehicle, wing):
    """ Calculate the vertical tail weight

        Assumptions:
           Conventional tail configuration

        Source:
            The Flight Optimization System Weight Estimation Method

       Inputs:
            vehicle - data dictionary with vehicle properties                   [dimensionless]
                -.mass_properties.max_takeoff: MTOW                             [kilograms]
            wing - data dictionary with vertical tail properties                [dimensionless]
                -.taper: taper of wing
                -.areas.reference: surface area of wing                         [m^2]

       Outputs:
            WVT - vertical tail weight                                          [kilograms]

        Properties Used:
            N/A
        """
    ac_type = vehicle.systems.accessories
    atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976()
    atmo_data = atmosphere.compute_values(vehicle.design_cruise_alt, 0)
    atmo_data_floor = atmosphere.compute_values(0, 0)
    DELTA = atmo_data.pressure / atmo_data_floor.pressure
    QCRUS = 1481.35 * DELTA * vehicle.design_mach_number ** 2  # Cruise dynamic pressure, psf
    SWPVT = wing.sweeps.quarter_chord
    CSVT = np.cos(SWPVT)
    TCVT = wing.thickness_to_chord
    ARVT = wing.aspect_ratio
    DG          = vehicle.mass_properties.max_takeoff / Units.lbs  # Design gross weight in lb
    TRVT        = wing.taper
    NVERT       = 1  # Number of vertical tails
    SVT = wing.areas.reference/Units.ft**2
    ULF = vehicle.envelope.ultimate_load
    if wing.t_tail:
        HHT = 1.0
    else:
        HHT = 0.0

    if ac_type == "business" or ac_type == "commuter":
        WVT = 0.073 * (1. + 0.2 * HHT) * (ULF * DG)**0.376 * QCRUS**0.122 * SVT**0.873 * (ARVT/CSVT**2)**0.357 / \
              (100 * TCVT/CSVT)**0.49
    else:
        WVT = 0.32 * DG ** 0.3 * (TRVT + 0.5) * NVERT ** 0.7 * (SVT)**0.85
    return WVT * Units.lbs

def tail_horizontal_FLOPS(vehicle, wing):
    """ Calculate the horizontal tail weight

        Assumptions:
           Conventional tail configuration

        Source:
            The Flight Optimization System Weight Estimation Method

       Inputs:
            vehicle - data dictionary with vehicle properties                   [dimensionless]
                -.mass_properties.max_takeoff: MTOW                             [kilograms]
            wing - data dictionary with vertical tail properties                [dimensionless]
                -.taper: taper of wing
                -.areas.reference: surface area of wing                         [m^2]

       Outputs:
            WHT - vertical tail weight                                          [kilograms]

        Properties Used:
            N/A
        """
    ac_type = vehicle.systems.accessories
    atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976()
    atmo_data = atmosphere.compute_values(vehicle.design_cruise_alt, 0)
    atmo_data_floor = atmosphere.compute_values(0, 0)
    DELTA = atmo_data.pressure / atmo_data_floor.pressure
    QCRUS = 1481.35 * DELTA * vehicle.design_mach_number ** 2  # Cruise dynamic pressure, psf
    ULF = vehicle.envelope.ultimate_load
    SHT     = wing.areas.reference / Units.ft **2
    DG      = vehicle.mass_properties.max_takeoff / Units.lbs
    TRHT    = wing.taper
    if ac_type == "business" or ac_type == "commuter":
        WHT = 0.016 * SHT**0.873 * (ULF*DG)**0.414 * QCRUS**0.122
    else:
        WHT     = 0.53 * SHT * DG ** 0.2 * (TRHT + 0.5)
    return WHT * Units.lbs

