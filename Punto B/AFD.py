from ayudasAFD import graficos
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

    def constructor(self,nombreArchivo):
        setattr(self,'nombreArchivo'+".afd",nombreArchivo)
        self.verificarCorregirCompletitudAFD()
    
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
                
        # Agregar estado limbo y ajustar transiciones si el AFD no es completo
        if not completo:
            estadoLimbo = 'q'+str(len(self.estados)+len(self.estadosLimbo))
            if estadoLimbo in estados:
                while estadoLimbo in estados:
                    estadoLimbo = 'q'+str(len(self.estados)+len(self.estadosLimbo)+1)
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
        estados = list(set(self.estados)-set(self.estadosAceptados))
        estadosLimbo = []
        
        # Verificamos cada estado del AFD
        for estado in estados:
            cont = 0
            for simbolo in self.alfabeto:
                if self.transicion[estado][simbolo] == estado:
                    cont += 1
            if cont == len(self.alfabeto):
                estadosLimbo.append(estado)

        self.estadosLimbo = estadosLimbo

        
    def hallarEstadosInaccesibles(self):
        # Inicializar la lista de estados accesibles con el estado inicial
        estados_accesibles = []
        estados_accesibles.append(self.estadoInicial[0])
        pila = []
        pila.append(self.estadoInicial[0])
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
        output = "#!nfe\n#alphabet\n"

        output += f"{self.alfabeto[0]}-{self.alfabeto[-1]}\n#states\n"
        
        # Imprimir estados de aceptación
        for estado in self.estados:
            output += f"{estado}\n"

        output += f"#initial\n{self.estadoInicial[0]}\n"

        output += "#accepting\n"
        for estado in self.estadosAceptados:
            output += f"{estado}\n"

        output += "#transitions\n"

        # Imprimir tabla de transiciones
        for estado in self.estados:
            for simbolo in self.alfabeto:
                destino = self.transicion[estado].get(simbolo, None)
                output += f"{estado}:{simbolo}>{destino}\n"
        
        return output
    
    def imprimirAFDSimplificado(self):
        return
    
    def exportar(self, nombreArchivo):
        archivo = open(nombreArchivo+".afd","w")
        archivo.write(self.pasarString())
        return archivo.close()
    
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
    
    def simplificarAFD(self, afdInput):
        return
    
    def eliminarEstadosInaccesibles(self):
        for estado in self.estadosInaccesibles:
            self.estados.remove(estado)
            for simbolo in self.alfabeto:
                self.transicion[estado].pop(simbolo)
        return
    def graficar(self):
        graficos(self.alfabeto,self.estados,self.transicion,self.estadoInicial,self.estadosAceptados,self.estadosLimbo)
    
def hallarComplemento(afdInput):
    for estado in afdInput.estados:
        if estado not in afdInput.estadosAceptados:
            afdInput.estadosAceptados.append(estado)
        else:
            afdInput.estadosAceptados.remove(estado)
    return afdInput
    
def hallarProductoCartesianoY(afd1, afd2):
    alfabeto = afd1.alfabeto
        
    estados = []
    for estado1 in afd1.estados:
        for estado2 in afd2.estados:
            estado = estado1 + estado2
            estados.append(estado)
        
    estadoInicial = []
    estadoIni = afd1.estadoInicial[0] + afd2.estadoInicial[0]
    estadoInicial.append(estadoIni)
        
    estadosAceptados = []
    for estado1 in afd1.estadosAceptados:
        for estado2 in afd2.estadosAceptados:
            estado = estado1 + estado2
            estadosAceptados.append(estado)
        
    transicion = {}
    for estado in estados:
        transicion[estado] = {}
        for simbolo in alfabeto:
            estado1 = estado[:len(afd1.estados[0])]
            estado2 = estado[len(afd1.estados[0]):]
            estado1_siguiente = afd1.transicion[estado1][simbolo]
            estado2_siguiente = afd2.transicion[estado2][simbolo]
            estado_siguiente = estado1_siguiente + estado2_siguiente
            transicion[estado][simbolo] = estado_siguiente
        
    afdResultado = AFD(alfabeto, estados, estadoInicial, estadosAceptados, transicion)
    return afdResultado
    
def hallarProductoCartesianoO(afd1, afd2):
    alfabeto = afd1.alfabeto
      
    estados = []
    for estado1 in afd1.estados:
        for estado2 in afd2.estados:
            estado = estado1 + estado2
            estados.append(estado)
        
    estadoInicial = []
    estadoIni = afd1.estadoInicial[0] + afd2.estadoInicial[0]
    estadoInicial.append(estadoIni)
        
    estadosAceptados = []
    for estado1 in afd1.estados:
        for estado2 in afd2.estados:
            if (estado1 in afd1.estadosAceptados and estado2 not in afd2.estadosAceptados) or (estado1 not in afd1.estadosAceptados and estado2 in afd2.estadosAceptados) or (estado1 in afd1.estadosAceptados and estado2 in afd2.estadosAceptados):
                estado = estado1 + estado2
                estadosAceptados.append(estado)
        
    transicion = {}
    for estado in estados:
        transicion[estado] = {}
        for simbolo in alfabeto:
            estado1 = estado[:len(afd1.estados[0])]
            estado2 = estado[len(afd1.estados[0]):]
            estado1_siguiente = afd1.transicion[estado1][simbolo]
            estado2_siguiente = afd2.transicion[estado2][simbolo]
            estado_siguiente = estado1_siguiente + estado2_siguiente
            transicion[estado][simbolo] = estado_siguiente
        
    afdResultado = AFD(alfabeto, estados, estadoInicial, estadosAceptados, transicion)
    return afdResultado
    
def hallarProductoCartesianoDiferencia(afd1, afd2):
    alfabeto = afd1.alfabeto
      
    estados = []
    for estado1 in afd1.estados:
        for estado2 in afd2.estados:
            estado = estado1 + estado2
            estados.append(estado)
        
    estadoInicial = []
    estadoIni = afd1.estadoInicial[0] + afd2.estadoInicial[0]
    estadoInicial.append(estadoIni)
        
    estadosAceptados = []
    for estado1 in afd1.estados:
        for estado2 in afd2.estados:
            if estado1 in afd1.estadosAceptados and estado2 not in afd2.estadosAceptados:
                estado = estado1 + estado2
                estadosAceptados.append(estado)
        
    transicion = {}
    for estado in estados:
        transicion[estado] = {}
        for simbolo in alfabeto:
            estado1 = estado[:len(afd1.estados[0])]
            estado2 = estado[len(afd1.estados[0]):]
            estado1_siguiente = afd1.transicion[estado1][simbolo]
            estado2_siguiente = afd2.transicion[estado2][simbolo]
            estado_siguiente = estado1_siguiente + estado2_siguiente
            transicion[estado][simbolo] = estado_siguiente
        
    afdResultado = AFD(alfabeto, estados, estadoInicial, estadosAceptados, transicion)
    return afdResultado

def hallarProductoCartesianoDiferenciaSimetrica(afd1, afd2):
    alfabeto = afd1.alfabeto
      
    estados = []
    for estado1 in afd1.estados:
        for estado2 in afd2.estados:
            estado = estado1 + estado2
            estados.append(estado)
        
    estadoInicial = []
    estadoIni = afd1.estadoInicial[0] + afd2.estadoInicial[0]
    estadoInicial.append(estadoIni)
        
    estadosAceptados = []
    for estado1 in afd1.estados:
        for estado2 in afd2.estados:
            if (estado1 in afd1.estadosAceptados and estado2 not in afd2.estadosAceptados) or (estado1 not in afd1.estadosAceptados and estado2 in afd2.estadosAceptados):
                estado = estado1 + estado2
                estadosAceptados.append(estado)

    
        
    transicion = {}
    for estado in estados:
        transicion[estado] = {}
        for simbolo in alfabeto:
            estado1 = estado[:len(afd1.estados[0])]
            estado2 = estado[len(afd1.estados[0]):]
            estado1_siguiente = afd1.transicion[estado1][simbolo]
            estado2_siguiente = afd2.transicion[estado2][simbolo]
            estado_siguiente = estado1_siguiente + estado2_siguiente
            transicion[estado][simbolo] = estado_siguiente
        
    afdResultado = AFD(alfabeto, estados, estadoInicial, estadosAceptados, transicion)
    return afdResultado  

def hallarProductoCartesiano(afd1, afd2, operacion):
    #Llamarlos dependiendo la operación.
    if operacion == 'insterseccion':
        return hallarProductoCartesianoY(afd1, afd2)
    elif operacion == 'union':
        return hallarProductoCartesianoO(afd1, afd2)
    elif operacion == 'diferencia':
        return hallarProductoCartesianoDiferencia(afd1, afd2)
    elif operacion == 'diferencia simetrica':
        return hallarProductoCartesianoDiferenciaSimetrica(afd1, afd2)
    else: 
        print('Operación no válida')

    
    
    

    
delta = {
    'q0': {'a': 'q1', 'b': 'q2'},
    'q1': {'a': '', 'b': 'q2'},
    'q2': {'a': 'q2', 'b': 'q3'},
    'q3': {'a':'','b':''}
}


delta2 ={
    'q0': {'a': 'q1', 'b': 'q2'},
    'q1': {'a': 'q1', 'b': 'q2'},
    'q2': {'a':'a','b':''}
}
afd2 = AFD(['a','b'],['q0','q1','q2'],['q0'],['q0','q1'],delta2)

delta3 = {
    'q0':{'a': 'q3','a': 'q1', 'b': 'q1'},
    'q1':{'a': 'q1', 'b': 'q3'},
    'q2':{'a': 'q2', 'b': 'q0'},
    'q3':{'a': 'q2', 'b': ''},
}

afd3 = AFD(['a','b'],['q0','q1','q2','q3'],['q0'],['q2','q3'],delta3)




# (self,alfabeto,estados,estadoInicial,estadosAceptados,delta)
afd1 = AFD(['a', 'b'], ['q0','q1','q2','q3'], ['q0'], ['q0'], delta)


afd1.exportar('nombre')
afd1.graficar()
afd2.graficar()
afd3.graficar()
'''
print(afd1.hallarEstadosLimbo())
print(afd1.imprimirAFDSimplificado()) #
print(afd1.hallarEstadosInaccesibles()) 
print(afd1.eliminarEstadosInaccesibles())
print(afd1.pasarString())
print(afd1.procesarCadena('abbaab'))
print(afd1.procesarCadenaConDetalles('abbaab'))
print(afd1.procesarListaCadenas('abbaab','prueba','no')) #
print(afd1.simplificarAFD('abbaab')) #
'''