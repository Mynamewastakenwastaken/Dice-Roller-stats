from tkinter import *

root = Tk()
root.title("Dice Roller")

Die_frame = LabelFrame(root, text="Dice", padx=8, pady=8)
Die_frame.pack(padx=10, pady=10)

Select_Label = Label(Die_frame, text="define dice").grid(row=0, column=2)
Active_Check0 = Checkbutton(Die_frame).grid(row=0, column=1)
Active_Check1 = Checkbutton(Die_frame).grid(row=1, column=1)
Active_Check2 = Checkbutton(Die_frame).grid(row=2, column=1)
Active_Check3 = Checkbutton(Die_frame).grid(row=3, column=1)
Active_Check4 = Checkbutton(Die_frame).grid(row=4, column=1)
Active_Check5 = Checkbutton(Die_frame).grid(row=5, column=1)
Active_Check6 = Checkbutton(Die_frame).grid(row=6, column=1)
Active_Check7 = Checkbutton(Die_frame).grid(row=7, column=1)
Active_Check8 = Checkbutton(Die_frame).grid(row=8, column=1)
Active_Check9 = Checkbutton(Die_frame).grid(row=9, column=1)
Active_Check10 = Checkbutton(Die_frame).grid(row=10, column=1)

Die_box1 = Entry(Die_frame, width=40).grid(row=1, column=2)
Die_box2 = Entry(Die_frame, width=40).grid(row=2, column=2)
Die_box3 = Entry(Die_frame, width=40).grid(row=3, column=2)
Die_box4 = Entry(Die_frame, width=40).grid(row=4, column=2)
Die_box5 = Entry(Die_frame, width=40).grid(row=5, column=2)
Die_box6 = Entry(Die_frame, width=40).grid(row=6, column=2)
Die_box7 = Entry(Die_frame, width=40).grid(row=7, column=2)
Die_box8 = Entry(Die_frame, width=40).grid(row=8, column=2)
Die_box9 = Entry(Die_frame, width=40).grid(row=9, column=2)
Die_box10 = Entry(Die_frame, width=40).grid(row=10, column=2)

Primary_Label = Label(Die_frame, text="primary").grid(row=0, column=3)
Primary_Check1 = Radiobutton(Die_frame).grid(row=1, column=3)
Primary_Check2 = Radiobutton(Die_frame).grid(row=2, column=3)
Primary_Check3 = Checkbutton(Die_frame).grid(row=3, column=3)
Primary_Check4 = Checkbutton(Die_frame).grid(row=4, column=3)
Primary_Check5 = Checkbutton(Die_frame).grid(row=5, column=3)
Primary_Check6 = Checkbutton(Die_frame).grid(row=6, column=3)
Primary_Check7 = Checkbutton(Die_frame).grid(row=7, column=3)
Primary_Check8 = Checkbutton(Die_frame).grid(row=8, column=3)
Primary_Check9 = Checkbutton(Die_frame).grid(row=9, column=3)
Primary_Check10 = Checkbutton(Die_frame).grid(row=10, column=3)

clicked = StringVar()
clicked.set("Sum")
Status_Drop1 = OptionMenu(Die_frame, clicked, "Sum", "Max", "Min").grid(row=1, column=4)
Status_Drop2 = OptionMenu(Die_frame, clicked, "Sum", "Max", "Min").grid(row=2, column=4)
Status_Drop3 = OptionMenu(Die_frame, clicked, "Sum", "Max", "Min").grid(row=3, column=4)
Status_Drop4 = OptionMenu(Die_frame, clicked, "Sum", "Max", "Min").grid(row=4, column=4)
Status_Drop5 = OptionMenu(Die_frame, clicked, "Sum", "Max", "Min").grid(row=5, column=4)
Status_Drop6 = OptionMenu(Die_frame, clicked, "Sum", "Max", "Min").grid(row=6, column=4)
Status_Drop7 = OptionMenu(Die_frame, clicked, "Sum", "Max", "Min").grid(row=7, column=4)
Status_Drop8 = OptionMenu(Die_frame, clicked, "Sum", "Max", "Min").grid(row=8, column=4)
Status_Drop9 = OptionMenu(Die_frame, clicked, "Sum", "Max", "Min").grid(row=9, column=4)
Status_Drop10 = OptionMenu(Die_frame, clicked, "Sum", "Max", "Min").grid(row=10, column=4)



def Dice_Correct(*args):      #function to return readable dice
    for x in args:
        if ',' in x:
            return x
        else:
            temp = list([val for val in x if val.isnumeric()])
            return "".join(temp)
def Dice_Construct(*args):
    for x in args:
        if ',' in x:
            temp = [float(e) for e in x.split(',')]
            return temp
        else:
            size = int(x)
            temp = []
            for i in range(0, size):
                temp.append(i+1)
            return temp

root.mainloop()