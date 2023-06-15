import dearpygui.dearpygui as dpg
import threading
import functools
from datetime import date, timedelta
from Program import Task, Program

def load_tasks_to_do(p: Program):
    tmp = list()
    for task in p.tasks:
        if task.state == Task.states[0]:
            tmp.append(task)
    return tmp

def load_finished_tasks(p: Program):
    tmp = list()
    for task in p.tasks:
        if task.state != Task.states[0]:
            tmp.append(task)
    return tmp


def task_block_to_do(task):
    with dpg.group(horizontal=True):
        dpg.add_text(task.title)
        dpg.add_text(task.description)
        dpg.add_text(task.deadline)
        dpg.add_text(task.state)
        def checkbox_callback(sender, app_data):
            group_id = dpg.get_item_parent(sender)
            dpg.delete_item(group_id)
            task.state = Task.states[1]
        dpg.add_checkbox(callback=checkbox_callback)

def task_block_done(task):
    with dpg.group(horizontal=True):
        dpg.add_text(task.title, tag="title")
        dpg.add_text(task.description)
        dpg.add_text(task.deadline)
        dpg.add_text(task.state)
        def checkbox_callback(sender, app_data):
            group_id = dpg.get_item_parent(sender)
            dpg.delete_item(group_id)
        dpg.add_checkbox(callback=checkbox_callback)

def tasks_to_do(prog):
    def inner():
        tasks = load_tasks_to_do(prog)
        with dpg.window(label="Tasks to do"):
            if len(tasks) == 0 or not tasks:
                dpg.add_text("No tasks to do!")
                return
            for task in tasks:
                task_block_to_do(task)
    return inner

def finished_tasks(prog):
    def inner():
        tasks = load_finished_tasks(prog)
        with dpg.window(label="Finised tasks"):
            if len(tasks) == 0 or not tasks:
                dpg.add_text("No tasks finished!")
                return
            for task in tasks:
                task_block_done(task)
                
    return inner

def open_tasks(prog):
    def inner():
        with dpg.window(label="Tasks"):
            dpg.add_button(label="Tasks to do", callback=tasks_to_do(prog))
            dpg.add_button(label="Finished tasks", callback=finished_tasks(prog))
    return inner

def add_task(prog):
    def inner():
        with dpg.window(label="Add task"):
            dpg.set_item_width(dpg.last_item(), width=300)
            title_input = dpg.add_input_text(label="Title")
            desc_input = dpg.add_input_text(label="Description")
            date_textbox = dpg.add_input_text(label="Deadline", default_value=(date.today()+timedelta(days=1)).strftime("%Y-%m-%d %H:%M"))
            
            def submit_task(sender, app_data):
                group_id = dpg.get_item_parent(sender)
                t = Task()
                t.title = dpg.get_value(title_input)
                t.description = dpg.get_value(desc_input)
                t.deadline = dpg.get_value(date_textbox)
                t.state = Task.states[0]
                prog.add_task(t)
                dpg.delete_item(group_id)
            dpg.add_button(label="Submit", callback=submit_task)
            
    return inner

def check_deadline(prog):
    for task in prog.tasks:
        if out := prog.check_deadline(task):
            window = dpg.get_item_alias("Primary Window")
            if window is not None:
                dpg.add_text(out[0], parent=window, color=out[1])
def schedule_check(prog):
    while True:
        check_deadline(prog)
        threading.Event().wait(300)

if __name__ == "__main__":
    prog = Program()
    dpg.create_context()

    with dpg.window(tag="Primary Window"):
        dpg.add_text("Welcome, shef jan!")
        dpg.add_button(label="Check tasks", callback=open_tasks(prog))
        dpg.add_button(label="Add task", callback=add_task(prog))
        
    threading.Thread(target=schedule_check, args=(prog,), daemon=True).start()

    dpg.create_viewport(title='To Do List', width=600, height=200)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()