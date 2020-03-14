import subprocess
import time

hour = 0

while True:
    if hour != 0:
        print(f"Hour {hour}, resetting..")

    proc = subprocess.Popen(["python3", "covidmap.py"])
    time.sleep(10800)
    proc.terminate()

    hour += 3
