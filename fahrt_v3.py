import time
import os
import platform

justInstalled = False

try:
    from colorama import Fore, init
except ModuleNotFoundError:
    print("[!] Colorama not found.")
    install = input("[*] Would you like to install? [y|n]: ")

    if install == "y":
        print("[*] Installing colorama...")
        os.system("pip install colorama")
        print("[*] Colorama was successfully installed.")
        justInstalled = True

try:
    from win10toast import ToastNotifier
except ModuleNotFoundError:
    print("[!] Win10toast not found.")
    install = input("[*] Would you like to install? [y|n]: ")

    if install == "y":
        print("[*] Installing win10toast...")
        os.system("pip install win10toast")
        print("[*] win10toast was successfully installed.")
        justInstalled = True

if justInstalled:
    print("[!] Module(s) installed. Please restart this program.")
    quit()

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
            print("")
            self.loop()

        else:
            self.start = input("Start Time: ")
            self.end = input("End Time: ")

            self.save_yn = input("Save Times? [y|n]: ")

            if self.save_yn == "y":
                self.save()
            else:
                print("")
                self.loop()

    def loop(self):
        
        if platform.system() == "Linux":
            os.system("clear")
        else:
            os.system("cls")

        self.start_split = self.start.split(":")
        self.end_split = self.end.split(":")

        self.now_hour = time.strftime("%H")
        self.now_minute = time.strftime("%M")
        self.now_second = time.strftime("%S")

        self.difference_hour = int(self.end_split[0]) - int(self.now_hour)
        self.difference_minutes = int(self.end_split[1]) - (int(self.now_minute) + 1)
        self.difference_seconds = 60 - int(self.now_second)


        self.start_hour_to_secs = int(self.start_split[0]) * 60 * 60
        self.start_minutes_to_secs = int(self.start_split[1]) * 60        

        self.end_hours_to_secs = int(self.end_split[0]) * 60 * 60
        self.end_minutes_to_secs = int(self.end_split[1]) * 60 

        self.now_hour_to_secs = int(self.now_hour) * 60 * 60
        self.now_minute_to_secs = int(self.now_minute) * 60

        self.start_total_secs = self.start_hour_to_secs + self.start_minutes_to_secs
        self.end_total_secs = self.end_hours_to_secs + self.end_minutes_to_secs
        self.now_total_secs = self.now_hour_to_secs + self.now_minute_to_secs + int(self.now_second)


        self.difference_secs = self.end_total_secs - self.now_total_secs

        getTime = self.toTime(self.difference_secs)


 

        if int(getTime.split(":")[0]) == 0 and int(getTime.split(":")[1]) < 10:
            color = Fore.LIGHTRED_EX
        elif int(getTime.split(":")[0]) == 0 and int(getTime.split(":")[1]) < 30:
            color = Fore.LIGHTYELLOW_EX
        else:
            color = Fore.LIGHTWHITE_EX

        if int(getTime.split(":")[0]) <= 0 and int(getTime.split(":")[1]) <= 0 and int(getTime.split(":")[2]) <= 0:
            print(color + "[!] Time is up" + R)
            self.progress()

            if platform.system() == "Linux":
                os.system("notify-send 'Countdown Timer\nTime is up!'")
            else:
                toaster = ToastNotifier()
                toaster.show_toast("Countdown Timer","Time is up!")

            quit()
        else:
            print(color + "[>] Time Left: " + self.toTime(self.difference_secs) + R)
            self.progress()


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

    def toTime(self, seconds):
        hours = int(seconds / 60 / 60)
        mins = int((seconds - (hours * 60 * 60)) / 60)
        secs = int(seconds - (mins * 60))

        out = "{:02d}".format(hours) + ":" + "{:02d}".format(mins) + ":" + "{:02d}".format(secs)

        return out

    def progress(self):
        percent = (self.now_total_secs - self.start_total_secs) / (self.end_total_secs - self.start_total_secs) * 100

        if percent > 100:
            percent = 100

        done = "#"*int(percent)
        todo = " "*int(100 - percent)

        print("[" + done + todo + "] " + "{:3d}".format(int(percent)) + "%")

Fahrt()