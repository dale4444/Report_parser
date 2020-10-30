import Tkinter as tk
from Tkinter import Text
import tkFileDialog as filedialog
import os
from bs4 import BeautifulSoup
from lxml import etree
import codecs

root = tk.Tk()
root.title("Platform Test Report Parser")
pages=[]

def open_file():
    for widget in frame.winfo_children():
        widget.destroy()
    filename = filedialog.askopenfilename(initialdir="./", title="Select HTML report file")
    filename = filename.replace("/","\\")
    file=os.path.basename(filename)
    pages.append(filename)
    label = tk.Label(frame, text=file, bg="gray")
    label.pack()

def execute():
    label3 = tk.Label(frame, text="Please wait for a moment or couple of minutes, depending on size of your report.")
    label3.pack()
    mystring = "fail"
    page = codecs.open(pages[0], "r" , "utf-8")
    soup = BeautifulSoup(page , 'lxml')
    tags = soup.find_all ("a")
    div = "div_"

    with open("Report_Analysis.txt", "w+") as f:
        for tag in tags:
            if mystring in tag:
                id_of_case = div+tag.parent.parent.find("td").text
                tags2 = soup.find_all ("div" , class_="Indentation" , id=id_of_case)
                test_case = tag.previous_element.previous_element.previous_element.previous_element.previous_element
                for tag2 in tags2:
                    ptc_list = tag2.find("p")
                    ptc_list = str(ptc_list)
                    split_word="ID: "
                    res=ptc_list.partition(split_word)[2]
                    output = "PTC ID: " + res [0:8]
                    f.write(output + "\n")
                    f.write(test_case + "\n")
                    tags3 = tag2.find_all("td", class_="NegativeResultCell")
                    for tag3 in tags3:
                        step=tag3.previous_sibling.previous_sibling.text
                        step=step.encode('utf-8','replace')
                        f.write(step + "\n")
                f.write("\n")
    f.close()
    label3 = tk.Label(frame, text="Done. Your analysis is generated in Report_analysis.txt in root file of this app.")
    label3.pack()

    def read():
        os.system("Report_Analysis.txt")
    readFile = tk.Button(frame, text="Open analysis file", padx=10, pady=5, fg='white', bg="#263D42", command=read)
    readFile.pack()

canvas = tk.Canvas (root, height=400, width=700, bg="#263D42")
canvas.pack()

frame = tk.Frame(root, bg="#7fa7b0")
frame.place(relwidth=0.8, relheight=0.7, relx=0.1, rely=0.1)

openFile = tk.Button(root, text="Open HTML report", padx=10, pady=5, fg='white', bg="#263D42", command=open_file)
openFile.pack()

executeParser = tk.Button(root, text="Execute Parser", padx=10, pady=5, fg='white', bg="#263D42", command=execute)
executeParser.pack()

root.mainloop()