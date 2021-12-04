from tkinter import *

home_page = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Home page</title>
</head>
<body>
    <h1>Hello, my dear user!</h1>
</body>
</html>
'''

def create_window():
    # Create window
    win = Tk()
    win['bg'] = "#755c48"
    win.title("window")
    win.geometry("640x320")
    # Create widgets
    frame_toolbar = Frame(win, bg="red", height="30") # The frame for navigation menu
    frame_toolbar.place(relwidth="1")
    # Buttons
    back_button = Button(frame_toolbar, text="Назад", bg="pink", width="10")
    back_button.place(relheight="1")
    forward_button = Button(frame_toolbar, text="Вперед", bg="pink", width=10)
    forward_button.place(x=80, relheight=1)
    update_button = Button(frame_toolbar, text="Обновить", bg="pink", width=10)
    update_button.place(x=160, relheight=1)
    # Url bar
    urlbar = Entry(frame_toolbar, bg="pink")
    urlbar.place(x=240, relheight=1, relwidth=0.9)
    # Frame for browsing pages
    frame_context = Frame(win, bg="light blue")
    frame_context.place(y=30, relwidth=1, relheight=1)





    win.mainloop()

create_window()

