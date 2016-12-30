from irsdk import TrkLoc, SessionState


class Track:
    name = None
    sectors = None


class Camera:
    num = None
    state = None
    car_idx = None
    group_number = None
    replay = None


class Weather:
    air_pressure = None
    air_temp = None
    track_temp = None
    humidity = None
    fog_level = None
    skies = None
    wind_dir = None
    wind_vel = None


class Driver:
    name = None
    irating = None
    license_level = None
    license_sublevel = None
    club_name = None
    team_id = None


class Car:
    is_spectator = False
    is_pace_car = False
    number = None
    name = None

    class_id = None
    user_id = None
    team_id = None
    team_name = None

    lap = None
    laps_complete = 0
    lap_dist = None
    fastest_time = None
    position = None
    class_position = None
    incidents = 0
    pit = False
    track_surface = TrkLoc.not_in_world


class Session:
    num = None
    state = SessionState.invalid
    flags = 0
    laps_remain = None
    time = None
    time_remain = None


class WeekendInfo:
    def __init__(self):
        self.display_units = None

        self.classes = {}
        self.cars = [None for x in range(64)]
        self.drivers = {}

        self.track = None
        self.weather = Weather()

        self.current_session = None
        self.sessions = {}

    def reset(self):
        self.__init__()

weekend_info = WeekendInfo()
camera = Camera()
