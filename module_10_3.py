from threading import Thread, Lock

lock = Lock()


class BankAccount:
    def __init__(self):
        self.balance = 1000

    def deposit(self, amount):
        with lock:
            self.balance += amount
        print(f'Deposited {amount}, new balance is {self.balance}')

    def withdraw(self, amount):
        with lock:
            self.balance -= amount
        print(f'Withdrew {amount}, new balance is {self.balance}')


def deposit_task(some_account, amount):
    for _ in range(5):
        some_account.deposit(amount)


def withdraw_task(some_account, amount):
    for _ in range(5):
        some_account.withdraw(amount)


account = BankAccount()

deposit_thread = Thread(target=deposit_task, args=(account, 100))
withdraw_thread = Thread(target=withdraw_task, args=(account, 150))

deposit_thread.start()
withdraw_thread.start()

deposit_thread.join()
withdraw_thread.join()
