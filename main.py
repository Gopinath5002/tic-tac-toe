from customtkinter import *
from PIL import Image
import cv2

root = CTk()
root.title("Infinity War")
root.geometry('400x640')
root.minsize(400,640)
set_appearance_mode('system')

cap = cv2.VideoCapture('preview.mp4')

video_frame = CTkFrame(root, bg_color='black',fg_color='transparent')
video_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
label = CTkLabel(video_frame, text="")
label.pack(expand=True)

def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (400, 640))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = CTkImage(dark_image=img, size=(400, 640))
        label.imgtk = imgtk
        label.configure(image=imgtk)
        root.after(10, lambda : update_frame())
    else:
        cap.release()
        cv2.destroyAllWindows()
        root.after_cancel(update_frame)
        for i in root.winfo_children():
            i.destroy()
        front()

custom_font = CTkFont(family="Helvetica", size=40, weight="bold")
custom_font1 = CTkFont(family="Comic Sans MS", size=40, weight="bold")
turn_font=CTkFont(family='Helvetica',size=20,weight='bold')

initial=0
o_list=[]
x_list=[]
darked=[]
current_focus = [0, 0]
player_1='Player_1'
player_2='Player_2'

def check_won(arr):
    valid_arrs=[[1,2,3],[4,5,6],[7,8,9],[1,5,9],[3,5,7],[1,4,7],[2,5,8],[3,6,9]]
    if sorted(arr) in valid_arrs:
        return True
    return False

def play_again():
    global initial,current_focus
    for i in root.winfo_children():
        i.destroy()
    o_list.clear()
    x_list.clear()
    initial=initial%2
    current_focus=[0,0]
    mainwindow()

def end(player):
    if player_1==player:
        clr='red'
    else:
        clr='blue'
    for i in root.winfo_children():
        i.destroy()
    f1=CTkFrame(root,fg_color='transparent') 
    f1.place(relx=0,rely=0.1,relwidth=1,relheight=0.73) 
    lbl_frame=CTkFrame(f1,fg_color='transparent')
    lbl_frame.pack()
    lbl=CTkLabel(lbl_frame,text='Infinity ',text_color='red',font=custom_font1)
    lbl.pack(side='left',fill='both')
    lbl1=CTkLabel(lbl_frame,text='War',text_color='blue',font=custom_font1)
    lbl1.pack(side='left',fill='both')
    CTkLabel(f1,text=f'{player} Won the Match',bg_color='transparent',font=("Comic Sans MS",25),text_color=clr).pack(pady=30)
    CTkButton(f1,text='Play Again',font=("Comic Sans MS",25),border_width=2,corner_radius=25,command=play_again).pack(pady=30)

def connect(index,turn_lbl,typ,main_map):
    global initial,o_list,x_list
    if typ%2==0:
        cur_list=x_list
        cur_color='red'
        turn=f"O : {player_2}'s Turn"
        turn_color='blue'
        typ='X'
        player=player_1
    else:
        cur_list=o_list
        cur_color='blue'
        turn=f"X : {player_1}'s Turn"
        turn_color='red'
        typ='O'
        player=player_2
    turn_lbl.configure(text=turn,text_color=turn_color)
    cur_list.append(index)
    main_map[index].configure(text=typ,text_color=cur_color,state='disabled',text_color_disabled=cur_color)
    initial+=1
    if len(cur_list)==4:
        dark=cur_list.pop(0)
        main_map[dark].configure(text=' ',state='normal',fg_color='transparent',border_color='white')
    if len(cur_list)==3:
        main_map[cur_list[0]].configure(border_color=cur_color)
    if check_won(cur_list):
        end(player)

def enter(event,main_map,btn):
    global x_list,o_list,current_focus
    main_map[btn].configure(border_color='white')
    i,j=divmod(btn-1,3)
    focus_idx=i * 3 + j + 1
    for idx, btn in main_map.items():
        if idx == focus_idx:
            btn.configure(border_color='black')
        elif x_list and o_list:
            if idx==x_list[0] and len(x_list)==3:
                btn.configure(border_color='red')
            elif idx==o_list[0] and len(o_list)==3:
                btn.configure(border_color='blue')
            else:
                btn.configure(border_color='white')
        else:
            btn.configure(border_color='white')
    current_focus=[i,j]

def leave(event,main_map,btn):
    global x_list,o_list,current_focus
    main_map[btn].configure(border_color='black')

def move_focus(event,main_map):
    global current_focus,o_list,x_list
    i, j = current_focus
    if event.keysym == 'Up' and i > 0:
        i -= 1
    elif event.keysym == 'Down' and i < 2:
        i += 1
    elif event.keysym == 'Left' and j > 0:
        j -= 1
    elif event.keysym == 'Right' and j < 2:
        j += 1
    elif event.keysym == 'Return':
        idx = i * 3 + j + 1
        main_map[idx].invoke()
    current_focus = [i, j]
    focus_idx = i * 3 + j + 1
    for idx, btn in main_map.items():
        if idx == focus_idx:
            btn.configure(border_color='black')
        elif x_list and o_list:
            if idx==x_list[0] and len(x_list)==3:
                btn.configure(border_color='red')
            elif idx==o_list[0] and len(o_list)==3:
                btn.configure(border_color='blue')
            else:
                btn.configure(border_color='white')
        else:
            btn.configure(border_color='white')

def mainwindow():
    for i in root.winfo_children():
            i.destroy()
    global current_focus,player_2,player_1
    f1=CTkFrame(root,fg_color='transparent') 
    f1.place(relx=0,rely=0.1,relwidth=1,relheight=0.73) 
    lbl_frame=CTkFrame(f1,fg_color='transparent')
    lbl_frame.pack()
    lbl=CTkLabel(lbl_frame,text='Infinity ',text_color='red',font=custom_font1)
    lbl.pack(side='left',fill='both')
    lbl1=CTkLabel(lbl_frame,text='War',text_color='blue',font=custom_font1)
    lbl1.pack(side='left',fill='both')
    turn=initial%2
    if turn:
        turn=f"O : {player_2}'s Turn"
        turn_color='blue'
    else:
        turn=f"X : {player_1}'s Turn"
        turn_color='red'
    turn_lbl=CTkLabel(f1,text=turn,font=turn_font,bg_color='transparent',text_color=turn_color)
    turn_lbl.pack(after=lbl_frame,pady=30)
    main_frame=CTkFrame(f1,width=280,height=280,corner_radius=25,border_color='white',border_width=2)
    main_frame.pack()
    en1=CTkButton(master=main_frame,text=' ',font=custom_font,fg_color='transparent',border_width=2,border_color='white',corner_radius=15,hover_color=('#EAEAEA','#202122'))
    en1.place(relx=0.08,rely=0.08,relwidth=0.25,relheight=0.25)
    en2=CTkButton(master=main_frame,text=' ',font=custom_font,fg_color='transparent',border_width=2,border_color='white',corner_radius=15,hover_color=('#EAEAEA','#202122'))
    en2.place(relx=0.38,rely=0.08,relwidth=0.25,relheight=0.25)
    en3=CTkButton(master=main_frame,text=' ',font=custom_font,fg_color='transparent',border_width=2,border_color='white',corner_radius=15,hover_color=('#EAEAEA','#202122'))
    en3.place(relx=0.68,rely=0.08,relwidth=0.25,relheight=0.25)
    en4=CTkButton(master=main_frame,text=' ',font=custom_font,fg_color='transparent',border_width=2,border_color='white',corner_radius=15,hover_color=('#EAEAEA','#202122'))
    en4.place(relx=0.08,rely=0.38,relwidth=0.25,relheight=0.25)
    en5=CTkButton(master=main_frame,text=' ',font=custom_font,fg_color='transparent',border_width=2,border_color='white',corner_radius=15,hover_color=('#EAEAEA','#202122'))
    en5.place(relx=0.38,rely=0.38,relwidth=0.25,relheight=0.25)
    en6=CTkButton(master=main_frame,text=' ',font=custom_font,fg_color='transparent',border_width=2,border_color='white',corner_radius=15,hover_color=('#EAEAEA','#202122'))
    en6.place(relx=0.68,rely=0.38,relwidth=0.25,relheight=0.25)
    en7=CTkButton(master=main_frame,text=' ',font=custom_font,fg_color='transparent',border_width=2,border_color='white',corner_radius=15,hover_color=('#EAEAEA','#202122'))
    en7.place(relx=0.08,rely=0.68,relwidth=0.25,relheight=0.25)
    en8=CTkButton(master=main_frame,text=' ',font=custom_font,fg_color='transparent',border_width=2,border_color='white',corner_radius=15,hover_color=('#EAEAEA','#202122'))
    en8.place(relx=0.38,rely=0.68,relwidth=0.25,relheight=0.25)
    en9=CTkButton(master=main_frame,text=' ',font=custom_font,fg_color='transparent',border_width=2,border_color='white',corner_radius=15,hover_color=('#EAEAEA','#202122'))
    en9.place(relx=0.68,rely=0.68,relwidth=0.25,relheight=0.25)
    main_map={1:en1,2:en2,3:en3,4:en4,5:en5,6:en6,7:en7,8:en8,9:en9}
    for idx,i in enumerate(main_map.values()):
        i.configure(command=lambda idx=idx: connect(idx+1,turn_lbl,initial,main_map))
        i.bind('<Enter>', lambda event,btn=idx: enter(event,main_map,btn=btn+1))
        i.bind('<Leave>', lambda event,btn=idx: leave(event,main_map,btn=btn+1))
    [i,j]=current_focus
    focus_idx = i * 3 + j + 1
    main_map[focus_idx].configure(border_color='black')
    root.bind('<Up>', lambda event: move_focus(event, main_map))
    root.bind('<Down>', lambda event: move_focus(event, main_map))
    root.bind('<Left>', lambda event: move_focus(event, main_map))
    root.bind('<Right>', lambda event: move_focus(event, main_map))
    root.bind('<Return>', lambda event: move_focus(event, main_map))

def get_name(p1,p2):
    global player_1,player_2
    player_1=p1
    player_2=p2
    mainwindow()

def front():
    f1=CTkFrame(root,fg_color='transparent') 
    f1.place(relx=0,rely=0.1,relwidth=1,relheight=0.73) 
    lbl_frame=CTkFrame(f1,fg_color='transparent')
    lbl_frame.pack()
    lbl=CTkLabel(lbl_frame,text='Infinity ',text_color='red',font=custom_font1)
    lbl.pack(side='left',fill='both')
    lbl1=CTkLabel(lbl_frame,text='War',text_color='blue',font=custom_font1)
    lbl1.pack(side='left',fill='both')
    login_frame=CTkFrame(f1,fg_color='transparent',width=300,height=400)
    login_frame.pack()
    CTkLabel(login_frame,text='Player 1 Name',bg_color='transparent',font=('Comic Sans MS',20),text_color='red').place(x=15,y=40)
    p1_entry=CTkEntry(login_frame,height=50,width=280,font=('Comic Sans MS',20),corner_radius=25,text_color='red')
    p1_entry.place(x=10,y=80)
    CTkLabel(login_frame,text='Player 2 Name',bg_color='transparent',font=('Comic Sans MS',20),text_color='blue').place(x=15,y=150)
    p2_entry=CTkEntry(login_frame,height=50,width=280,font=('Comic Sans MS',20),corner_radius=25,text_color='blue')
    p2_entry.place(x=10,y=190)
    st_btn=CTkButton(login_frame,text='Play',font=('Comic Sans MS',25),command=lambda : get_name(p1_entry.get().capitalize(),p2_entry.get().capitalize()),border_width=2,width=180,height=50,corner_radius=25)
    st_btn.place(x=55,y=280)

if __name__ == '__main__':
    update_frame()
    root.mainloop()