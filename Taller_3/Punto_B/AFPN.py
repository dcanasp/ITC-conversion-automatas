from collections import deque
 
class AFPN:
    def __init__(self, estados=None, estado_inicial=None, estados_aceptacion=None, Sigma=None, Gamma=None, Delta=None):
        if ".pda" in estados:
            with open(estados, 'r') as file:
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
                estados_aceptacion = 0
                while estados_aceptacion < len(partes[i]):
                    #cambiar cada salto de linea por una coma
                    if partes[i][estados_aceptacion]=="\n":
                        partes[i]=partes[i].replace("\n",",")
                    estados_aceptacion+=1
                i+=1 
            #Remover el inicio de cada partes[i] hasta la primera coma
            i=0
            while i < len(partes):
                estados_aceptacion = 0
                while estados_aceptacion < len(partes[i]):
                    if partes[i][estados_aceptacion]==",":
                        partes[i]=partes[i][estados_aceptacion+1:]
                        break
                    estados_aceptacion+=1
                i+=1
            #Quitar la coma que esta presente al final de cada partes[i], si la hay
            i=0
            for parte in partes:
                if parte[len(parte)-1]==",":
                    partes[i]=parte[:len(parte)-1]
                i+=1
            #Obtener los estados
            estados=partes[0].split(',')
            #Obtener el estado inicial
            estado_inicial=partes[1]
            #Obtener los estados de aceptacion
            estados_aceptacion=partes[2].split(',')
            #Obtener el alfabeto de entrada
            Sigma=self.obtenerAlfabeto(partes[3])
            #Obtener el alfabeto de la pila
            Gamma=self.obtenerAlfabeto(partes[4])
            #Obtener la funcion de transicion
            Delta=partes[5].split(',')

        self.estados = estados
        self.estadoInicial = estado_inicial
        self.estadosAceptacion = estados_aceptacion
        self.cinta = Sigma
        self.alfabetoPila = Gamma
        self.Pila=[]
        self.Delta = Delta
    
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
        for estado in self.estadosAceptacion:
            representacion += estado + ", "
        representacion = representacion[:len(representacion)-2] + "\n"
        representacion += "Alfabeto de entrada: "
        representacion += "\n"
        for simbolo in self.cinta:
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
            representacion += str(transicion) + "\n"
        return representacion

    
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
        # self.estadoActual = self.estadoInicial
        estadoActual = self.estadoInicial
        estadoActualArray = [estadoActual]
        pila = []
        for letra in cadena:
            print(letra)
            bandera = False
            for key, value in self.Delta.items():
                if key[0] == estadoActual and key[1] == letra and (top(pila)==key[2] or ( key[1]=='$' and len(pila)==0)):
                    pila.append(key[3])
                    estadoActualArray = value
                    bandera = True
                break
            if bandera:
                continue
            for key, value in self.Delta.items():
                if key[0] == estadoActual and key[1] == '$' and (top(pila)==key[2] or ( key[1]=='$' and len(pila)==0)):
                    estadoActualArray = value
                    bandera = True
                break
            if bandera:
                continue
            return False
        return True


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
            aceptado = self.procesarCadena(cadena   )
            if aceptado == False:
                procedimientoFinal += "Cadena no aceptada"
                procedimientoFinal += "\n"
                return procedimientoFinal
            elif aceptado == "" and len(self.Pila) == 0:
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
        # Combinar los estados del AFPN con los estados del AFD
        for estadoAFPN in self.estados:
            for estadoAFD in afd.estados:
                nuevoEstado = estadoAFPN + estadoAFD
                nuevoQ.append(nuevoEstado)
                if estadoAFPN in self.estadosAceptacion and estadoAFD in afd.estadosAceptacion:
                    nuevoF.append(nuevoEstado)
        
        for estadoAFPN in self.estados:
            for estadoAFD in afd.estados:
                for simbolo in self.cinta:
                    for simboloAFD in afd.cinta:
                        transicionesAFPN = self.obtenerTransiciones(estadoAFPN, simbolo, simbolo)
                        transicionesAFD = afd.obtenerTransiciones(estadoAFD, simboloAFD)
                        for transicionAFPN in transicionesAFPN:
                            for transicionAFD in transicionesAFD:
                                nuevoEstadoAFPN = self.leer_hasta_subcadena(">", transicionAFPN)
                                nuevoEstadoAFD = afd.leer_hasta_subcadena(">", transicionAFD)
                                nuevoEstado = nuevoEstadoAFPN + nuevoEstadoAFD
                                nuevoSimbolo = self.leer_desde_subcadena(">", transicionAFPN)
                                nuevoSimboloAFD = afd.leer_desde_subcadena(">", transicionAFD)
                                nuevoSimboloTransicion = nuevoSimbolo + nuevoSimboloAFD
                                if (nuevoEstado, nuevoSimboloTransicion) not in nuevoDelta:
                                    nuevoDelta.append((nuevoEstado, nuevoSimboloTransicion))

        nuevoAFPN = AFPN()
        nuevoAFPN.estados = nuevoQ
        nuevoAFPN.estadoInicial = self.estadoInicial + afd.estadoInicial
        nuevoAFPN.estadosAceptacion = nuevoF
        nuevoAFPN.cinta = self.cinta + afd.cinta
        nuevoAFPN.alfabetoPila = self.alfabetoPila
        nuevoAFPN.Delta = nuevoDelta
        
        return nuevoAFPN
    
def top(pila):
    if pila:
        return pila[-1]    # this will get the last element of stack
    else:
        return None
# Pila=AFPN("AFPN.pda")
#print(Pila)
#print(Pila.modificarPila(["a","b","c"],"pop","a"))
#print(Pila.obtenerTransiciones("q0","a","A"))
#print(Pila.leerLetra("bb"))
#print(Pila.procesarCadenaConDetalles("abab"))
# Definir la lista de cadenas a procesar
#listaCadenas = ["abab", "aabb", "abba"]
# Llamar al método procesarListaCadenas
#Pila.procesarListaCadenas(listaCadenas, "resultados.txt", True)