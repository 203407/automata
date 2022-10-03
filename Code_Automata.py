import time
import psycopg2
from tkinter import *
from tkinter import messagebox as MessageBox


#alfabeto
alfabeto = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z",
            "a","b","c","d","e","f","g","h","i","j","k","l","m","n","ñ","o","p","q","r","s","t","u","v","w","x","y","z",
            "0","1","2","3","4","5","6","7","8","9",
            " ","'","*",";","="]

#tablas de transiciones grandisima :( 
tabla_transiciones_god = [["q0","S","q1"],["q0","s","q1" ],["q1","E","q2" ],["q1","e","q2"],["q2","L","q3"],["q2","l","q3"],
                        ["q3","E","q4" ],["q3","e","q4" ],["q4","C","q5"],["q4","c","q5"],["q5","T","q6"],
                        ["q5","t","q6" ],["q6"," ","q7" ],["q6","*","q11"],["q7"," ","q7"],
                        # q7 a q8 con a..Z
                        #minusculas
                        ["q7","a","q8"],["q7","b","q8"],["q7","c","q8"],["q7","d","q8"],["q7","e","q8"],["q7","f","q8"],
                        ["q7","g","q8"],["q7","h","q8"],["q7","i","q8"],["q7","j","q8"],["q7","k","q8"],["q7","l","q8"],
                        ["q7","m","q8"],["q7","n","q8"],["q7","o","q8"],["q7","p","q8"],["q7","q","q8"],["q7","r","q8"],
                        ["q7","s","q8"],["q7","t","q8"],["q7","u","q8"],["q7","v","q8"],["q7","w","q8"],["q7","x","q8"],["q7","z","q8"],
                        #mayusculas
                        ["q7","A","q8"],["q7","B","q8"],["q7","C","q8"],["q7","D","q8"],["q7","E","q8"],["q7","F","q8"],
                        ["q7","G","q8"],["q7","H","q8"],["q7","I","q8"],["q7","J","q8"],["q7","K","q8"],["q7","L","q8"],
                        ["q7","M","q8"],["q7","N","q8"],["q7","O","q8"],["q7","P","q8"],["q7","Q","q8"],["q7","R","q8"],
                        ["q7","S","q8"],["q7","T","q8"],["q7","U","q8"],["q7","V","q8"],["q7","W","q8"],["q7","X","q8"],["q7","Z","q8"],                                                
                        ["q7","*","q10" ],

                        # q8 a q8 con a..Z
                        #minusculas
                        ["q8","a","q8"],["q8","b","q8"],["q8","c","q8"],["q8","d","q8"],["q8","e","q8"],["q8","f","q8"],
                        ["q8","g","q8"],["q8","h","q8"],["q8","i","q8"],["q8","j","q8"],["q8","k","q8"],["q8","l","q8"],
                        ["q8","m","q8"],["q8","n","q8"],["q8","o","q8"],["q8","p","q8"],["q8","q","q8"],["q8","r","q8"],
                        ["q8","s","q8"],["q8","t","q8"],["q8","u","q8"],["q8","v","q8"],["q8","w","q8"],["q8","x","q8"],["q8","z","q8"],
                        #mayusculas
                        ["q8","A","q8"],["q8","B","q8"],["q8","C","q8"],["q8","D","q8"],["q8","E","q8"],["q8","F","q8"],
                        ["q8","G","q8"],["q8","H","q8"],["q8","I","q8"],["q8","J","q8"],["q8","K","q8"],["q8","L","q8"],
                        ["q8","M","q8"],["q8","N","q8"],["q8","O","q8"],["q8","P","q8"],["q8","Q","q8"],["q8","R","q8"],
                        ["q8","S","q8"],["q8","T","q8"],["q8","U","q8"],["q8","V","q8"],["q8","W","q8"],["q8","X","q8"],["q8","Z","q8"],
                        
                        ["q8",",","q7"],["q8"," ","q9"],

                        ["q9"," ","q9"],
                        # q9 a q8 con a..Z
                        #minusculas
                        ["q9","a","q8"],["q9","b","q8"],["q9","c","q8"],["q9","d","q8"],["q9","e","q8"],["q9","f","q8"],
                        ["q9","g","q8"],["q9","h","q8"],["q9","i","q8"],["q9","j","q8"],["q9","k","q8"],["q9","l","q8"],
                        ["q9","m","q8"],["q9","n","q8"],["q9","o","q8"],["q9","p","q8"],["q9","q","q8"],["q9","r","q8"],
                        ["q9","s","q8"],["q9","t","q8"],["q9","u","q8"],["q9","v","q8"],["q9","w","q8"],["q9","x","q8"],["q9","z","q8"],
                        #mayusculas
                        ["q9","A","q8"],["q9","B","q8"],["q9","C","q8"],["q9","D","q8"],["q9","E","q8"],["q9","F","q8"],
                        ["q9","G","q8"],["q9","H","q8"],["q9","I","q8"],["q9","J","q8"],["q9","K","q8"],["q9","L","q8"],
                        ["q9","M","q8"],["q9","N","q8"],["q9","O","q8"],["q9","P","q8"],["q9","Q","q8"],["q9","R","q8"],
                        ["q9","S","q8"],["q9","T","q8"],["q9","U","q8"],["q9","V","q8"],["q9","W","q8"],["q9","X","q8"],["q9","Z","q8"],
                        ["q9",",","q7" ],["q9","F","q12" ],["q9","f","q12"],
                        ["q2","a","q2"],["q2","'","q3"],
                        ["q10"," ","q10" ],["q10","F","q12" ],["q10","f","q12"],["q11"," ","q11"],["q11","F","q12"],
                        ["q11","f","q12" ],["q12","R","q13" ],["q12","r","q13"],["q13","O","q14"],["q13","o","q14"],
                        ["q14","M","q15" ],["q14","m","q15" ],["q15"," ","q16"],["q16"," ","q16"],
                         # q16 a q17 con a..Z
                        #minusculas
                        ["q16","a","q17"],["q16","b","q17"],["q16","c","q17"],["q16","d","q17"],["q16","e","q17"],["q16","f","q17"],
                        ["q16","g","q17"],["q16","h","q17"],["q16","i","q17"],["q16","j","q17"],["q16","k","q17"],["q16","l","q17"],
                        ["q16","m","q17"],["q16","n","q17"],["q16","o","q17"],["q16","p","q17"],["q16","q","q17"],["q16","r","q17"],
                        ["q16","s","q17"],["q16","t","q17"],["q16","u","q17"],["q16","v","q17"],["q16","w","q17"],["q16","x","q17"],["q16","z","q17"],
                        #mayusculas
                        ["q16","A","q17"],["q16","B","q17"],["q16","C","q17"],["q16","D","q17"],["q16","E","q17"],["q16","F","q17"],
                        ["q16","G","q17"],["q16","H","q17"],["q16","I","q17"],["q16","J","q17"],["q16","K","q17"],["q16","L","q17"],
                        ["q16","M","q17"],["q16","N","q17"],["q16","O","q17"],["q16","P","q17"],["q16","Q","q17"],["q16","R","q17"],
                        ["q16","S","q17"],["q16","T","q17"],["q16","U","q17"],["q16","V","q17"],["q16","W","q17"],["q16","X","q17"],["q16","Z","q17"],
                         # q17 a q17 con a..Z
                        #minusculas
                        ["q17","a","q17"],["q17","b","q17"],["q17","c","q17"],["q17","d","q17"],["q17","e","q17"],["q17","f","q17"],
                        ["q17","g","q17"],["q17","h","q17"],["q17","i","q17"],["q17","j","q17"],["q17","k","q17"],["q17","l","q17"],
                        ["q17","m","q17"],["q17","n","q17"],["q17","o","q17"],["q17","p","q17"],["q17","q","q17"],["q17","r","q17"],
                        ["q17","s","q17"],["q17","t","q17"],["q17","u","q17"],["q17","v","q17"],["q17","w","q17"],["q17","x","q17"],["q17","z","q17"],
                        #mayusculas
                        ["q17","A","q17"],["q17","B","q17"],["q17","C","q17"],["q17","D","q17"],["q17","E","q17"],["q17","F","q17"],
                        ["q17","G","q17"],["q17","H","q17"],["q17","I","q17"],["q17","J","q17"],["q17","K","q17"],["q17","L","q17"],
                        ["q17","M","q17"],["q17","N","q17"],["q17","O","q17"],["q17","P","q17"],["q17","Q","q17"],["q17","R","q17"],
                        ["q17","S","q17"],["q17","T","q17"],["q17","U","q17"],["q17","V","q17"],["q17","W","q17"],["q17","X","q17"],["q17","Z","q17"],
                        ["q17",";","q19"],
                        ["q17"," ","q18" ],["q18"," ","q18" ],["q18",";","q19"],["q18","W","q20"],["q18","w","q20"],
                        ["q20","E","q21" ],["q20","e","q21" ],["q21","R","q22"],["q21","r","q22"],["q22","E","q23"],
                        ["q22","e","q23" ],["q23"," ","q24" ],["q24"," ","q24"],
                         # q24 a q25 con a..Z
                        #minusculas
                        ["q24","a","q25"],["q24","b","q25"],["q24","c","q25"],["q24","d","q25"],["q24","e","q25"],["q24","f","q25"],
                        ["q24","g","q25"],["q24","h","q25"],["q24","i","q25"],["q24","j","q25"],["q24","k","q25"],["q24","l","q25"],
                        ["q24","m","q25"],["q24","n","q25"],["q24","o","q25"],["q24","p","q25"],["q24","q","q25"],["q24","r","q25"],
                        ["q24","s","q25"],["q24","t","q25"],["q24","u","q25"],["q24","v","q25"],["q24","w","q25"],["q24","x","q25"],["q24","z","q25"],
                        #mayusculas
                        ["q24","A","q25"],["q24","B","q25"],["q24","C","q25"],["q24","D","q25"],["q24","E","q25"],["q24","F","q25"],
                        ["q24","G","q25"],["q24","H","q25"],["q24","I","q25"],["q24","J","q25"],["q24","K","q25"],["q24","L","q25"],
                        ["q24","M","q25"],["q24","N","q25"],["q24","O","q25"],["q24","P","q25"],["q24","Q","q25"],["q24","R","q25"],
                        ["q24","S","q25"],["q24","T","q25"],["q24","U","q25"],["q24","V","q25"],["q24","W","q25"],["q24","X","q25"],["q24","Z","q25"],
                        # q25 a q25 con a..Z
                        #minusculas
                        ["q25","a","q25"],["q25","b","q25"],["q25","c","q25"],["q25","d","q25"],["q25","e","q25"],["q25","f","q25"],
                        ["q25","g","q25"],["q25","h","q25"],["q25","i","q25"],["q25","j","q25"],["q25","k","q25"],["q25","l","q25"],
                        ["q25","m","q25"],["q25","n","q25"],["q25","o","q25"],["q25","p","q25"],["q25","q","q25"],["q25","r","q25"],
                        ["q25","s","q25"],["q25","t","q25"],["q25","u","q25"],["q25","v","q25"],["q25","w","q25"],["q25","x","q25"],["q25","z","q25"],
                        #mayusculas
                        ["q25","A","q25"],["q25","B","q25"],["q25","C","q25"],["q25","D","q25"],["q25","E","q25"],["q25","F","q25"],
                        ["q25","G","q25"],["q25","H","q25"],["q25","I","q25"],["q25","J","q25"],["q25","K","q25"],["q25","L","q25"],
                        ["q25","M","q25"],["q25","N","q25"],["q25","O","q25"],["q25","P","q25"],["q25","Q","q25"],["q25","R","q25"],
                        ["q25","S","q25"],["q25","T","q25"],["q25","U","q25"],["q25","V","q25"],["q25","W","q25"],["q25","X","q25"],["q25","Z","q25"],
                        ["q25","=","q26"],["q25"," ","q27"],["q27"," ","q27"],["q27","=","q26"],["q26"," ","q26"],
                        # q26 a q28 con 0..9
                        ["q26","0","q28"],["q26","1","q28"],["q26","2","q28"],["q26","3","q28"],["q26","4","q28"],["q26","5","q28"],
                        ["q26","6","q28"],["q26","7","q28"],["q26","8","q28"],["q26","9","q28"],                        
                        ["q26","'","q32"],
                        # q28 a q28 con 0..9
                        ["q28","0","q28"],["q28","1","q28"],["q28","2","q28"],["q28","3","q28"],["q28","4","q28"],["q28","5","q28"],
                        ["q28","6","q28"],["q28","7","q28"],["q28","8","q28"],["q28","9","q28"],                

                        ["q28",";","q29"],["q28"," ","q30"],["q30"," ","q30"],["q30",";","q31"],["q30","A","q37"],["q30","a","q37"],
                        ["q30","O","q39"],["q30","o","q39"],
                        #q32 a q32 con 0...9                        
                        ["q32","0","q32"],["q32","1","q32"],["q32","2","q32"],["q32","3","q32"],["q32","4","q32"],["q32","5","q32"],
                        ["q32","6","q32"],["q32","7","q32"],["q32","8","q32"],["q32","9","q32"],                
                        #q32 a q32 con a...Z                         
                        #minusculas
                        ["q32","a","q32"],["q32","b","q32"],["q32","c","q32"],["q32","d","q32"],["q32","e","q32"],["q32","f","q32"],
                        ["q32","g","q32"],["q32","h","q32"],["q32","i","q32"],["q32","j","q32"],["q32","k","q32"],["q32","l","q32"],
                        ["q32","m","q32"],["q32","n","q32"],["q32","o","q32"],["q32","p","q32"],["q32","q","q32"],["q32","r","q32"],
                        ["q32","s","q32"],["q32","t","q32"],["q32","u","q32"],["q32","v","q32"],["q32","w","q32"],["q32","x","q32"],["q32","z","q32"],
                        #mayusculas
                        ["q32","A","q32"],["q32","B","q32"],["q32","C","q32"],["q32","D","q32"],["q32","E","q32"],["q32","F","q32"],
                        ["q32","G","q32"],["q32","H","q32"],["q32","I","q32"],["q32","J","q32"],["q32","K","q32"],["q32","L","q32"],
                        ["q32","M","q32"],["q32","N","q32"],["q32","O","q32"],["q32","P","q32"],["q32","Q","q32"],["q32","R","q32"],
                        ["q32","S","q32"],["q32","T","q32"],["q32","U","q32"],["q32","V","q32"],["q32","W","q32"],["q32","X","q32"],["q32","Z","q32"],
                        
                        ["q32","'","q34"],["q34",";","q33"],["q34"," ","q35"],["q35"," ","q35"],["q35",";","q36"],["q35","A","q37"],
                        ["q35","a","q37"],["q35","O","q39"],["q35","o","q39"],["q37","N","q38"],["q37","n","q38"],["q38","D","q24"],
                        ["q38","d","q24"],["q39","R","q24"],["q35","r","q24"],
                        ["q29"," ","q29"],["q31"," ","q31"],["q33"," ","q33"],["q36"," ","q36"],["q19"," ","q19"]
                        ]



DBNAME = ""
DBPASS = ""
NAMETABLE = ""


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
           
            conn = psycopg2.connect(
                host = 'localhost',
                user = 'postgres',
                password = passdb,
                database = nombredb
            )
            
            cur = conn.cursor()
            
            cur.execute("select exists(select * from information_schema.tables where table_name=%s)", (f'{namtb}',))
            if cur.fetchone()[0]:
                MessageBox.showinfo("about","Datos correctos")
            else:
                MessageBox.showinfo("about","tabla no encontrada")
                dbtable2.delete(0,'end')
                dbpass2.delete(0,'end')
                dbaname2.delete(0,'end')
            
            conn.close()
    
    except Exception as ex:
         MessageBox.showinfo("about","no se pudo crear la conexion con los datos proporcionados")



def checksqltense():

    #Bandera para saber si pertenece al alfabeto
    bandera = True
    #tabla para almacenar los estados 
    tabla_mvestados = []
    #estado inicial 
    EI = "q0"
    #estados finales
    EF = ["q19","q29","q31","q33","q36"]
    #estado actual 
    EA = EI
    #caracteres validos de la cadena
    caracteres_validos = []
    #caractees invalidos de la cadena
    caracteres_invalidos = []


    cadena = textsql2.get()    

    for data in cadena:    
    #verificar que el caracter pertenezca al alfabetos
        if data in alfabeto:    
            #buscar en la tabla de transiciones 
            for df in tabla_transiciones_god:  
                if data in df and EA in df:                            
                    #agregar elementos en la tabla de estados recorrido si es que es necerio mostrar
                    #df[2] a donde se dirigio
                    tabla_mvestados.append([EA, data, df[2]])
                    #actualziar el estado en que nos encontramos
                    EA = df[2]     
                    #Caracteres validos (si es que es necesario mostrar)
                    caracteres_validos.append(data)                
        else:
            #caracteres invalidos (si es que es necesario mostrar)
            caracteres_invalidos.append(data)
            bandera = False
            
    # if caracteres_validos != []:
    #     print(f'Los siguietnes son los caracteres validos de la cadena {caracteres_validos}')

    # if caracteres_invalidos != []:
    #     print(f'Los siguietnes son los caracteres invalidos de la cadena {caracteres_invalidos}')

    #determinar si al final la cadena es valida o no
    if (EA in EF) and (bandera == True):       
        return True
        #print('la cadena es valida')
        #Tabla de transiciones
        #print("transciones generadas")
        #for x in tabla_mvestados:
           # print(x)
        
    else:        
        return False
        #print('la cadena no es valida')
        #Tabla de transiciones
        #if tabla_mvestados != []:
         #   print("transciones generadas")
          #  for x in tabla_mvestados:
           #     print(x)


def  checkdbsql():


    lookd = checksqltense()
    l = textsql2.get()

    try:
        conn = psycopg2.connect(
            host = 'localhost',
            user = 'postgres',
            password = DBPASS,
            database = DBNAME
        )
        if lookd: 
            
            try:
                con = conn.cursor()
                
                print(l)
                con.execute(l)        
                mascota = con.fetchone()                
                MessageBox.showinfo("about","La sentencia se valida y tiene consistendia con la base de datos")

            except psycopg2.Error as e:                
                MessageBox.showinfo("about","La cadena es valida pero no tiene consistencia con la base de datos")    
            finally:
                conn.close()
        else:
            MessageBox.showinfo("about","La cadena no es una sentencia valida de sql")

    except Exception as ex:
        pass
    finally:
        textsql2.delete(0,'end')
        conn.close()
        


raiz = Tk()
raiz.title("Automatas")
raiz.geometry("800x600")
raiz.config(background="Light green")

dbaname = Label(raiz, text="Nombre de la base de datos:")
dbaname.place(relx=0.2,rely=0.1,relheight=0.04,relwidth=0.27)

dbaname2 = Entry(raiz,)
dbaname2.place(relx=0.5,rely=0.1,relheight=0.04,relwidth=0.27)

dbpass = Label(raiz, text="contraseña base de datos:")
dbpass.place(relx=0.2,rely=0.2,relheight=0.04,relwidth=0.27)

dbpass2 = Entry(raiz, )
dbpass2.place(relx=0.5,rely=0.2,relheight=0.04,relwidth=0.27)

dbtable = Label(raiz, text="Nombre de la tabla de la base de datos:")
dbtable.place(relx=0.2,rely=0.3,relheight=0.04,relwidth=0.27)

dbtable2 = Entry(raiz, )
dbtable2.place(relx=0.5,rely=0.3,relheight=0.04,relwidth=0.27)


bt = Button(raiz,text="Validar informacion",background="orange",command=add_Data)
bt.place(relx=0.35,rely=0.4,relheight=0.04,relwidth=0.27)



textsql = Label(raiz, text="Validar sentencia sql: ",background="yellow")
textsql.place(relx=0.35,rely=0.6,relheight=0.04,relwidth=0.27)

textsql2 = Entry(raiz)
textsql2.place(relx=0.35,rely=0.7,relheight=0.1,relwidth=0.27)

bt2 = Button(raiz,text="Validar informacion",background="orange",command=checkdbsql)
bt2.place(relx=0.35,rely=0.9,relheight=0.04,relwidth=0.27)

raiz.mainloop()
