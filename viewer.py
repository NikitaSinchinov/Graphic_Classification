import matplotlib.pyplot as plt

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


i = 0
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
        wrong_volt.append(a[i+2])



fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12,8))
fig.subplots_adjust(left=0.06, bottom=0.08, right=0.97, top=0.89, wspace=0.1, hspace=0.25)
plt.suptitle("Некорректный заряд                                         Корректный заряд", weight='bold', size='xx-large')
axes[0, 0].grid(True)
axes[0, 0].set_title("Токи")
#axes[0, 0].plot(right_curr[0])

axes[0, 1].grid(True)
axes[0, 1].set_title("Токи")
#axes[0, 1].plot(wrong_curr[0])

axes[1, 0].grid(True)
axes[1, 0].set_title("Напряжения")
#axes[1, 0].plot(right_volt[0])

axes[1, 1].grid(True)
axes[1, 1].set_title("Напряжения")
#axes[1, 1].plot(wrong_volt[0])
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
print("неправильных: ", counter)
plt.show()

