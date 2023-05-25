# from Punto_B.AFD import AFD_class

class AFN():
    #1
    def __init__(self, alfabeto, estados, estadoInicial, estadosAceptacion, delta):
        setattr(self, 'alfabeto', alfabeto)
        setattr(self, 'estados', estados)
        setattr(self, 'estadoInicial', estadoInicial)
        setattr(self, 'estadosAceptados', estadosAceptacion)
        setattr(self, 'transicion', delta)
        setattr(self, 'estadosInaccesibles', [])
    
    #3
    def hallarEstadosInaccesibles(self):
        estados_alcanzables = set()
        estados_visitados = set([self.estadoInicial])

        while estados_visitados:
            estado_actual = estados_visitados.pop()
            estados_alcanzables.add(estado_actual)
            transiciones = self.obtener_transiciones_desde_estado(estado_actual)
            for _, destinos in transiciones:
                for destino in destinos:
                    if destino not in estados_alcanzables:
                        estados_visitados.add(destino)

        estados_inaccesibles = set(self.estados) - estados_alcanzables

        # Eliminar transiciones hacia estados inaccesibles
        self.transicion = {(origen, simbolo): destinos for (origen, simbolo), destinos in self.transicion.items() if origen not in estados_inaccesibles and all(destino not in estados_inaccesibles for destino in destinos)}

        self.estadosInaccesibles = estados_inaccesibles

    def obtener_transiciones_desde_estado(self, estado):
        return [(origen, destinos) for (origen, simbolo), destinos in self.transicion.items() if origen == estado]
    
    #4
    def toString(self):
        output = ''
        output += '#!nfa\n'
        output += '#alphabet\n'
        output += f"{self.alfabeto[0]}-{self.alfabeto[-1]}\n"
        output += '#states\n'
        for estado in self.estados:
            output += ''.join(estado) + '\n'
        output += '#initial\n'
        output += self.estadoInicial + '\n'
        output += '#accepting\n'
        for estado in self.estadosAceptados:
            output += ''.join(estado) + '\n'
        output += '#transitions\n'
        for (origen, simbolo), destinos in self.transicion.items():
            destinos_str = ';'.join(destinos)
            output += f'{origen}:{simbolo}>{destinos_str}\n'
        return output

    #5
    def imprimirAFNSimplificado(self):
        self.hallarEstadosInaccesibles()
        estados_minimizados = set(self.estados) - set(self.estadosInaccesibles)
        print('#!nfa')
        print('#alphabet')
        print('-'.join(self.alfabeto))
        print('#states')
        print(' '.join(estados_minimizados))
        print('#initial')
        print(self.estadoInicial)
        print('#accepting')
        print(' '.join(self.estadosAceptados))
        print('#transitions')
        for (origen, simbolo), destinos in self.transicion.items():
            if origen in estados_minimizados:
                destinos_minimizados = [destino for destino in destinos if destino in estados_minimizados]
                if destinos_minimizados:
                    destinos_str = ';'.join(destinos_minimizados)
                    print(f'{origen}:{simbolo}>{destinos_str}')
                    
    #6
    def exportar(self, nombreArchivo):
        archivo = open(nombreArchivo+".nfa","w")
        archivo.write(self.toString())
        return archivo.close()
    

    #8
    def procesarCadena(self, cadena):
        # Inicializar el conjunto de estados actuales con el estado inicial
        estados_actuales = set([self.estadoInicial])

        # Recorrer la cadena y actualizar los estados actuales en cada transición
        for simbolo in cadena:
            # Obtener los estados siguientes a partir de los estados actuales y el símbolo actual
            estados_siguientes = set()
            for estado_actual in estados_actuales:
                if (estado_actual, simbolo) in self.transicion:
                    estados_siguientes.update(self.transicion[(estado_actual, simbolo)])

            # Actualizar los estados actuales con los estados siguientes
            estados_actuales = estados_siguientes

        # Verificar si al menos uno de los estados actuales es un estado de aceptación
        for estado_actual in estados_actuales:
            if estado_actual in self.estadosAceptados:
                return True

        return False
    
    #9
    def procesarCadenaConDetalles(self, cadena):
        # Inicializar el estado actual con el estado inicial
        estado_actual = self.estadoInicial

        # Imprimir el estado inicial y la cadena de entrada
        print(f"[{estado_actual},{cadena}]->", end="")

        # Recorrer la cadena y actualizar el estado actual en cada transición
        for i, simbolo in enumerate(cadena):
            # Obtener los estados siguientes a partir del estado actual y el símbolo actual
            estados_siguientes = self.transicion.get((estado_actual, simbolo), [])

            # Si no hay transición para el símbolo actual, la cadena es rechazada
            if not estados_siguientes:
                print("Cadena rechazada.")
                return False

            # Actualizar el estado actual con el primer estado siguiente
            estado_actual = estados_siguientes[0]

            # Imprimir la transición si la cadena no se ha procesado completamente
            if i < len(cadena) - 1:
                cadena_restante = cadena[i+1:]
                print(f"[{estado_actual},{cadena_restante}]->", end="")

        # Verificar si el estado actual es un estado de aceptación
        if estado_actual in self.estadosAceptados:
            return("Aceptación.")
        else:
            return("Cadena rechazada.")

    #10
    def computarTodosLosProcesamientos(self, cadena, nombreArchivo):
        procesamientosAceptados = []
        procesamientosRechazados = []
        procesamientosAbortados = []

        def procesar(cadena, estado_actual, procesamiento):
            procesamiento += f"-> {estado_actual}"
            if not cadena:
                if estado_actual in self.estadosAceptados:
                    procesamientosAceptados.append(procesamiento + "-> Aceptación")
                else:
                    procesamientosRechazados.append(procesamiento + "-> Rechazo")
                return

            simbolo = cadena[0]
            restante = cadena[1:]

            if (estado_actual, simbolo) in self.transicion:
                for estado_siguiente in self.transicion[(estado_actual, simbolo)]:
                    procesar(restante, estado_siguiente, procesamiento + f"({simbolo})")

            procesamientosAbortados.append(procesamiento + "-> Abortado")

        procesar(cadena, self.estadoInicial, "")

        # Guardar los resultados en archivos
        with open(f"{nombreArchivo}Aceptadas.txt", "w") as file:
            for procesamiento in procesamientosAceptados:
                file.write(procesamiento + "\n")

        with open(f"{nombreArchivo}Rechazadas.txt", "w") as file:
            for procesamiento in procesamientosRechazados:
                file.write(procesamiento + "\n")

        with open(f"{nombreArchivo}Abortadas.txt", "w") as file:
            for procesamiento in procesamientosAbortados:
                file.write(procesamiento + "\n")

        # Imprimir los resultados en pantalla
        print("Procesamientos Aceptados:")
        for procesamiento in procesamientosAceptados:
            print(procesamiento)

        print("\nProcesamientos Rechazados:")
        for procesamiento in procesamientosRechazados:
            print(procesamiento)

        print("\nProcesamientos Abortados:")
        for procesamiento in procesamientosAbortados:
            print(procesamiento)

        num_procesamientos = len(procesamientosAceptados) + len(procesamientosRechazados) + len(procesamientosAbortados)
        print(f"\nNúmero de procesamientos realizados: {num_procesamientos}")
        return num_procesamientos
    #2
def constructor(nombreArchivo):
        try:
            with open(nombreArchivo+".nfa","r") as archivo:
                datos = archivo.readlines()
                for i in range(len(datos)):
                    datos[i] = datos[i].strip()
                estados = []
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
                        estadoInicial=datos[i+1]
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
                            nuevonuevo_estado = nuevo_estado.split(';')
                            # print(estado,caracter,nuevonuevo_estado)
                            tuplas = (estado,caracter)
                            transiciones[tuplas]=list(nuevonuevo_estado)
                            # print(transiciones)
            # print(alfabeto,estados,estadoInicial,estadosAceptados,transiciones)
            return AFN(alfabeto, estados, estadoInicial, estadosAceptados, transiciones)

        except(FileNotFoundError):
            print("No se encontró el archivo")
    
# INSTANCIA
afn_instancia = AFN(['a', 'b', 'c'], ['q0', 'q1', 'q2', 'q3'], 'q0', ['q1'], {
    ('q0', 'a'): ['q1','q1','q3'],
    ('q0', 'b'): [],
    ('q1', 'a'): ['q1'],
    ('q1', 'b'): ['q2'],
    ('q2', 'a'): [],
    ('q2', 'b'): ['q1','q2'],
    ('q3', 'a'): [],
    ('q3', 'b'): ['q3'],
})
# afd = afn_instancia.toAFD()
# afd.toString()
# # print("instanciaalfabeto")
# # print(afn_instancia.estados)
# print(afn_instancia.toString())
# print(afn_instancia.imprimirAFNSimplificado())
# afn_instancia.exportar("instancia")
# segundainstancia =constructor("instancia")
# print("######################################### SEGUNDA")
# print(segundainstancia.imprimirAFNSimplificado())
# print(afn_instancia.procesarCadenaConDetalles("aaaa"))
# # afn_instancia.toString()
# # print("#############################################################################################################")
# # afn_instancia.imprimirAFNSimplificado()
# # afn_instancia.exportar("AFN_prueba")


# AFN_prueba =constructor("AFN_prueba")

# print(AFN_prueba.toString())
afn_instancia = AFN(['a', 'b'], ['q0', 'q1', 'q2', 'q3'], 'q0', ['q1'], {
    ('q0', 'a'): ['q0','q1','q3'],
    ('q0', 'b'): [],
    ('q1', 'a'): ['q1'],
    ('q1', 'b'): ['q2'],
    ('q2', 'a'): [],
    ('q2', 'b'): ['q1','q2'],
    ('q3', 'a'): [],
    ('q3', 'b'): ['q3'],
})