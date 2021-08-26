import os
import time
import psutil
import datetime


class AfterburnerMonitor():

    def __init__(self, path_to_afterburner_log):
        self.path_to_afterburner_log = path_to_afterburner_log
        self.remove_history()
        self.is_afterburner_executed()

    def remove_history(self):
        os.remove(self.path_to_afterburner_log)
        time.sleep(3)  # Delay for Afterburner history creating

    def get_metrics_by_time(self, target_time):
        self.is_afterburner_executed()
        with open(self.path_to_afterburner_log, 'r') as file:
            lines = file.readlines()
        GPU_Name = lines[1].split(", ")[2].replace('\n', '')

        for metrics in lines:
            metrics = metrics.replace('\n', '')
            metrics = metrics.replace(' ', '')
            metrics = metrics.split(",")

            str_target_time = datetime.datetime.strftime(
                target_time, "%d-%m-%Y%H:%M:%S")
            if str_target_time == metrics[1]:
                print(metrics)
                return {"GPU_Name": GPU_Name,
                        "GPU_Temperature": metrics[2],
                        "GPU_Usage": metrics[3],
                        "GPU_Memory_Usage": metrics[4],
                        "CPU_Temperature": metrics[5],
                        "CPU_Usage": metrics[6],
                        "RAM_Usage": metrics[7]}

    def get_avg_metrics_by_time_range(self, start_time, end_time):
        self.is_afterburner_executed()
        with open(self.path_to_afterburner_log, 'r') as file:
            lines = file.readlines()
        GPU_Name = lines[1].split(", ")[2].replace('\n', '')
        avg_metrics = {"GPU_Name": GPU_Name,
                       "GPU_Temperature": 0.0,
                       "GPU_Usage": 0.0,
                       "GPU_Memory_Usage": 0.0,
                       "CPU_Temperature": 0.0,
                       "CPU_Usage": 0.0,
                       "RAM_Usage": 0.0}
        metric_counter = 0
        for metrics in lines:
            metrics = metrics.replace('\n', '')
            metrics = metrics.replace(' ', '')
            metrics = metrics.split(",")

            if datetime.datetime.strptime(metrics[1], "%d-%m-%Y%H:%M:%S") >= start_time \
                    and datetime.datetime.strptime(metrics[1], "%d-%m-%Y%H:%M:%S") <= end_time \
                    and metrics[0] == "80":
                if self.validate_metrics(metrics):
                    if float(metrics[3]) == 0.0:
                        continue
                    index = 2
                    for key in avg_metrics:
                        if key != "GPU_Name":
                            avg_metrics[key] += float(metrics[index])
                            index += 1
                    metric_counter += 1

        if metric_counter == 0:
            raise Exception(
                "Count of written metrics equal 0. This period of time was not recorded in history")

        for key in avg_metrics:
            if key != "GPU_Name":
                avg_metrics[key] = avg_metrics[key] / metric_counter

        return avg_metrics

    def get_current_metrics(self):
        self.is_afterburner_executed()
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

    def validate_metrics(self, metrics):
        for i in range(2, len(metrics)):
            try:
                float(metrics[i])
            except:
                return False
        return True

    def is_afterburner_executed(self):
        if not "MSIAfterburner.exe" in (p.name() for p in psutil.process_iter()):
            raise Exception("Afterburner not executed")


if __name__ == '__main__':
    try:
        a = AfterburnerMonitor("HardwareMonitoring.hml")
        print(a.get_avg_metrics_by_time_range(start_time=datetime.datetime.strptime("26-08-2021 04:06:41", "%d-%m-%Y %H:%M:%S"),
                                              end_time=datetime.datetime.strptime("26-08-2021 04:06:50", "%d-%m-%Y %H:%M:%S")))
        print(a.get_metrics_by_time(datetime.datetime.strptime(
            "26-08-2021 04:06:41", "%d-%m-%Y %H:%M:%S")))
        print(a.get_current_metrics())
    except Exception as e:
        print(e)
