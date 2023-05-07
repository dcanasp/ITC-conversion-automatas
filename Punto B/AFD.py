# from ayudasAFD import prueba,segunda #esto es lo mismo
#NO CREAR MAS FUNCIONES EN ESTE ARCHIVO, SI SE NECESITAN IR A ayudasAFD, U OTROS ARCHIVOS COMO LOS VAYAN NECESITANDO


class AFD:
    def __init__(self,alfabeto,estados,estadoInicial,estadosAceptados,delta):
        setattr(self,'alfabeto',alfabeto)
        setattr(self,'estados',estados)
        setattr(self,'estadoInicial',estadoInicial)
        setattr(self,'estadosAceptados',estadosAceptados)
        setattr(self,'transicion',delta)
        setattr(self,'estadosLimbo',[])
        setattr(self,'estadosInaccesibles',[])
        self.verificarCorregirCompletitudAFD()

    def crearArchivo(self,nombreArchivo):
        setattr(self,'nombreArchivo',nombreArchivo)
        self.verificarCorregirCompletitudAFD()
        self.exportar()
    
    def verificarCorregirCompletitudAFD(self):
        alfabeto = self.alfabeto
        estados = self.estados
        transicion = self.transicion
        
        # Verificar si el AFD es completo
        completo = True
        for estado in estados:
            for simbolo in alfabeto:
                if transicion[estado][simbolo] not in estados :
                    completo = False
                    break
            if not completo:
                break
                
        # Agregar estado limbo y ajustar transiciones si el AFD no es completo
        if not completo:
            estadoLimbo = 'q'+str(len(self.estados)+len(self.estadosLimbo))
            estados.append(estadoLimbo)
            transicion[estadoLimbo] = {}
            
            # Agregar transiciones del estado limbo para cada símbolo del alfabeto
            for simbolo in alfabeto:
                transicion[estadoLimbo][simbolo] = estadoLimbo
                
            # Ajustar transiciones de los estados que no tenían transiciones definidas para algún símbolo del alfabeto
            for estado in estados:
                for simbolo in alfabeto:
                    if transicion[estado][simbolo] not in estados:
                        transicion[estado][simbolo] = estadoLimbo
                        
            self.estados = estados
            self.transicion = transicion
            self.estadosLimbo = estadoLimbo
            
            print("El AFD no era completo, se agregó el estado limbo", estadoLimbo)
        else:
            print("El AFD es completo, no se agregó ningún estado limbo")
    
    def hallarEstadosLimbo(self):
        return
        

    def hallarEstadosInaccesibles(self):
        # Inicializar la lista de estados accesibles con el estado inicial
        estados_accesibles = []
        estados_accesibles.append(self.estadoInicial[0])
        pila = self.estadoInicial
        ##estados_accesibles[self.estados.index(self.estadoInicial[0])] = 1
        # Recorrer los estados y simular las transiciones a través del alfabeto
        while pila != []:
            estado = pila.pop()
            for simbolo in self.alfabeto:
                # Obtener el estado al que se transita desde el estado actual y con el símbolo actual
                try:
                    estado_siguiente = self.transicion[estado][simbolo]
                except KeyError:
                    estado_siguiente = None

                # Si el estado siguiente no está en la lista de estados accesibles,
                # agregarlo a la lista para futuras iteraciones
                if estado_siguiente not in estados_accesibles:
                    estados_accesibles.append(estado_siguiente)
                    pila.append(estado_siguiente)

                

        # Cualquier estado que no esté en la lista de estados accesibles es inaccesible
        for estado in self.estados:
            if estado not in estados_accesibles:
                self.estadosInaccesibles.append(estado)

        # Si hay estados inaccesibles, imprimir un mensaje y devolver True
        if self.estadosInaccesibles:
            print(self.estadosInaccesibles)
            return True

        # Si no hay estados inaccesibles, devolver False
        else:
            return False
    
    def pasarString(self):
        # Imprimir estados, alfabeto y estado inicial
        output = f"Estados: {self.estados}\nAlfabeto: {self.alfabeto}\nEstado inicial: {self.estadoInicial}\n"
        
        # Imprimir estados de aceptación
        output += f"Estados de aceptación: {self.estadosAceptados}\n"
        
        # Imprimir estados inaccesibles
        output += f"Estados inaccesibles: {self.estadosInaccesibles}\n"
        
        # Imprimir estados limbo
        output += f"Estados limbo: {self.estadosLimbo}\n"
        
        # Imprimir tabla de transiciones
        output += "Tabla de transiciones:\n"
        for estado in self.estados:
            output += f"{estado}:\n"
            for simbolo in self.alfabeto:
                destino = self.transicion[estado].get(simbolo, None)
                output += f"    {simbolo} -> {destino}\n"
        
        return output
    
    def imprimirAFDSimplificado(self):
        return
    
    def exportar(self):
        return
    
    def procesarCadena(self,cadena):
        # Recorrer la cadena y actualizar el estado actual en cada transición
        for simbolo in cadena:
            # Obtener el estado siguiente a partir del estado actual y el símbolo actual
            estado_siguiente = self.transicion[self.estadoInicial[0]][simbolo]

            # Si no hay transición para el símbolo actual, la cadena es rechazada
            if estado_siguiente is None:
                return False

            # Actualizar el estado actual
            estado_actual = estado_siguiente

        # Si el estado actual es un estado de aceptación, la cadena es aceptada; de lo contrario, es rechazada
        if estado_actual in self.estadosAceptados:
            return True
        else:
            return False
    
    def procesarCadenaConDetalles(self,cadena):
        # Inicializar el estado actual con el estado inicial
        estado_actual = self.estadoInicial[0]
        salida = ''
        i = 0

        # Recorrer la cadena y actualizar el estado actual en cada transición
        for simbolo in cadena:
            # Obtener el estado siguiente a partir del estado actual y el símbolo actual
            estado_siguiente = self.transicion[estado_actual][simbolo]

            # Actualizar el estado actual
            estado_actual = estado_siguiente

            # Imprimir el estado actual después de procesar el símbolo actual
            salida += f'[{estado_actual},{cadena[i:]}]->'
            i += 1

        if estado_actual in self.estadosAceptados:
            return print(salida+'Aceptacion')
        else:
            return print(salida+'No Aceptacion')
    
    def procesarListaCadenas(self, listaCadenas,nombreArchivo, imprimirPantalla):
        return
    
    def hallarComplemento(self,afdInput):
        return
    
    def hallarProductoCartesianoY(self, afd1, afd2):
        return 
    
    def hallarProductoCartesianoO(self, afd1, afd2):
        return
    
    def hallarProductoCartesianoDiferencia(self, afd1, afd2):
        return

    def hallarProductoCartesianoDiferenciaSimetrica(self, afd1, afd2):
        return    

    def hallarProductoCartesiano(self, afd1, afd2, operacion):
        #Llamarlos dependiendo la operación.
        self.hallarProductoCartesianoY()
        self.hallarProductoCartesianoO()
        self.hallarProductoCartesianoDiferencia()
        self.hallarProductoCartesianoDiferenciaSimetrica()
        return 
    
    def simplificarAFD(afdInput):
        return
    
    

    
delta = {
    'q0': {'a': 'q0', 'b': 'q1'},
    'q1': {'a': 'q1', 'b': 'q1'}
}
afd = AFD(['a', 'b'], ['q0', 'q1'], ['q0'], ['q0'], delta)
print(afd.pasarString())

