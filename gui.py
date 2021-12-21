import tkinter as tk
from tkinter import  filedialog,messagebox

root = tk.Tk()

root.title("")
canvas = tk.Canvas(root,height=500,width=600,bg='orange')
canvas.pack()

frame = tk.Frame(root)
frame.place(relwidth=0.9,relheight=0.9,relx=0.05,rely=0.05)


title = tk.Label(root,fg="green",text="Network based candidate gene predictor ",font=("Arial",20)).place(x=60,y=100)


file_l = tk.Label(root,text="Upload *.tsv",font=("Arial",10))
file_l.place(x=100,y=200)

file_name = tk.Entry(root,width=62)
file_name.place(x=180,y=200)

def f_e(event):
		file_name.delete(0,'end')


file_name.bind("<KeyRelease>", f_e)

def browse():
	filename = filedialog.askopenfilename(initialdir="/",filetypes=[("TSV Files","*.tsv")])
	file_name.delete(0,"end")

	file_name.insert(0,filename)

choose = tk.Button(root,text="Choose a file",font=("Arial",10),command=browse )
choose.place(x=180,y=230)
choose.focus_set()

method_l = tk.Label(text="Algorithm : ",font=("Arial",10))
method_l.place(x=100,y=270)

method = tk.IntVar()


majority_v = tk.Radiobutton(root,text = "Majority voting score",font=("Arial",10),variable=method,value=1 )
majority_v.place(x=190,y=280,anchor = "w")


hishigaki = tk.Radiobutton(root,text = "Hishigaki algorithm",font=("Arial",10),variable=method,value=2 )
hishigaki.place(x=340,y=280,anchor = "w")


def object():
	if file_name.get() == "" and method.get() == 0:
		messagebox.showerror('Inputs missing',"Please upload a file and select the desired algorithm.")
	elif method.get() == 0:
		messagebox.showerror('Mssing algoritm!',"Please select the desired algorithm.")
	elif file_name.get() == "":
		messagebox.showerror('File missing!', "Please select a file first.")

	else:
		from gene_predictor import network
		p1 = network()
		p1.network_graphing(file_name.get(), method.get())
		if network.Total_proteins !=0 and network.unknown ==0:
			messagebox.showinfo("","Unknown proteins are not detected in the given network ! ")
		elif network.Total_proteins !=0 and network.unknown !=0:
			root.destroy()
			from gui2 import w2

submit = tk.Button(root,height=2,width=10,bg="blue",text ='Submit',fg="white",font=("Arial",10),command=object)
submit.place(x=250,y=350)

root.resizable(False,False) # for both width and height
root.mainloop()

