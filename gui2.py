import tkinter as tk
from tkinter import ttk,scrolledtext,messagebox
from gene_predictor import network
import os

w2 = tk.Tk()

w2.title("")
canvas = tk.Canvas(w2, bg="grey", height=600, width=1200)
canvas.pack()

title = tk.Label(w2, bg="grey", text="Result Page ", font=("Arial", 20)).place(x=10, y=10)

method_l = tk.Label(w2, font=("Arial", 10), text=network.method)
method_l.place(x=60, y=60)

protein_l = tk.Label(w2, bg="grey", text=" Number of proteins", font=("Arial", 11))
protein_l.place(x=100, y=100)

n_proteins = tk.Entry(w2,bg="grey",fg="white", width=7, font=("Arial", 11))
n_proteins.place(x=250, y=100)
n_proteins.delete(0, "end")
n_proteins.insert(0, network.Total_proteins)


def n_p(event):
	n_proteins.delete(0, "end")
	n_proteins.insert(0, network.Total_proteins)


n_proteins.bind("<KeyRelease>", n_p)

inter_l = tk.Label(w2, bg="grey", text=" Number of interactions", font=("Arial", 11))
inter_l.place(x=550, y=100)

n_inter = tk.Entry(w2,bg="grey",fg="white",width=7, font=("Arial", 11))
n_inter.place(x=720, y=100)
n_inter.insert(0, network.Number_of_interactions)

def p(event):
	n_inter.delete(0, "end")
	n_inter.insert(0,network.Number_of_interactions)
	

n_inter.bind("<KeyRelease>",p)

unknown_l = tk.Label(w2, bg="grey", text=" Number of unknown proteins", font=("Arial", 11))
unknown_l.place(x=100, y=150)

n_unknown = tk.Entry(w2,bg="grey",fg="white", width=7, font=("Arial", 11))
n_unknown.place(x=300, y=150)
n_unknown.insert(0, len(network.unknown))

def unkp(event):
	n_unknown.delete(0, "end")
	n_unknown.insert(0, len(network.unknown))


n_unknown.bind("<KeyRelease>", unkp)


unknown_l = tk.Label(w2, bg="grey", text=" Number of predicted proteins", font=("Arial", 11))
unknown_l.place(x=550, y=150)

n_pred = tk.Entry(w2,bg="grey",fg="white", width=7, font=("Arial", 11))
n_pred.place(x=750, y=150)
n_pred.insert(0, (len(network.predicted.keys())))

def pred(event):
	n_pred.delete(0, "end")
	n_pred.insert(0, (len(network.unknown)-len(network.multiple_function_candidates.keys())))


n_pred.bind("<KeyRelease>", pred)

criteria_l = tk.Label(w2, bg="grey", text=" Criteria : ", font=("Arial", 11))
criteria_l.place(x=100, y=200)

criteria = tk.IntVar()

def combo_l():
	if criteria.get() == 1:
		if len(list_s) != 0:
			combo["values"] = list_s
			combo.current(0)
		else:
			combo["values"] = "None"
			combo.current(0)

	elif criteria.get() == 2:
		if len(list_m) != 0:
			combo["values"] = list_m
			combo.current(0)
		else:
			combo["values"] = "None"
			combo.current(0)

	else:
		if len(list_ac) != 0:
			combo["values"] = list_ac
			combo.current(0)
		else:
			combo["values"] = "None"
			combo.current(0)


single_r = tk.Radiobutton(w2,bg="grey",text = "Top five candidates for single functions",font=("Arial",11),variable=criteria,value=1,command = combo_l )
single_r.place(x=190,y=210,anchor = "w")

multiple_r = tk.Radiobutton(w2,bg="grey",text = "Candidates for multiple functions",font=("Arial",11),variable=criteria,value=2,command = combo_l )
multiple_r.place(x=500,y=210,anchor = "w")

pred_r = tk.Radiobutton(w2,bg="grey",text = "Predicted mostly accurate function",font=("Arial",11),variable=criteria,value=3 ,command = combo_l)
pred_r.place(x=750,y=210,anchor = "w")

s = tk.StringVar()

text_w = scrolledtext.ScrolledText(w2, height=15, width=80,undo=True,font=("Arial", 11))
text_w.place(x=410, y=250)


list_s = []
for i in network.single_function_candidates.keys():
	list_s.append(i)

list_m = []
for i in network.multiple_function_candidates.keys():
	list_m.append(i)

list_ac = []
for i in network.predicted.keys():
	list_ac.append(i)

def cmb(event):
	combo.delete(0, "end")
	combo_l()

combo_label=tk.Label(w2,bg="grey",text="By protein name/functionality : ",font=("Arial", 11))
combo_label.place(x=105, y=330)
combo= ttk.Combobox(w2,width=30,textvariable = s, font=("Arial", 11))
combo.place(x=105, y=360)

combo["values"] = "None"
combo.current(0)

combo.bind("<KeyRelease>", cmb)

def all():
	text_w.delete(1.0,"end")
	string =""
	if criteria.get() ==0:
		messagebox.showerror('Mssing criteria!', "Please select the desired criteria first.")
	else:
		if criteria.get() == 1:
			for i in network.single_function_candidates.keys():
				string = string + "\n\n\u2022 " + str(i) + " : "
				values = str(network.single_function_candidates[i]).split(',')
				for p in values:
					string = string + "\n\n\t" + str(p)
		elif criteria.get() == 2:
			for i in network.multiple_function_candidates:
				string = string + "\n\n\u2022 " + str(i) + " : "
				values = str(network.multiple_function_candidates[i]).split(',')
				for fun in values:
					string = string + "\n\n\t" + str(fun)
		else:
			for i in network.predicted:
				string = string + "\n\n\u2022 " + str(i) + " : " + str(network.predicted[i])
		text_w.insert(1.0, string)

All= tk.Button(w2,bg='green',fg="white",width=10,command = all,text="Show All", font=("Arial", 11))
All.place(x=105, y=260)

def s_search():
	text_w.delete(1.0,"end")
	string = ""
	if criteria.get() == 0 :
		messagebox.showerror('Mssing criteria!', "Please select the desired criteria first.")
	else:
		key = s.get()
		if key != "None":
			if criteria.get() == 1:
				string = string + "\n\n" + str(key) + " : "
				values = str(network.single_function_candidates[key]).split(',')
				for p in values:
					string = string + "\n\n\t" + str(p)
			elif criteria.get() == 2:
				string = string + "\n\n" + str(key) + " : "
				values = str(network.multiple_function_candidates[key]).split(',')
				for fun in values:
					string = string + "\n\n\t" + str(fun)

			else:
				string = string + "\n\n" + str(key) + " : " + str(network.predicted[key])

		text_w.insert(1.0, string)

search = tk.Button(w2,bg="light blue",width=10,command = s_search,text="search", font=("Arial", 11))
search.place(x=105, y=400)

w2.resizable(False, False)  # for both width and height

def exit():
	w2.destroy()
	os.system('python gui.py')

home = tk.Button(w2,bg="light blue",width=10,command = exit,text="Home", font=("Arial", 11))
home.place(x=500, y=550)


w2.mainloop()
