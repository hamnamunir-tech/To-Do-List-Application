import os
import datetime
TASKS_FILE = "tasks.txt"
class Task:
    def __init__(self, description, completed=False, deadline=None):
        self.description = description
        self.completed = completed
        self.deadline = deadline
    def __str__(self):
        status = "[x]" if self.completed else "[ ]"
        deadline_str = f" (Due: {self.deadline})" if self.deadline else ""
        return f"{status} {self.description}{deadline_str}"

    def to_file(self):
        return f"{self.description}|{self.completed}|{self.deadline if self.deadline else ''}\n"

    @staticmethod
    def from_file(line):
        parts = line.strip().split("|")
        description = parts[0]
        completed = parts[1] == "True"
        deadline = parts[2] if parts[2] else None
        return Task(description, completed, deadline)


def load_tasks():
    tasks = []
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            for line in file:
                tasks.append(Task.from_file(line))
    return tasks


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        for task in tasks:
            file.write(task.to_file())


def add_task():
    description = input("Enter task description: ")
    deadline = input("Enter deadline (YYYY-MM-DD) or press Enter to skip: ")
    try:
        deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d").date() if deadline else None
    except ValueError:
        print("Invalid date format. Task will be added without a deadline.")
        deadline = None

    tasks = load_tasks()
    tasks.append(Task(description, False, deadline))
    save_tasks(tasks)
    print("Task added successfully!")


def view_tasks():
    tasks = load_tasks()
    tasks.sort(key=lambda t: t.deadline if t.deadline else datetime.date.max)
    if not tasks:
        print("No tasks available.")
        return

    for index, task in enumerate(tasks, start=1):
        print(f"{index}. {task}")


def mark_completed():
    tasks = load_tasks()
    view_tasks()
    try:
        task_num = int(input("Enter task number to mark as completed: "))
        if 1 <= task_num <= len(tasks):
            tasks[task_num - 1].completed = True
            save_tasks(tasks)
            print("Task marked as completed!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")


def delete_task():
    tasks = load_tasks()
    view_tasks()
    try:
        task_num = int(input("Enter task number to delete: "))
        if 1 <= task_num <= len(tasks):
            del tasks[task_num - 1]
            save_tasks(tasks)
            print("Task deleted successfully!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")


def main():
    while True:
        print("\nTo-Do List Application")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            mark_completed()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()
