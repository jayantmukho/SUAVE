
# Electric_Multicopter.py
# 
# Created: Feb 2020, M Clarke
#          Sep 2020, M. Clarke 

#----------------------------------------------------------------------
#   Imports
# ---------------------------------------------------------------------
import SUAVE
from SUAVE.Core                                                           import Units, Data
from SUAVE.Methods.Power.Battery.Sizing                                   import initialize_from_mass
from SUAVE.Methods.Propulsion                                             import propeller_design
from SUAVE.Methods.Weights.Buildups.eVTOL.empty                           import empty
from SUAVE.Methods.Center_of_Gravity.compute_component_centers_of_gravity import compute_component_centers_of_gravity
from SUAVE.Methods.Propulsion.electric_motor_sizing                       import size_optimal_motor
from SUAVE.Methods.Weights.Correlations.Propulsion                        import nasa_motor, hts_motor , air_cooled_motor
import numpy as np
from copy import deepcopy

# ----------------------------------------------------------------------
#   Build the Vehicle
# ----------------------------------------------------------------------
def vehicle_setup():
    
    # ------------------------------------------------------------------
    #   Initialize the Vehicle
    # ------------------------------------------------------------------    
    vehicle                                     = SUAVE.Vehicle()
    vehicle.tag                                 = 'multicopter'
    vehicle.configuration                       = 'eVTOL'
    # ------------------------------------------------------------------
    #   Vehicle-level Properties
    # ------------------------------------------------------------------    
    # mass properties
    vehicle.mass_properties.takeoff             = 2080. * Units.lb 
    vehicle.mass_properties.operating_empty     = 1666. * Units.lb            
    vehicle.mass_properties.max_takeoff         = 2080. * Units.lb               
    vehicle.mass_properties.center_of_gravity   = [[2.6, 0., 0. ]] 
                                                
    # This needs updating                       
    vehicle.passengers                          = 5
    vehicle.reference_area                      = 73  * Units.feet**2 
    vehicle.envelope.ultimate_load              = 5.7   
    vehicle.envelope.limit_load                 = 3.  
                                                
    wing = SUAVE.Components.Wings.Main_Wing()   
    wing.tag                                    = 'main_wing'  
    wing.aspect_ratio                           = 1.  
    wing.spans.projected                        = 0.1
    wing.chords.root                            = 0.1
    wing.chords.tip                             = 0.1
    wing.origin                                 = [[2.6, 0., 0. ]] 
    wing.symbolic                               = True 
    vehicle.append_component(wing)
    
    # ------------------------------------------------------    
    # FUSELAGE    
    # ------------------------------------------------------    
    # FUSELAGE PROPERTIES
    fuselage                                    = SUAVE.Components.Fuselages.Fuselage()
    fuselage.tag                                = 'fuselage'
    fuselage.configuration                      = 'Tube_Wing'  
    fuselage.seats_abreast                      = 2.  
    fuselage.seat_pitch                         = 3.  
    fuselage.fineness.nose                      = 0.88   
    fuselage.fineness.tail                      = 1.13   
    fuselage.lengths.nose                       = 3.2   * Units.feet 
    fuselage.lengths.tail                       = 6.4  * Units.feet
    fuselage.lengths.cabin                      = 6.4  * Units.feet 
    fuselage.lengths.total                      = 16.0  * Units.feet 
    fuselage.width                              = 5.85  * Units.feet 
    fuselage.heights.maximum                    = 4.65  * Units.feet  
    fuselage.heights.at_quarter_length          = 3.75  * Units.feet  
    fuselage.heights.at_wing_root_quarter_chord = 4.65  * Units.feet 
    fuselage.heights.at_three_quarters_length   = 4.26  * Units.feet 
    fuselage.areas.wetted                       = 236.  * Units.feet**2 
    fuselage.areas.front_projected              = 0.14  * Units.feet**2    
    fuselage.effective_diameter                 = 5.85  * Units.feet  
    fuselage.differential_pressure              = 0. 
    
    # Segment  
    segment                          = SUAVE.Components.Fuselages.Segment() 
    segment.tag                      = 'segment_1'  
    segment.origin                   = [0., 0. ,0.]  
    segment.percent_x_location       = 0.  
    segment.percent_z_location       = 0.0 
    segment.height                   = 0.1   * Units.feet   
    segment.width                    = 0.1 * Units.feet     
    segment.length                   = 0.  
    segment.effective_diameter       = 0.1 * Units.feet   
    fuselage.append_segment(segment)            
                                                
    # Segment                                   
    segment                         = SUAVE.Components.Fuselages.Segment()
    segment.tag                     = 'segment_2'  
    segment.origin                  = [4.*0.3048 , 0. ,0.1*0.3048 ]  
    segment.percent_x_location      = 0.25  
    segment.percent_z_location      = 0.05 
    segment.height                  = 3.75  * Units.feet 
    segment.width                   = 5.65  * Units.feet  
    segment.length                  = 3.2   * Units.feet  
    segment.effective_diameter      = 5.65  * Units.feet 
    fuselage.append_segment(segment)            
                                                
    # Segment                                   
    segment                         = SUAVE.Components.Fuselages.Segment()
    segment.tag                     = 'segment_3'  
    segment.origin                  = [8.*0.3048 , 0. ,0.34*0.3048 ]  
    segment.percent_x_location      = 0.5  
    segment.percent_z_location      = 0.071 
    segment.height                  = 4.65  * Units.feet 
    segment.width                   = 5.55  * Units.feet  
    segment.length                  = 3.2   * Units.feet
    segment.effective_diameter      = 5.55  * Units.feet 
    fuselage.append_segment(segment)            
                                                
    # Segment                                  
    segment                         = SUAVE.Components.Fuselages.Segment()
    segment.tag                     = 'segment_4'  
    segment.origin                  = [12.*0.3048 , 0. ,0.77*0.3048 ] 
    segment.percent_x_location      = 0.75 
    segment.percent_z_location      = 0.089  
    segment.height                  = 4.73  * Units.feet  
    segment.width                   = 4.26  * Units.feet   
    segment.length                  = 3.2   * Units.feet  
    segment.effective_diameter      = 4.26  * Units.feet 
    fuselage.append_segment(segment)            
                                                
    # Segment                                   
    segment                         = SUAVE.Components.Fuselages.Segment()
    segment.tag                     = 'segment_5'  
    segment.origin                  = [16.*0.3048 , 0. ,2.02*0.3048 ] 
    segment.percent_x_location      = 1.0
    segment.percent_z_location      = 0.158 
    segment.height                  = 0.67 * Units.feet
    segment.width                   = 0.33 * Units.feet
    segment.length                  = 3.2   * Units.feet 
    segment.effective_diameter      = 0.33  * Units.feet
    fuselage.append_segment(segment)             
                                                
    # add to vehicle
    vehicle.append_component(fuselage)   
       
    #------------------------------------------------------------------
    # PROPULSOR
    #------------------------------------------------------------------
    net                      = SUAVE.Components.Energy.Networks.Battery_Propeller()
    net.number_of_engines    = 6
    net.nacelle_diameter     = 0.6 * Units.feet # need to check 
    net.engine_length        = 0.5 * Units.feet
    net.areas                = Data()
    net.areas.wetted         = np.pi*net.nacelle_diameter*net.engine_length + 0.5*np.pi*net.nacelle_diameter**2
    net.voltage              =  500.
    net.identical_propellers = True

    #------------------------------------------------------------------
    # Design Electronic Speed Controller 
    #------------------------------------------------------------------
    esc             = SUAVE.Components.Energy.Distributors.Electronic_Speed_Controller()
    esc.efficiency  = 0.95
    net.esc         = esc
    
    #------------------------------------------------------------------
    # Design Payload
    #------------------------------------------------------------------
    payload                       = SUAVE.Components.Energy.Peripherals.Avionics()
    payload.power_draw            = 0.
    payload.mass_properties.mass  = 200. * Units.kg
    net.payload                   = payload

    #------------------------------------------------------------------
    # Design Avionics
    #------------------------------------------------------------------
    avionics            = SUAVE.Components.Energy.Peripherals.Avionics()
    avionics.power_draw = 200. * Units.watts
    net.avionics        = avionics
                                                
    #------------------------------------------------------------------
    # Design Battery
    #------------------------------------------------------------------
    bat                                                 = SUAVE.Components.Energy.Storages.Batteries.Constant_Mass.Lithium_Ion()
    bat.specific_energy                                 = 350. * Units.Wh/Units.kg
    bat.resistance                                      = 0.005
    bat.max_voltage                                     = net.voltage     
    bat.mass_properties.mass                            = 300. * Units.kg
    initialize_from_mass(bat, bat.mass_properties.mass)
    net.battery                                         = bat

    #------------------------------------------------------------------
    # Design Rotors  
    #------------------------------------------------------------------ 
    # atmosphere and flight conditions for propeller/rotor design
    g                            = 9.81                                   # gravitational acceleration  
    speed_of_sound               = 340                                    # speed of sound 
    Hover_Load                   = vehicle.mass_properties.takeoff*g      # hover load   
    design_tip_mach              = 0.7                                    # design tip mach number 
    
    rotor                        = SUAVE.Components.Energy.Converters.Rotor() 
    rotor.tip_radius             = 3.95 * Units.feet
    rotor.hub_radius             = 0.6  * Units.feet 
    rotor.disc_area              = np.pi*(rotor.tip_radius**2) 
    rotor.number_of_blades       = 3
    rotor.freestream_velocity    = 10.0
    rotor.angular_velocity       = (design_tip_mach*speed_of_sound)/rotor.tip_radius   
    rotor.design_Cl              = 0.7
    rotor.design_altitude        = 1000 * Units.feet                   
    rotor.design_thrust          = Hover_Load/(net.number_of_engines-1) # contingency for one-engine-inoperative condition

    rotor.airfoil_geometry       = ['../Vehicles/Airfoils/NACA_4412.txt'] 
    rotor.airfoil_polars         = [['../Vehicles/Airfoils/Polars/NACA_4412_polar_Re_50000.txt' ,
                                     '../Vehicles/Airfoils/Polars/NACA_4412_polar_Re_100000.txt' ,
                                     '../Vehicles/Airfoils/Polars/NACA_4412_polar_Re_200000.txt' ,
                                     '../Vehicles/Airfoils/Polars/NACA_4412_polar_Re_500000.txt' ,
                                     '../Vehicles/Airfoils/Polars/NACA_4412_polar_Re_1000000.txt' ]]
    
    rotor.airfoil_polar_stations = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]      
    rotor                        = propeller_design(rotor)     
    
    # Appending rotors with different origins
    origins                 = [[ 0.,2.,1.4],[ 0.0,-2.,1.4],
                                [2.5,4.,1.4] ,[2.5,-4.,1.4],
                                [5.0,2.,1.4] ,[5.0,-2.,1.4]]
    
    for ii in range(6):
        rotor          = deepcopy(rotor)
        rotor.tag      = 'propeller' # weight estimation gets confused since it's looking for hard coded names
        rotor.origin   = [origins[ii]]
        net.propellers.append(rotor)
    
    #------------------------------------------------------------------
    # Design Motors
    #------------------------------------------------------------------
    # Motor
    motor                      = SUAVE.Components.Energy.Converters.Motor() 
    motor.efficiency           = 0.95
    motor.nominal_voltage      = bat.max_voltage * 0.5
    motor.mass_properties.mass = 3. * Units.kg 
    motor.origin               = rotor.origin  
    motor.propeller_radius     = rotor.tip_radius   
    motor.no_load_current      = 2.0     
    motor                      = size_optimal_motor(motor,rotor)
    net.motor                  = motor 
                                                
    # Define motor sizing parameters            
    max_power  = rotor.design_power * 1.2
    max_torque = rotor.design_torque * 1.2
    
    # test high temperature superconducting motor weight function 
    mass = hts_motor(max_power) 
    
    # test NDARC motor weight function 
    mass = nasa_motor(max_torque)
    
    # test air cooled motor weight function 
    mass                        = air_cooled_motor(max_power) 
    motor.mass_properties.mass  = mass 
    
    # Appending motors with different origins    
    for ii in range(6):
        rotor_motor = deepcopy(motor)
        rotor_motor.tag = 'motor'
        net.motors.append(rotor_motor)        

    
    vehicle.append_component(net)
    
    vehicle.weight_breakdown  = empty(vehicle)
    compute_component_centers_of_gravity(vehicle)
    vehicle.center_of_gravity() 
    
    return vehicle
