from threading import Thread
import time

class my_counter(Thread):

    def run(self):
        self.start_count()

    def start_count(self):
        for i in range(5):
            print("hey")
            # print(f"{self.name} is on {self.start}")
            # self.start += 1
            time.sleep(1)


if __name__ == '__main__':
    for i in range(3):
        t = my_counter()
        t.start()

