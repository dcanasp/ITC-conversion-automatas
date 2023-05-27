from graficar import graficos

class AFD_class:
    def __init__(self,alfabeto,estados,estadoInicial,estadosAceptados,delta):
        setattr(self,'alfabeto',alfabeto)
        setattr(self,'estados',estados)
        setattr(self,'estadoInicial',estadoInicial)
        setattr(self,'estadosAceptados',estadosAceptados)
        setattr(self,'transicion',delta)
        setattr(self,'estadosLimbo',[])
        setattr(self,'estadosInaccesibles',[])
        self.verificarCorregirCompletitudAFD()
    
        ##Para la conversión AFN TO AFD
    
    #Nuevos métodos para la construcción del AFD basado en una instancia de AFN
    def agregarEstado(self, estado):
        self.estados.append(estado)

    def agregarTransicion(self, estado, simbolo, destino):
        self.transicion[(estado, simbolo)] = destino
    
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
            print("Estados inaccesibles: ", self.estadosInaccesibles)
            return True

        # Si no hay estados inaccesibles, devolver False
        else:
            return False
    
    def pasarString(self):
        # Imprimir estados, alfabeto y estado inicial
        output = "#!dfa\n#alphabet\n"

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

        print(output)
        
        return output
    
    #Metodo para imprimir el AFD recibiendolo de la instancia de un AFN.
    def pasarStringAFNtoAFD(self):
        # Imprimir estados, alfabeto y estado inicial
        output = "#!dfa\n#alphabet\n"

        output += f"{self.alfabeto[0]}-{self.alfabeto[-1]}\n#states\n"

        # Imprimir estados
        for estado in self.estados:
            output += f"{estado}\n"

        # Imprimir estado inicial
        output += f"#initial\n{self.estadoInicial}\n"

        # Imprimir estados de aceptación
        output += "#accepting\n"
        for estado in self.estadosAceptados:
            output += f"{estado}\n"

        # Imprimir transiciones
        output += "#transitions\n"
        for estado in self.estados:
            for simbolo in self.alfabeto:
                destino = self.transicion.get((estado, simbolo), None)
                if destino is not None:
                    output += f"{estado}:{simbolo}>{destino}\n"

        print(output)
        return output
    
    def imprimirAFDSimplificado(self):
        self.pasarString()
    
    def exportar(self, nombreArchivo):
        archivo = open(nombreArchivo+".dfa","w")
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
            return salida+'\tAceptacion'
        else:
            return salida+'\tNo Aceptacion'
    
    def procesarListaCadenas(self, listaCadenas,nombreArchivo, imprimirPantalla: bool):
        output = ''

        for cadena in listaCadenas:
            output += cadena+'\t'+self.procesarCadenaConDetalles(cadena)+'\n'

        archivo = open(nombreArchivo+".afd","w")
        archivo.write(output)
        archivo.close()

        if imprimirPantalla:
            print(output)
 
    def eliminarEstadosInaccesibles(self):
        for estado in self.estadosInaccesibles:
            self.estados.remove(estado)
            for simbolo in self.alfabeto:
                self.transicion[estado].pop(simbolo)

    def graficar(self):
        graficos(self.alfabeto,self.estados,self.transicion,self.estadoInicial,self.estadosAceptados,self.estadosLimbo)


def constructor(nombreArchivo):
        try:
            with open(nombreArchivo+".dfa","r") as archivo:
                datos = archivo.readlines()
                for i in range(len(datos)):
                    datos[i] = datos[i].strip()
                estados = []
                estadoInicial = []
                estadosAceptados = []
                transiciones = {}
                
                for i in range(len(datos)):
                    if datos[i] == '#alphabet':
                        cadena = datos[i+1]
                        inicio = ord(cadena[0])
                        fin = ord(cadena[-1])
                        alfabeto = [chr(i) for i in range(inicio, fin+1)]
                    if datos[i] == '#states':
                        for j in range(i+1,len(datos)):
                            if datos[j] == '#initial':
                                break
                            else:
                                estados.append(datos[j])
                    if datos[i] == '#initial':
                        estadoInicial.append(datos[i+1])
                    if datos[i] == '#accepting':
                        for j in range(i+1,len(datos)):
                            if datos[j] == '#transitions':
                                break
                            else:
                                estadosAceptados.append(datos[j])
                    if datos[i] == '#transitions':
                        for j in range(i+1,len(datos)):
                                estado, transicion = datos[j].split(':')
                                caracter, nuevo_estado = transicion.split('>')
                                
                                if estado not in transiciones:
                                    transiciones[estado] = {}
                                
                                transiciones[estado][caracter] = nuevo_estado
            afd = AFD_class(alfabeto, estados, estadoInicial, estadosAceptados, transiciones)
            return afd

        except(FileNotFoundError):
            print("No se encontró el archivo")
    
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
        
    afdResultado = AFD_class(alfabeto, estados, estadoInicial, estadosAceptados, transicion)
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
        
    afdResultado = AFD_class(alfabeto, estados, estadoInicial, estadosAceptados, transicion)
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
        
    afdResultado = AFD_class(alfabeto, estados, estadoInicial, estadosAceptados, transicion)
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
        
    afdResultado = AFD_class(alfabeto, estados, estadoInicial, estadosAceptados, transicion)
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

def simplificarAFD(afd):
    # Eliminar estados inaccesibles
        afd.hallarEstadosInaccesibles()
        afd.eliminarEstadosInaccesibles()

        # Inicializar la tabla de pares de estados no marcados
        unmarked_pairs = set()
        for state1 in afd.estados:
            for state2 in afd.estados:
                if state1 != state2 and frozenset([state1, state2]) not in unmarked_pairs:
                    if (state1 in afd.estadosAceptados) != (state2 in afd.estadosAceptados):
                        continue
                    unmarked_pairs.add(frozenset([state1, state2]))

        # Marcar pares de estados distinguibles
        marked_pairs = set()
        new_marked_pairs = set()
        while True:
            for pair in unmarked_pairs:
                state1, state2 = pair
                for symbol in afd.alfabeto:
                    next_pair = frozenset([afd.transicion[state1][symbol], afd.transicion[state2][symbol]])
                    if next_pair in marked_pairs:
                        new_marked_pairs.add(pair)
                        break
            if not new_marked_pairs:
                break
            marked_pairs.update(new_marked_pairs)
            unmarked_pairs -= new_marked_pairs
            new_marked_pairs.clear()

        # Construir el AFD mínimo
        min_states = []
        for pair in unmarked_pairs:
            state1, state2 = pair
            found = False
            for min_state in min_states:
                if state1 in min_state or state2 in min_state:
                    min_state.update(pair)
                    found = True
                    break
            if not found:
                min_states.append(set(pair))
        for state in afd.estados:
            found = False
            for min_state in min_states:
                if state in min_state:
                    found = True
                    break
            if not found:
                min_states.append({state})

        min_alphabet = afd.alfabeto
        min_transition_function = {}
        for min_state in min_states:
            representative = next(iter(min_state))
            min_transition_function[tuple(sorted(min_state))] = {}
            for symbol in afd.alfabeto:
                next_state = afd.transicion[representative][symbol]
                for s in min_states:
                    if next_state in s:
                        min_transition_function[tuple(sorted(min_state))][symbol] = tuple(sorted(s))
                        break

        min_initial_state = None
        for min_state in min_states:
            if afd.estadoInicial[0] in min_state:
                min_initial_state = tuple(sorted(min_state))
                break

        min_final_states = set()
        for final_state in afd.estadosAceptados:
            for min_state in min_states:
                if final_state in min_state:
                    min_final_states.add(tuple(sorted(min_state)))
                    break
        
        return AFD_class(min_alphabet,
                   {tuple(sorted(state)) for state in min_states},
                   tuple(sorted(min_initial_state)),
                   {tuple(sorted(state)) for state in min_final_states},
                   min_transition_function)