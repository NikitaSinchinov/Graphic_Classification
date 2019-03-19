# Программа для бинарной классификации графиков зарядки

import xlrd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

exel_data_file = xlrd.open_workbook('log_data_21.xlsx')
sheet = exel_data_file.sheet_by_index(0)

row_nubmer = sheet.nrows
cols_number = sheet.ncols

# Номера столбцов напряжение тока и Времени
voltage_col = 4
current_col = 5
date_col = 7

logg_date = []
logg_voltage = []
logg_current = []

# Берем дату и время записи
for row in range(1, row_nubmer):
    logg_date.append(sheet.cell_value(row, date_col))
    logg_voltage.append(sheet.cell_value(row, voltage_col))
    logg_current.append(sheet.cell_value(row, current_col))
    # "Перевернем" ток
    logg_current[row-1] = 1024 - logg_current[row-1]

    # Если по какой-либо причине данные в ячейке имеют некорректный формат, записать в ячейку время из предыдущей + 1 минута
    if type(logg_date[row - 1]) != float:
        logg_date[row - 1] = list(logg_date[row - 2])
        logg_date[row - 1][4] = logg_date[row - 1][4] + 1
    else:
        logg_date[row - 1] = list(xlrd.xldate_as_tuple(logg_date[row - 1], exel_data_file.datemode))

print(len(logg_voltage))

# Процедура поиска графиков на заданном отрезке
# sp - start point
# ep - end point
def graphic_find(sp, ep):
    mass = []  # На выходе в этот массив запишутся все найденные и нормализованные данные зарядок
    counter_c = 0  # Счетчик зарядок
    date_of = []  # В этом массиве хранятся дата и время каждой зарядки
    for point in range(sp, ep - 1):

        X = []
        Curr = []
        Volt = []
        I1 = logg_current[point]
        I2 = logg_current[point + 1]

        # Находим точку начала зарядки по значению и производной от тока
        if I2 > 500 and I2 - I1 > 20: #600
            print("___________________________")
            print("Начало: " + str(logg_date[point][:]))
            counter_points = 0   #Счетчик точек
            for end_point in range(point, ep - 1):
                #Вектор X содержит массив данных времени для каждой зарядки (пока не используется)
                X.append(logg_date[end_point])
                Curr.append(logg_current[end_point])
                Volt.append(logg_voltage[end_point])

                I1 = logg_current[end_point]
                I2 = logg_current[end_point + 1]
                U1 = logg_current[end_point]
                U2 = logg_current[end_point + 1]
                counter_points += 1
                if I2 < 500 and U2 - U1 < -30:
                    print("Конец: " + str(logg_date[end_point][:]))
                    print("___________________________")

                    if counter_points > 30:
                        #Добавляем в конец массива нормализованные данные тока и напряжения от новой найденной зарядки
                        mass.append([Curr, Volt])
                        date_of.append([])
                        date_of[counter_c].append(logg_date[point][:])
                        date_of[counter_c].append(logg_date[end_point][:])
                        counter_c += 1
                    break
    print("Найдено зарядок: ", counter_c)
    print("")
    return mass

# nn - no classification, no normalization database
nn_base = graphic_find(0, 10000)


def good_btn_clicked(event, sop):
    print("Правильная зарядка")
    cn_base_file = open("cn_base_file.txt", "a")
    cn_base_file.write(str(nn_base[sop][0]) + "\n")
    cn_base_file.write(str(nn_base[sop][1]) + "\n")
    cn_base_file.write("1" + "\n")
    cn_base_file.close()
    global cnt
    cnt += 1
    axes[0].clear()
    axes[1].clear()
    axes[0].grid(True)
    axes[1].grid(True)
    axes[0].plot(nn_base[cnt][0], "limegreen")
    axes[1].plot(nn_base[cnt][1], "darkviolet")
    plt.draw()

def hz_btn_clicked(event, sop):
    print("Не знаю")
    global cnt
    cnt += 1
    axes[0].clear()
    axes[1].clear()
    axes[0].grid(True)
    axes[1].grid(True)
    axes[0].plot(nn_base[cnt][0], "limegreen")
    axes[1].plot(nn_base[cnt][1], "darkviolet")
    plt.draw()
def bad_btn_clicked(event, sop):
    print("Плохая зарядка")
    cn_base_file = open("cn_base_file.txt", "a")
    cn_base_file.write(str(nn_base[sop][0]) + "\n")
    cn_base_file.write(str(nn_base[sop][1]) + "\n")
    cn_base_file.write("0" + "\n")
    cn_base_file.close()
    global cnt
    cnt += 1
    axes[0].clear()
    axes[1].clear()
    axes[0].grid(True)
    axes[1].grid(True)
    axes[0].plot(nn_base[cnt][0], "limegreen")
    axes[1].plot(nn_base[cnt][1], "darkviolet")
    plt.draw()

fig, axes = plt.subplots(nrows=2, ncols=1)
fig.subplots_adjust(left=0.08, bottom=0.19, right=0.95, top=0.94)

# Создадим оси для кнопки
axes_bad_btn_add = plt.axes([0.08, 0.05, 0.23, 0.075])
axes_hz_btn_add = plt.axes([0.4, 0.05, 0.23, 0.075])
axes_good_btn_add = plt.axes([0.72, 0.05, 0.23, 0.075])
# Создадим кнопки
bad_button = Button(axes_bad_btn_add, 'Неправильная')
hz_button = Button(axes_hz_btn_add, 'Не знаю')
good_button = Button(axes_good_btn_add, 'Правильная')

cnt = 0
axes[0].grid(True)
axes[1].grid(True)
axes[0].plot(nn_base[0][0], "limegreen")
axes[1].plot(nn_base[0][1], "darkviolet")

# Подпишемся на событие обработки нажатия кнопки
good_button.on_clicked(lambda event: good_btn_clicked(event, cnt))
hz_button.on_clicked(lambda event: hz_btn_clicked(event, cnt))
bad_button.on_clicked(lambda event: bad_btn_clicked(event, cnt))

plt.show()

