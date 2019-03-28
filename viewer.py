import matplotlib.pyplot as plt
import mplcursors

f = open("cn_base_file.txt", 'r')
a = f.readlines()

right_volt = []
right_curr = []
wrong_volt = []
wrong_curr = []

for each in range(0, len(a)):
    if (a[each].replace("\n", "") == '0') or (a[each].replace("\n", "") == '1'):
        a[each] = float(a[each])
    else:
        a[each] = a[each].split(" ")
        for el in range(0, len(a[each])):
            a[each][el] = float(a[each][el])

'''i = 0
while i < len(a)-4:
    if i == 0:
        i = i + 2
    else:
        i = i + 3
    if a[i] == 1:
        right_curr.append(a[i+1])
        right_volt.append(a[i+2])
    elif a[i] == 0:
        wrong_curr.append(a[i+1])
        wrong_volt.append(a[i+2])'''



fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12,8))
fig.subplots_adjust(left=0.06, bottom=0.08, right=0.97, top=0.89, wspace=0.1, hspace=0.25)
plt.suptitle("Некорректный заряд                                           Корректный заряд",
             weight='bold', size='xx-large')
axes[0, 0].grid(True)
axes[0, 0].set_title("Токи")

axes[0, 1].grid(True)
axes[0, 1].set_title("Токи")

axes[1, 0].grid(True)
axes[1, 0].set_title("Напряжения")

axes[1, 1].grid(True)
axes[1, 1].set_title("Напряжения")

'''
counter = 0
for graph in range(0, len(right_curr)):
    axes[0, 0].plot(right_curr[graph])
    axes[1, 0].plot(right_volt[graph])
    counter += 1
print("Правильных: ", counter)
counter = 0
for graph in range(0, len(wrong_curr)):
    axes[0, 1].plot(wrong_curr[graph])
    axes[1, 1].plot(wrong_volt[graph])
    counter += 1
print("Неправильных: ", counter)'''

i = 2000
while i < 2200: # - 4
    if i == 0:
        i = i + 2
    else:
        i = i + 3

    if a[i] == 1:
        axes[0, 1].plot(a[i-2], gid=i)
        axes[1, 1].plot(a[i-1], gid=i)
    elif a[i] == 0:
        axes[0, 0].plot(a[i-2], gid=i)
        axes[1, 0].plot(a[i-1], gid=i)

def find_time(event):
    for curve in axes[1, 1].get_lines():
        if curve.contains(event)[0]:
            setted_curr = []
            setted_volt = []
            print("Строки данных этого графика для тока и напряжения соответственно: ")
            setted_curr = curve.get_gid()-1
            print(setted_curr)
            setted_volt = curve.get_gid()
            print(setted_volt)
            


fig.canvas.mpl_connect("button_press_event", find_time)
print(a[8])
plt.show()