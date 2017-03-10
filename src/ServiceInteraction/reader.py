from PyQt5.QtCore import QThread, pyqtSlot
import irsdk

import src.ServiceInteraction.data as data


class DataReader(QThread):
    class State:

        def __init__(self):
            self.connected = False
            self.current_tick = -1
            self.weather_tick = -1
            self.drivers_tick = -1

        def reset(self):
            self.__init__()

    def __init__(self):
        QThread.__init__(self)

        self.stop = False
        self.state = DataReader.State()

    def check_service(self, ir):
        if self.state.connected and not (ir.is_initialized and ir.is_connected):
            self.state.reset()
            data.weekend_info.reset()
            data.camera = None
            ir.shutdown()
        elif not self.state.connected and ir.startup('data.bin') and ir.is_initialized and ir.is_connected:
            self.state.connected = True

    def update_track(self, ir):
        if not data.weekend_info.track:
            track = data.Track()
            if ir['WeekendInfo']:
                track.name = ir['WeekendInfo']['TrackDisplayName']
                track.city = ir['WeekendInfo']['TrackCity']
                track.country = ir['WeekendInfo']['TrackCountry']

            if ir['SplitTimeInfo']:
                track.sectors = []
                for sec in ir['SplitTimeInfo']['Sectors']:
                    track.sectors.append(sec['SectorStartPct'])

            data.weekend_info.track = track

    def update_camera(self, ir):
        #TODO implement
        pass

    def update_weather(self, ir):
        if ir.get_session_info_update_by_key('AirTemp') != self.state.weather_tick:
            self.state.weather_tick = ir.get_session_info_update_by_key('AirTemp')
            weather = data.weekend_info.weather
            weather.track_temp = ir['TrackTemp']
            weather.air_temp = ir['AirTemp']
            weather.air_pressure = ir['AirPressure']
            weather.fog_level = ir['FogLevel']
            weather.wind_dir = ir['WindDir']
            weather.wind_vel = ir['WindVel']
            weather.skies = ir['Skies']
            weather.humidity = ir['Humidity']

    def update_cars(self, ir):
        if not ir['DriverInfo']:
            return

        if self.state.drivers_tick != ir.get_session_info_update_by_key('DriverInfo'):
            self.state.drivers_tick = ir.get_session_info_update_by_key('DriverInfo')
            cars_info = ir['DriverInfo']['Drivers']
            for car_info in cars_info:
                if not car_info:
                    break

                user_id = car_info['UserID']
                if user_id not in data.weekend_info.drivers:
                    driver = data.Driver()
                    driver.name = car_info['UserName']
                    driver.club_name = car_info['ClubName']
                    driver.irating = car_info['IRating']
                    driver.license_level = car_info['LicLevel']
                    driver.license_sublevel = car_info['LicSubLevel']
                    driver.team_id = car_info['TeamID']
                    data.weekend_info.drivers[user_id] = driver

                if car_info['CarIdx'] not in data.weekend_info.cars:
                    car = data.Car()
                    car.is_pace_car = car_info['CarIsPaceCar']
                    car.is_spectator = car_info['IsSpectator']
                    car.number = car_info['CarNumber']
                    car.name = car_info['CarScreenName']
                    car.class_id = car_info['CarClassID']
                    car.team_id = car_info['TeamID']
                    car.team_name = car_info["TeamName"]
                    data.weekend_info.cars[car_info['CarIdx']] = car

                data.weekend_info.cars[car_info['CarIdx']].user_id = car_info['UserID']

                class_id = car_info['CarClassID']
                if class_id not in data.weekend_info.classes:
                    data.weekend_info.classes[class_id] = car_info["CarClassShortName"]

    def update_session(self, ir):
        current_session = ir['SessionNum']
        data.weekend_info.current_session = current_session
        if current_session not in data.weekend_info.sessions:
            data.weekend_info.sessions[current_session] = data.Session()

        session = data.weekend_info.sessions[current_session]
        session.num = current_session
        session.state = ir['SessionState']
        session.flags = ir['SessionFlags']
        session.time = ir['SessionTime']
        session.time_remain = ir['SessionTimeRemain']
        session.laps_remain = ir['SessionLapsRemain']

        if ir['SessionInfo']:
            sessions = ir['SessionInfo']['Sessions']
            if not sessions:
                return

            for session_info in sessions:
                if session_info['SessionNum'] != current_session:
                    continue



    def update_car_status(self, ir):
        laps = ir['CarIdxLap']
        laps_complete = ir['CarIdxLapCompleted']
        fastest_times = ir['CarIdxEstTime']
        distances = ir['CarIdxLapDistPct']
        positions = ir['CarIdxPosition']
        class_positions = ir['CarIdxClassPosition']
        pits = ir['CarIdxOnPitRoad']
        surfaces = ir['CarIdxTrackSurface']
        for i in range(64):
            car = data.weekend_info.cars[i]
            if not car:
                break

            car.lap = laps[i]
            car.laps_complete = laps_complete[i]
            car.lap_dist = distances[i]
            car.fastest_time = fastest_times[i]
            car.position = positions[i]
            car.class_position = class_positions[i]
            car.pit = pits[i]
            car.track_surface = surfaces[i]

    def update_data(self, ir):
        if not data.weekend_info.display_units:
            data.weekend_info.display_units = ir['DisplayUnits']

        self.update_track(ir)
        self.update_weather(ir)
        self.update_camera(ir)
        self.update_cars(ir)
        self.update_session(ir)
        self.update_car_status(ir)

        pass

    @pyqtSlot()
    def run(self):
        ir = irsdk.IRSDK()
        while not self.stop:
            self.check_service(ir)
            if self.state.connected:
                if self.state.current_tick < ir.last_session_info_update:
                    self.state.current_tick = ir.last_session_info_update
                    self.update_data(ir)

                self.msleep(100)
            else:
                self.sleep(3)
