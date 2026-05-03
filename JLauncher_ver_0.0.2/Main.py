import tkinter as tk
import tkinter.font as font
import tkinter.filedialog
import tkinter.messagebox
import os
import subprocess
from PIL import Image, ImageTk
from win32api import GetSystemMetrics


def gameinfo_update():#gameinfo配列の要素数が足りないとき追加
    for i in gameinfo:
        if(len(i)!=(edit_id_max+1)):
            for j in range(edit_id_max+1-len(i)):
                #print(j)
                i.append("")

#ゲームの全情報を格納している配列[名前、実行ファイルパス、説明テキストパス、製作者名、スクショパス]
gameinfo = [["A_GAME_NAME","B_GAME_NAME","C_GAME_NAME"],
            ["pathA","pathB","pathC"],
            ["A_EXP_TXT_PATH","B_EXP_TXT_PATH","C_EXP_TXT_PATH"],
            ["ProducerA","ProducerB","producerC"],
            ["PIC_PATH_A","PIC_PATH_B","PIC_PATH_C"]
            ]
gameinfo_text = open("GAME_INFO.txt", "r",encoding="UTF-8")
lines = gameinfo_text.readlines()

gameinfo_text.close()
edit_id_max = int(lines[0])
#print(len(lines))

if(((edit_id_max+1)*5 + 1) > len(lines)):
    for i in range(((edit_id_max+1)*5+1)-len(lines)):
        #print(i)
        lines.append("")

#print(len(lines))
gameinfo_update()

readlines = 0

for i in range(5):
    for j in range(edit_id_max+1):
        gameinfo[i][j]=lines[readlines+1]
        gameinfo[i][j].replace("\n","")
        readlines+=1

game_button = []

edit_id = 0
#edit_id_max=2
main_id = 0
nowDir = os.path.abspath(os.path.dirname(__file__))


def createPassWindow():
    passwindow = tk.Toplevel(root)
    passwindow.geometry("320x100+"+str(int((GetSystemMetrics(0)-320)/2))+"+"+str(int((GetSystemMetrics(1)-160)/2)))
    passwindow.title("パスワードを入力")
    passwindow.resizable(False, False)

    label_pass = tk.Label(passwindow, text="パスワードを入力してください\n(部員以外は操作しないでください)", font=("Menlo",15))
    label_pass.place(x=5,y=5)

    entry_pass = tk.Entry(passwindow, width=40)
    entry_pass.place(x=10,y=70)

    button_pass = tk.Button(passwindow, text="OK", font = ("Menlo",15),command = passaccept(entry_pass,passwindow))
    button_pass.place(x=270,y=70)


def passaccept(passentry, gui):
    def x():
        if(passentry.get() == "adminijakuden"):
            gui.destroy()
            createEditWindow()
        else:
            tk.messagebox.showinfo(title="間違ったパスワード", message="パスワードが間違っています")
            gui.destroy()
    return x


def createEditWindow():#settingボタンをおす


    def id_r():
        global edit_id
        if (edit_id < edit_id_max):
            edit_id += 1
        else:
            if (edit_id == edit_id_max):
                edit_id = 0
        update_edit()


    def id_l():
        global edit_id
        if (edit_id > 0):
            edit_id -= 1
        else:
            if (edit_id == 0):
                edit_id = edit_id_max
        update_edit()


    def id_minus():
        global edit_id,edit_id_max
        if(edit_id_max>0):
            edit_id_max-=1
        if(edit_id>edit_id_max):
            edit_id-=1
        update_edit()


    def id_plus():
        global edit_id_max
        edit_id_max+=1
        update_edit()


    def open_file_exe():
        gameinfo[0][edit_id] = str(entry_name.get())
        gameinfo[3][edit_id] = str(entry_pro.get())

        gameinfo[1][edit_id] = tk.filedialog.askopenfilename(filetypes=[("exeファイル","*.exe")],initialdir=nowDir)
        gameinfo[1][edit_id] = gameinfo[1][edit_id].replace(nowDir.replace("\\","/"),'')
        update_edit()


    def open_file_txt():
        gameinfo[0][edit_id] = str(entry_name.get())
        gameinfo[3][edit_id] = str(entry_pro.get())

        gameinfo[2][edit_id] = tk.filedialog.askopenfilename(filetypes=[("txtファイル","*.txt")],initialdir=nowDir)
        gameinfo[2][edit_id] = gameinfo[2][edit_id].replace(nowDir.replace("\\","/"), '')
        update_edit()


    def open_file_png():
        gameinfo[0][edit_id] = str(entry_name.get())
        gameinfo[3][edit_id] = str(entry_pro.get())

        gameinfo[4][edit_id] = tk.filedialog.askopenfilename(filetypes=[("画像ファイル","*.png;*.jpg;*.bmp")],initialdir=nowDir)
        gameinfo[4][edit_id] = gameinfo[4][edit_id].replace(nowDir.replace("\\","/"), '')
        update_edit()


    def apply_setting():
        global entry_name
        global entry_pro

        gameinfo[0][edit_id]=str(entry_name.get())
        gameinfo[3][edit_id]=str(entry_pro.get())
        #print(gameinfo[0][0])

        write_data=[""]*((edit_id_max+1)*5+1)
        write_data[0]=str(edit_id_max)

        writelines=0

        for i in range(5):
            for j in range(edit_id_max + 1):
                write_data[writelines + 1] = gameinfo[i][j]
                #print(write_data[writelines+1])
                writelines += 1

        for i in range(len(write_data)):
            write_data[i] = write_data[i].replace("\n","")
            write_data[i]+="\n"
        #print(len(write_data))

        gameinfo_text_write = open("GAME_INFO.txt","w",encoding="UTF-8")
        gameinfo_text_write.writelines(write_data)
        gameinfo_text_write.close()
        #print(gameinfo[0][3])
        update_edit()
        update_root()


    def update_edit():#セッティング画面を描画
        leftcursor = tk.Button(editwindow, text="<", command=id_l)
        leftcursor.place(x=10, y=10)

        rightcursor = tk.Button(editwindow, text=">", command=id_r)
        rightcursor.place(x=130, y=10)

        minuscursor = tk.Button(editwindow, text="-", command=id_minus)
        minuscursor.place(x=150,y=10)

        pluscursor = tk.Button(editwindow, text="+", command=id_plus)
        pluscursor.place(x=170,y=10)

        label_id = tk.Label(editwindow, text="  "+str(edit_id)+"/"+str(edit_id_max)+"  ", font=("", 20))
        label_id.place(x=45, y=10)

        label_caution = tk.Label(editwindow, text="部員以外操作しないでください。\n間違って開いた場合は右上の✖ボタンを押して閉じてください。",font=("Menlo",15))
        label_caution.place(x=440,y=420)

        label_name = tk.Label(editwindow, text="GAME NAME:", font=("Menlo",15))
        label_filepath = tk.Label(editwindow, text="FILE(.exe) PATH:", font=("Menlo", 15))
        label_textpath = tk.Label(editwindow, text="TEXT FILE(.txt) PATH:", font=("Menlo", 15))
        label_pro = tk.Label(editwindow, text="CREATER NAME:", font=("Menlo", 15))
        label_picpath = tk.Label(editwindow, text="PICTURE FILE(.png) PATH:",font=("Menlo",15))

        label_name.place(x=10,y=40)
        label_filepath.place(x=10,y=70)
        label_textpath.place(x=10,y=100)
        label_pro.place(x=10,y=130)
        label_picpath.place(x=10,y=160)
        gameinfo_update()
        global entry_name
        global entry_pro
        entry_name = tk.Entry(editwindow,width=100)
        entry_pro = tk.Entry(editwindow,width=100)
        entry_name.insert(tk.END,gameinfo[0][edit_id])
        entry_pro.insert(tk.END, gameinfo[3][edit_id])

        entry_name.place(x=180,y=42)
        entry_pro.place(x=180,y=132)

        button_se_file = tk.Button(editwindow, text="SELECT FILE",font=("Menlo",10), command=open_file_exe)
        button_se_text = tk.Button(editwindow, text="SELECT FILE", font=("Menlo", 10), command=open_file_txt)
        button_se_pic = tk.Button(editwindow, text="SELECT FILE", font=("Menlo", 10), command=open_file_png)

        button_se_file.place(x=180,y=70)
        button_se_text.place(x=230, y=100)
        button_se_pic.place(x=240, y=160)

        label_se_file["text"]=gameinfo[1][edit_id]
        label_se_text["text"]=gameinfo[2][edit_id]
        label_se_pic["text"]=gameinfo[4][edit_id]

        label_se_file.place(x=300, y=70)
        label_se_text.place(x=320, y=100)
        label_se_pic.place(x=340, y=160)


        button_save = tk.Button(editwindow,text="APPLY",command=apply_setting,font=("Menlo",20))
        button_save.place(x=820,y=490)

    editwindow = tk.Toplevel(root)
    editwindow.title("JLauncher Setting Window")
    editwindow.geometry("960x540")
    editwindow.resizable(False, False)
    label_se_file = tk.Label(editwindow, text=gameinfo[1][edit_id], font=("Menlo", 10))
    label_se_text = tk.Label(editwindow, text=gameinfo[2][edit_id], font=("Menlo", 10))
    label_se_pic = tk.Label(editwindow, text=gameinfo[4][edit_id], font=("Menlo", 10))

    label_se_file.place(x=300, y=70)
    label_se_text.place(x=320, y=100)
    label_se_pic.place(x=340, y=160)
    update_edit()


def id_main(i):
    def x():
        global main_id
        main_id=i
        #print(main_id)
        update_root()
    return x


def run_game():
    global main_id
    #print(nowDir+gameinfo[1][main_id].replace("/","\\"))
    subprocess.run(nowDir+gameinfo[1][main_id].replace("/","\\").replace("\n",""))


def update_root():#メイン画面を描画
    global main_id
    #print("Root update")
    frame_gb = tk.Frame(root, width=500, height=750, bg="gray")
    frame_gb.place(x=0, y=0)

    basic_font = font.Font(frame_gb, family="TkIconFont", size=25, weight="bold")



    global game_button

    if(len(game_button)!=edit_id_max+1):
        game_button=[]
        for n in range(edit_id_max + 1):
            game_button.append(tk.Button(frame_gb, text=gameinfo[0][n].replace("\n",""),width=22,anchor="center",font=basic_font, command=id_main(n), relief="solid"))
            game_button[n].place(x=16, y=10+ n * 90)
    else:
        for n in range(edit_id_max + 1):
            game_button[n]=tk.Button(frame_gb, text=gameinfo[0][n].replace("\n",""),width=22,anchor="center", font=basic_font,command=id_main(n),relief="solid")
            game_button[n].place(x=16, y=10+ n * 90)

    editmode_button = tk.Button(root, text="setting", font=("", 10), bg="gray", command=createPassWindow)
    editmode_button.place(x=1030, y=0)
    #print(gameinfo[3][main_id])

    label_cre["text"] = "Creator : "+ gameinfo[3][main_id].replace("\n","")

    txt_path = nowDir+gameinfo[2][main_id].replace("/","\\").replace("\n","")

    #print(txt_path)
    try:
        label_exp["text"]=open(txt_path).read()
    except:
        print("")

    png_path = nowDir+gameinfo[4][main_id].replace("/","\\").replace("\n","")
    #print(png_path)
    try:
        pngFile = Image.open(png_path)
        pngFile=pngFile.resize((480,270))
        pngFile = ImageTk.PhotoImage(pngFile)
        cv=tk.Canvas(bg="white",width=480,height=270)
        cv.place(x=540, y=40)
        cv.create_image(1,1,image=pngFile,anchor=tkinter.NW)
    except:
        print("")

    buttonpng = Image.open("./Data/Play_Button.png")
    buttonpng = ImageTk.PhotoImage(buttonpng)

    run_button = tk.Button(root, text="PLAY", font=("Menlo",30),bg="gray",command=run_game,image=buttonpng,relief = "flat",borderwidth=1)
    run_button.place(x=940,y=640)
    root.mainloop()

root = tk.Tk()
root.title("Jakuden Launcher")
root.geometry("1080x720+"+str(int((GetSystemMetrics(0)-1080)/2))+"+"+str(int((GetSystemMetrics(1)-720)/2)))
root.resizable(False,False)
root.wm_iconbitmap("./Data/icon.ico")
label_cre = tk.Label(root, text="Creator : "+gameinfo[3][main_id], font=("Menlo",20))
label_cre.place(x=540,y=360)


txt_path = nowDir+gameinfo[2][main_id].replace("/","\\").replace("\n","")
#print(txt_path)
expng = Image.open("./Data/Ex_Window.png")
expng = ImageTk.PhotoImage(expng)
cv2 = tk.Canvas(bg="white", width=500, height=180)
cv2.place(x=540, y=410)
cv2.create_image(2,2,image=expng,anchor=tkinter.NW)

try:
    label_exp = tk.Label(root,bg="white", text=open(txt_path).read(), font=("Menlo",16),anchor="e",justify="left")
    label_exp.place(x=550, y=420)
except:
    print("")

update_root()

root.mainloop()
