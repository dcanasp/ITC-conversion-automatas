class AFPD:
    def obtenerAlfabeto(self, alfabeto):
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
    
    def __init__(self, Q=None, q0=None, F=None, Sigma=None, Gamma=None, Delta=None):
        if ".pda" in Q:
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
        representacion = "Estados: "
        representacion += "\n"
        for estado in self.estados:
            representacion += estado + ", "
        representacion = representacion[:len(representacion)-2] + "\n"
        representacion += "Estado Inicial: " + "\n"
        representacion += self.estadoInicial + "\n"
        representacion += "Estados de aceptación: "
        representacion += "\n"
        if self.estadosAceptacion is type(list):
            for estado in self.estadosAceptacion:
                representacion += estado + ", "
        else:
            representacion += str(self.estadosAceptacion) + "\n" + "\n"
        representacion = representacion[:len(representacion)-2] + "\n"
        representacion += "Alfabeto de entrada: "
        representacion += "\n"
        for simbolo in self.alfabeto:
            representacion += simbolo + ", "
        representacion = representacion[:len(representacion)-2] + "\n"
        representacion += "Alfabeto de la pila: "
        representacion += "\n"
        for simbolo in self.alfabetoPila:
            representacion += simbolo + ", "
        representacion = representacion[:len(representacion)-2] + "\n"
        representacion += "Transiciones: "
        representacion += "\n"
        for transicion in self.Delta:
            representacion += transicion + "\n"
        return representacion

    def modificarPila(self,pila,operacion,parametro):
        pila=self.Pila
        if operacion==pila[len(pila)-1]:
            if parametro=="$":
                pila.pop(len(pila)-1)
            else:
                if pila[len(pila)-1]=="$":
                    pila.pop(len(pila)-1)
                pila.append(parametro)
        else:
            return False
        return pila
    
    def obtenerTransiciones(self,estado,letra,letraPila):
        transiciones=self.Delta
        transicionesFinal=[]
        for transicion in transiciones:
            self.leer_hasta_subcadena(">",transicion)
            if transicion.find(estado+":"+letra+":"+letraPila)!=-1:
                transicionesFinal.append(transicion)
        return transicionesFinal
    
    def leerLetra(self, cadena):
        if self.Pila == []:
            self.Pila.append("$")
        transiciones = self.obtenerTransiciones(self.estadoActual, cadena[0], self.Pila[len(self.Pila) - 1])
        if not transiciones:
            return False
        else:
            for transicion in transiciones:
                transicionInicial = self.leer_hasta_subcadena(">", transicion)
                transicionSiguiente = self.leer_desde_subcadena(">", transicion)
                if (self.estadoActual + ":" + cadena[0] + ":" + self.Pila[len(self.Pila) - 1]) == transicionInicial:
                    operacion = self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", transicionInicial))
                    parametro = self.leer_desde_subcadena(":", transicionSiguiente)
                    self.Pila = self.modificarPila(self.Pila, operacion, parametro)
                    self.estadoActual = self.leer_hasta_subcadena(":", transicionSiguiente)
                    if len(self.Pila) != 0 and self.Pila[len(self.Pila) - 1] == "$":
                        self.Pila.pop(len(self.Pila) - 1)
                    cadena = self.leer_desde_subcadena(cadena[0], cadena)
        return cadena

    def procesarCadena(self, cadena):
        self.estadoActual = self.estadoInicial
        while len(cadena) > 0 or self.Pila:
            cadena = self.leerLetra(cadena)
            if cadena == False:
                print("Cadena no aceptada")
                return False
            elif cadena == "" and len(self.Pila) == 0:
                print("Cadena aceptada")
                return True
        print("Cadena no aceptada")
        return False

    def leerLetraConDetalles(self, cadena):
        if self.Pila == []:
            self.Pila.append("$")
        
        transiciones = self.obtenerTransiciones(self.estadoActual, cadena[0], self.Pila[len(self.Pila) - 1])
        if not transiciones:
            return False, ""  # Devolver un par de valores: cadena y procedimiento vacío
        
        for transicion in transiciones:
            transicionInicial = self.leer_hasta_subcadena(">", transicion)
            transicionSiguiente = self.leer_desde_subcadena(">", transicion)
            
            if (self.estadoActual + ":" + cadena[0] + ":" + self.Pila[len(self.Pila) - 1]) == transicionInicial:
                operacion = self.leer_desde_subcadena(":", self.leer_desde_subcadena(":", transicionInicial))
                parametro = self.leer_desde_subcadena(":", transicionSiguiente)
                
                self.Pila = self.modificarPila(self.Pila, operacion, parametro)
                estadoAnterior = self.estadoActual
                self.estadoActual = self.leer_hasta_subcadena(":", transicionSiguiente)
                
                if len(cadena) - 1 > 0:
                    procedimiento = "(" + estadoAnterior + "," + cadena + "," + operacion + ") ->"
                else:
                    procedimiento = "(" + estadoAnterior + "," + cadena + "," + operacion + ")"
                
                if len(self.Pila) != 0 and self.Pila[len(self.Pila) - 1] == "$":
                    self.Pila.pop(len(self.Pila) - 1)
                
                cadena = self.leer_desde_subcadena(cadena[0], cadena)
                return cadena, procedimiento
        
        return False, ""
    
    def procesarCadenaConDetalles(self, cadena):
        procedimientoFinal = "Procedimiento: \n"
        self.estadoActual = self.estadoInicial
        while len(cadena) > 0 or self.Pila:
            cadena, procedimiento = self.leerLetraConDetalles(cadena)
            procedimientoFinal += procedimiento + "\n"
            if cadena == False:
                procedimientoFinal += "Cadena no aceptada"
                procedimientoFinal += "\n"
                return procedimientoFinal
            elif cadena == "" and len(self.Pila) == 0:
                procedimientoFinal += "Cadena aceptada"
                procedimientoFinal += "\n"
                return procedimientoFinal
        procedimientoFinal += "Cadena no aceptada"
        procedimientoFinal += "\n"
        return procedimientoFinal
    
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

    def hallarProductoCartesianoConAFD(self, afd):
        nuevoQ = []
        nuevoF = []
        nuevoDelta = []
        # Combinar los estados del AFPD con los estados del AFD
        for estadoAFPD in self.estados:
            for estadoAFD in afd.estados:
                nuevoEstado = estadoAFPD + estadoAFD
                nuevoQ.append(nuevoEstado)
                if estadoAFPD in self.estadosAceptacion and estadoAFD in afd.estadosAceptacion:
                    nuevoF.append(nuevoEstado)
        
        for estadoAFPD in self.estados:
            for estadoAFD in afd.estados:
                for simbolo in self.alfabeto:
                    for simboloAFD in afd.alfabeto:
                        transicionesAFPD = self.obtenerTransiciones(estadoAFPD, simbolo, simbolo)
                        transicionesAFD = afd.obtenerTransiciones(estadoAFD, simboloAFD)
                        for transicionAFPD in transicionesAFPD:
                            for transicionAFD in transicionesAFD:
                                nuevoEstadoAFPD = self.leer_hasta_subcadena(">", transicionAFPD)
                                nuevoEstadoAFD = afd.leer_hasta_subcadena(">", transicionAFD)
                                nuevoEstado = nuevoEstadoAFPD + nuevoEstadoAFD
                                nuevoSimbolo = self.leer_desde_subcadena(">", transicionAFPD)
                                nuevoSimboloAFD = afd.leer_desde_subcadena(">", transicionAFD)
                                nuevoSimboloTransicion = nuevoSimbolo + nuevoSimboloAFD
                                if (nuevoEstado, nuevoSimboloTransicion) not in nuevoDelta:
                                    nuevoDelta.append((nuevoEstado, nuevoSimboloTransicion))

        nuevoAFPD = AFPD()
        nuevoAFPD.estados = nuevoQ
        nuevoAFPD.estadoInicial = self.estadoInicial + afd.estadoInicial
        nuevoAFPD.estadosAceptacion = nuevoF
        nuevoAFPD.alfabeto = self.alfabeto + afd.alfabeto
        nuevoAFPD.alfabetoPila = self.alfabetoPila
        nuevoAFPD.Delta = nuevoDelta
        
        return nuevoAFPD