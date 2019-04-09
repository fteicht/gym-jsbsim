import math
import collections
from gym_jsbsim import utils


class BoundedProperty(collections.namedtuple('BoundedProperty', ['name', 'description', 'min', 'max'])):
    def get_legal_name(self):
        return utils.AttributeFormatter.translate(self.name)


class Property(collections.namedtuple('Property', ['name', 'description'])):
    def get_legal_name(self):
        return utils.AttributeFormatter.translate(self.name)


# position and attitude
altitude_sl_ft = BoundedProperty('position/h-sl-ft', 'altitude above mean sea level [ft]', -1400, 85000)
pitch_rad = BoundedProperty('attitude/pitch-rad', 'pitch [rad]', -0.5 * math.pi, 0.5 * math.pi)
roll_rad = BoundedProperty('attitude/roll-rad', 'roll [rad]', -math.pi, math.pi)
heading_deg = BoundedProperty('attitude/psi-deg', 'heading [deg]', 0, 360)
sideslip_deg = BoundedProperty('aero/beta-deg', 'sideslip [deg]', -180, +180)
lat_geod_deg = BoundedProperty('position/lat-geod-deg', 'geocentric latitude [deg]', -90, 90)
lng_geoc_deg = BoundedProperty('position/long-gc-deg', 'geodesic longitude [deg]', -180, 180)
dist_travel_m = Property('position/distance-from-start-mag-mt', 'distance travelled from starting position [m]')
delta_heading = BoundedProperty('position/delta-heading-to-target-deg', 'delta heading to target [deg]', -180, 180)
delta_altitude = BoundedProperty('position/delta-altitude-to-target-ft', 'delta altitude to target [ft]', -40000, 40000)

# velocities
u_fps = BoundedProperty('velocities/u-fps', 'body frame x-axis velocity [ft/s]', -2200, 2200)
v_fps = BoundedProperty('velocities/v-fps', 'body frame y-axis velocity [ft/s]', -2200, 2200)
w_fps = BoundedProperty('velocities/w-fps', 'body frame z-axis velocity [ft/s]', -2200, 2200)
v_north_fps = BoundedProperty('velocities/v-north-fps', 'velocity true north [ft/s]', float('-inf'), float('+inf'))
v_east_fps = BoundedProperty('velocities/v-east-fps', 'velocity east [ft/s]', float('-inf'), float('+inf'))
v_down_fps = BoundedProperty('velocities/v-down-fps', 'velocity downwards [ft/s]', float('-inf'), float('+inf'))
p_radps = BoundedProperty('velocities/p-rad_sec', 'roll rate [rad/s]', -2 * math.pi, 2 * math.pi)
q_radps = BoundedProperty('velocities/q-rad_sec', 'pitch rate [rad/s]', -2 * math.pi, 2 * math.pi)
r_radps = BoundedProperty('velocities/r-rad_sec', 'yaw rate [rad/s]', -2 * math.pi, 2 * math.pi)
altitude_rate_fps = Property('velocities/h-dot-fps', 'rate of altitude change [ft/s]')
phi_dot = BoundedProperty('velocities/phidot-rad_sec', 'rad/s', -2 * math.pi, 2 * math.pi)
theta_dot = BoundedProperty('velocities/thetadot-rad_sec', 'rad/s', -2 * math.pi, 2 * math.pi)
v_air = BoundedProperty('velocities/vc-fps', 'airspeed in knots', 0, 4400)

# Acceleration
p_dot = BoundedProperty('accelerations/pdot-rad_sec2', 'rad/s²',  -(8/180) * math.pi, (8/180) * math.pi)
q_dot = BoundedProperty('accelerations/qdot-rad_sec2', 'rad/s²',  -(8/180) * math.pi, (8/180) * math.pi)
r_dot = BoundedProperty('accelerations/rdot-rad_sec2', 'rad/s²',  -(8/180) * math.pi, (8/180) * math.pi)
v_dot = BoundedProperty('accelerations/vdot-ft_sec2', 'ft/s²', -4.0, 4.0)
w_dot = BoundedProperty('accelerations/wdot-ft_sec2', 'ft/s²', -4.0, 4.0)
u_dot = BoundedProperty('accelerations/wdot-ft_sec2', 'ft/s²', -4.0, 4.0)

# accelerations
n_pilot_x = Property('accelerations/n-pilot-x-norm', 'pilot body x-axis acceleration, normalised')
n_pilot_y = Property('accelerations/n-pilot-y-norm', 'pilot body y-axis acceleration, normalised')
n_pilot_z = Property('accelerations/n-pilot-z-norm', 'pilot body z-axis acceleration, normalised')

# controls state
aileron_left = BoundedProperty('fcs/left-aileron-pos-norm', 'left aileron position, normalised', -1, 1)
aileron_right = BoundedProperty('fcs/right-aileron-pos-norm', 'right aileron position, normalised', -1, 1)
elevator = BoundedProperty('fcs/elevator-pos-norm', 'elevator position, normalised', -1, 1)
rudder = BoundedProperty('fcs/rudder-pos-norm', 'rudder position, normalised', -1, 1)
flap = BoundedProperty('fcs/flap-pos-norm', 'flap position, normalised', 0, 1)
speedbrake = BoundedProperty('fcs/speedbrake-pos-norm', 'speedbrake position, normalised', 0, 1)
throttle = BoundedProperty('fcs/throttle-pos-norm', 'throttle position, normalised', 0, 1)
gear = BoundedProperty('gear/gear-pos-norm', 'landing gear position, normalised', 0, 1)


# engines
engine_running = Property('propulsion/engine/set-running', 'engine running (0/1 bool)')
all_engine_running = Property('propulsion/set-running', 'set engine running (-1 for all engines)')
engine_thrust_lbs = Property('propulsion/engine/thrust-lbs', 'engine thrust [lb]')
fuel_contents_lbs_0 = Property('propulsion/tank[0]/contents-lbs', 'Fuel content in selected tank')
fuel_contents_lbs_1 = Property('propulsion/tank[1]/contents-lbs', 'Fuel content in selected tank')

# controls command
aileron_cmd = BoundedProperty('fcs/aileron-cmd-norm', 'aileron commanded position, normalised', -1., 1.)
elevator_cmd = BoundedProperty('fcs/elevator-cmd-norm', 'elevator commanded position, normalised', -1., 1.)
rudder_cmd = BoundedProperty('fcs/rudder-cmd-norm', 'rudder commanded position, normalised', -1., 1.)
throttle_cmd = BoundedProperty('fcs/throttle-cmd-norm', 'throttle commanded position, normalised', 0., 1.)
mixture_cmd = BoundedProperty('fcs/mixture-cmd-norm', 'engine mixture setting, normalised', 0., 1.)
throttle_1_cmd = BoundedProperty('fcs/throttle-cmd-norm[1]', 'throttle 1 commanded position, normalised', 0., 1.)
mixture_1_cmd = BoundedProperty('fcs/mixture-cmd-norm[1]', 'engine mixture 1 setting, normalised', 0., 1.)
gear_all_cmd = BoundedProperty('gear/gear-cmd-norm', 'all landing gear commanded position, normalised', 0., 1.)
left_brake_cmd_norm = BoundedProperty('fcs/left-brake-cmd-norm', 'Left brake command(normalized)', 0., 1.)
right_brake_cmd_norm = BoundedProperty('fcs/right-brake-cmd-norm', 'Right brake command(normalized)', 0., 1.)
steer_cmd_norm = BoundedProperty('fcs/steer-cmd-norm', 'Steer command(normalized)', -1., 1.)

# trim commands
pitch_trim = BoundedProperty('fcs/pitch-trim-cmd-norm', 'pitch trim command, normalised', -1, 1)
roll_trim = BoundedProperty('fcs/roll-trim-cmd-norm', 'roll trim command, normalised', -1, 1)
yaw_trim = BoundedProperty('fcs/yaw-trim-cmd-norm', 'yaw trim command, normalised', -1, 1)

# simulation
sim_dt = Property('simulation/dt', 'JSBSim simulation timestep [s]')
sim_time_s = Property('simulation/sim-time-sec', 'Simulation time [s]')

# initial conditions
initial_altitude_ft = BoundedProperty('ic/h-sl-ft', 'initial altitude MSL [ft]', altitude_sl_ft.min, altitude_sl_ft.max)
initial_terrain_altitude_ft = Property('ic/terrain-elevation-ft', 'initial terrain alt [ft]')
initial_longitude_geoc_deg = Property('ic/long-gc-deg', 'initial geocentric longitude [deg]')
initial_latitude_geod_deg = Property('ic/lat-geod-deg', 'initial geodesic latitude [deg]')
initial_u_fps = Property('ic/u-fps', 'body frame x-axis velocity; positive forward [ft/s]')
initial_v_fps = Property('ic/v-fps', 'body frame y-axis velocity; positive right [ft/s]')
initial_w_fps = Property('ic/w-fps', 'body frame z-axis velocity; positive down [ft/s]')
initial_p_radps = Property('ic/p-rad_sec', 'roll rate [rad/s]')
initial_q_radps = Property('ic/q-rad_sec', 'pitch rate [rad/s]')
initial_r_radps = Property('ic/r-rad_sec', 'yaw rate [rad/s]')
initial_roc_fpm = Property('ic/roc-fpm', 'initial rate of climb [ft/min]')
initial_heading_deg = BoundedProperty('ic/psi-true-deg', 'initial (true) heading [deg]', heading_deg.min, heading_deg.max)
ic_h_agl_ft = BoundedProperty('ic/h-agl-ft', '', altitude_sl_ft.min, altitude_sl_ft.max)
h_agl_ft = BoundedProperty('position/h-agl-ft', '', altitude_sl_ft.min, altitude_sl_ft.max)

# target conditions
target_altitude_ft = BoundedProperty('tc/h-sl-ft', 'target altitude MSL [ft]', altitude_sl_ft.min, altitude_sl_ft.max)
target_heading_deg = BoundedProperty('tc/target-heading-deg', 'target heading [deg]', heading_deg.min, heading_deg.max)

prp_dict = {"altitude_sl_ft": altitude_sl_ft,
	"pitch_rad": pitch_rad,
	"roll_rad": roll_rad,
	"heading_deg": heading_deg,
	"sideslip_deg": sideslip_deg,
	"lat_geod_deg": lat_geod_deg,
	"lng_geoc_deg": lng_geoc_deg,
	"dist_travel_m": dist_travel_m,
	"delta_heading": delta_heading,
	"delta_altitude": delta_altitude,
	"u_fps": u_fps,
	"v_fps": v_fps,
	"w_fps": w_fps,
	"v_north_fps": v_north_fps,
	"v_east_fps": v_east_fps,
	"v_down_fps": v_down_fps,
	"p_radps": p_radps,
	"q_radps": q_radps,
	"r_radps": r_radps,
	"altitude_rate_fps": altitude_rate_fps,
	"n_pilot_x": n_pilot_x,
	"n_pilot_y": n_pilot_y,
	"n_pilot_z": n_pilot_z,
	"aileron_left": aileron_left,
	"aileron_right": aileron_right,
	"elevator": elevator,
	"rudder": rudder,
	"throttle": throttle,
	"gear": gear,
	"left_brake_cmd_norm": left_brake_cmd_norm,
	"right_brake_cmd_norm": right_brake_cmd_norm,
	"steer_cmd_norm": steer_cmd_norm,
	"engine_running": engine_running,
	"all_engine_running": all_engine_running,
	"engine_thrust_lbs": engine_thrust_lbs,
	"aileron_cmd": aileron_cmd,
	"elevator_cmd": elevator_cmd,
	"rudder_cmd": rudder_cmd,
	"throttle_cmd": throttle_cmd,
	"mixture_cmd": mixture_cmd,
	"throttle_1_cmd": throttle_1_cmd,
	"mixture_1_cmd": mixture_1_cmd,
	"gear_all_cmd": gear_all_cmd,
	"sim_dt": sim_dt,
	"sim_time_s": sim_time_s,
	"initial_altitude_ft": initial_altitude_ft,
	"initial_terrain_altitude_ft": initial_terrain_altitude_ft,
	"initial_longitude_geoc_deg": initial_longitude_geoc_deg,
	"initial_latitude_geod_deg": initial_latitude_geod_deg,
	"initial_u_fps": initial_u_fps,
	"initial_v_fps": initial_v_fps,
	"initial_w_fps": initial_w_fps,
	"initial_p_radps": initial_p_radps,
	"initial_q_radps": initial_q_radps,
	"initial_r_radps": initial_r_radps,
	"initial_roc_fpm": initial_roc_fpm,
	"initial_heading_deg": initial_heading_deg,
	"target_altitude_ft": target_altitude_ft,
	"target_heading_deg": target_heading_deg,
	"p_dot": p_dot,
	"q_dot": q_dot,
	"r_dot": r_dot,
	"v_dot": v_dot,
	"w_dot": w_dot,
	"u_dot":u_dot,
	"phi_dot": phi_dot,
	"theta_dot": theta_dot,
	"v_air": v_air,
	"fuel_contents_lbs_0": fuel_contents_lbs_0,
	"fuel_contents_lbs_1": fuel_contents_lbs_1,
	"ic_h_agl_ft": ic_h_agl_ft,
	"h_agl_ft": h_agl_ft
	}


class Vector2(object):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def heading_deg(self):
        """ Calculate heading in degrees of vector from origin """
        heading_rad = math.atan2(self.x, self.y)
        heading_deg_normalised = (math.degrees(heading_rad) + 360) % 360
        return heading_deg_normalised

    @staticmethod
    def from_sim(sim: 'simulation.Simulation') -> 'Vector2':
        return Vector2(sim[v_east_fps], sim[v_north_fps])


class GeodeticPosition(object):
    def __init__(self, latitude_deg: float, longitude_deg: float):
        self.lat = latitude_deg
        self.lon = longitude_deg

    def heading_deg_to(self, destination: 'GeodeticPosition') -> float:
        """ Determines heading in degrees of course between self and destination """
        difference_vector = destination - self
        return difference_vector.heading_deg()

    @staticmethod
    def from_sim(sim: 'simulation.Simulation') -> 'GeodeticPosition':
        """ Return a GeodeticPosition object with lat and lon from simulation """
        lat_deg = sim[lat_geod_deg]
        lon_deg = sim[lng_geoc_deg]
        return GeodeticPosition(lat_deg, lon_deg)

    def __sub__(self, other) -> Vector2:
        """ Returns difference between two coords as (delta_lat, delta_long) """
        return Vector2(self.lon - other.lon, self.lat - other.lat)
