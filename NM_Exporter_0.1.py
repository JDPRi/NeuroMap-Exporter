#by Joe Richards
import os, fnmatch, array, pip, tkinter as tk
from tkinter import filedialog, StringVar
from colour import Color

allFiles=[]
mainbg = Color("#99AABB")
root = tk.Tk()
root.configure(bg=mainbg)
v1 = StringVar()
v2 = StringVar()
root.title("NM Exporter (Version 0.1)")
var1 = tk.IntVar()
var2 = tk.IntVar()
var3 = tk.IntVar()
var4 = tk.IntVar()
var5 = tk.IntVar()

root.minsize(600,300)
root.maxsize(600,300)


def find_ogfolder():

    global ogfolder
    ogfolder =filedialog.askdirectory()
    v1.set(ogfolder)
    
def find_destfolder():

    global target_folder
    target_folder=filedialog.askdirectory()
    v2.set(target_folder)
    
def selection():
    if (var1.get() == 0 or var2.get()==0 or var3.get()==0 or var4.get()==0):
        var5.set(0)

    if (var1.get() ==1 and var2.get()==1 and var3.get()==1 and var4.get()==1):
        var5.set(1)
        
def all_selection():
    var1.set(var5.get())
    var2.set(var5.get())
    var3.set(var5.get())
    var4.set(var5.get())

ogfolderbttn=tk.Button(root, text="choose folder", borderwidth = 2, command=find_ogfolder)
ogfolderlb = tk.Entry(root,textvariable=v1, borderwidth=2,width=70)
        
destfolderbttn = tk.Button(root, text ="choose folder", borderwidth =2, command =find_destfolder)
destfolderlb = tk.Entry(root, textvariable=v2, borderwidth=2, width=70)

file_types = ["Firings", "MFR", "MUAPs", "stats", "all"]

c1= tk.Checkbutton(root, text = "firings",width=23, variable = var1 , onvalue=1, offvalue=0, anchor="w",padx=5, command = selection).place(x=50,y=80)
c2= tk.Checkbutton(root, text = "MFR (will take a while)",width=23, variable = var2 , onvalue=1, offvalue=0,anchor="w" ,padx=5, command = selection).place(x=50,y=100)
c3= tk.Checkbutton(root, text = "MUAPs",width=23, variable = var3 , onvalue=1, offvalue=0,anchor="w",padx=5, command = selection).place(x=50,y=120)
c4= tk.Checkbutton(root, text = "stats",width=23, variable = var4 , onvalue=1, offvalue=0,anchor="w",padx=5, command = selection).place(x=50,y=140)
c5= tk.Checkbutton(root, text = "all", width=23, variable = var5 , onvalue=1, offvalue=0,anchor ="w",padx=5, command = all_selection).place(x=50,y=160)

ogfolderbttn.place(x=50,y=15)
ogfolderlb.place(x=150,y=15)
destfolderbttn.place(x=50,y=45)
destfolderlb.place(x=150,y=45)

copywritelb = tk.Label(root, text="Made by JDPRichards", borderwidth=2, width=85,bg="red").place(x=0,y=280)

v1.set("select file to import from")
v2.set("select file to export to")


def findAll(pattern, path):
    file=[]
    for root,dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                file.append(os.path.join(root, name))
    return file


def find_single(pattern, path):
    result=""
    for root,dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result = os.path.join(root, name)
    return result

def combine_single_subject(file_type, ogfolder, target_folder):
    str_num=""
    file_type = file_type+".txt"
    look_for = '*'+file_type
    all_files = findAll(look_for,ogfolder)
    subjects=[]
    for file in all_files:
        file=file.split("\\")[len(file.split("\\"))-1]
        if (file.split("_")[0] not in subjects):
            subjects.append(file.split("_")[0])
            
    for num in range(1,len(subjects)+1):
        if num <10:
            if num != 0:
                str_num= "0"+str(num)
        else:
            str_num = str(num)
        
        look_for = str_num+'*_'+ file_type
        subject_files = findAll(look_for,ogfolder)
        w = open(target_folder+"/"+"subject "+str_num+" "+file_type, "w")
        w.write("")
        w.close()
        a = open(target_folder+"/"+"subject "+str_num+" "+file_type, "a+")
        for file2 in range(0,len(subject_files)):
            current_file = subject_files[file2]
            split_location = current_file.split("\\")
            filename = split_location[len(split_location)-1]
            filename_data = filename.split("_")
            r = open(current_file, "r")
            headers = r.readline()
            
            splitheaders = headers.split("	")
            a.write(current_file)
            a.write("\n")
            
            if (file_type!="stats.txt"):
                a.write(",file01,file01")
                for i in range(0, len(splitheaders)):
                    a.write(",file01")
                a.write("\n")

                a.write(",TIME,ANALOGTIME")
                for i in range(0,len(splitheaders)):
                    a.write(","+splitheaders[i])

                a.write(",FRAME_NUMBERS,FRAME_NUMBERS")
                for i in range(0, len(splitheaders)):
                    a.write(",ANALOG")
                a.write("\n")
                for i in range(0,len(splitheaders)+2):
                    a.write(",ORIGINAL")
                a.write("\n")

                a.write("ITEM")
                
                for i in range(0,len(splitheaders)+2):
                    a.write(",0")
                a.write("\n")
                
            else:
                a.write(",file01,file01")
                for i in range(0, len(splitheaders)-1):
                    a.write(",file01")
                a.write("\n")

                a.write(",TIME,ANALOGTIME")
                for i in range(0,len(splitheaders)-1):
                    a.write(","+splitheaders[i])
                a.write("\n")
                a.write(",FRAME_NUMBERS,FRAME_NUMBERS")
                for i in range(0, len(splitheaders)-1):
                    a.write(",ANALOG")
                a.write("\n")
                for i in range(0,len(splitheaders)+1):
                    a.write(",ORIGINAL")
                a.write("\n")

                a.write("ITEM")
                
                for i in range(0,len(splitheaders)+1):
                    a.write(",0")
                a.write("\n")
                
            j = 0
            data = r.readline()
            while (data!=""):
                a.write(str(j+1)+","+str(j)+","+str(j))
                splitdata = data.split("	")
                if (file_type == "_stats.txt"):
                    for i in range(0, len(splitheaders)-1):
                        a.write(","+splitdata[i])
                    a.write("\n")
                    
                else:
                    for i in range(0,len(splitheaders)):
                        a.write(","+splitdata[i])
                j=j+1
                data =r.readline()
            r.close()
            a.write("\n\n\n\n\n")
        a.close()
        r=open(target_folder+"/"+"subject "+str_num+" "+file_type,"r")
        alldata= r.read()
        w = open(target_folder+"/"+"subject "+str_num+" "+file_type, "w")
        w.write(alldata.replace(",","	"))
        

def set_layout(file_type, ogfolder, target_folder):
    str_num=""
    file_type = "_"+file_type+".txt"
    look_for = '*'+file_type

    all_files = findAll(look_for,ogfolder)

    for file2 in range(0, len(all_files)):
        current_file = all_files[file2]
        split_location = current_file.split("\\")
        filename = split_location[len(split_location)-1]
        filename_data = filename.split("_")
        r = open(current_file, "r")
        headers = r.readline()
        w = open(target_folder+"/"+filename, "w")
        w.write("")
        w.close()
        a = open(target_folder+"/"+filename, "a+")
        splitheaders = headers.split("	")

        if (file_type!="_stats.txt"):
            
            a.write(",file01,file01")
            for i in range(0, len(splitheaders)):
                a.write(",file01")
            a.write("\n")

            a.write(",TIME,ANALOGTIME")
            for i in range(0,len(splitheaders)):
                a.write(","+splitheaders[i])

            a.write(",FRAME_NUMBERS,FRAME_NUMBERS")
            for i in range(0, len(splitheaders)):
                a.write(",ANALOG")
            a.write("\n")
            for i in range(0,len(splitheaders)+2):
                a.write(",ORIGINAL")
            a.write("\n")

            a.write("ITEM")
            
            for i in range(0,len(splitheaders)+2):
                a.write(",0")
            a.write("\n")
            
        else:

            a.write(",file01,file01")
            for i in range(0, len(splitheaders)-1):
                a.write(",file01")
            a.write("\n")

            a.write(",TIME,ANALOGTIME")
            for i in range(0,len(splitheaders)-1):
                a.write(","+splitheaders[i])
            a.write("\n")
            a.write(",FRAME_NUMBERS,FRAME_NUMBERS")
            for i in range(0, len(splitheaders)-1):
                a.write(",ANALOG")
            a.write("\n")
            for i in range(0,len(splitheaders)+1):
                a.write(",ORIGINAL")
            a.write("\n")

            a.write("ITEM")
            
            for i in range(0,len(splitheaders)+1):
                a.write(",0")
            a.write("\n")
        
        
        j = 0
        data = r.readline()
        while (data!=""):
            a.write(str(j+1)+","+str(j)+","+str(j))
            splitdata = data.split("	")
            if (file_type == "_stats.txt"):
                for i in range(0, len(splitheaders)-1):
                    a.write(","+splitdata[i])
                a.write("\n")
            else:
                for i in range(0,len(splitheaders)):
                    a.write(","+splitdata[i])
            j=j+1
            data =r.readline()
        r.close()
        r=open(target_folder+"/"+filename,"r")
        a.close()
        alldata= r.read()
        a.close()
        w = open(target_folder+"/"+filename, "w")
        w.write(alldata.replace(",","	"))
            
        
def convert():
    if (var1.get() == 1):
        set_layout("firings", ogfolder, target_folder)
    if (var2.get()==1):
        set_layout("MFR", ogfolder, target_folder)
    if (var3.get()==1):
        set_layout("MUAPs", ogfolder, target_folder)
    if (var4.get()==1):
        set_layout("stats", ogfolder, target_folder)

def combine():
    if (var1.get() == 1):
        combine_single_subject("firings", ogfolder, target_folder)
    if (var2.get()==1):
        combine_single_subject("MFR", ogfolder, target_folder)
    if (var3.get()==1):
        combine_single_subject("MUAPs", ogfolder, target_folder)
    if (var4.get()==1):
        combine_single_subject("stats", ogfolder, target_folder)

convertbttn = tk.Button(root, text="Convert", borderwidth=2,padx=20,pady=5, command =convert).place(x=50,y=220)
combinebttn = tk.Button(root, text="Combine", borderwidth=2,padx=20,pady=5, command =combine).place(x=150,y=220)

root.mainloop()

print("Finished")
