import numpy as np
import folium
from shapely.geometry import Point, LineString
from geographiclib.geodesic import Geodesic

from gym_jsbsim.catalogs.catalog import Catalog as prp

def get_bearing(p1, p2):
    """
    :param p1: (long,lat)
    :param p2: (long,lat)
    :return: bearing in degrees [0,360]
    """
    long1, lat1 = p1
    long2, lat2 = p2
    brng = Geodesic.WGS84.Inverse(lat1, long1, lat2, long2)['azi1']
    return (brng+360)%360


class taxi_path(object):
    """
    Compute n centerline next points in regards to the aircraft location and heading.
    """

    def __init__(self):
        
        # LOOP
        self.centerlinepoints = [(1.369889125000043, 43.625578879000045),(1.3684100810000928, 43.62700014200004),(1.3668620630000419, 43.62848768500004),(1.3666688410000916, 43.628705049000075),(1.3666178020000643, 43.628754238000056),(1.3665762220000488, 43.62880708500006),(1.3665458220000914, 43.628859970000065),(1.3665218470000582, 43.62891972700004),(1.3664907020000783, 43.62901451600004),(1.3664544040000806, 43.629143740000075),(1.3664379450000865, 43.62923652100005),(1.366429758000038, 43.62928267400008),(1.3664213190000396, 43.62933563300004),(1.3663952990000894, 43.629835666000076),(1.366392762000089, 43.62993075300005),(1.3664001590000794, 43.630007540000065),(1.3664236900000901, 43.63007954500006),(1.3664629070000842, 43.63016006500004),(1.3665071650000868, 43.630228016000046),(1.366532558000074, 43.630260132000046),(1.3665859670000486, 43.63031450800008),(1.3666448280000623, 43.63036507500004),(1.3667184050000856, 43.63041347600006),(1.3667822460000707, 43.63045029300008),(1.3668491230000654, 43.63048443200006),(1.3669623630000842, 43.630540824000036),(1.3670003540000835, 43.63055768700008),(1.3670646130000819, 43.630568992000065),(1.3671076770000923, 43.63057656800004),(1.3672162010000761, 43.63058918100006),(1.367328541000063, 43.63059559900006),(1.367398784000045, 43.63059538500005),(1.3674664400000438, 43.63059196200004),(1.3675809370000707, 43.63057845000009),(1.3676469250000878, 43.63056678200007),(1.367693149000047, 43.63055512600005),(1.3677376020000906, 43.630539413000065),(1.3677996140000914, 43.63051240900006),(1.367877629000077, 43.63047454000008),(1.3679639130000396, 43.63042025000004),(1.367986396000049, 43.630397266000045),(1.3687260750000405, 43.62968615900007),(1.3694795590000695, 43.628964652000036),(1.3695462910000629, 43.62890069000008),(1.3699761760000797, 43.628488649000076),(1.3706840500000794, 43.62780372900005),(1.3727649170000404, 43.62580836700005),(1.3727954180000665, 43.62571976300006),(1.3728083210000932, 43.62566091500008),(1.3728145350000887, 43.625606608000055),(1.3728142150000622, 43.62554483100007),(1.3728064660000427, 43.62549054100003),(1.372781352000061, 43.625414988000045),(1.372739091000085, 43.62533720500005),(1.372709056000076, 43.62529500800008),(1.3726745690000826, 43.62525442900005),(1.3726469960000713, 43.62522629400007),(1.3725954100000877, 43.625179322000065),(1.3722427040000866, 43.624981097000045),(1.3721857870000918, 43.62495189400005),(1.3721634540000878, 43.62494315500004),(1.3721129600000381, 43.62492082400007),(1.3720678800000883, 43.62490775200007),(1.3720197600000574, 43.62489954900008),(1.371840546000044, 43.62486923100005),(1.371712875000071, 43.624864254000045),(1.3710522390000506, 43.62480435800006),(1.370725921000087, 43.62477477300007),(1.370376368000052, 43.62474324900006),(1.3693200770000544, 43.62465130000004),(1.3679380720000722, 43.624526202000084),(1.3675893980000637, 43.624491737000085),(1.3675753960000634, 43.624490576000085),(1.3674685180000665, 43.624469360000035),(1.367367553000065, 43.62443900900007),(1.3672915940000507, 43.62440889000004),(1.3672285440000564, 43.62437709200009),(1.3671698550000428, 43.62433968500005),(1.3671226240000465, 43.62430098100003),(1.3670802710000771, 43.62425429800004),(1.367044192000094, 43.62419917400007),(1.367034146000094, 43.62417766500005),(1.3670256470000481, 43.624159467000084),(1.3670098290000396, 43.62411282800008),(1.3669949630000815, 43.62404044900006),(1.3669930200000522, 43.62401908600003),(1.3669982240000422, 43.623968406000074),(1.367009757000062, 43.62391868800006),(1.367024496000056, 43.623877281000034),(1.3670437860000675, 43.62383656800006),(1.367917989000091, 43.62299686500006),(1.3699186000000623, 43.62107520900008),(1.3701417820000756, 43.62086083400004),(1.3711781980000524, 43.61986532100008),(1.3714684410000473, 43.619586533000074),(1.3717033320000382, 43.61936091200005),(1.3718095560000734, 43.61931423800007),(1.371920965000072, 43.619277622000084),(1.371984454000085, 43.61926176800006),(1.3720495120000464, 43.61924895700008),(1.3721161380000808, 43.61923918900004),(1.3721843320000744, 43.61923246400005),(1.3722492330000478, 43.619239770000036),(1.372253864000072, 43.61924059200004),(1.3723047970000835, 43.619249627000045),(1.3723853050000798, 43.61926963900004),(1.372480676000066, 43.61930279500007),(1.3729006940000659, 43.61953032400004),(1.3740993070000513, 43.62018680400007),(1.374458086000061, 43.620386034000035),(1.374527770000043, 43.620450933000086),(1.374567865000074, 43.62049700600005),(1.3746011880000424, 43.62054324300004),(1.3746394290000694, 43.62061307200008),(1.374648387000093, 43.62063803800004),(1.3746537840000883, 43.62065307800009),(1.3746639290000644, 43.62069574900005),(1.3746694580000849, 43.62078843300009),(1.3746675930000833, 43.62086356700007),(1.3746574650000412, 43.62091427100006),(1.3746405570000775, 43.62096326200009),(1.3746205680000685, 43.62100407100007),(1.3745955520000734, 43.62104361000007),(1.3745655110000712, 43.62108187900009),(1.3745304440000723, 43.62111887900005),(1.3732963560000826, 43.62230475600006),(1.371928457000081, 43.623619216000066),(1.3715156390000516, 43.62401590700006),(1.370725921000087, 43.62477477300007),(1.3699752730000796, 43.62549609600006),(1.369889125000043, 43.625578879000045)]
        
        self.centerline = LineString(self.centerlinepoints)
        self.shortest_dist = None
        self.map = None
        self.path = None

    def update_path2(self, aircraft_loc, aircraft_heading, id_path, nb_point):
        """
        :param ref_pts: aircraft (longitude,latitude)
        :param ac_heading:
        :param id_path: the id of the next centerline point from the centerlipoints list
        :param nb_point: The number of point to take in account
        :return: list[[(long,lat),distance,heading],[.....]]
        """
        next_point = False
        output = []
        id_path=min(id_path, len(self.centerlinepoints)-1)
        
        # compute angle between aircraft and next point
        angle_basic = aircraft_heading - get_bearing(aircraft_loc, self.centerlinepoints[id_path])
        angle_basic360 = (abs(angle_basic)+360)%360
        angle_ac_nextpoint = min(angle_basic360, 360-angle_basic360)

        if Point(aircraft_loc).distance(Point(self.centerlinepoints[id_path]))*100000 < 1 or angle_ac_nextpoint > 60:
            # I move to the next centerline point
            next_point = True
            # I keep my next n points
            my_points_state = self.centerlinepoints[id_path+1:min(id_path+nb_point+1, len(self.centerlinepoints)-1)]
        else:
            # I keep my next n points
            my_points_state = self.centerlinepoints[id_path:min(id_path+nb_point, len(self.centerlinepoints)-1)]
        # I compute heading and distance of my next n points
        for p in my_points_state:
            output.append([p, Point(aircraft_loc).distance(Point(p))*100000, get_bearing(aircraft_loc, p)])
        
        # Compute the shortest distance to the centerline
        self.shortest_dist = self.centerline.distance(Point(aircraft_loc))*100000 #Point((1.3578, 43.587434)).distance(Point((1.3577, 43.587288)))*100000 = 17m

        return output, next_point
    
    def clear_rendering(self):
        """Clear the map object and rendered path so th next call to render_simulation()
           will start from a fresh map and empty path
        """
        self.path = None
        self.map = None
    
    def render_simulation(self, sim, html_filename='gym_jsb_sim_map.html', refresh_period=60):
        """Render the simulation, i.e. current taxiing path on a folium map written to the
           given html file which is automatically updated by the browser ever given refresh
           period (in seconds).

        # Parameters
        sim: Simulation object
        html_filename: Path to the html file to write containing the folium rendering
        refresh_period: period time in seconds between 2 successive automatic page updates
                        by the browser (different from the period time between 2 calls to
                        this method)
        """
        lon = sim.get_property_value(prp.position_long_gc_deg)
        lat = sim.get_property_value(prp.position_lat_geod_deg)
        html_update_filename = html_filename[0:html_filename.rfind('.')] + '_update.html'
        if (self.map is None):
            self.map = folium.Map(location=[lat, lon], zoom_start=18)
            for p in self.centerlinepoints:
                folium.Marker((p[1], p[0]), popup=p).add_to(self.map)
            folium.PolyLine(taxiPath.centerlinepoints, color='blue', weight=2.5, opacity=1).add_to(self.map)
            self.path = folium.PolyLine([(lat, lon)], color='red', weight=2.5, opacity=1)
            self.path.add_to(self.map)
            f = open(html_filename, 'w')
            f.write('<!DOCTYPE html>\n' +
                    '<HTML>\n' +
                    '<HEAD>\n' +
                    '<META http-equiv="refresh" content="{}">\n' +
                    '</HEAD>\n' +
                    '<FRAMESET>\n' +
                    '<FRAME src="{}">\n' +
                    '</FRAMESET>\n' +
                    '</HTML>'.format(refresh_period, html_update_filename))
            f.close()
        else:
            self.path.locations.append(folium.utilities.validate_location((lat, lon)))
            self.map.location = folium.utilities.validate_location((lat, lon))
        self.map.save(html_update_filename)
