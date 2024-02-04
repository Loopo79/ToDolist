import flet as ft

class ToDoApp(ft.UserControl):
    def build(self):

        self.newTask = ft.TextField(hint_text="Whats needs to be done?",
                            multiline = True,
                            shift_enter = True,
                            on_submit = self.add_clicked,
                            )
        
        self.addButton = ft.ElevatedButton("Add",
                            icon="park_rounded",
                            icon_color="black",
                            on_click=self.add_clicked,
                            )
        self.tasks = ft.Column(controls = [])
        
        self.clearTasks = ft.ElevatedButton("Clear tasks",
                                            on_click = self.openAlert,
                                            )
        
        self.currentTask = ft.Dropdown(hint_text = 'Current Task',
                                       on_change = self.taskSelected,
                                       )
        
        self.menu = ft.Row( [self.newTask,
                             self.addButton,
                             self.clearTasks,
                             ],
                              width = 1000 )
        
        self.ColumnTotal = ft.Column(controls = [self.menu,
                                        self.currentTask,
                                        self.tasks,
                                        ],
                            width = 1000)

        self.clearAllAlert = ft.AlertDialog(
            modal=True,
            title=ft.Text("Select a choice"),
            content=ft.Text("What tasks do you want to clear?"),
            actions=[
                ft.TextButton("Clear all tasks", on_click=self.clearAllTasks),
                ft.TextButton("Clear all completed tasks", on_click=self.clearCompleted),
                ft.TextButton("Cancel", on_click=self.closeAlert),
                ],
            actions_alignment=ft.MainAxisAlignment.END,
            )

        self.completedTasks = []

        self.clickTimes = []
        
        return self.ColumnTotal

    def checkbox_changed(self,e):
        self.currentTask.options.clear()
        for i in self.tasks.controls:
            dropdowni = ft.dropdown.Option(i.label)
            if i.value == None:
                self.tasks.controls.remove(i)
            elif not i.value and i not in self.currentTask.options:
                self.currentTask.options.append(dropdowni)
            elif i not in self.completedTasks:
                self.clickTimes.append(1)
                text = "Congats! :) "
                if len(self.clickTimes) <= 5:
                    text += "(click it again to delete it)"
                
                self.completedTasks.append(i)
                self.page.snack_bar = ft.SnackBar(ft.Text(text),
                                             bgcolor = ft.colors.GREEN_500,
                                             duration = 2500,
                                             )
                self.page.snack_bar.open = True

        tup = ()
        for i in self.tasks.controls:
            tup += ( (i.label, i.value),)
        self.page.client_storage.set("tasks", tup)
        
        self.update()
        self.page.update()
        
    
    def add_clicked(self,e):
        newText = self.newTask.value.strip().replace('\n', '')
        if newText != '' and newText != ' ' * len(newText):
            check = ft.Checkbox(label=newText,
                                              on_change=self.checkbox_changed,
                                              tristate = True,
                                              value = False)
            self.currentTask.options.append(ft.dropdown.Option(newText))
            self.tasks.controls.append(check)
            self.newTask.value = ""
            self.newTask.focus()

            tup = ()
            for i in self.tasks.controls:
                tup += ( (i.label, i.value),)
            self.page.client_storage.set("tasks", tup)

        self.update()

    
    def openAlert(self,e):
        self.page.dialog = self.clearAllAlert
        self.page.dialog.open = True
        self.page.update()
        self.update()

    def clearAllTasks(self,e):
        self.clearAllAlert.open = False
        self.tasks.controls.clear()
        self.currentTask.options.clear()
        self.snack_bar = ft.SnackBar(ft.Text("All tasks cleared! :)"),
                                     bgcolor = ft.colors.GREEN,
                                     duration = 2500,
                                     )
        self.snack_bar.open = True
        self.page.update()
        self.update()


    def closeAlert(self,e):
        self.clearAllAlert.open = False
        self.page.update()
        self.update()

    def clearCompleted(self,e):
        for i in range(len(self.tasks.controls))[::-1]:
            if self.tasks.controls[i].value:
                self.tasks.controls.pop(i)
        self.clearAllAlert.open = False
        self.update()
        self.page.update()
    

    def taskSelected(self,e):
        self.snack_bar = ft.SnackBar(ft.Text(f"{self.currentTask.value} has been selected"),
                                     bgcolor = ft.colors.GREEN,
                                     duration = 2500,
                                     )
        self.snack_bar.open = True
        self.page.update()
        self.update()
    
    
def main(page: ft.Page):
    page.title = 'To do list'
    page.theme = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary=ft.colors.PURPLE,
        primary_container=ft.colors.YELLOW),
    )

    
    page.scroll = "adaptive"

    todo = ToDoApp()

    page.add(ft.Row(controls = [todo,
                                ],
                    vertical_alignment = ft.CrossAxisAlignment.START,
                    )
             )
    if todo.page.client_storage.contains_key("tasks"):

            for i in todo.page.client_storage.get("tasks"):

                for e in todo.tasks.controls:

                    if i[0] == e.label:
                        break

                else:
                    todo.tasks.controls.append( ft.Checkbox ( label = i[0],
                                                              value = i[1],
                                                              tristate = True,
                                                              on_change = todo.checkbox_changed,
                                                                ) )
                    todo.currentTask.options.append(ft.dropdown.Option( i[0] ))
    todo.update()

ft.app(main)