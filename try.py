import argparse
import time

def task1():
    print("Task 1 is running")
    # Simulate a long-running task
    time.sleep(5)
    print("Task 1 is done")

def task2():
    print("Task 2 is running")
    # Simulate a long-running task
    time.sleep(3)
    print("Task 2 is done")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run different tasks.')
    parser.add_argument('task', choices=['task1', 'task2'], help='The task to run')

    args = parser.parse_args()

    if args.task == 'task1':
        task1()
    elif args.task == 'task2':
        task2()
