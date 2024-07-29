from threading import Thread
from time import sleep


class Knight(Thread):
    def __init__(self, name, power):
        super().__init__()
        self.name = name
        self.power = power

    def run(self):
        print(f'{self.name}, на нас напали!')
        enemies_left = 100
        current_day = 0
        while enemies_left > 0:
            sleep(1)
            enemies_left -= self.power
            current_day += 1
            print(f'{self.name} сражается {current_day} дней(дня)..., осталось {enemies_left} воинов.')
        print(f'{self.name} одержал победу спустя {current_day} дней(дня)!')


first_knight = Knight('Sir Lancelot', 10)
second_knight = Knight("Sir Galahad", 20)

first_knight.start()
sleep(1.1)
second_knight.start()

first_knight.join()
second_knight.join()

print('Все битвы закончились!')
