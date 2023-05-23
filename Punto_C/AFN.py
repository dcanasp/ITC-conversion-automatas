class AutomataNoDeterminista:
    def __init__(self, alfabeto, estados, estado_inicial, estados_aceptacion, delta):
        self.alfabeto = alfabeto
        self.estados = estados
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion
        self.estados_inaccesibles = set()  # Atributo para almacenar los estados inaccesibles
        self.delta = delta
    
    # def __init__(self):
    #     # inicializar atributos
    #     self.alfabeto = set()
    #     self.estados = set()
    #     self.estadoInicial = None
    #     self.estadosAceptacion = set()
    #     self.estadosInaccesibles = set()
    #     self.tablaTransiciones = {}

    def hallarEstadosInaccesibles(self):
        # Realizamos un recorrido BFS (Breadth-First Search) para encontrar los estados inaccesibles

        # Creamos un conjunto para almacenar los estados accesibles
        estados_accesibles = {self.estado_inicial}

        # Creamos una cola para realizar el recorrido BFS
        cola = [self.estado_inicial]

        while cola:
            estado_actual = cola.pop(0)

            # Obtenemos los estados siguientes desde el estado actual
            estados_siguientes = set()
            for simbolo in self.alfabeto:
                if estado_actual in self.delta and simbolo in self.delta[estado_actual]:
                    estados_siguientes.update(self.delta[estado_actual][simbolo])

            # Agregamos los estados siguientes al conjunto de estados accesibles
            nuevos_estados_accesibles = estados_siguientes - estados_accesibles
            estados_accesibles.update(nuevos_estados_accesibles)

            # Agregamos los nuevos estados a la cola para seguir recorriendo
            cola.extend(nuevos_estados_accesibles)

        # Los estados inaccesibles serán aquellos que no están en el conjunto de estados accesibles
        self.estados_inaccesibles = self.estados - estados_accesibles


    def toString(self):
        # Imprimir representación del autómata

        # Imprimir estados
        print("Estados:", self.estados)

        # Imprimir estado inicial
        print("Estado inicial:", self.estado_inicial)

        # Imprimir estados de aceptación
        print("Estados de aceptación:", self.estados_aceptacion)

        # Imprimir estados inaccesibles
        print("Estados inaccesibles:", self.estados_inaccesibles)

        # Imprimir tabla de transiciones
        print("Tabla de transiciones:")
        for estado_actual in self.delta:
            for simbolo in self.delta[estado_actual]:
                estados_siguientes = self.delta[estado_actual][simbolo]
                print(f"Delta({estado_actual}, {simbolo}) = {estados_siguientes}")


    def imprimirAFNSimplificado(self):
        # Imprimir representación simplificada del autómata

        # Imprimir estados
        print("Estados:", self.estados - self.estados_inaccesibles)

        # Imprimir estado inicial
        print("Estado inicial:", self.estado_inicial)

        # Imprimir estados de aceptación
        print("Estados de aceptación:", self.estados_aceptacion)

        # Imprimir tabla de transiciones
        print("Tabla de transiciones:")
        for estado_actual in self.delta:
            # Si el estado actual no es inaccesible
            if estado_actual not in self.estados_inaccesibles:
                for simbolo in self.delta[estado_actual]:
                    estados_siguientes = self.delta[estado_actual][simbolo]
                    # Si los estados siguientes no son inaccesibles
                    estados_siguientes = estados_siguientes - self.estados_inaccesibles
                    print(f"Delta({estado_actual}, {simbolo}) = {estados_siguientes}")

    # def AFNtoAFD(afn): #FALTA
        
    
    def procesarCadena(self, cadena):
            estados_actuales = {self.estado_inicial}

            for simbolo in cadena:
                estados_siguientes = set()
                
                for estado_actual in estados_actuales:
                    if (estado_actual, simbolo) in self.delta:
                        estados_siguientes.update(self.delta[(estado_actual, simbolo)])

                estados_actuales = estados_siguientes

            return any(estado in self.estadosAceptacion for estado in estados_actuales)

    def procesarCadenaConDetalles(self, cadena):
        # Procesar la cadena, determinar si es aceptada o rechazada, e imprimir los estados tomados

        estado_actual = self.estadoInicial
        estados_tomados = [estado_actual]

        for simbolo in cadena:
            # Verificar si el símbolo pertenece al alfabeto
            if simbolo not in self.alfabeto:
                return False  # Cadena rechazada

            # Obtener los estados siguientes a través de la transición
            if estado_actual in self.delta and simbolo in self.delta[estado_actual]:
                estados_siguientes = self.delta[estado_actual][simbolo]
            else:
                return False  # Cadena rechazada

            # Actualizar el estado actual con los estados siguientes
            estado_actual = estados_siguientes

            estados_tomados.append(estado_actual)

        # Verificar si el estado actual es un estado de aceptación
        if estado_actual in self.estados_aceptacion:
            # Cadena aceptada
            print(f"La cadena '{cadena}' es aceptada por el autómata.")
            print("Estados tomados:")
            for estado in estados_tomados:
                print(estado)
            return True
        else:
            # Cadena rechazada
            print(f"La cadena '{cadena}' es rechazada por el autómata.")
            return False


    def computarTodosLosProcesamientos(self, cadena, nombreArchivo):
        procesamientos_aceptados = []
        procesamientos_rechazados = []
        procesamientos_abortados = []
        num_procesamientos = 0

        with open(nombreArchivo + "Aceptadas.txt", "w") as archivo_aceptadas:
            with open(nombreArchivo + "Rechazadas.txt", "w") as archivo_rechazadas:
                with open(nombreArchivo + "Abortadas.txt", "w") as archivo_abortadas:
                    for procesamiento in self.generarProcesamientos(cadena):
                        num_procesamientos += 1

                        estado_actual = self.estadoInicial
                        transiciones = []
                        aceptado = False

                        for simbolo in procesamiento:
                            estado_siguiente = self.transicion(estado_actual, simbolo)
                            transiciones.append((estado_actual, simbolo, estado_siguiente))
                            estado_actual = estado_siguiente

                        if estado_actual in self.estadosAceptacion:
                            aceptado = True
                            procesamientos_aceptados.append(transiciones)
                            archivo_aceptadas.write(self.formatoProcesamiento(transiciones) + "\n")
                        elif estado_actual in self.estados:
                            procesamientos_rechazados.append(transiciones)
                            archivo_rechazadas.write(self.formatoProcesamiento(transiciones) + "\n")
                        else:
                            procesamientos_abortados.append(transiciones)
                            archivo_abortadas.write(self.formatoProcesamiento(transiciones) + "\n")

                        print("Procesamiento:", self.formatoProcesamiento(transiciones))
                        print("Estado Final:", estado_actual)
                        print("Aceptado:", aceptado)
                        print("-------------------------")

        return num_procesamientos

    def generarProcesamientos(self, cadena):
        procesamientos = [[]]
        for simbolo in cadena:
            nuevos_procesamientos = []
            for procesamiento in procesamientos:
                estado_actual = procesamiento[-1] if procesamiento else self.estadoInicial
                transiciones = self.tablaTransiciones.get((estado_actual, simbolo), set())
                for estado in transiciones:
                    nuevos_procesamientos.append(procesamiento + [estado])
            procesamientos = nuevos_procesamientos
        return procesamientos

    def transicion(self, estado_actual, simbolo):
        transiciones = self.tablaTransiciones.get((estado_actual, simbolo), set())
        if len(transiciones) == 1:
            return next(iter(transiciones))
        return None

    def formatoProcesamiento(self, procesamiento):
        return "->".join(f"{transicion[0]}({transicion[1]})" for transicion in procesamiento)


    def procesarListaCadenas(self, listaCadenas, nombreArchivo, imprimirPantalla):
        if not nombreArchivo:
            nombreArchivo = "resultados.txt"

        with open(nombreArchivo, "w") as archivo:
            for cadena in listaCadenas:
                procesamientos_aceptados = []
                procesamientos_rechazados = []
                procesamientos_abortados = []

                for procesamiento in self.generarProcesamientos(cadena):
                    estado_actual = self.estadoInicial
                    transiciones = []

                    for simbolo in procesamiento:
                        estado_siguiente = self.transicion(estado_actual, simbolo)
                        transiciones.append((estado_actual, simbolo))
                        estado_actual = estado_siguiente

                    if estado_actual in self.estadosAceptacion:
                        procesamientos_aceptados.append(transiciones)
                    elif estado_actual in self.estados:
                        procesamientos_rechazados.append(transiciones)
                    else:
                        procesamientos_abortados.append(transiciones)

                num_procesamientos = len(procesamientos_aceptados) + len(procesamientos_rechazados) + len(procesamientos_abortados)
                num_procesamientos_aceptados = len(procesamientos_aceptados)
                num_procesamientos_abortados = len(procesamientos_abortados)
                num_procesamientos_rechazados = len(procesamientos_rechazados)
                cadena_aceptada = num_procesamientos_aceptados > 0

                if imprimirPantalla:
                    print("Cadena:", cadena)
                    print("Procesamientos Aceptados:")
                    for procesamiento in procesamientos_aceptados:
                        print(self.formatoProcesamiento(procesamiento))
                    print("Número de Procesamientos:", num_procesamientos)
                    print("Número de Procesamientos Aceptados:", num_procesamientos_aceptados)
                    print("Número de Procesamientos Abortados:", num_procesamientos_abortados)
                    print("Número de Procesamientos Rechazados:", num_procesamientos_rechazados)
                    print("Aceptada:", cadena_aceptada)
                    print("-------------------------")

                archivo.write(f"Cadena: {cadena}\n")
                archivo.write("Procesamientos Aceptados:\n")
                for procesamiento in procesamientos_aceptados:
                    archivo.write(f"{self.formatoProcesamiento(procesamiento)}\n")
                archivo.write(f"Número de Procesamientos: {num_procesamientos}\n")
                archivo.write(f"Número de Procesamientos Aceptados: {num_procesamientos_aceptados}\n")
                archivo.write(f"Número de Procesamientos Abortados: {num_procesamientos_abortados}\n")
                archivo.write(f"Número de Procesamientos Rechazados: {num_procesamientos_rechazados}\n")
                archivo.write(f"Aceptada: {cadena_aceptada}\n")
                archivo.write("-------------------------\n")

    def procesarCadenaConversion(self, cadena):
        # Convertir el AFN a un AFD
        afd = self.AFNtoAFD()

        # Procesar la cadena con el AFD
        return afd.procesarCadena(cadena)

    def procesarCadenaConDetallesConversion(self, cadena):
        # Convertir el AFN a un AFD
        afd = self.AFNtoAFD()

        # Procesar la cadena con el AFD y obtener los detalles
        aceptada, procesamientos = afd.procesarCadenaConDetalles(cadena)

        # Imprimir los estados del AFD que va tomando al procesar cada símbolo
        for estado, simbolo in procesamientos:
            print("Estado: {}".format(estado))

        # Retornar el resultado de aceptación/rechazo
        return aceptada
    

    
def procesarListaCadenasConversion(self, listaCadenas, nombreArchivo, imprimirPantalla=True):
    # Verificar si el nombre de archivo es válido, de lo contrario asignar uno por defecto
    if not nombreArchivo:
        nombreArchivo = "procesamientos.txt"

    # Abrir el archivo para escribir los resultados
    with open(nombreArchivo, "w") as archivo:
        for cadena in listaCadenas:
            # Convertir el AFN a un AFD
            afd = self.AFNtoAFD()

            # Procesar la cadena con el AFD y obtener los detalles
            aceptada, procesamientos = afd.procesarCadenaConDetalles(cadena)

            # Imprimir los detalles en el archivo
            archivo.write("Cadena: {}\n".format(cadena))
            archivo.write("Detalles:\n")
            for estado, simbolo in procesamientos:
                archivo.write("{} - {}\n".format(estado, simbolo))
            archivo.write("Aceptada: {}\n".format(aceptada))
            archivo.write("\n")

            # Imprimir en pantalla si es necesario
            if imprimirPantalla:
                print("Cadena: {}".format(cadena))
                print("Detalles:")
                for estado, simbolo in procesamientos:
                    print("{} - {}".format(estado, simbolo))
                print("Aceptada: {}".format(aceptada))
                print()

    # Imprimir mensaje de finalización
    print("Procesamiento de cadenas completado. Resultados guardados en el archivo: {}".format(nombreArchivo))
"""afn = AFN() #prueba procesarlistaCadenas
# Configurar el AFN

listaCadenas = ["00101", "01010", "11011"]
nombreArchivo = "resultados"
imprimirPantalla = True

afn.procesarListaCadenas(listaCadenas, nombreArchivo, imprimirPantalla)"""
"""afn = AFN()  #prueba procesamiento
# Configurar el AFN

cadena = "00101"
nombreArchivo = "procesamientos"
num_procesamientos = afn.computarTodosLosProcesamientos(cadena, nombreArchivo)
print("Número de Procesamientos:", num_procesamientos)"""

# Creamos una instancia del autómata
"""automata = AutomataNoDeterminista(alfabeto, estados, estado_inicial, estados_aceptacion, delta)

# Definimos los atributos del autómata
alfabeto = {'0', '1'}
estados = {'q0', 'q1', 'q2', 'q3'}
estado_inicial = 'q0'
estados_aceptacion = {'q3'}
estados_inaccesibles = set()
delta = {
    'q0': {'0': {'q1'}, '1': {'q0', 'q1'}},
    'q1': {'0': {'q2'}, '1': {'q0'}},
    'q2': {'0': {'q2'}, '1': {'q2'}},
    'q3': {'0': {'q3'}, '1': {'q3'}}
}


# Hallamos los estados inaccesibles
automata.hallarEstadosInaccesibles()

# Mostramos los estados inaccesibles
print("Estados inaccesibles:", automata.estados_inaccesibles)
automata.toString()
# Imprimimos el autómata simplificado
automata.imprimirAFNSimplificado()
#procesamos una cadena
cadena = '0011'
es_aceptada = automata.procesarCadena(cadena)
if es_aceptada:
    print(f"La cadena '{cadena}' es aceptada por el autómata.")
else:
    print(f"La cadena '{cadena}' es rechazada por el autómata.")"""
"""
afn = AutomataNoDeterminista()

# Definir atributos del AFN de ejemplo
afn.alfabeto = {'0', '1'}
afn.estados = {'q0', 'q1', 'q2'}
afn.estadoInicial = 'q0'
afn.estadosAceptacion = {'q2'}
afn.tablaTransiciones = {
    ('q0', '0'): {'q1'},
    ('q0', '1'): {'q0'},
    ('q1', '0'): {'q1'},
    ('q1', '1'): {'q2'},
    ('q2', '0'): {'q2'},
    ('q2', '1'): {'q2'},
}

# Procesar una cadena de ejemplo
cadena = '101'
resultado = afn.procesarCadena(cadena)

if resultado:
    print("La cadena '{}' es aceptada por el autómata.".format(cadena))
else:
    print("La cadena '{}' es rechazada por el autómata.".format(cadena))


afn = AutomataNoDeterminista()
# Configurar el AFN

cadena = "00101"
afn.procesarCadenaConDetalles(cadena)"""
