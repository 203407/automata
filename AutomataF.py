import psycopg2
from tkinter import *
from tkinter import messagebox as MessageBox

import re

#alfabeto
alfabeto = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
            "a","b","c","d","e","f","g","h","i","j","k","l","m","n","ñ","o","p","q","r","s","t","u","v","w","x","y","z",
            "0","1","2","3","4","5","6","7","8","9",
            " ","'","*",";","=",",","<",">","!",]

#conjunto de transiciones basado en el automata                       
tabla_transiciones_god = [["q0","S",["q1"]],["q0","s",["q1"] ],["q1","E",["q2"] ],["q1","e",["q2"]],["q2","L",["q3"]],["q2","l",["q3"]],
                        ["q3","E",["q4"] ],["q3","e",["q4"] ],["q4","C",["q5"] ],["q4","c",["q5"]],["q5","T",["q6"]],
                        ["q5","t",["q6"] ],["q6"," ",["q7"] ],["q6","*",["q13"] ],["q7"," ",["q7"]],["q7","*",["q13"]],
                        # q7 a q8 con a..Z
                        #minusculas
                        ["q7","a",["q8"]],["q7","b",["q8"]],["q7","c",["q8"]],["q7","d",["q8"]],["q7","e",["q8"]],["q7","f",["q8"]],
                        ["q7","g",["q8"]],["q7","h",["q8"]],["q7","i",["q8"]],["q7","j",["q8"]],["q7","k",["q8"]],["q7","l",["q8"]],
                        ["q7","m",["q8"]],["q7","n",["q8"]],["q7","o",["q8"]],["q7","p",["q8"]],["q7","q",["q8"]],["q7","r",["q8"]],
                        ["q7","s",["q8"]],["q7","t",["q8"]],["q7","u",["q8"]],["q7","v",["q8"]],["q7","w",["q8"]],["q7","x",["q8"]],["q7","z",["q8"]],
                        #mayusculas
                        ["q7","A",["q8"]],["q7","B",["q8"]],["q7","C",["q8"]],["q7","D",["q8"]],["q7","E",["q8"]],["q7","F",["q8"]],
                        ["q7","G",["q8"]],["q7","H",["q8"]],["q7","I",["q8"]],["q7","J",["q8"]],["q7","K",["q8"]],["q7","L",["q8"]],
                        ["q7","M",["q8"]],["q7","N",["q8"]],["q7","O",["q8"]],["q7","P",["q8"]],["q7","Q",["q8"]],["q7","R",["q8"]],
                        ["q7","S",["q8"]],["q7","T",["q8"]],["q7","U",["q8"]],["q7","V",["q8"]],["q7","W",["q8"]],["q7","X",["q8"]],["q7","Z",["q8"]],                                                                        
                        ["q8",",",["q9"]],["q8"," ",["q11"]],
                         # q8 a q10 con a..Z
                        #minusculas
                        ["q8","a",["q10"]],["q8","b",["q10"]],["q8","c",["q10"]],["q8","d",["q10"]],["q8","e",["q10"]],["q8","f",["q10"]],
                        ["q8","g",["q10"]],["q8","h",["q10"]],["q8","i",["q10"]],["q8","j",["q10"]],["q8","k",["q10"]],["q8","l",["q10"]],
                        ["q8","m",["q10"]],["q8","n",["q10"]],["q8","o",["q10"]],["q8","p",["q10"]],["q8","q",["q10"]],["q8","r",["q10"]],
                        ["q8","s",["q10"]],["q8","t",["q10"]],["q8","u",["q10"]],["q8","v",["q10"]],["q8","w",["q10"]],["q8","x",["q10"]],["q8","z",["q10"]],
                        #mayusculas
                        ["q8","A",["q10"]],["q8","B",["q10"]],["q8","C",["q10"]],["q8","D",["q10"]],["q8","E",["q10"]],["q8","F",["q10"]],
                        ["q8","G",["q10"]],["q8","H",["q10"]],["q8","I",["q10"]],["q8","J",["q10"]],["q8","K",["q10"]],["q8","L",["q10"]],
                        ["q8","M",["q10"]],["q8","N",["q10"]],["q8","O",["q10"]],["q8","P",["q10"]],["q8","Q",["q10"]],["q8","R",["q10"]],
                        ["q8","S",["q10"]],["q8","T",["q10"]],["q8","U",["q10"]],["q8","V",["q10"]],["q8","W",["q10"]],["q8","X",["q10"]],["q8","Z",["q10"]],
                        ["q9"," ",["q9"]],
                         # q9 a q10 con a..Z
                        #minusculas
                        ["q9","a",["q10"]],["q9","b",["q10"]],["q9","c",["q10"]],["q9","d",["q10"]],["q9","e",["q10"]],["q9","f",["q10"]],
                        ["q9","g",["q10"]],["q9","h",["q10"]],["q9","i",["q10"]],["q9","j",["q10"]],["q9","k",["q10"]],["q9","l",["q10"]],
                        ["q9","m",["q10"]],["q9","n",["q10"]],["q9","o",["q10"]],["q9","p",["q10"]],["q9","q",["q10"]],["q9","r",["q10"]],
                        ["q9","s",["q10"]],["q9","t",["q10"]],["q9","u",["q10"]],["q9","v",["q10"]],["q9","w",["q10"]],["q9","x",["q10"]],["q9","z",["q10"]],
                        #mayusculas
                        ["q9","A",["q10"]],["q9","B",["q10"]],["q9","C",["q10"]],["q9","D",["q10"]],["q9","E",["q10"]],["q9","F",["q10"]],
                        ["q9","G",["q10"]],["q9","H",["q10"]],["q9","I",["q10"]],["q9","J",["q10"]],["q9","K",["q10"]],["q9","L",["q10"]],
                        ["q9","M",["q10"]],["q9","N",["q10"]],["q9","O",["q10"]],["q9","P",["q10"]],["q9","Q",["q10"]],["q9","R",["q10"]],
                        ["q9","S",["q10"]],["q9","T",["q10"]],["q9","U",["q10"]],["q9","V",["q10"]],["q9","W",["q10"]],["q9","X",["q10"]],["q9","Z",["q10"]],
                         # q10 a q10 con a..Z
                        #minusculas
                        ["q10","a",["q10"]],["q10","b",["q10"]],["q10","c",["q10"]],["q10","d",["q10"]],["q10","e",["q10"]],["q10","f",["q10"]],
                        ["q10","g",["q10"]],["q10","h",["q10"]],["q10","i",["q10"]],["q10","j",["q10"]],["q10","k",["q10"]],["q10","l",["q10"]],
                        ["q10","m",["q10"]],["q10","n",["q10"]],["q10","o",["q10"]],["q10","p",["q10"]],["q10","q",["q10"]],["q10","r",["q10"]],
                        ["q10","s",["q10"]],["q10","t",["q10"]],["q10","u",["q10"]],["q10","v",["q10"]],["q10","w",["q10"]],["q10","x",["q10"]],["q10","z",["q10"]],
                        #mayusculas
                        ["q10","A",["q10"]],["q10","B",["q10"]],["q10","C",["q10"]],["q10","D",["q10"]],["q10","E",["q10"]],["q10","F",["q10"]],
                        ["q10","G",["q10"]],["q10","H",["q10"]],["q10","I",["q10"]],["q10","J",["q10"]],["q10","K",["q10"]],["q10","L",["q10"]],
                        ["q10","M",["q10"]],["q10","N",["q10"]],["q10","O",["q10"]],["q10","P",["q10"]],["q10","Q",["q10"]],["q10","R",["q10"]],
                        ["q10","S",["q10"]],["q10","T",["q10"]],["q10","U",["q10"]],["q10","V",["q10"]],["q10","W",["q10"]],["q10","X",["q10"]],["q10","Z",["q10"]],
                        ["q10",",",["q9"]],["q10"," ",["q11"]],["q11",",",["q9"]],["q11"," ",["q11"]],["q11","f",["q12"]],["q11","F",["q12"]],
                        ["q13","f",["q12"]],["q13","F",["q12"]],["q13"," ",["q13"]],["q12","R",["q14"]],["q12","r",["q14"]],["q14","o",["q15"]],
                        ["q14","O",["q15"]],["q15","M",["q16"]],["q15","m",["q16"]],["q16"," ",["q17"]],["q17"," ",["q17"]],
                         # q17 a q18 con a..Z
                        #minusculas
                        ["q17","a",["q18"]],["q17","b",["q18"]],["q17","c",["q18"]],["q17","d",["q18"]],["q17","e",["q18"]],["q17","f",["q18"]],
                        ["q17","g",["q18"]],["q17","h",["q18"]],["q17","i",["q18"]],["q17","j",["q18"]],["q17","k",["q18"]],["q17","l",["q18"]],
                        ["q17","m",["q18"]],["q17","n",["q18"]],["q17","o",["q18"]],["q17","p",["q18"]],["q17","q",["q18"]],["q17","r",["q18"]],
                        ["q17","s",["q18"]],["q17","t",["q18"]],["q17","u",["q18"]],["q17","v",["q18"]],["q17","w",["q18"]],["q17","x",["q18"]],["q17","z",["q18"]],
                        #mayusculas
                        ["q17","A",["q18"]],["q17","B",["q18"]],["q17","C",["q18"]],["q17","D",["q18"]],["q17","E",["q18"]],["q17","F",["q18"]],
                        ["q17","G",["q18"]],["q17","H",["q18"]],["q17","I",["q18"]],["q17","J",["q18"]],["q17","K",["q18"]],["q17","L",["q18"]],
                        ["q17","M",["q18"]],["q17","N",["q18"]],["q17","O",["q18"]],["q17","P",["q18"]],["q17","Q",["q18"]],["q17","R",["q18"]],
                        ["q17","S",["q18"]],["q17","T",["q18"]],["q17","U",["q18"]],["q17","V",["q18"]],["q17","W",["q18"]],["q17","X",["q18"]],["q17","Z",["q18"]],
                         # q18 a q18 con a..Z
                        #minusculas
                        ["q18","a",["q18"]],["q18","b",["q18"]],["q18","c",["q18"]],["q18","d",["q18"]],["q18","e",["q18"]],["q18","f",["q18"]],
                        ["q18","g",["q18"]],["q18","h",["q18"]],["q18","i",["q18"]],["q18","j",["q18"]],["q18","k",["q18"]],["q18","l",["q18"]],
                        ["q18","m",["q18"]],["q18","n",["q18"]],["q18","o",["q18"]],["q18","p",["q18"]],["q18","q",["q18"]],["q18","r",["q18"]],
                        ["q18","s",["q18"]],["q18","t",["q18"]],["q18","u",["q18"]],["q18","v",["q18"]],["q18","w",["q18"]],["q18","x",["q18"]],["q18","z",["q18"]],
                        #mayusculas
                        ["q18","A",["q18"]],["q18","B",["q18"]],["q18","C",["q18"]],["q18","D",["q18"]],["q18","E",["q18"]],["q18","F",["q18"]],
                        ["q18","G",["q18"]],["q18","H",["q18"]],["q18","I",["q18"]],["q18","J",["q18"]],["q18","K",["q18"]],["q18","L",["q18"]],
                        ["q18","M",["q18"]],["q18","N",["q18"]],["q18","O",["q18"]],["q18","P",["q18"]],["q18","Q",["q18"]],["q18","R",["q18"]],
                        ["q17","S",["q18"]],["q18","T",["q18"]],["q18","U",["q18"]],["q18","V",["q18"]],["q18","W",["q18"]],["q18","X",["q18"]],["q18","Z",["q18"]],
                        ["q18",";",["q19"]],["q18"," ",["q20"]],["q20"," ",["q20"]],["q20",";",["q19"]],["q20","W",["q21"]],["q20","w",["q21"]],
                        ["q21","H",["q22"]],["q21","h",["q22"]],["q22","E",["q23"]],["q22","e",["q23"]],["q23","R",["q24"]],["q23","r",["q24"]],
                        ["q24","E",["q25"]],["q24","e",["q25"]],["q25"," ",["q26"]],["q26"," ",["q26"]],
                         # q26 a q27 o a q42 con a..Z
                        #minusculas
                        ["q26","a",["q27"]],["q26","b",["q27"]],["q26","c",["q27"]],["q26","d",["q27"]],["q26","e",["q27"]],["q26","f",["q27"]],
                        ["q26","g",["q27"]],["q26","h",["q27"]],["q26","i",["q27"]],["q26","j",["q27"]],["q26","k",["q27"]],["q26","l",["q27"]],
                        ["q26","m",["q27"]],["q26","n",["q27","q42"]],["q26","o",["q27"]],["q26","p",["q27"]],["q26","q",["q27"]],["q26","r",["q27"]],
                        ["q26","s",["q27"]],["q26","t",["q27"]],["q26","u",["q27"]],["q26","v",["q27"]],["q26","w",["q27"]],["q26","x",["q27"]],["q26","z",["q27"]],
                        #mayusculas
                        ["q26","A",["q27"]],["q26","B",["q27"]],["q26","C",["q27"]],["q26","D",["q27"]],["q26","E",["q27"]],["q26","F",["q27"]],
                        ["q26","G",["q27"]],["q26","H",["q27"]],["q26","I",["q27"]],["q26","J",["q27"]],["q26","K",["q27"]],["q26","L",["q27"]],
                        ["q26","M",["q27"]],["q26","N",["q27","q42"]],["q26","O",["q27"]],["q26","P",["q27"]],["q26","Q",["q27"]],["q26","R",["q27"]],
                        ["q26","S",["q27"]],["q26","T",["q27"]],["q26","U",["q27"]],["q26","V",["q27"]],["q26","W",["q27"]],["q26","X",["q27"]],["q26","Z",["q27"]],                        
                         # q27 a q27 con a..Z
                        #minusculas
                        ["q27","a",["q27"]],["q27","b",["q27"]],["q27","c",["q27"]],["q27","d",["q27"]],["q27","e",["q27"]],["q27","f",["q27"]],
                        ["q27","g",["q27"]],["q27","h",["q27"]],["q27","i",["q27"]],["q27","j",["q27"]],["q27","k",["q27"]],["q27","l",["q27"]],
                        ["q27","m",["q27"]],["q27","n",["q27"]],["q27","o",["q27"]],["q27","p",["q27"]],["q27","q",["q27"]],["q27","r",["q27"]],
                        ["q27","s",["q27"]],["q27","t",["q27"]],["q27","u",["q27"]],["q27","v",["q27"]],["q27","w",["q27"]],["q27","x",["q27"]],["q27","z",["q27"]],
                        #mayusculas
                        ["q27","A",["q27"]],["q27","B",["q27"]],["q27","C",["q27"]],["q27","D",["q27"]],["q27","E",["q27"]],["q27","F",["q27"]],
                        ["q27","G",["q27"]],["q27","H",["q27"]],["q27","I",["q27"]],["q27","J",["q27"]],["q27","K",["q27"]],["q27","L",["q27"]],
                        ["q27","M",["q27"]],["q27","N",["q27"]],["q27","O",["q27"]],["q27","P",["q27"]],["q27","Q",["q27"]],["q27","R",["q27"]],
                        ["q27","S",["q27"]],["q27","T",["q27"]],["q27","U",["q27"]],["q27","V",["q27"]],["q27","W",["q27"]],["q27","X",["q27"]],["q27","Z",["q27"]],
                        
                        ["q27","=",["q29"]],
                        ["q27","<",["q29","q47"]],
                        ["q27",">",["q29","q47"]],                        
                        ["q27","!",["q47"]],
                        ["q47","=",["q29"]],


                        ["q27"," ",["q28"]],["q28"," ",["q28"]],

                        ["q28","=",["q29"]],
                        ["q28","<",["q29","q48"]],
                        ["q28",">",["q29","q48"]],                        
                        ["q28","!",["q48"]],
                        ["q48","=",["q29"]],



                        ["q29"," ",["q29"]],
                        # q29 a q30 con 0..9
                        ["q29","0",["q30"]],["q29","1",["q30"]],["q29","2",["q30"]],["q29","3",["q30"]],["q29","4",["q30"]],["q29","5",["q30"]],
                        ["q29","6",["q30"]],["q29","7",["q30"]],["q29","8",["q30"]],["q29","9",["q30"]], 
                           # q30 a q30 con 0..9
                        ["q30","0",["q30"]],["q30","1",["q30"]],["q30","2",["q30"]],["q30","3",["q30"]],["q30","4",["q30"]],["q30","5",["q30"]],
                        ["q30","6",["q30"]],["q30","7",["q30"]],["q30","8",["q30"]],["q30","9",["q30"]],["q30",";",["q31"]],["q30"," ",["q32"]], 
                        ["q32"," ",["q3 "]],["q32",";",["q33"]],
                        ["q29","'",["q34"]],
                         # q34 a q34 con 0..9
                        ["q34","0",["q34"]],["q34","1",["q34"]],["q34","2",["q34"]],["q34","3",["q34"]],["q34","4",["q34"]],["q29","5",["q34"]],
                        ["q34","6",["q34"]],["q34","7",["q34"]],["q34","8",["q34"]],["349","9",["q34"]], 
                         # q34 a q34 con a..Z
                        #minusculas
                        ["q34","a",["q34"]],["q34","b",["q34"]],["q34","c",["q34"]],["q34","d",["q34"]],["q34","e",["q34"]],["q34","f",["q34"]],
                        ["q34","g",["q34"]],["q34","h",["q34"]],["q34","i",["q34"]],["q34","j",["q34"]],["q34","k",["q34"]],["q34","l",["q34"]],
                        ["q34","m",["q34"]],["q34","n",["q34"]],["q34","o",["q34"]],["q34","p",["q34"]],["q34","q",["q34"]],["q34","r",["q34"]],
                        ["q34","s",["q34"]],["q34","t",["q34"]],["q34","u",["q34"]],["q34","v",["q34"]],["q34","w",["q34"]],["q34","x",["q34"]],["q34","z",["q34"]],
                        #mayusculas
                        ["q34","A",["q34"]],["q34","B",["q34"]],["q34","C",["q34"]],["q34","D",["q34"]],["q34","E",["q34"]],["q34","F",["q34"]],
                        ["q34","G",["q34"]],["q34","H",["q34"]],["q34","I",["q34"]],["q34","J",["q34"]],["q34","K",["q34"]],["q34","L",["q34"]],
                        ["q34","M",["q34"]],["q34","N",["q34"]],["q34","O",["q34"]],["q34","P",["q34"]],["q34","Q",["q34"]],["q34","R",["q34"]],
                        ["q34","S",["q34"]],["q34","T",["q34"]],["q34","U",["q34"]],["q34","V",["q34"]],["q34","W",["q34"]],["q34","X",["q34"]],["q34","Z",["q34"]],
                        ["q34","'",["q35"]],
                        ["q35",";",["q36"]],["q35"," ",["q37"]],["q37"," ",["q37"]],["q37",";",["q38"]],
                        ["q32","A",["q39"]],["q32","a",["q39"]],["q32","O",["q41"]],["q32","o",["q41"]],
                        ["q37","A",["q39"]],["q37","a",["q39"]],["q37","O",["q41"]],["q37","o",["q41"]],
                        ["q39","N",["q40"]],["q39","n",["q40"]],["q40","D",["q46"]],["q40","d",["q46"]],
                        ["q41","R",["q46"]],["q41","r",["q46"]],
                        ["q42","O",["q43"]],["q42","o",["q43"]],
                        ["q43","T",["q44"]],["q43","t",["q44"]],
                        ["q44"," ",["q45"]],["q45"," ",["q45"]],
                        # q45 a q27  con a..Z
                        #minusculas
                        ["q45","a",["q27"]],["q45","b",["q27"]],["q45","c",["q27"]],["q45","d",["q27"]],["q45","e",["q27"]],["q45","f",["q27"]],
                        ["q45","g",["q27"]],["q45","h",["q27"]],["q45","i",["q27"]],["q45","j",["q27"]],["q45","k",["q27"]],["q45","l",["q27"]],
                        ["q45","m",["q27"]],["q45","n",["q27"]],["q45","o",["q27"]],["q45","p",["q27"]],["q45","q",["q27"]],["q45","r",["q27"]],
                        ["q45","s",["q27"]],["q45","t",["q27"]],["q45","u",["q27"]],["q45","v",["q27"]],["q45","w",["q27"]],["q45","x",["q27"]],["q45","z",["q27"]],
                        #mayusculas
                        ["q45","A",["q27"]],["q45","B",["q27"]],["q45","C",["q27"]],["q45","D",["q27"]],["q45","E",["q27"]],["q45","F",["q27"]],
                        ["q45","G",["q27"]],["q45","H",["q27"]],["q45","I",["q27"]],["q45","J",["q27"]],["q45","K",["q27"]],["q45","L",["q27"]],
                        ["q45","M",["q27"]],["q45","N",["q27"]],["q45","O",["q27"]],["q45","P",["q27"]],["q45","Q",["q27"]],["q45","R",["q27"]],
                        ["q45","S",["q27"]],["q45","T",["q27"]],["q45","U",["q27"]],["q45","V",["q27"]],["q45","W",["q27"]],["q45","X",["q27"]],["q45","Z",["q27"]],      
                        ["q46"," ",["q26"]],
                        
]

DBNAME = ""
DBPASS = ""
NAMETABLE = ""

#Estado inicial
EI = "q0"
    #estados finales
EF = ["q19","q31","q33","q36","q38"]    #estados finales
    #estado actual 
EA = EI    

def add_Data(): 
    nombredb = dbaname2.get()
    passdb = dbpass2.get()    
    namtb = dbtable2.get()
    
    global DBNAME;
    global DBPASS;
    global NAMETABLE;

    DBNAME = nombredb
    DBPASS = passdb
    NAMETABLE = namtb
    
    dbtable2.delete(0,'end')
    dbpass2.delete(0,'end')
    dbaname2.delete(0,'end')
    try:
        
        if psycopg2.connect(host = 'localhost',user = 'postgres',password = passdb,database = nombredb):                        
           
            conn = psycopg2.connect(host = 'localhost',user = 'postgres',password = passdb,database = nombredb)
            
            cur = conn.cursor()
            
            cur.execute("select exists(select * from information_schema.tables where table_name=%s)", (f'{namtb}',))
            if cur.fetchone()[0]:
                MessageBox.showinfo("about","Datos correctos")
                bt2.configure(state='normal')
                textsql2.configure(state='normal',borderwidth=0.5, relief="solid")
                textsql.configure(background="lime")
            else:
                MessageBox.showinfo("about",f'tabla " {NAMETABLE} " no encontrada')
                dbtable2.delete(0,'end')
                dbpass2.delete(0,'end')
                dbaname2.delete(0,'end')
            
            conn.close()
    
    except Exception as ex:
         MessageBox.showinfo("about","no se pudo crear la conexion con los datos proporcionados")


def checksqltense(cadena,estadoActual):    
   
    if cadena == "":        
        return estadoActual in EF  #revisar si el estado actual es un estado final
    else:
        letra = cadena[0:1]                        
        
        if letra in alfabeto:     #verificar que este en el alfabeto             
            
            for transi in tabla_transiciones_god:    #iteraciones para revisar si existe la transicion

                if letra == "*":  #al usar" "re.search" no admite el caracter "*" asi que lo convertimos
                    letra = "\*"                       

                if re.search(letra,transi[1]) and re.search(estadoActual,transi[0]):     #revisar que exista la transicion            
                    newstring = cadena[1:]            
                    for x in transi[2]:      #iterar los diferentes caminos que existan 
                        if checksqltense(newstring,x):  #recursividad para iterar esos caminos
                            return True                
                            
        else:
            return 0


def  checkdbsql():

    cadena = textsql2.get() 
    lookd = checksqltense(cadena,EA)
    l = textsql2.get()

    try:
        conn = psycopg2.connect(host = 'localhost',user = 'postgres',password = DBPASS,database = DBNAME)
        if lookd: 
            
            try:
                con = conn.cursor()                                
                con.execute(l)                                     
                MessageBox.showinfo('about',f'La sentencia es valida y tiene consistencia con la base de datos\n {cadena}')

            except psycopg2.Error as e:                
                MessageBox.showinfo('about',f'La cadena es valida pero no tiene consistencia con la base de datos \n {cadena}')    
            finally:
                conn.close()
        else:
            MessageBox.showinfo("about",f'La cadena no es una sentencia valida de sql \n {cadena}')

    except Exception as ex:
        pass
    finally:
        textsql2.delete(0,'end')
        conn.close()
        


raiz = Tk()
raiz.title("Automatas")
raiz.geometry("800x600")
raiz.config(background="Light green")

dbtitle = Label(raiz, text="Evaluador de sentencias SQL",borderwidth=0.5, relief="solid")
dbtitle.place(relx=0.35,rely=0.03,relheight=0.04,relwidth=0.27)


dbaname = Label(raiz, text="Nombre de la base de datos:",borderwidth=0.5, relief="solid")
dbaname.place(relx=0.2,rely=0.1,relheight=0.04,relwidth=0.27)

dbaname2 = Entry(raiz,borderwidth=0.5, relief="solid")
dbaname2.place(relx=0.5,rely=0.1,relheight=0.04,relwidth=0.27)

dbpass = Label(raiz, text="contraseña base de datos:",borderwidth=0.5, relief="solid")
dbpass.place(relx=0.2,rely=0.2,relheight=0.04,relwidth=0.27)

dbpass2 = Entry(raiz, borderwidth=0.5, relief="solid")
dbpass2.place(relx=0.5,rely=0.2,relheight=0.04,relwidth=0.27)

dbtable = Label(raiz, text="Nombre de la tabla de la base de datos:",borderwidth=0.5, relief="solid")
dbtable.place(relx=0.2,rely=0.3,relheight=0.04,relwidth=0.27)

dbtable2 = Entry(raiz, borderwidth=0.5, relief="solid")
dbtable2.place(relx=0.5,rely=0.3,relheight=0.04,relwidth=0.27)


bt = Button(raiz,text="Validar informacion",background="orange",command=add_Data)
bt.place(relx=0.35,rely=0.4,relheight=0.04,relwidth=0.27)



textsql = Label(raiz, text="Validar sentencia sql: ",background="red",borderwidth=0.5, relief="solid")
textsql.place(relx=0.35,rely=0.6,relheight=0.04,relwidth=0.27)

textsql2 = Entry(raiz)
textsql2.configure(state='disabled')
textsql2.place(relx=0.29,rely=0.7,relheight=0.1,relwidth=0.40)

bt2 = Button(raiz,text="Validar informacion",background="orange",command=checkdbsql)
bt2.configure(state='disabled')
bt2.place(relx=0.35,rely=0.9,relheight=0.04,relwidth=0.27)

raiz.mainloop()