import subprocess
import tkinter as tk
import threading

def update_Dots():
    global stop_spinner
    dots = ['.', '..', '...']
    if not stop_spinner:
        current_dot = (update_Dots.counter % len(dots))
        status.config(text=f"Provádění ping{dots[current_dot]}")
        update_Dots.counter += 1
        root.after(750, update_Dots)


update_Dots.counter = 0

def ping_ip():
    
    if ip_address.get() != "":
        global stop_spinner
        stop_spinner = False
        update_Dots()

        result_label.config(text="")
        averageConnectSpeed.config(text="")
        button.config(state=tk.DISABLED)
        root.update_idletasks()
        ip = ip_address.get().split(";")
        expand = 0
        if (len(ip) > 8):
            expand = 30
        count = 0
        averageConnect = 0
        averageCount = 0;        
        

        for i in ip:
            try:
                response = subprocess.check_output(f"ping -n 4 {i}", shell=True, text=True)
                response = response.split(" ")
                if response[9] != "Destination":
                    times = [response[10],response[15],response[20],response[25]]
                    pingTime = []
                    for j in times:
                        if j.find("=") != -1:
                            pingTime.append(j[j.find("=")+1:j.find("s")-1])
                    if len(pingTime) != 0:
                        avg = 0
                        for j in pingTime:
                            if (j == "<1"):
                                avg += 0
                            avg += int(j)
                        averageConnect += avg / len(pingTime)
                        avg = str(round(avg,2) / len(pingTime)) + " ms"
                    else:
                        avg = "<1ms"
                        averageConnect += 0
                    previousText = result_label.cget("text")
                    previousText += f"Pinged: {i} průměrná odezva: {avg}\n\n"
                    if count > 6:
                        getX = root.geometry().find("x")
                        getPlus = root.geometry().find("+")
                        root.geometry(f"600x{int(root.geometry()[getX+1:getPlus]) + expand}")
                    result_label.config(text=previousText)
                    root.update_idletasks()
                    count += 1
                    averageCount += 1
                else: 
                    previousText = result_label.cget("text")
                    previousText += f"Pinged {i} Reply: Destination host unreachable\n\n"
                    if count > 6:
                        getX = root.geometry().find("x")
                        getPlus = root.geometry().find("+")
                        root.geometry(f"600x{int(root.geometry()[getX+1:getPlus]) + expand}")
                    result_label.config(text=previousText)
                    root.update_idletasks()
                    count += 1
            except subprocess.CalledProcessError:
                previousText = result_label.cget("text")
                previousText += f"Error pinging IP: {i}\n\n"
                if count > 6:
                    getX = root.geometry().find("x")
                    getPlus = root.geometry().find("+")
                    root.geometry(f"600x{int(root.geometry()[getX+1:getPlus]) + expand}")
                result_label.config(text=previousText)
                root.update_idletasks()
                count += 1
        stop_spinner = True
        if averageCount != 0:
            if averageConnect/averageCount != 0:
                averageConnect = round(averageConnect/averageCount,2)
            else:
                averageConnect = "<1"
            averageConnectSpeed.config(text=f"Celková průměrná odezva: {averageConnect} ms")
        else:
            pass
        button.config(state=tk.NORMAL)
        status.config(text="Výsledky ping:")
        previousText = result_label.cget("text")[:len(result_label.cget("text"))-2]
        result_label.config(text=previousText)
        root.update_idletasks()
    else:
        status.config(text="Zadejte prosím IP")
        root.update_idletasks()

def start_ping():
    threading.Thread(target=ping_ip, daemon=True).start()

root = tk.Tk()
root.title("Ping App")
root.geometry("600x400")

header = tk.Label(root,text="Zadejte IP pro ping:",font=("Arial",12,"bold"))
header.pack()

ip_address = tk.Entry(root, width=50)
ip_address.pack()


button = tk.Button(root, text="PING", command=start_ping)
button.pack(pady=5)

status = tk.Label(root,text="",font=("Arial",12,"bold"))
status.pack()

result_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
result_label.pack()

averageConnectSpeed = tk.Label(root, text="", font=("Arial", 12,"bold"), justify="left")
averageConnectSpeed.pack(pady=2)


root.mainloop()
