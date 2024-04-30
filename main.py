class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def delete_task(self, task_number):
        try:
            del self.tasks[task_number - 1]
        except IndexError:
            print("Invalid task number.")

    def mark_complete(self, task_number):
        try:
            self.tasks[task_number - 1] = f"{self.tasks[task_number - 1]} (completed)"
        except IndexError:
            print("Invalid task number.")

    def display_tasks(self):
        for i, task in enumerate(self.tasks, 1):
            print(f"{i}. {task}")

def main():
    todo_list = ToDoList()
    while True:
        print("\n1. Add task\n2. Delete task\n3. Mark complete\n4. Display tasks\n5. Quit")
        option = input("Choose an option: ")
        if option == "1":
            task = input("Enter a task: ")
            todo_list.add_task(task)
        elif option == "2":
            task_number = int(input("Enter the task number to delete: "))
            todo_list.delete_task(task_number)
        elif option == "3":
            task_number = int(input("Enter the task number to mark complete: "))
            todo_list.mark_complete(task_number)
        elif option == "4":
            todo_list.display_tasks()
        elif option == "5":
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()