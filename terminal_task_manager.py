import json
import time
from datetime import datetime
from pathlib import Path

class TaskManager:
    
    task_schema = {
        "task_name" : str,
        "task_description" : str | None,
        "task_status" : str,
        "task_creation_date" : int,
        "task_deadline" : int | None,
        "task_completion_date" : int | None,
    }
    
    def __init__(self, file_path = 'tasks.json'):
        self.file_path = Path(file_path)
        
        # Create the file if it does not exist
        if not self.file_path.exists():
            with open(file_path, 'w') as f:
                json.dump([], f)
        
    def get_all_tasks(self):
        # Load all tasks from the file
        with open(self.file_path, 'r') as f :
            tasks = json.load(f)
        return tasks
    
    def save_task(self, task):
        tasks = self.get_all_tasks()
        exist = False
        for old_task in tasks:
            if old_task['task_name'] == task['task_name']:
                old_task.update(task)
                exist = True
                break
        if not exist:
            # Set default values for optional fields
            if 'task_description' not in task:
                task['task_description'] = None
                
            if 'task_deadline' not in task:
                task['task_deadline'] = None
                
            if 'task_completion_date' not in task:
                task['task_completion_date'] = None
                
            task['task_status'] = 'pending'
            task['task_creation_date'] = datetime.now().timestamp()
            
            tasks.append(task)
        
        # Save all tasks back to the file
        with open(self.file_path, 'w') as f:
            json.dump(tasks, f)
        
    def get_task(self, task_name):
        # Retrieve a specific task by name
        tasks = self.get_all_tasks()
        for task in tasks:
            if task['task_name'] == task_name:
                return task
        return None
    
    def delete_task(self, task_name):
        # Delete a specific task by name
        tasks = self.get_all_tasks()
        for task in tasks:
            if task['task_name'] == task_name:
                tasks.remove(task)
            
            with open(self.file_path, 'w') as f:
                json.dump(tasks, f)
            
            return True
        
        return False

def main():
    main_menu = """
    HI welcome To Terminal Task Manager
    
1. Add task
2. Get task
3. Delete task
4. List all tasks
5. Exit
    """
    
    print(main_menu)
    
    menu_choice : str = 'no choice'
    
    # Prompt user for a valid menu choice
    while not menu_choice.isdigit() or (int(menu_choice) < 1 and int(menu_choice) > 5):
        menu_choice = input("Enter your choice: ")
    
    menu_choice = int(menu_choice) # type: ignore
    
    task_manager = TaskManager()
    
    if menu_choice == 1:
        # Add a new task
        task_name = input("Enter task name: ")

        task = task_manager.get_task(task_name)

        if task is not None:
            print("Task already exists")
            return

        task_description = input("Enter task description: ")

        task_have_deadline = input("Do you want to set a deadline? (y/n): ").lower() == 'y'
        
        if task_have_deadline:
            task_deadline = input("Enter task deadline (YYYY-MM-DD): ")
            task_deadline = datetime.strptime(task_deadline, "%Y-%m-%d").timestamp()
        else:
            task_deadline = None
            
        task = {
            "task_name" : task_name,
            "task_description" : task_description,
            "task_deadline" : task_deadline,
        }
        
        task_manager.save_task(task)
        print("\n")
        print("Task saved successfully !")
        
        time.sleep(1)
        
        main()
        
    elif menu_choice == 2:
        # Get a specific task
        task_name = input("Enter task name: ")
        
        task = task_manager.get_task(task_name)
        
        if task is None:
            print("Task not found")
            return
        
        print("Task name:", task['task_name'])
        print("Task description:", task['task_description'])
        print("Task status:", task['task_status'])
        if task['task_deadline'] is not None:
            print("Task deadline:", datetime.fromtimestamp(task['task_deadline']).strftime("%Y-%m-%d"))
        else:
            print("Task deadline: No deadline")

        if task['task_completion_date'] is not None:
            print("Task completion date:", datetime.fromtimestamp(task['task_completion_date']).strftime("%Y-%m-%d"))
        else:
            print("Task completion date: Not completed")
            
        time.sleep(1)
        
        print("\n")
        
        get_task_menu = """
1. Edit task
2. Delete task
3. Go back to main menu
    """

        print(get_task_menu)
        
        get_task_choice : str = 'no choice'
        while not get_task_choice.isdigit() or (int(get_task_choice) < 1 and int(get_task_choice) > 3):
            get_task_choice = input("Enter your choice: ")

        get_task_choice = int(get_task_choice) # type: ignore
        
        get_task_main(task, get_task_choice)

    elif menu_choice == 3:
        # Delete a specific task
        task_name = input("Enter task name: ")
        
        task = task_manager.get_task(task_name)
        
        if task is None:
            print("Task not found")
            return
        
        task_manager.delete_task(task_name)
        print("\n")
        print("Task deleted successfully !")
        
        time.sleep(1)
        
        main()

    elif menu_choice == 4:
        # List all tasks
        tasks = task_manager.get_all_tasks()

        if len(tasks) == 0:
            print("No tasks found")
            return

        task_enum = [(i + 1, task) for i, task in enumerate(tasks)]
        
        for i, task in task_enum:
            print(f"{i}. {task['task_name']}")
            
        time.sleep(1)
        
        all_tasks_menu = """
1. select a task by number
2. Go back to main menu
    """

        print(all_tasks_menu)
        
        all_tasks_choice : str = 'no choice'
        while not all_tasks_choice.isdigit() or (int(all_tasks_choice) < 1 and int(all_tasks_choice) > 2):
            all_tasks_choice = input("Enter your choice: ")

        all_tasks_choice = int(all_tasks_choice) # type: ignore
        
        if all_tasks_choice == 1:
            task_number = input("Enter task number: ")
            task_number = int(task_number) - 1
            
            if task_number < 0 or task_number >= len(tasks):
                print("Invalid task number")
                return
            
            task = tasks[task_number]
            
            print("\n")
            print("Task name:", task['task_name'])
            print("Task description:", task['task_description'])
            print("Task status:", task['task_status'])
            if task['task_deadline'] is not None:
                print("Task deadline:", datetime.fromtimestamp(task['task_deadline']).strftime("%Y-%m-%d"))
            else:
                print("Task deadline: No deadline")
            if task['task_completion_date'] is not None:
                print("Task completion date:", datetime.fromtimestamp(task['task_completion_date']).strftime("%Y-%m-%d"))
            else:
                print("Task completion date: Not completed")

            time.sleep(1)
            
            get_task_main(task, 1)
    
        elif all_tasks_choice == 2:
            main()

def get_task_main(task, get_task_choice):
    task_manager = TaskManager()
    
    if get_task_choice == 1:
        # Edit the specific task
        should_edit_name = input("Do you want to edit the task name? (y/n): ").lower() == 'y'
        
        if should_edit_name:
            task_name = input("Enter new task name: ")
            task['task_name'] = task_name
            
        should_edit_description = input("Do you want to edit the task description? (y/n): ").lower() == 'y'

        if should_edit_description:
            task_description = input("Enter new task description: ")
            task['task_description'] = task_description
            
        should_edit_deadline = input("Do you want to edit the task deadline? (y/n): ").lower() == 'y'

        if should_edit_deadline:
            task_deadline = input("Enter new task deadline (YYYY-MM-DD): ")
            task_deadline = datetime.strptime(task_deadline, "%Y-%m-%d").timestamp()
            task['task_deadline'] = task_deadline
            
        should_edit_task_status = input("Do you want to edit the task status? (y/n): ").lower() == 'y'

        if should_edit_task_status:
            task_status = input("Enter new task status (completed/abandonned/pending): ").lower()
            task['task_status'] = task_status
            
        task_manager.save_task(task)
        print("\n")
        print("Task updated successfully !")
        
        time.sleep(1)
        
        main()
        
    elif get_task_choice == 2:
        # Delete the task
        task_manager.delete_task(task['task_name'])
        print("\n")
        print("Task deleted successfully !")
        
        main()
        
    elif get_task_choice == 3:
        # Go back to main menu
        main()
    
if __name__ == "__main__":
    main()
    