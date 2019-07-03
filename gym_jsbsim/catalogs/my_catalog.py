""" Defines custom properties not implemented in JSBSim """


from enum import Enum
import shapefile
from gym.spaces import Box, Discrete
from gym_jsbsim.catalogs.property import Property
from gym_jsbsim.catalogs.jsbsim_catalog import JsbsimCatalog
from gym_jsbsim.envs.taxi_utils import * 



"""
amdb_path = "/home/nico/amdb"
taxiPath = taxi_path(ambd_folder_path=amdb_path, number_of_points_to_use=8)
reader = shapefile.Reader(taxiPath.fname, encodingErrors="replace")
taxi_freq_state = 30
"""

import gym_jsbsim.catalogs.utils as utils


class MyCatalog(Property, Enum):

    # position and attitude

    delta_heading = Property('position/delta-heading-to-target-deg', 'delta heading to target [deg]', -180, 180)
    delta_altitude = Property('position/delta-altitude-to-target-ft', 'delta altitude to target [ft]', -40000, 40000)

    # controls command

    throttle_cmd_dir = Property('fcs/throttle-cmd-dir', 'direction to move the throttle', 0, 2, Discrete)
    incr_throttle = Property('fcs/incr-throttle','incrementation throttle', 0, 1)
    aileron_cmd_dir = Property('fcs/aileron-cmd-dir', 'direction to move the aileron', 0, 2, Discrete)
    incr_aileron = Property('fcs/incr-aileron', 'incrementation aileron', 0, 1)
    elevator_cmd_dir = Property('fcs/elevator-cmd-dir', 'direction to move the elevator', 0, 2, Discrete)
    incr_elevator = Property('fcs/incr-elevator', 'incrementation elevator', 0, 1)
    rudder_cmd_dir = Property('fcs/rudder-cmd-dir', 'direction to move the rudder', 0, 2, Discrete)
    incr_rudder = Property('fcs/incr-rudder', 'incrementation rudder', 0, 1)

    # target conditions

    target_altitude_ft = Property('tc/h-sl-ft', 'target altitude MSL [ft]', JsbsimCatalog.position_h_sl_ft.min, JsbsimCatalog.position_h_sl_ft.max)
    target_heading_deg = Property('tc/target-heading-deg', 'target heading [deg]', JsbsimCatalog.attitude_psi_deg.min, JsbsimCatalog.attitude_psi_deg.max)
    target_time = Property('tc/target-time-sec', 'target time [sec]', 0)
    target_latitude_geod_deg = Property('tc/target-latitude-geod-deg', 'target geocentric latitude [deg]', -90, 90)
    target_longitude_geod_deg = Property('tc/target-longitude-geod-deg', 'target geocentric longitude [deg]', -180, 180)

    # following path

    steady_flight = Property('steady_flight', 'steady flight mode', 0, 1)
    turn_flight = Property('turn_flight', 'turn flight mode', 0, 1)

    #dist_heading_centerline_matrix = Property('dist_heading_centerline_matrix', 'dist_heading_centerline_matrix', '2D matrix with dist,angle of the next point from the aircraft to 1km (max 10 points)', [0, -45, 0, -45, 0, -45, 0, -45, 0, -45, 0, -45, 0, -45, 0, -45], [1000, 45, 1000, 45, 1000, 45, 1000, 45, 1000, 45, 1000, 45, 1000, 45, 1000, 45])
    d1 = Property('d1', 'd1', 0, 1000) 
    d2 = Property('d2', 'd2', 0, 1000) 
    d3 = Property('d3', 'd3', 0, 1000) 
    d4 = Property('d4', 'd4', 0, 1000) 
    d5 = Property('d5', 'd5', 0, 1000) 
    d6 = Property('d6', 'd6', 0, 1000) 
    d7 = Property('d7', 'd7', 0, 1000) 
    d8 = Property('d8', 'd8', 0, 1000)
    a1 = Property('a1', 'a1', -180, 180)  
    a2 = Property('a2', 'a2', -180, 180)  
    a3 = Property('a3', 'a3', -180, 180)   
    a4 = Property('a4', 'a4', -180, 180)  
    a5 = Property('a5', 'a5', -180, 180)  
    a6 = Property('a6', 'a6', -180, 180)  
    a7 = Property('a7', 'a7', -180, 180)  
    a8 = Property('a8', 'a8', -180, 180)

    shortest_dist = Property('shortest_dist', 'shortest distance between aircraft and path [m]', 0.0, 1000.0)
    taxi_freq_state = Property('taxi-freq-state','frequence to update taxi state',0)
    nb_step = Property('nb_step', 'shortest distance between aircraft and path [m]')


    # functions updating custom properties

    @classmethod
    def update_delta_altitude(cls, sim):
        value = sim.get_property_value(JsbsimCatalog.position_h_sl_ft) - sim.get_property_value(cls.target_altitude_ft)
        sim.set_property_value(cls.delta_altitude, value)

    @classmethod
    def update_delta_heading(cls, sim):
        value = utils.reduce_reflex_angle_deg(sim.get_property_value(JsbsimCatalog.attitude_psi_deg) - sim.get_property_value(cls.target_heading_deg))
        sim.set_property_value(cls.delta_heading, value)

    @staticmethod
    def update_property_incr(sim, discrete_prop, prop, incr_prop):
        value = sim.get_property_value(discrete_prop)
        if value == 0:
            pass
        else :
            if value == 1:
                sim.set_property_value(prop, sim.get_property_value(prop) - sim.get_property_value(incr_prop))
            elif value == 2:
                sim.set_property_value(prop, sim.get_property_value(prop) + sim.get_property_value(incr_prop))
            sim.set_property_value(discrete_prop, 0)

    @classmethod
    def update_throttle_cmd_dir(cls, sim):
        cls.update_property_incr(sim, cls.throttle_cmd_dir, JsbsimCatalog.fcs_throttle_cmd_norm, MyCatalog.incr_throttle)

    @classmethod
    def update_aileron_cmd_dir(cls, sim):
        cls.update_property_incr(sim, cls.aileron_cmd_dir, JsbsimCatalog.fcs_aileron_cmd_norm, MyCatalog.incr_aileron)

    @classmethod
    def update_elevator_cmd_dir(cls, sim):
        cls.update_property_incr(sim, cls.elevator_cmd_dir, JsbsimCatalog.fcs_elevator_cmd_norm, MyCatalog.incr_elevator)

    @classmethod
    def update_rudder_cmd_dir(cls, sim):
        cls.update_property_incr(sim, cls.rudder_cmd_dir, JsbsimCatalog.fcs_rudder_cmd_norm, MyCatalog.incr_rudder)


    @classmethod
    def update_da(cls, sim):
        #print("sim.get_property_value(nb_step), taxi_freq_state", sim.get_property_value(nb_step), taxi_freq_state)
        #print(taxi_freq_state)
        if (sim.get_property_value(cls.nb_step)%taxi_freq_state==1):
            #start_time = time.time()
            df = taxiPath.update_path((sim.get_property_value(JsbsimCatalog.position_lat_geod_deg), sim.get_property_value(JsbsimCatalog.position_long_gc_deg)), reader)
            #print("--- %s seconds ---" % (time.time() - start_time))
            
            dist = utils.shortest_ac_dist(0, 0, df[0][0].x, df[0][0].y, df[1][0].x, df[1][0].y)
            #print("shortest_dist2", dist)
            sim.set_property_value(cls.shortest_dist, dist)
            #print(sim.get_property_value(shortest_dist))

            for i in range(1,len(df)):
                if (df[i][1] <= 1000000000):
                    sim.set_property_value(cls.get_var_by_name("d"+str(i)), df[i][1])
                    sim.set_property_value(cls.get_var_by_name("a"+str(i)), utils.reduce_reflex_angle_deg(df[i][2] - sim.get_property_value(JsbsimCatalog.attitude_psi_deg)))
                    #sim.set_property_value(cls.get_var_by_name("a"+str(i)), df[i][2])
                else:
                    sim.set_property_value(cls.get_var_by_name("d"+str(i)), 1000)
                    sim.set_property_value(cls.get_var_by_name("a"+str(i)), 0)
        sim.set_property_value(cls.nb_step, int(sim.get_property_value(cls.nb_step))+1)

    @classmethod
    def update_custom_properties(cls,sim,prop):
        update_custom_properties = {cls.delta_altitude : cls.update_delta_altitude,

                                    cls.delta_heading: cls.update_delta_heading,

                                    cls.throttle_cmd_dir: cls.update_throttle_cmd_dir,

                                    cls.aileron_cmd_dir: cls.update_aileron_cmd_dir,

                                    cls.elevator_cmd_dir : cls.update_elevator_cmd_dir,

                                    cls.rudder_cmd_dir : cls.update_rudder_cmd_dir#,

                                    #cls.d1 : cls.update_da
                                }
        if prop in update_custom_properties:
            update_custom_properties[prop](sim)

            
    @classmethod
    def init_custom_properties(cls,sim,prop):
        init_custom_properties = { cls.taxi_freq_state : 30,
                                   
                                   cls.incr_throttle: 0.05,

                                   cls.incr_aileron : 0.05,

                                   cls.incr_elevator : 0.05,

                                   cls.incr_rudder : 0.05
        }

        if prop in init_custom_properties:
            sim.set_property_value(prop,init_custom_properties[prop])

    @classmethod
    def get_var_by_name(cls, string):
        dict_da = {
        "d1": cls.d1,
        "d2": cls.d2,
        "d3": cls.d3,
        "d4": cls.d4,
        "d5": cls.d5,
        "d6": cls.d6,
        "d7": cls.d7,
        "d8": cls.d8,
        "a1": cls.a1,
        "a2": cls.a2,
        "a3": cls.a3,
        "a4": cls.a4,
        "a5": cls.a5,
        "a6": cls.a6,
        "a7": cls.a7,
        "a8": cls.a8
        }
        return dict_da[string]
