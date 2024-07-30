from threading import Thread
import queue
from time import sleep


class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False


class Customer:
    def __init__(self, number):
        self.number = number


class Cafe:
    def __init__(self, tables_):
        self.queue = queue.Queue()
        self.tables = tables_

    def customer_arrival(self):
        LIMIT = 20
        threads = []
        for i in range(LIMIT):
            print(f'Посетитель номер {i + 1} прибыл.')
            customer = Customer(i + 1)
            threads.append(Thread(target=self.reception, args=(customer,)))
            threads[-1].start()
            sleep(1)
        for thread in threads:
            thread.join()

    def reception(self, customer):
        current_tables = [table.is_busy for table in self.tables]
        if all(current_tables):
            self.queue.put(customer)
            print(f'Посетитель номер {customer.number} ожидает свободный стол.')
        else:
            self.serve_customer(customer)

    def serve_customer(self, customer):
        current_tables = [table.is_busy for table in self.tables]
        free_table_i = current_tables.index(False)
        print(f'Посетитель номер {customer.number} сел за стол {free_table_i + 1}')
        self.tables[free_table_i].is_busy = True
        sleep(5)
        print(f'Посетитель номер {customer.number} покушал и ушёл.')
        self.tables[free_table_i].is_busy = False
        if not self.queue.empty():
            self.reception(self.queue.get())


# Создаем столики в кафе
table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

# Инициализируем кафе
cafe = Cafe(tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()
