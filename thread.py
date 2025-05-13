import threading
import multiprocessing
import time 
import queue

shared_queue = queue.Queue()


def cpu_bound_task():
    total = 0
    for i in range(10**8):  
        total += i
    print(f"CPU-bound task result: {total}")

def print_numbers():
    for i in range(10):
        print(f"number : {i}")
        shared_queue.put(i)
        cpu_bound_task()
        time.sleep(1)

def print_letter():
    while True:
        try:
            number = shared_queue.get(timeout=3)
            print(f"letter: corresponding to number {number}")
            time.sleep(1)
        except queue.Empty:
            break

def elements_queue():
    while True:
        try:
            number1 = shared_queue.get(timeout=3)
            print(f"letter: to number {number1}")
            time.sleep(1)
        except queue.Empty:
            break  

def after_all_thread():
    print("✅ All previous t hread fiinish.This is the final thread.")
    time.sleep(1)
    try:
        number1 = shared_queue.get_nowait()
        print(f"letter: to number {number1}")
    except queue.Empty:
        print("Queue is empty. No more items to process.")

    print("🎉 Done with everything!")
    
    

def process_job():
    t1 = threading.Thread(target=print_numbers)
    t2 = threading.Thread(target=print_letter)
    t3 = threading.Thread(target=elements_queue)

    t1.start()
    t2.start()
    t3.start()

# Wait for t1, t2, and t3 to complete
    t1.join()
    t2.join()
    t3.join()

    print("✅ Done with multithreading")

# Now run the last thread
    t4 = threading.Thread(target=after_all_thread)
    t4.start()
    t4.join()
    
    
if __name__ == "__main__":
    p=multiprocessing.Process(target=process_job)
    p.start()
    p.join()

    print("✔️ Main program done")
