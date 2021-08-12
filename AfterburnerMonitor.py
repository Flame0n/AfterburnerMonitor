import os
import time
import psutil
import datetime


class AfterburnerMonitor():

    def __init__(self):
        self.path_to_afterburner_log = "HardwareMonitoring.hml"
        os.remove(self.path_to_afterburner_log)
        time.sleep(3)  # Delay for Afterburner history creating

    def get_metrics_by_time(self, time):
        pass

    def get_avg_metrics_by_time_range(self, start_time, end_time):
        pass

    def get_current_metrics(self):
        if os.path.exists(self.path_to_afterburner_log) and self.is_afterburner_executed():
            with open(self.path_to_afterburner_log, 'r') as file:
                lines = file.readlines()

            GPU_Name = lines[1].split(",")[2][1:]
            last_line = lines[-1]
            metrics = last_line.split(",")

            return {"GPU_Name": GPU_Name,
                    "GPU_Temperature": metrics[2],
                    "GPU_Usage": metrics[3],
                    "GPU_VID_Usage": metrics[4],
                    "GPU_Memory_Usage": metrics[5],
                    "CPU_Temperature": metrics[6],
                    "CPU_Usage": metrics[7],
                    "RAM_Usage": metrics[8]}
        else:
            raise Exception(
                "Afterburner process not executed or history not being written")

    def is_afterburner_executed(self):
        return True if "MSIAfterburner.exe" in (p.name() for p in psutil.process_iter()) else False


if __name__ == '__main__':
    a = AfterburnerMonitor()
    print(a.get_current_metrics())

    start = datetime.datetime.now()
    print(start)
    time.sleep(2)
    end = datetime.datetime.now()
