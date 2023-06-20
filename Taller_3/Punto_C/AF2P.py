class AF2P:
    def obtenerAlfabeto(self, alfabeto):
        letras=[]
        i=0
        while i < len(alfabeto):
            if alfabeto[i].find("-") != -1:
                rango=alfabeto.split("-")
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
    
    def __init__(self, Q=None, q0=None, F=None, Sigma=None, Gamma=None, Delta=None):
        if ".msm" in Q:
            with open(Q, 'r') as file:
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
            #Quitar la coma que esta presente al final de cada partes[i], si la hay
            i=0
            for parte in partes:
                if parte[len(parte)-1]==",":
                    partes[i]=parte[:len(parte)-1]
                i+=1
            #Obtener los estados
            Q=partes[0].split(',')
            #Obtener el estado inicial
            q0=partes[1]
            #Obtener los estados de aceptacion
            F=partes[2].split(',')
            #Obtener el alfabeto de entrada
            Sigma=partes[3]
            #Obtener el alfabeto de la pila
            Gamma=partes[4]
            #Obtener la funcion de transicion
            Delta=partes[5].split(',')

        self.estados = Q
        self.estadoInicial = q0
        self.estadosAceptacion = F
        self.alfabeto = self.obtenerAlfabeto(Sigma)
        self.alfabetoPila = self.obtenerAlfabeto(Gamma)
        self.Pila=[]
        self.Pila2=[]

        self.Delta = []
        for seccion in Delta:
            estadoInicio=self.leer_hasta_subcadena(":",seccion)
            letra=self.leer_hasta_subcadena(":",self.leer_desde_subcadena(":",seccion))
            letraTransicion=self.leer_hasta_subcadena(">",self.leer_desde_subcadena(":",self.leer_desde_subcadena(":",seccion)))
            transiciones=self.leer_desde_subcadena(">",self.leer_desde_subcadena(":",seccion))
            transiciones=transiciones.split(";")
            for transicion in transiciones:
                self.Delta.append(estadoInicio+":"+letra+":"+letraTransicion+">"+transicion)
        self.Delta=list(set(self.Delta))
        self.Delta.sort()

    def leer_desde_subcadena(self, subcadena, cadena):
        posicion = cadena.find(subcadena)
        if posicion != -1:
            contenido_leido = cadena[posicion+1:]
            return contenido_leido
        else:
            return "None"
        
    def leer_hasta_subcadena(self, subcadena, cadena):
        posicion = cadena.find(subcadena)
        if posicion != -1:
            contenido_leido = cadena[:posicion]
            return contenido_leido
        else:
            return "None"
    
    def __str__(self):
        representacion = "Estados: " + "\n"
        representacion += ", ".join(self.estados)
        representacion += "\n"
        representacion += "Estado Inicial: " + "\n" + self.estadoInicial + "\n"
        representacion += "Estados de aceptación: " + "\n"
        representacion += ", ".join(self.estadosAceptacion) + "\n"
        representacion += "Alfabeto de entrada: " + "\n"
        representacion += ", ".join(self.alfabeto) + "\n"
        representacion += "Alfabeto de la pila: " + "\n"
        representacion += ", ".join(self.alfabetoPila) + "\n"
        representacion += "Transiciones: " + "\n"
        representacion += "\n".join(self.Delta)
        representacion += "\n"
        return representacion

    def modificarPila(self,pila,operacion1,operacion2,parametro1,parametro2):
        pila=self.Pila
        pila2=self.Pila2
        if operacion1=="$":
            if pila[len(pila)-1]!="$":
                pila.append(parametro1)
            else:
                pila.pop(len(pila)-1)
                pila.append(parametro1)
        else:
            if parametro1=="$":
                pila.pop(len(pila)-1)
            else:
                pila[len(pila)-1]=parametro1
        if operacion2=="$":
            if pila2[len(pila2)-1]!="$":
                pila2.append(parametro2)
            else:
                pila2.pop(len(pila2)-1)
                pila2.append(parametro2)
        else:
            if parametro2=="$":
                pila2.pop(len(pila2)-1)
            else:
                pila2[len(pila2)-1]=parametro2
        self.Pila=pila
        self.Pila2=pila2
    
    def obtenerTransiciones(self,estado,letra,letraPila,letraPila2):
        letraPilaInicial=letraPila
        letraPila2Inicial=letraPila2
        transiciones=self.Delta
        transicionesFinal=[]
        for transicion in transiciones:
            if transicion.find(estado+":"+letra+":"+letraPila+":"+letraPila2)!=-1:
                transicionesFinal.append(transicion)
        if transicionesFinal==[]:
            letraPila=letraPilaInicial
            letraPila2="$"
            for transicion in transiciones:
                if transicion.find(estado+":"+letra+":"+letraPila+":"+letraPila2)!=-1:
                    transicionesFinal.append(transicion)
        if transicionesFinal==[]:
            letraPila="$"
            letraPila2=letraPila2Inicial
            for transicion in transiciones:
                if transicion.find(estado+":"+letra+":"+letraPila+":"+letraPila2)!=-1:
                    transicionesFinal.append(transicion)
        if transicionesFinal==[]:
            letraPila="$"
            letraPila2="$"
            for transicion in transiciones:
                if transicion.find(estado+":"+letra+":"+letraPila+":"+letraPila2)!=-1:
                    transicionesFinal.append(transicion)
        return transicionesFinal
    
    def leerLetra(self, cadena):
        if self.Pila == []:
            self.Pila.append("$")
        if self.Pila2 == []:
            self.Pila2.append("$")
        transiciones = self.obtenerTransiciones(self.estadoActual, cadena[0], self.Pila[len(self.Pila) - 1], self.Pila2[len(self.Pila2) - 1])
        if not transiciones:
            return False
        else:
            for transicion in transiciones:
                transicionInicial = self.leer_hasta_subcadena(">", transicion)
                transicionSiguiente = self.leer_desde_subcadena(">", transicion)
                if (self.estadoActual + ":" + cadena[0] + ":" + self.Pila[len(self.Pila) - 1] + ":" + self.Pila2[len(self.Pila2) - 1]) == transicionInicial:
                    operacion1 = self.leer_hasta_subcadena(":", self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", transicionInicial)))
                    operacion2 = self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", transicionInicial)))
                    parametro1 = self.leer_hasta_subcadena(":", self.leer_desde_subcadena(":", transicionSiguiente))
                    parametro2 = self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", transicionSiguiente))
                    self.modificarPila(self.Pila, operacion1, operacion2, parametro1, parametro2)
                    self.estadoActual = self.leer_hasta_subcadena(":", transicionSiguiente)
                    if len(self.Pila) != 0 and self.Pila[len(self.Pila) - 1] == "$":
                        self.Pila.pop(len(self.Pila) - 1)
                    if len(self.Pila2) != 0 and self.Pila2[len(self.Pila2) - 1] == "$":
                        self.Pila2.pop(len(self.Pila2) - 1)
                    cadena = self.leer_desde_subcadena(cadena[0], cadena)
                elif (self.estadoActual + ":" + cadena[0] + ":" + self.Pila[len(self.Pila) - 1] + ":" + "$") == transicionInicial:
                    operacion1 = self.leer_hasta_subcadena(":", self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", transicionInicial)))
                    operacion2 = "$"
                    parametro1 = self.leer_hasta_subcadena(":", self.leer_desde_subcadena(":", transicionSiguiente))
                    parametro2 = self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", transicionSiguiente))
                    self.modificarPila(self.Pila, operacion1, "$", parametro1, parametro2)
                    self.estadoActual = self.leer_hasta_subcadena(":", transicionSiguiente)
                    if len(self.Pila) != 0 and self.Pila[len(self.Pila) - 1] == "$":
                        self.Pila.pop(len(self.Pila) - 1)
                    if len(self.Pila2) != 0 and self.Pila2[len(self.Pila2) - 1] == "$":
                        self.Pila2.pop(len(self.Pila2) - 1)
                    cadena = self.leer_desde_subcadena(cadena[0], cadena)
                elif (self.estadoActual + ":" + cadena[0] + ":" + "$" + ":" + self.Pila2[len(self.Pila2) - 1]) == transicionInicial:
                    operacion1 = "$"
                    operacion2 = self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", transicionInicial)))
                    parametro1 = self.leer_hasta_subcadena(":", self.leer_desde_subcadena(":", transicionSiguiente))
                    parametro2 = self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", transicionSiguiente))
                    self.modificarPila(self.Pila, "$", operacion2, parametro1, parametro2)
                    self.estadoActual = self.leer_hasta_subcadena(":", transicionSiguiente)
                    if len(self.Pila) != 0 and self.Pila[len(self.Pila) - 1] == "$":
                        self.Pila.pop(len(self.Pila) - 1)
                    if len(self.Pila2) != 0 and self.Pila2[len(self.Pila2) - 1] == "$":
                        self.Pila2.pop(len(self.Pila2) - 1)
                    cadena = self.leer_desde_subcadena(cadena[0], cadena)
                elif (self.estadoActual + ":" + cadena[0] + ":" + "$" + ":" + "$") == transicionInicial:
                    operacion1 = "$"
                    operacion2 = "$"
                    parametro1 = self.leer_hasta_subcadena(":", self.leer_desde_subcadena(":", transicionSiguiente))
                    parametro2 = self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", transicionSiguiente))
                    self.modificarPila(self.Pila, "$", "$", parametro1, parametro2)
                    self.estadoActual = self.leer_hasta_subcadena(":", transicionSiguiente)
                    if len(self.Pila) != 0 and self.Pila[len(self.Pila) - 1] == "$":
                        self.Pila.pop(len(self.Pila) - 1)
                    if len(self.Pila2) != 0 and self.Pila2[len(self.Pila2) - 1] == "$":
                        self.Pila2.pop(len(self.Pila2) - 1)
                    cadena = self.leer_desde_subcadena(cadena[0], cadena)
        return cadena

    def procesarCadena(self, cadena):
        self.estadoActual = self.estadoInicial
        while len(cadena) > 0 or self.Pila or self.Pila2:
            print("Estado actual: ", self.estadoActual)
            print("Cadena: ", cadena)
            print("Pilas: " , self.Pila , "|" , self.Pila2)
            cadena = self.leerLetra(cadena)
            if cadena == False:
                print("Cadena no aceptada")
                return False
            elif cadena == "" and len(self.Pila) == 0 and len(self.Pila2) == 0:
                print("Estado actual: ", self.estadoActual)
                print("Cadena: ", cadena)
                print("Pilas: " , self.Pila , "|" , self.Pila2)
                print("Cadena aceptada")
                return True
        print("Cadena no aceptada")
        return False
    
    def leerLetraConDetalles(self, cadena):
        if self.Pila == []:
            self.Pila.append("$")
        if self.Pila2 == []:
            self.Pila2.append("$")
        transiciones = self.obtenerTransiciones(self.estadoActual, cadena[0], self.Pila[-1], self.Pila2[-1])
        if not transiciones:
            return False, ""
        else:
            for transicion in transiciones:
                transicionInicial = self.leer_hasta_subcadena(">", transicion)
                transicionSiguiente = self.leer_desde_subcadena(">", transicion)
                if (self.estadoActual + ":" + cadena[0] + ":" + self.Pila[-1] + ":" + self.Pila2[-1]) == transicionInicial:
                    operacion1 = self.leer_hasta_subcadena(":", self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", transicionInicial)))
                    operacion2 = self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", transicionInicial)))
                    parametro1 = self.leer_hasta_subcadena(":", self.leer_desde_subcadena(":", transicionSiguiente))
                    parametro2 = self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", transicionSiguiente))
                    self.modificarPila(self.Pila, operacion1, operacion2, parametro1, parametro2)
                    if len(self.Pila) != 0 and self.Pila[-1] == "$":
                        self.Pila.pop()
                    if len(self.Pila2) != 0 and self.Pila2[-1] == "$":
                        self.Pila2.pop()
                    estadoAnterior = self.estadoActual
                    self.estadoActual = self.leer_hasta_subcadena(":", transicionSiguiente)
                    if len(cadena) - 1 > 0:
                        procedimiento = "(" + estadoAnterior + "," + cadena + "," + operacion1 + "," + operacion2 + ") ->"
                    else:
                        procedimiento = "(" + estadoAnterior + "," + cadena + "," + operacion1 + "," + operacion2 + ")"
                    cadena = self.leer_desde_subcadena(cadena[0], cadena)
                    return cadena, procedimiento
                elif (self.estadoActual + ":" + cadena[0] + ":" + self.Pila[-1] + ":" + "$") == transicionInicial:
                    operacion1 = self.leer_hasta_subcadena(":", self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", transicionInicial)))
                    operacion2 = "$"
                    parametro1 = self.leer_hasta_subcadena(":", self.leer_desde_subcadena(":", transicionSiguiente))
                    parametro2 = self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", transicionSiguiente))
                    self.modificarPila(self.Pila, operacion1, "$", parametro1, parametro2)
                    if len(self.Pila) != 0 and self.Pila[-1] == "$":
                        self.Pila.pop()
                    if len(self.Pila2) != 0 and self.Pila2[-1] == "$":
                        self.Pila2.pop()
                    estadoAnterior = self.estadoActual
                    self.estadoActual = self.leer_hasta_subcadena(":", transicionSiguiente)
                    if len(cadena) - 1 > 0:
                        procedimiento = "(" + estadoAnterior + "," + cadena + "," + operacion1 + "," + operacion2 + ") ->"
                    else:
                        procedimiento = "(" + estadoAnterior + "," + cadena + "," + operacion1 + "," + operacion2 + ")"
                    cadena = self.leer_desde_subcadena(cadena[0], cadena)
                    return cadena, procedimiento
                elif (self.estadoActual + ":" + cadena[0] + ":" + "$" + ":" + self.Pila2[-1]) == transicionInicial:
                    operacion1 = "$"
                    operacion2 = self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", transicionInicial)))
                    parametro1 = self.leer_hasta_subcadena(":", self.leer_desde_subcadena(":", transicionSiguiente))
                    parametro2 = self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", transicionSiguiente))
                    self.modificarPila(self.Pila, "$", operacion2, parametro1, parametro2)
                    self.estadoActual = self.leer_hasta_subcadena(":", transicionSiguiente)
                    if len(self.Pila) != 0 and self.Pila[-1] == "$":
                        self.Pila.pop()
                    if len(self.Pila2) != 0 and self.Pila2[-1] == "$":
                        self.Pila2.pop()
                    estadoAnterior = self.estadoActual
                    self.estadoActual = self.leer_hasta_subcadena(":", transicionSiguiente)
                    if len(cadena) - 1 > 0:
                        procedimiento = "(" + estadoAnterior + "," + cadena + "," + operacion1 + "," + operacion2 + ") ->"
                    else:
                        procedimiento = "(" + estadoAnterior + "," + cadena + "," + operacion1 + "," + operacion2 + ")"
                    cadena = self.leer_desde_subcadena(cadena[0], cadena)
                    return cadena, procedimiento
                elif (self.estadoActual + ":" + cadena[0] + ":" + "$" + ":" + "$") == transicionInicial:
                    operacion1 = "$"
                    operacion2 = "$"
                    parametro1 = self.leer_hasta_subcadena(":", self.leer_desde_subcadena(":", transicionSiguiente))
                    parametro2 = self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", transicionSiguiente))
                    self.modificarPila(self.Pila, "$", "$", parametro1, parametro2)
                    self.estadoActual = self.leer_hasta_subcadena(":", transicionSiguiente)
                    if len(self.Pila) != 0 and self.Pila[-1] == "$":
                        self.Pila.pop()
                    if len(self.Pila2) != 0 and self.Pila2[-1] == "$":
                        self.Pila2.pop()
                    estadoAnterior = self.estadoActual
                    self.estadoActual = self.leer_hasta_subcadena(":", transicionSiguiente)
                    if len(cadena) - 1 > 0:
                        procedimiento = "(" + estadoAnterior + "," + cadena + "," + operacion1 + "," + operacion2 + ") ->"
                    else:
                        procedimiento = "(" + estadoAnterior + "," + cadena + "," + operacion1 + "," + operacion2 + ")"
                    cadena = self.leer_desde_subcadena(cadena[0], cadena)
                    return cadena, procedimiento
            return False, ""
    
    def procesarCadenaConDetalles(self, cadena):
        procedimientoFinal = "Procedimiento: \n"
        self.estadoActual = self.estadoInicial
        while len(cadena) > 0 or self.Pila or self.Pila2:
            cadena, procedimiento = self.leerLetraConDetalles(cadena)
            procedimientoFinal += procedimiento + "\n"
            if cadena == False:
                procedimientoFinal += "Cadena no aceptada"
                procedimientoFinal += "\n"
                return procedimientoFinal
            elif cadena == "" and len(self.Pila) == 0 and len(self.Pila2) == 0:
                procedimientoFinal += "Cadena aceptada"
                procedimientoFinal += "\n"
                return procedimientoFinal
        procedimientoFinal += "Cadena no aceptada"
        procedimientoFinal += "\n"
    
    def procesarListaCadenas(self, listaCadenas, nombreArchivo=None, imprimirPantalla=False):
        if nombreArchivo is None:
            nombreArchivo = "resultados.txt"
        try:
            with open(nombreArchivo, "w") as archivo:
                for cadena in listaCadenas:
                    resultado = self.procesarCadenaConDetalles(cadena)    
                    if imprimirPantalla:
                        print("Cadena:", cadena)
                        print(resultado)
                        print()
                    archivo.write("Cadena: " + cadena + "\n")
                    archivo.write(resultado + "\n")      
            print("Procesamiento de cadenas completado. Resultados guardados en:", nombreArchivo)
        except IOError:
            print("Error al abrir el archivo:", nombreArchivo)
    
Pila=AF2P("AF2P.msm")

#Pila=AF2P(["q0","q1","q2","q3"],"q0","q3","a-c","A-B",["q0:a:$:$>q0:A:$","q0:b:A:$>q1:A:B","q1:b:A:$>q1:A:B","q1:a:A:B>q2:$:B","q2:a:A:B>q2:$:B","q2:c:$:B>q3:$:$","q3:c:$:B>q3:$:$"])

#print(Pila)

#Pila.estadoActual=Pila.estadoInicial
#print(Pila.leerLetra("acc"))

#Pila.estadoActual=Pila.estadoInicial
#Pila.procesarCadena("aabbcc")

#Pila.estadoActual=Pila.estadoInicial
#print(Pila.leerLetraConDetalles("c"))

#Pila.estadoActual=Pila.estadoInicial
#print(Pila.procesarCadenaConDetalles("aababbaaacc"))

#Pila.Pila=["$"]
#Pila.Pila2=["$"]
#Pila.modificarPila(Pila.Pila,"$","$","A","A")

#Pila.obtenerTransiciones("q0","a","$","$")

#Pila.procesarListaCadenas(["aaabbaaacc","aaabbaaaccc"], "resultados.txt", True)