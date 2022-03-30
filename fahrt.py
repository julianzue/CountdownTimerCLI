import time
import os
from colorama import Fore, init

init()

# colors 
g = Fore.LIGHTGREEN_EX
r = Fore.LIGHTRED_EX
y = Fore.LIGHTYELLOW_EX
R = Fore.RESET

class Fahrt():
    def __init__(self):

        if os.path.isfile("times.txt"):
            
            read_file = open("times.txt", "r")
            get_time = read_file.read().split("|")

            self.start = input(y + "[*] " + R + "Start Time (" + get_time[0] + "): ")
            self.end = input(y + "[*] " + R + "End Time (" + get_time[1] + "): ")

            if self.start == "":
                self.start = get_time[0]
            else:
                update = input(y + "[*] " + R + "Update Start Time? (" + self.start + ") [y|n]: ")
                if update == "y":
                    self.updateStartTime(self.start)

            if self.end == "":
                self.end = get_time[1]
            else:
                update = input(y + "[*] " + R + "Update End Time? (" + self.end + ") [y|n]: ")
                if update == "y":
                    self.updateEndTime(self.end)

            read_file.close()
            self.loop()

        else:
            self.start = input("Start Time: ")
            self.end = input("End Time: ")

            self.save_yn = input("Save Times? [y|n]: ")

            if self.save_yn == "y":
                self.save()
            else:
                self.loop()

    def loop(self):
        self.start_split = self.start.split(":")
        self.end_split = self.end.split(":")

        self.now_hour = time.strftime("%H")
        self.now_minute = time.strftime("%M")
        self.now_second = time.strftime("%S")

        self.difference_hour = int(self.end_split[0]) - int(self.now_hour)
        self.difference_minutes = int(self.end_split[1]) - (int(self.now_minute) + 1)
        self.difference_seconds = 60 - int(self.now_second)

        if self.difference_seconds == 60:
            self.difference_seconds = 0

        if self.difference_hour == 0 and self.difference_minutes < 30:
            color = Fore.LIGHTYELLOW_EX
        else:
            color = Fore.LIGHTWHITE_EX

        print(color + "Countdown: " + "{:02d}".format(self.difference_hour) + ":" + "{:02d}".format(self.difference_minutes) + ":" + "{:02d}".format(self.difference_seconds) + R + "\r", end="")

        time.sleep(1)

        try:
            self.loop()
        except KeyboardInterrupt:
            print("")
            quit()


    def save(self):
        file = open("times.txt", "w")
        file.write(self.start + "|" + self.end + "|")
        file.close()

        print("")
        print("[*] Successfully saved to 'times.txt'.")
        print("")

        self.loop()

    def updateStartTime(self, starttime):
        read_file = open("times.txt", "r")
        get_end_time = read_file.read().split("|")[1]
        read_file.close()

        write_file = open("times.txt", "w")
        write_file.write(starttime + "|" + get_end_time)
        write_file.close()

        print(g + "[*] " + R + "Start Time successfully updated (" + starttime + ").")

    def updateEndTime(self, endtime):
        read_file = open("times.txt", "r")
        get_start_time = read_file.read().split("|")[0]
        read_file.close()

        write_file = open("times.txt", "w")
        write_file.write(get_start_time + "|" + endtime)
        write_file.close()

        print(g + "[*] " + R + "End Time successfully updated (" + endtime + ").")


Fahrt()