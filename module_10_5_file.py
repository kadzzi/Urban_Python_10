from os import path
from multiprocessing import Process, Lock
import pickle


lock = Lock()


class WarehouseManager:

    def process_request(self, request):

        lock.acquire()

        if path.isfile('shared_data.pkl'):
            with open('shared_data.pkl', 'rb') as file:
                self.data = pickle.load(file)
        else:
            self.data = {}

        if request[0] in self.data.keys():
            match request[1]:
                case "receipt":
                    self.data[request[0]] += request[2]
                case "shipment":
                    if self.data[request[0]] < request[2]:
                        print(f'Невозможно огрузить {request[2]} {request[0]}! В наличии {self.data[request[0]]}')
                    elif self.data[request[0]] == request[2]:
                        self.data[request[0]] -= request[2]
                        print(f'Товар {request[0]} закончился!')
                    else:
                        self.data[request[0]] -= request[2]
        else:
            match request[1]:
                case "receipt":
                    self.data[request[0]] = request[2]
                case "shipment":
                    print(f'Товара {request[0]} нет в наличии!')
        with open('shared_data.pkl', 'wb') as file:
            pickle.dump(self.data, file)

        lock.release()

    def run(self, requests_):
        current_processes = []
        for request in requests_:
            current_processes.append(Process(target=self.process_request, args=(request,)))
            current_processes[-1].start()
        for process in current_processes:
            process.join()
        with open('shared_data.pkl', 'rb') as file:
            self.data = pickle.load(file)

        # from multiprocessing import Pool
        # with Pool(processes=len(requests_)) as p:
        #     p.map(self.process_request, requests_)
        # with open('shared_data.pkl', 'rb') as file:
        #     self.data = pickle.load(file)


if __name__ == "__main__":
    # Создаем менеджера склада
    manager = WarehouseManager()

    # Множество запросов на изменение данных о складских запасах
    requests = [
        ("product1", "receipt", 100),
        ("product2", "receipt", 150),
        ("product1", "shipment", 30),
        ("product3", "receipt", 200),
        ("product2", "shipment", 50)
    ]

    # Запускаем обработку запросов
    manager.run(requests)

    # Выводим обновленные данные о складских запасах
    print(manager.data)
