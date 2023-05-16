#!nfe
#1) Constructor(alfabeto, estados, estadoInicial, estadosAceptacion,Delta) de la clase para inicializar los atributos.
class AFNLambda:
    #Función para obtener el alfabeto de un input
    def obtenerAlfabeto(alfabeto):
        letras=[]
        i=0
        alfabeto=alfabeto.split(',')
        while i < len(alfabeto):
            if alfabeto[i].find("-")==True:
                rango=alfabeto[i].split("-")
                for letra in range(ord(rango[0]),ord(rango[1])+1):
                    letras.append(chr(letra))
                i+=1
            elif len(alfabeto[i])==1:
                letras.append(alfabeto[i])
                i+=1
            elif alfabeto[i]=="" or alfabeto[i]==" ":
                i+=1
                continue
            else:
                print("Error en el alfabeto, revisa la entrada")
                letras=False
                break
            letras=list(dict.fromkeys(letras))
        return letras

    def __init__(self, alfabeto=None, estados=None, estadoInicial=None, estadosAceptacion=None, Delta=None):
        if ".txt" in alfabeto:
            with open(alfabeto, 'r') as file:
                contenido = file.read()
                partes = contenido.split('#')
            i=0
            while i < len(partes):
                if partes[i]=="" or partes[i]==" ": #Si la parte esta vacia, la elimina
                    partes.pop(i)
                    continue
                i+=1
            i=0
            partes.pop(0)
            while i < len(partes):
                f = 0
                while f < len(partes[i]):
                    #cambiar cada salto de linea por una coma
                    if partes[i][f]=="\n":
                        partes[i]=partes[i].replace("\n",",")
                    f+=1
                i+=1
            #Remover el inicio de cada partes[i] hasta la primera coma
            i=0
            while i < len(partes):
                f = 0
                while f < len(partes[i]):
                    if partes[i][f]==",":
                        partes[i]=partes[i][f+1:]
                        break
                    f+=1
                i+=1
            #Remover el final de cada partes[i] desde la ultima coma
            i=0
            while i < len(partes):
                f = len(partes[i])-1
                while f > 0:
                    if partes[i][f]==",":
                        partes[i]=partes[i][:f]
                        break
                    f-=1
                i+=1
            #Obtener el alfabeto
            alfabeto=AFNLambda.obtenerAlfabeto(partes[0])
            #Obtener los estados
            estados=partes[1].split(',')
            #Obtener el estado inicial
            estadoInicial=partes[2]
            #Obtener los estados de aceptacion
            estadosAceptacion=partes[3].split(',')
            #Obtener la funcion de transicion
            Delta=partes[4].split(',')
        
        self.alfabeto = alfabeto
        self.estados = estados
        self.estadoInicial = estadoInicial
        self.estadosAceptacion = estadosAceptacion
        self.Delta = Delta
        self.estadosInaccesibles = []

    def __str__(self):
        representation = "AFNLambda\n"
        representation += "Estados: " + str(self.estados) + "\n"
        representation += "Estado inicial: " + str(self.estadoInicial) + "\n"
        representation += "Estados de aceptación: " + str(self.estadosAceptacion) + "\n"
        representation += "Estados inaccesibles: " + str(self.estadosInaccesibles) + "\n"
        representation += "Delta (Transiciones):\n"
        for transicion in self.Delta:
            representation += "\t" + transicion + "\n"
        return representation

    def calcularLambdaClausura(estado):
        estados=[]
        if estado.find(","):
            estados=estado.split(",")
        else:
            estados.append(estado)
        listaEstados = []
        x=0
        while x < len(estados):
            if estados[x] in Automata.estados:
                i=0
                while i < len(Automata.Delta):
                    if Automata.Delta[i].find(estados[x])==0:
                        if Automata.Delta[i].find("$")!=-1:
                            listaEstados.append(Automata.Delta[i][len(estados[x])+3:])
                    i+=1
            x+=1
        #Separar los estados de la lista
        i=0
        listaEstadosFinal=[]
        while i < len(listaEstados):
            listaEstadosFinal=listaEstadosFinal+listaEstados[i].split(";")
            print(listaEstadosFinal)
            i+=1
        return listaEstadosFinal

    def leer_desde_subcadena(subcadena, cadena):
        posicion = cadena.find(subcadena)
        if posicion != -1:
            contenido_leido = cadena[posicion+1:]
            return contenido_leido
        else:
            return "None"
        
    def leer_hasta_subcadena(subcadena, cadena):
        posicion = cadena.find(subcadena)
        if posicion != -1:
            contenido_leido = cadena[:posicion]
            return contenido_leido
        else:
            return "None"
        
    def hallarEstadosInaccesibles():
        estados=Automata.estados
        delta=Automata.Delta
        for estado in estados:
            i=0
            encontrado=False
            while i < len(delta):
                subcadena=AFNLambda.leer_desde_subcadena(">",delta[i])
                if subcadena.find(estado)!=-1:
                    encontrado=True
                    break
                i+=1
            if encontrado==False:
                Automata.estadosInaccesibles.append(estado)
        return Automata.estadosInaccesibles
    
    def exportar(nombre_archivo, contenido):
        nombre_archivo_con_extension = nombre_archivo + ".nfe"
        with open(nombre_archivo_con_extension, 'w') as archivo:
            archivo.write(contenido)

    def procesarCadena(cadena):
        estados = Automata.estados
        estadoInicial = Automata.estadoInicial
        estadosAceptacion = Automata.estadosAceptacion
        delta = Automata.Delta
        estadoActual=[]
        estadoActual.append(estadoInicial)
        estadosDelta=[]
        indice=0
        while indice < len(cadena):
            i=0
            print("indice",indice)
            print("i",i)
            f=0
            while f<len(delta):
                if delta[i].find(estadoActual[0]+":")!=-1:
                    if delta[i].find(";")!=-1:
                        print("delta[i]",delta[i])
                        temporal=delta[i].split(";")
                        for f in range(len(temporal)):
                            if f==0:
                                estadosDelta.append(temporal[f][len(estadoActual[0])+1:])
                            else:
                                estadosDelta.append(temporal[f]+temporal[f])
                        print("estadosDelta",estadosDelta)
                    else:
                        print("delta[i] 2",delta[i])
                        estadosDelta.append(delta[i])
                        print("estadosDelta 2",estadosDelta)
                i+=1
            while len(estadosDelta)!=0:
                print("estadosDelta",estadosDelta)
                subcadena=AFNLambda.leer_desde_subcadena(":",estadosDelta[0])
                estadosDelta.pop(0)
                print("subcadena",subcadena)
                if AFNLambda.leer_hasta_subcadena(":",subcadena)!=-1:
                    print(Automata.Delta[i])
                indice+=1
                i+=1
            print("Aqui")
            if i==len(Automata.Delta):
                indice+=1
                continue
        estadosDelta=[]

Automata = AFNLambda("PruebaITC.txt")
AFNLambda.hallarEstadosInaccesibles()
#print("Estados inaccesibles",Automata.estadosInaccesibles)
AFNLambda.procesarCadena("abgc")
print(Automata)