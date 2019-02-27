from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfile
import threading
import operator
import queue
from threading import Thread

Tk().withdraw() 
archivo = askopenfilename()
repeticiones=256
codigo = ""

class marchando(Thread):

    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except:
                pass
            finally:
                self.tasks.task_done()

class dobleNodo:
     
    def __init__(self ,simbolo=[],freq= [],der = None , izq = None):
        
        self.simbolo = simbolo
        self.freq = freq
        self.sig = None
        self.ant = None
        self.der = der
        self.izq = izq

    def __str__(self):
        return "Datos {} y simbolo {}".format(self.freq,self.simbolo)
 
class piscinaHilos:
    def __init__(self, num_threads):
        self.tasks = queue.Queue(num_threads)
        for _ in range(num_threads):
            marchando(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        self.tasks.join()


class listaArbol:
    
    def __init__(self):

        self.prim = None
        self.ult = None
    
    def isEmpty(self):
        return self.prim == None

    def listSize(self ,node):
        count = 0
        node = self.prim
        while node is not None:
            count = count + 1
            node = node.sig

        return count

    def aniadeFinal(self,simbolo , freq):
        nuevoNodo = dobleNodo(simbolo = simbolo, freq = freq)  
        if self.prim is None:
            self.prim = nuevoNodo
            self.ult = nuevoNodo       
        else:
            self.ult.sig = nuevoNodo
            nuevoNodo.ant = self.ult
            self.ult = nuevoNodo

    def imprime (self, node):
        while node != None:
            ult = node 
            node = node.sig

    def eliminaF(self):
        if self.prim == None:
            print("aqui andamos")
        elif self.prim == self.ult:
            self.prim = None 
            self.ult = None
        else:           
            self.ult = self.ult.ant
            self.ult.sig = None

    def buscaAniade(self , node , auxiliar1 , auxiliarExtra , simbolo , freq):
        node = self.prim
        while node is not None:
            
            if(freq >= self.prim.freq):
                dn = dobleNodo(simbolo=simbolo , freq=freq)
                dn.der = auxiliar1
                dn.izq = auxiliarExtra
                self.prim.ant = dn
                dn.sig = self.prim
                self.prim = dn
                return

            if(node.freq <= freq):
                dn = dobleNodo(simbolo=simbolo , freq=freq)
                dn.der = auxiliar1
                dn.izq = auxiliarExtra
                dn.sig = node
                node.ant.sig = dn
                dn.ant = node.ant
                node.ant = dn
                return

            node = node.sig
            
   
def encuentra(actual,dato):
    global codigo
    if actual is not None:
        if dato == actual.simbolo:
            return "1"
        if (encuentra(actual.izq,dato ) == "1"):
            codigo += "0"
            return "1"
        if (encuentra(actual.der,dato ) == "1"):
            codigo += "1"
            return "1"           
    return "0"
        
def buscar_recur(top):
    global codigo
    for i in range(0,repeticiones):#este es con una funcion
        encuentra(top,i)      
    return codigo
    
def freq(text):
    prim_pos = 0
    d = {}
    while prim_pos < repeticiones:     
        d[prim_pos] = 0
        prim_pos += 1
    for c in text:
        if c not in d:
            d[c] = 1
        else:
            d[c] += 1
    return d

def intercambiar(listS, listF,prim_pos , seg_pos):
    #print (prim_pos)
    #print (seg_pos)
    while prim_pos<seg_pos:
        #print(f"comprobando {listS[prim_pos]}  frecuencia {listF[listS[prim_pos]]}")
        #print(f"comprobando {listS[prim_pos+1]}  frecuencia {listF[listS[prim_pos+1]]}")
        if listF[listS[prim_pos]] < listF[listS[prim_pos+1]]:
            auxiliar = listS[prim_pos]
            listS[prim_pos] = listS[prim_pos+1]
            listS[prim_pos+1] = auxiliar 
        prim_pos +=2                
             
if __name__ == "__main__":  
    lista_simbolos = []
    lista_freq = []
    work = 64
    start = 0 
    link = listaArbol()     
    f=open(archivo,"rb")    
    q=[]
    datos = []

    while 1:
        datos.append(f.read(1024))
        if not datos[len(datos)-1]:
            break

        q.append(queue.Queue())
        tj=threading.Thread(target=lambda qq, arg: qq.put(freq(arg)), args=(q[len(q)-1], datos[len(datos)-1]))
        tj.start()

    auxiliar = {}  
    for i in range (0,repeticiones):
        auxiliar[i] = 0

    for i in range(0,len(q)):
        result=q[i].get()
        result2 = result.items()
        for i2 in result:
            auxiliar[i2] += result[i2]
        
    auxiliarExtra= auxiliar.items()
      
    for item in auxiliarExtra:
        lista_simbolos.append(item[0])            
        lista_freq.append(item[1])
    
    t2 = []
    piscina = piscinaHilos(4)
    
    for i in range(0,256):
        
        for t in range(0,4):
            begin = (t*64)+(i%2)
            end = begin + 64
            if (end >= 256):
                end = 255
            #print(f"asignadas desde {begin} hasta {end}")
            piscina.add_task(intercambiar,lista_simbolos,lista_freq,begin,end)
        piscina.wait_completion()
                     
    for i in range(0,len(lista_simbolos)):
        if lista_freq[lista_simbolos[i]] is not 0:
            link.aniadeFinal(lista_simbolos[i],lista_freq[lista_simbolos[i]])
    
    while(link.listSize(link.prim) >1 ):
        auxiliar = dobleNodo(link.ult.simbolo ,link.ult.freq,link.ult.der , link.ult.izq)
        link.eliminaF()
        auxiliarExtra = dobleNodo(link.ult.simbolo ,link.ult.freq,link.ult.der , link.ult.izq)
        link.buscaAniade(link.prim,auxiliar , auxiliarExtra , -1 , auxiliar.freq+auxiliarExtra.freq)
        link.eliminaF()
    
    comp = buscar_recur(link.prim)
 
archivosave=asksaveasfile(mode='w', defaultextension=".txt")
archivosave.write(comp)
archivosave.close()

