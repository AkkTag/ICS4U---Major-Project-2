from pathlib import Path
from tkinter import Label, Tk, Canvas, Entry, Button, PhotoImage, StringVar
from PIL import Image, ImageTk

def setup_login_page():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Akshaj Homework\ICS4U - Major Project 2\build\assetsLogin\frame0")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    

    window = Tk()
    window.geometry("896x640")
    window.configure(bg="#FFA1F8")
    window.title("Game Login")
    action_var = StringVar(value="")

    def on_login():
        username.delete(0, 'end')
        password.delete(0, 'end')
        action_var.set("login")
        window.withdraw()

    def on_signup():
        username.delete(0, 'end')
        password.delete(0, 'end')
        action_var.set("signup")
        window.withdraw()

    def on_close():
        action_var.set("closed")

    def removeUserholder(text):
        # x=100.0,
        # y=94.0,
        # width=286.0,
        # height=60.0
        #usernamePlaceholder.place_configure(x=110.0, y=94.0, width=276.0, height=60.0)
        if len(text) > 0:
            usernamePlaceholder.config(text="")
            usernamePlaceholder.place_configure(x=376.0, y=94.0, width=10.0, height=60.0)
        else:
            usernamePlaceholder.config(text="Username")
            usernamePlaceholder.place_configure(x=110.0, y=94.0, width=276.0, height=60.0)

    def removePassholder(text):
        # x=520.0,
        # y=94.0,
        # width=278.0,
        # height=60.0
        #passwordPlaceholder.place_configure(x=530.0, y=94.0, width=268.0, height=60.0)
        if len(text) > 0:
            passwordPlaceholder.config(text="")
            passwordPlaceholder.place_configure(x=788.0, y=94.0, width=10.0, height=60.0)
        else:
            passwordPlaceholder.config(text="Password")
            passwordPlaceholder.place_configure(x=535.0, y=94.0, width=263.0, height=60.0)
    

    def on_username_edit(event):
        removeUserholder(username.get())
    
    def on_password_edit(event):
        removePassholder(password.get())


    def on_entry_focus_in(event):
        event.widget.config(insertwidth=2)  # normal visible caret

    def on_entry_focus_out(event):
        event.widget.config(insertwidth=0) #hide caret when not focused

    #pygame.mixer.music.load(relative_to_assets("bg music.mp3"))
    #pygame.mixer.music.play(-1) #play bg music on loop

    canvas = Canvas(
        window,
        bg="#3232ff",
        width=900,
        height=640,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)
    canvas.bind("<Button-1>", lambda e: window.focus_set())  # Unfocus entries when clicking canvas

    canvas.create_rectangle(
        28.0,
        30.0,
        872.0,
        613.0,
        fill="#7dafff",
        outline=""
    )

    og_title = Image.open(relative_to_assets("Dynastic Title Image Source.png"))

    # shrink to 70% of the original size
    new_t_width = int(og_title.width * 0.59)
    new_t_height = int(og_title.height * 0.745)

    small_title = og_title.resize((new_t_width, new_t_height), Image.Resampling.LANCZOS)
    title_image = ImageTk.PhotoImage(small_title)

    #title_image = PhotoImage(file=relative_to_assets("Dynastic Title Image Source.png"))
    canvas.create_image(450.0, 322.0, image=title_image)

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    
    entry_bg_1 = canvas.create_image(
        241.0,
        126.5,
        image=entry_image_1
    )
    username = Entry(
        bd=0,
        bg="#529AFF",
        fg="light blue",
        insertbackground="light blue",
        highlightthickness=0,
        font=("Bold", 20)
    )
    username.place(
        x=90.0,
        y=94.0,
        width=296.0,
        height=60.0
    )

    username.bind("<KeyRelease>", on_username_edit)

    username.bind("<FocusIn>", on_entry_focus_in)
    username.bind("<FocusOut>", on_entry_focus_out)

    usernamePlaceholder = Label(
        master=window,
        text="Username",
        fg="light blue",
        bg="#529AFF",
        font=("Bold", 25)
    )

    usernamePlaceholder.place(
        x=100.0,
        y=94.0,
        width=286.0,
        height=60.0
    )

    usernamePlaceholder.bind("<Button-1>", lambda e: username.focus())

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    
    entry_bg_2 = canvas.create_image(
        661.0,
        127.0,
        image=entry_image_2,
        anchor="center"
    )
    password = Entry(
        bd=0,
        bg="#529AFF",
        fg="light blue",
        insertbackground="light blue",
        highlightthickness=0,
        font=("Bold", 20)
    )
    password.place(
        x=515.0,
        y=94.0,
        width=283.0,
        height=60.0
    )

    password.bind("<KeyRelease>", on_password_edit)

    password.bind("<FocusIn>", on_entry_focus_in)
    password.bind("<FocusOut>", on_entry_focus_out)


    passwordPlaceholder = Label(
        master=window,
        text="Password",
        fg="light blue",
        bg="#529AFF",
        font=("Bold", 25),
    )

    passwordPlaceholder.place(
        x=525.0,
        y=94.0,
        width=273.0,
        height=60.0
    )

    passwordPlaceholder.bind("<Button-1>", lambda e: password.focus())

    #username entry image
    # entry_image_1 = PhotoImage(file=relative_to_assets("username.png"))
    # canvas.create_image(456.0, 162.0, image=entry_image_1)

    # username = Entry(
    #     bd=0,
    #     bg="#529AFF",
    #     fg="light blue",
    #     highlightthickness=0,
    #     font=("Bold", 30)
    # )
    # username.place(
    #     x=97.0,
    #     y=114.0,
    #     width=718.0,
    #     height=85.0
    # )

    

    # entry_image_2 = PhotoImage(file=relative_to_assets("password.png")) #
    # canvas.create_image(456.0, 306.0, image=entry_image_2)

    # password = Entry(
    #     bd=0,
    #     bg="#529AFF",
    #     fg="light blue",
    #     highlightthickness=0,
    #     font=("Bold", 30),
    # )
    # password.place(
    #     x=97.0,
    #     y=260.0,
    #     width=718.0,
    #     height=85.0
    # )

    

    # removeUserholder(username.get())
    # removePassholder(password.get())

    def on_window_map(event):
        # When the window is deiconified (mapped), ensure placeholders match entry contents
        removeUserholder(username.get())
        removePassholder(password.get())

    window.bind("<Map>", on_window_map)
    
    og_bg = Image.open(relative_to_assets("bg image.png"))

    cropped_image = og_bg.crop((0, 0, 900, 560))
    bg_image = ImageTk.PhotoImage(cropped_image)

    #canvas.create_image(43.0, 70.0, image=bg_image, anchor="nw")
    
    # button_image_1 = PhotoImage(file=relative_to_assets("login_button.png"))
    
    # button_1 = Button(
    #     image=button_image_1,
    #     borderwidth=0,
    #     highlightthickness=0,
    #     command=on_login,
    #     relief="flat"
    # )

    # button_1.place(
    #     x=240.0,
    #     y=490.0,
    #     width=188.40599060058594,
    #     height=74.92960357666016
    # )

    # button_image_2 = PhotoImage(file=relative_to_assets("signup_button.png"))
    
    # button_2 = Button(
    #     image=button_image_2,
    #     borderwidth=0,
    #     highlightthickness=0,
    #     command=on_signup,
    #     relief="flat"
    # )

    # button_2.place(
    #     x=475.0,
    #     y=490.0,
    #     width=204.1064910888672,
    #     height=74.92960357666016
    # )

    button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
    
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=on_login,
        relief="flat"
    )
    button_1.place(
        x=230.0,
        y=493.0,
        width=188.40599060058594,
        height=74.92960357666016
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=on_signup,
        relief="flat"
    )
    button_2.place(
        x=483.0,
        y=493.0,
        width=204.1064910888672,
        height=74.92960357666016
    )
    



    


    # canvas.create_line(
    #     28.0,
    #     27.0,
    #     28.0,
    #     573.0,
    #     fill="#529AFF",
    #     width=2
    # )

    # canvas.create_line(
    #     28.0,
    #     27.0,
    #     872.0,
    #     27.0,
    #     fill="#529AFF",
    #     width=2
    # )

    window.resizable(False, False)
    window.protocol("WM_DELETE_WINDOW", on_close)
    
    window.photo_images = [
        entry_image_1,
        entry_image_2,
        button_image_1,
        button_image_2,
        bg_image,
        title_image,
        button_image_1,
        button_image_2,
    ]

    return window, action_var, username, password
