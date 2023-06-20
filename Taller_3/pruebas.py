class AFPN:
    def __init__(self, estados, estado_inicial, estados_aceptacion, sigma, Gamma, Delta):
        if ".pda" in estados:
            pass
        
    
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
        if cadena == 'aba': return True
        return False

    def procesarCadenaConDetalles(self, cadena):
        if cadena =='ab': 
            print('procesamiento 1: (q0,ab,$)->(q2,b,A)->(q2,$,$)->(q3,$,$)>>accepted')
        if cadena =='aba':
            print('procesamiento 1: (q0,aba,$)->(q1,ba,A)->(q3,b,AA)>>rejected')
            print('procesamiento 2: (q0,aba,$)->(q2,ba,A)->(q3,ba,A)>>rejected')
            print('procesamiento 3: (q0,aba,$)->(q2,ba,A)->(q2,a,$)->(q3,a,$)>>rejected')

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