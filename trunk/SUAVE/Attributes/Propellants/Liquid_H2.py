## @ingroup Attributes-Propellants
# Liquid H2
#
# Created:  Unk 2013, SUAVE TEAM 
# Modified: Apr 2015, SUAVE TEAM 
#           Feb 2016, M. Vegh 
#           Jan 2018, W. Maier 

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
from .Propellant import Propellant

# ----------------------------------------------------------------------
#  Liquid H2 Propellant Class
# ----------------------------------------------------------------------
## @ingroup Attributes-Propellants
class Liquid_H2(Propellant):
    """Holds values for this propellant
    
    Assumptions:
    None
    
    Source:
    None
    """

    def __defaults__(self):
        """This sets the default values.

        Assumptions:
        None

        Source:
        Values commonly available
        http://arc.uta.edu/publications/td_files/Kristen%20Roberts%20MS.pdf

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """ 
        
        self.tag                        = 'Liquid_H2' 
        self.reactant                   = 'O2' 
        self.density                    = 70.88                            # [kg/m^3] 
        self.specific_energy            = 120.0e6                         # [J/kg] 
        self.energy_density             = self.density * self.specific_energy # [J/m^3] 
        self.stoichiometric_fuel_to_air = 0.0291 
        self.temperatures.autoignition  = 845.15                           # [K]         