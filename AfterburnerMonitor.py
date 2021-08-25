import os
import time
import psutil
import datetime


class AfterburnerMonitor():

    def __init__(self):
        self.path_to_afterburner_log = "HardwareMonitoring.hml"
        # os.remove(self.path_to_afterburner_log)
        time.sleep(3)  # Delay for Afterburner history creating
        if not self.is_afterburner_executed():
            raise Exception("Afterburner process not executed")

    def get_metrics_by_time(self, target_time):
        if os.path.exists(self.path_to_afterburner_log) and self.is_afterburner_executed():
            with open(self.path_to_afterburner_log, 'r') as file:
                lines = file.readlines()

            GPU_Name = lines[1].split(", ")[2][1:].replace('\n', '')

            for metrics in lines:
                metrics = metrics.replace('\n', '')
                metrics = metrics.replace(' ', '')
                metrics = metrics.split(",")

                str_time = datetime.datetime.strftime(target_time, "%d-%m-%Y%H:%M:%S")
                if str_time == metrics[1]:
                    print(metrics)
                    return {"GPU_Name": GPU_Name,
                            "GPU_Temperature": metrics[2],
                            "GPU_Usage": metrics[3],
                            "GPU_Memory_Usage": metrics[4],
                            "CPU_Temperature": metrics[5],
                            "CPU_Usage": metrics[6],
                            "RAM_Usage": metrics[7]}
        else:
            raise Exception(
                "Afterburner process not executed or history not being written")

    def get_avg_metrics_by_time_range(self, start_time, end_time):
        pass

    def get_current_metrics(self):
        if os.path.exists(self.path_to_afterburner_log) and self.is_afterburner_executed():
            with open(self.path_to_afterburner_log, 'r') as file:
                lines = file.readlines()

            GPU_Name = lines[1].split(",")[2][1:]

            metrics = lines[-1].split(",")

            return {"GPU_Name": GPU_Name,
                    "GPU_Temperature": metrics[2],
                    "GPU_Usage": metrics[3],
                    "GPU_Memory_Usage": metrics[4],
                    "CPU_Temperature": metrics[5],
                    "CPU_Usage": metrics[6],
                    "RAM_Usage": metrics[7]}
        else:
            raise Exception(
                "Afterburner process not executed or history not being written")

    def is_afterburner_executed(self):
        return True if "MSIAfterburner.exe" in (p.name() for p in psutil.process_iter()) else False


if __name__ == '__main__':
    a = AfterburnerMonitor()
    print(a.get_metrics_by_time(datetime.datetime.strptime(
        "23-08-2021 08:13:46", "%d-%m-%Y %H:%M:%S")))
