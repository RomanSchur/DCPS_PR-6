import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from matplotlib.colors import ListedColormap

def create_area(rows, number_E, number_T):
    area = []
    for _ in range(rows):
        line = create_line(number_E, number_T)#фурмувуання рядка
        area.append(line)
    return np.array(area)

def create_line(number_E, number_T):
    live_trees = [0] * number_T
    dead_trees = [1] * number_E
    line = live_trees + dead_trees
    random.shuffle(line)#рандомно розміщуємо згорівші і живі дерева
    return line

def choose_start_tree(rows, column,area, T_burn):
    row = random.randint(0, rows - 1)#вибір рандомного рядка
    col = random.randint(0, column - 1)#вибір рандомної колонки
    area[row, col] = T_burn #дерево на пересіченні загоряється
    return area

def update(area, P_burn, rows, column, T_burn):
    copy_area = np.copy(area)
    for i in range(rows):
        for j in range(column):
            if copy_area[i, j] > 1:#дерево яке горить
                copy_area[i, j] -= 1#зменшення часу горіння
                if copy_area[i, j] == 1:
                    copy_area[i, j] = 1#якщо час горіння пройшо,то дерево стає згорівшим
            elif copy_area[i, j] == 0:#якщо дерево живе
                neighbors = []
                if i > 0:
                    neighbors.append(area[i - 1, j])
                if i < rows - 1:
                    neighbors.append(area[i + 1, j])
                if j > 0:
                    neighbors.append(area[i, j - 1])
                if j < column - 1:
                    neighbors.append(area[i, j + 1])

                if any(n > 1 for n in neighbors) and random.random() < P_burn:#якщо є сусідні дерева,як горять
                    copy_area[i, j] = T_burn
    return copy_area

def create_visualization(area):
    colors = ["green", "black", "yellow", "orange", "red"] #для позначення стану дерев
    сolormap = ListedColormap(colors)
    figure, graph = plt.subplots()#створення фігури і графіка
    img = graph.imshow(area, animated=True, cmap=сolormap, vmin=0, vmax=4)#зображення додаєься на графік
    graph.set_xticks([])#видалення міток осі х
    graph.set_yticks([])#видалення міток осі н
    return figure, img

def update_visualization(frame, area, img, P_burn, rows, column, T_burn):
    updated_area = update(area, P_burn, rows, column, T_burn)#оновлюємо полотно
    img.set_array(updated_area)#заміна старої іформації
    return img, updated_area

def main():
    while True:
        try:
            rows = int(input("Введіть кількість рядків простору: "))
            if rows > 0:
                break
            else:
                print("Кількість рядків має бути більше 0!")
        except ValueError:
            print("Некоректний ввід. Введіть ціле число.")

    while True:
        try:
            column = int(input("Введіть довжину рядка: "))
            if column > 0:
                break
            else:
                print("Довжина кожного рядка має бути більше 0!")
        except ValueError:
            print("Некоректний ввід. Введіть ціле число.")

    while True:
        try:
            num_E = int(input("Введіть початкову кількість згорілих дерев: "))
            if num_E >= 0:
                break
            else:
                print("Кількість згорілих дерев не може бути від'ємною!")
        except ValueError:
            print("Некоректний ввід. Введіть ціле число.")

    while True:
        try:
            num_T = int(input("Введіть початкову кількість живих дерев: "))
            if num_T >= 0:
                break
            else:
                print("Кількість живих дерев не може бути від'ємною!")
        except ValueError:
            print("Некоректний ввід. Введіть ціле число.")

    while True:
        sum_trees = num_E + num_T
        if sum_trees > column:
            print("Кількість згорілих і здорових дерев не повинна бути більшою за площу!:")
            num_E = int(input("Введіть початкову кількість згорілих дерев: "))
            num_T = int(input("Введіть початкову кількість живих дерев: "))
        else:
            break

    while True:
        try:
            P_burn = float(input("Введіть шанс загоряння(0.0 - 1.0): "))
            if 0 <= P_burn <= 1:
                break
            else:
                print("Шанс загоряння повинен бути в діапазоні від 0.0 до 1.0!")
        except ValueError:
            print("Некоректний ввід. Введіть число з плаваючою комою")

    while True:
        try:
            T_burn = int(input("Введіть час горіння дерева (2-4): "))
            if 2 <= T_burn <= 4:
                break
            else:
                print("Час повинен бути в діапазоні від 2 до 4!")
        except ValueError:
            print("Некоректний ввід. Введіть ціле число.")

    while True:
        try:
            Num_iterations = int(input("Введіть кількість кроків пожежі: "))
            if Num_iterations >= 0:
                break
            else:
                print("Кількість ітерацій не може бути від'ємним значенням!")
        except ValueError:
            print("Некоректний ввід. Введіть ціле число.")

    area = create_area(rows, num_E, num_T)#створення початкового полотна
    area = choose_start_tree(rows, column,area, T_burn)#додавання дерева з якого починається пожежа

    fig, img = create_visualization(area)#початкова візуалізація

    def update_frame(frame):
        nonlocal area  # для зовнішньої видимості
        img_returned, updated_area = update_visualization(frame, area, img, P_burn, rows, column, T_burn)#отримання оновленого зображення
        area = updated_area  # Оновлюємо area для наступної ітерації
        return img_returned,

    ani = animation.FuncAnimation(fig,update_frame,frames=Num_iterations,blit=False,repeat=False,interval=1000)# Створення анімацї
    plt.show()

if __name__ == "__main__":
    main()