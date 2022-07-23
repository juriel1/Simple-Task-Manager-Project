from tkinter import *
from tkinter.font import Font
from tkinter import font

#-ROOT
root=Tk()
root.geometry("1200x700")
root.minsize(1200,700)
root.maxsize(1200,700)

#- MAIN FRAME
frame=Frame(root,width=300,height=300)
frame.pack(expand=True, fill=BOTH) #.grid(row=0,column=0)

#-MAIN CANVAS
size_scroll = 700
canvas=Canvas(frame,bg='#10494D',width=300,height=300,scrollregion=(0,0,500,size_scroll))

#-SCROLLBAR
vbar=Scrollbar(frame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)

#-CONFI MAIN CANVAS
canvas.config(width=1200,height=700)
canvas.config( yscrollcommand=vbar.set)
canvas.pack(side=LEFT,expand=True,fill=BOTH)

##--FONTS--##
entry_font = Font(size=35)
txt_tasks_font = Font(size=15)

###'--CLASS SYSTEM'--###
class system:
    number_task = 0
    List_task=[]
    txt_file = []
    state_btn_file = FALSE
    def new_task(self,txt,size_scroll_):
        reset_entry()
        t=Task()
        self.List_task.append(t.create(txt,170+150*self.number_task,self.number_task))
        self.number_task += 1
        if self.number_task>4:
            canvas.config(scrollregion=(0,0,500,size_scroll_+225))
            global size_scroll
            size_scroll +=225
    def delete_task(self,id,size_scroll_,txt):
        self.write_txt_file(self,txt,"d")
        self.number_task-=1
        canvas.delete(id)
        list = canvas.find_all()
        if self.number_task>3:
            canvas.config(scrollregion=(0, 0, 500, size_scroll_ - 225))
            global size_scroll
            size_scroll -= 225
        if len(list)+1>1:
            for e in range(id,list[-1]+1):
                canvas.move(e, 0, -150)
    def write_txt_file(self,txt,action):
        if action=="d":
            self.txt_file.remove(txt)
        if action=="a":
            self.txt_file.append(txt)
    def save_data(self):
        file_data = open("_data_.txt","w")
        for line in self.txt_file:
            file_data.write(line+"\n")
        file_data.close()
    def load_data(self):
        file_data = open("_data_.txt","r")
        for line in file_data.readlines():
            self.new_task(self,line,size_scroll)
    def move_obj(self,obje=Frame()):
        if self.state_btn_file == TRUE:
            obje.config(width=1, height=1)
            self.state_btn_file = FALSE
        else:
            obje.config(width=64, height=56)
            self.state_btn_file = TRUE

###'--CLASS TASK--'##
class Task:
    def create(self,txt,pos,num,sys=system):
        sys.write_txt_file(sys,txt,"a")
        frame_task = Frame(frame, width=950, height=215, bg="#0E2E59")
        txt_task = Label(frame_task, text="esto es el texto de una task", width=72, height=8, bg="#0E2E59",fg="white",font=txt_tasks_font,anchor='nw',wraplength=800)

        btn_delete = Button(frame_task, text="Delete", width=10, height=3, bg="#103466",fg="white")
        btn_hide = Button(frame_task, text="Hide", width=10, height=3, bg="#103466",fg="white")
        txt_task.place(x=5,y=5)
        txt_task.config(text=txt)
        btn_delete.place(x=825, y=70)
        btn_hide.place(x=825, y=10)
        win=canvas.create_window(475,pos, width=920, height=135, window=frame_task)
        id_ = win
        btn_delete.config(command=lambda :sys.delete_task(sys,id_,size_scroll,txt))
        btn_hide.config(command=lambda : self.hide_task(frame_task,txt_task,btn_delete,btn_hide))
        return win
    def hide_task(self,frame_=Frame,txt_=Label,btn_d=Button,btn_h=Button):
        frame_.config(bg="#104963")
        txt_.config(bg="#104963",fg="gray")
        btn_d.config(bg="#104963",fg="gray")
        btn_h.config(bg="#104963",fg="gray", text="Uncover",command=lambda : self.uncover_task(frame_,txt_,btn_d,btn_h))

    def uncover_task(self,frame_=Frame,txt_=Label,btn_d=Button,btn_h=Button):
        frame_.config(bg="#0E2E59")
        txt_.config(bg="#0E2E59",fg="white")
        btn_d.config(bg="#0E2E59",fg="white")
        btn_h.config(bg="#0E2E59",fg="white", text="Hide",command=lambda : self.hide_task(frame_,txt_,btn_d,btn_h))

#-ENTRY TASK
entry_task = Entry(canvas,width=30,font=entry_font,bg="#10494D",fg="white")
entry_task.place(x=20,y=40)
def reset_entry():
    entry_task.delete("0","end")

#- "DEF" FUNCION UX FOR BUTTONS
def changeOnHover(button, colorOnHover, colorOnLeave):
    button.bind("<Enter>", func=lambda e: button.config(background=colorOnHover))
    button.bind("<Leave>", func=lambda e: button.config(background=colorOnLeave))

#-BUTTON ENTRY TASK
sys = system
btn_task = Button(canvas,text="Add",width=10,height=3,bg="#135559",fg="white",relief=FLAT,command=lambda :sys.new_task(sys, entry_task.get(), size_scroll))
btn_task.place(x=825,y=39)
changeOnHover(btn_task, "#135559", "#10484D")

def call_new_task():
    sys.new_task(sys, entry_task.get(), size_scroll)
def on_enter(event):
    call_new_task()
entry_task.bind("<Return>",on_enter)

#-PANEL FILE
frame_btn_file = Frame(root,width=1,height=1,bg="white")#w=64,h=56
frame_btn_file.place(x=0,y=25)#24y

#-PANEL HIGHER WINDOW
frame_higher = Frame(root,width=1202,height=25,bg="white")
frame_higher.place(x=0,y=0)

#-BUTTON FILE
btn_file = Button(frame_higher,text="File",width=8,height=1,command=lambda :sys.move_obj(sys,frame_btn_file),bg="white",relief=FLAT)
btn_file.place(x=-2,y=-1)
changeOnHover(btn_file, "gray", "white")

#-BUTTON SAVE
btn_save = Button(frame_btn_file,text="Save",width=8,height=1,command=lambda :sys.save_data(sys),bg="white",relief=FLAT)
btn_save.place(x=0,y=0)
changeOnHover(btn_save, "gray", "white")

#-BUTTON LOAD
btn_load = Button(frame_btn_file,text="Load",width=8,height=1,command=lambda :sys.load_data(sys),bg="white",relief=FLAT)
btn_load.place(x=0,y=30)
changeOnHover(btn_load, "gray", "white")

###-ROO LOOP-###
root.mainloop()