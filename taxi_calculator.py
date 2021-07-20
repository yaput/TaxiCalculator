import re
from datetime import datetime, time
import logging

class FareCalculator:
    total_distance = 0.0
    current_fare = 0.0
    devider = 0
    fare_multiplier = 0
    multiplier = 0
    latest_distance = 0.0
    
    input_format = r'[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9] (.*)'

    def __init__(self) -> None:
        pass

    def fare_adjuster(self, distance: float) -> int:
        self.total_distance = distance - self.latest_distance
        if (distance <= 1000): # distance in meters
            self.current_fare = 400
            self.total_distance = distance
        elif (distance <= 10000 and distance > 1000):
            # += 40 yen every 400 meters
            self.devider = 400
            self.fare_multiplier = 40
            self.total_distance 
        elif (distance > 10000):
            self.devider = 350
            self.fare_multiplier = 40
        
        # above 1 Km then we start to calculate the multiplier fare
        if (distance > 1000):
            self.total_distance = distance - self.latest_distance
            self.multiplier = self.total_distance // self.devider
            addition_fare = self.multiplier * self.fare_multiplier
            self.current_fare += addition_fare
        
        self.latest_distance = distance
        return self.current_fare

    def calculate_fare(self, trip_log: list) -> int:
        result = 0
        if (self.__validate_format__(trip_log)):
            time_list = self.__get_time_list__(trip_log)
            mileage_list = self.__get_mileage_list__(trip_log)

            if (self.__validate_time_step__(time_list) and 
            self.__validate_time_interval__(time_list) and 
            self.__validate_mileage__(mileage_list)):
                # proces no error raised
                for mileage in mileage_list:
                    self.fare_adjuster(mileage)
            result = self.current_fare
            self.__reset__()
        return round(result) if result > 0 else "" 

    def __validate_format__(self, trip_log: list) -> bool:
        # private method to validate input before processing
        if (len(trip_log) < 2):
            logging.error("Data can't be less than 2 row")
            return False
            
        for log in trip_log:
            if (log == ""):
                logging.error("Data can't be empty line")
                return False

            match_format = re.match(self.input_format, log)
            if (match_format == None):
                logging.error("Data format must follow: hh:mm:ss.fff<space>xxxxxxxx.f example 00:00:00.000 0.0")
                return False
        return True

    def __validate_time_step__(self, time_list: list) -> bool:
        for x in range(len(time_list) - 1):
            time1 = datetime.strptime(time_list[x], '%H:%M:%S.%f')
            time2 = datetime.strptime(time_list[x+1], '%H:%M:%S.%f')
            if (time1.time() > time2.time()): # the past time has been sent, assuming the time value has to be later than the previous one.
                logging.error("Data time can't use past time")
                return False
        return True

    def __validate_time_interval__(self, time_list: list) -> bool:
        for x in range(len(time_list) - 1):
            time1 = datetime.strptime(time_list[x], '%H:%M:%S.%f')
            time2 = datetime.strptime(time_list[x+1], '%H:%M:%S.%f')
            time_diff = (time2 - time1).total_seconds()
            if (time_diff > (60 * 5) ): # the past time has been sent, assuming the time value has to be later than the previous one.
                logging.error("Data time interval has to be less than equal to 5 minutes")
                return False
        return True
    
    def __validate_mileage__(self, mileage_list: list) -> bool:
        total = 0.0
        for mileage in mileage_list:
            total = total + mileage
        if (total > 0.0):
            return True
        logging.error("Data mileage can't be 0.0 m")
        return False
    
    def __get_time_list__(self, trip_log: list) -> list:
        time_list = []
        for trip in trip_log:
            data = trip.split()
            time_list.append(data[0])
        return time_list

    def __get_mileage_list__(self, trip_log: list) -> list:
        mileage_list = []
        for trip in trip_log:
            data = trip.split()
            if (len(data) > 1):
                mileage_list.append(float(data[1]))
            else:
                raise Exception("Unsupported format")
        return mileage_list
    
    def __reset__(self):
        self.total_distance = 0.0
        self.current_fare = 0.0
        self.devider = 0
        self.fare_multiplier = 0
        self.multiplier = 0