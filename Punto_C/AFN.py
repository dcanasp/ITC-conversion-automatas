from Punto_B.AFD import AFD_class
from collections import defaultdict
from graficar import graficosAFN

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
    
    #11
    def procesarListaCadenas(self, listaCadenas, nombreArchivo, imprimirPantalla):
        if not nombreArchivo:
            nombreArchivo = "resultados.txt"

        with open(nombreArchivo, "w") as file:
            for cadena in listaCadenas:
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

                num_posibles_procesamientos = len(procesamientosAceptados) + len(procesamientosRechazados) + len(procesamientosAbortados)
                num_aceptados = len(procesamientosAceptados)
                num_rechazados = len(procesamientosRechazados)
                num_abortados = len(procesamientosAbortados)

                file.write(f"Cadena: {cadena}\n")
                file.write("Procesamientos Aceptados:\n")
                for procesamiento in procesamientosAceptados:
                    file.write(procesamiento + "\n")

                file.write("\nProcesamientos Rechazados:\n")
                for procesamiento in procesamientosRechazados:
                    file.write(procesamiento + "\n")

                file.write("\nProcesamientos Abortados:\n")
                for procesamiento in procesamientosAbortados:
                    file.write(procesamiento + "\n")

                file.write(f"\nNúmero de posibles procesamientos: {num_posibles_procesamientos}\n")
                file.write(f"Número de procesamientos de aceptación: {num_aceptados}\n")
                file.write(f"Número de procesamientos de rechazo: {num_rechazados}\n")
                file.write(f"Número de procesamientos abortados: {num_abortados}\n\n")

                if imprimirPantalla:
                    print(f"Cadena: {cadena}")
                    print("Procesamientos Aceptados:")
                    for procesamiento in procesamientosAceptados:
                        print(procesamiento)

                    print("\nProcesamientos Rechazados:")
                    for procesamiento in procesamientosRechazados:
                        print(procesamiento)

                    print("\nProcesamientos Abortados:")
                    for procesamiento in procesamientosAbortados:
                        print(procesamiento)

                    print(f"\nNúmero de posibles procesamientos: {num_posibles_procesamientos}")
                    print(f"Número de procesamientos de aceptación: {num_aceptados}")
                    print(f"Número de procesamientos de rechazo: {num_rechazados}")
                    print(f"Número de procesamientos abortados: {num_abortados}\n")
    
    #7
    def AFNtoAFD(self):  
        print("Tabla de Transiciones del AFN:")
        print(f"{'Estado Antiguo':^20} | {'Símbolo':^10} | {'Estado Nuevo':^20}")
        print('-' * 55)
        for transicion, estados_nuevos in self.transicion.items():
            estado_antiguo, simbolo = transicion
            estados_nuevos_str = ', '.join(estados_nuevos) if estados_nuevos else '$'
            print(f"{estado_antiguo:^20} | {simbolo:^10} | {estados_nuevos_str:^20}")
        print()
        
        
        # Crear un nuevo objeto AFD
        afd = AFD_class(self.alfabeto, [], self.estadoInicial, [], {})

        # Obtener el cierre-ε del estado inicial del AFN
        estado_inicial_afn = self.estadoInicial
        cierre_inicial = [estado_inicial_afn]

        # Agregar el cierre-ε del estado inicial como estado inicial del AFD
        estado_inicial_afd = self.obtenerEstadoID(cierre_inicial)
        afd.agregarEstado(estado_inicial_afd)

        # Crear una tabla de transiciones para el AFD
        tabla_transiciones = defaultdict(dict)
        cierre_estados = {estado_inicial_afd: cierre_inicial}

        # Procesar nuevos estados hasta que no haya más transiciones
        procesados = set([estado_inicial_afd])

        while procesados:
            estado_actual_afd = procesados.pop()

            for simbolo in self.alfabeto:
                nuevos_estados = self.obtenerTransiciones(cierre_estados[estado_actual_afd], simbolo)

                if nuevos_estados:
                    estado_destino_afd = self.obtenerEstadoID(nuevos_estados)

                    tabla_transiciones[estado_actual_afd][simbolo] = estado_destino_afd

                    if estado_destino_afd not in afd.estados:
                        afd.agregarEstado(estado_destino_afd)
                        procesados.add(estado_destino_afd)
                        cierre_estados[estado_destino_afd] = nuevos_estados

        # Construir las transiciones completas del AFD
        for estado_afd in afd.estados:
            for simbolo in self.alfabeto:
                estado_destino_afd = tabla_transiciones[estado_afd].get(simbolo, None)

                if estado_destino_afd:
                    afd.agregarTransicion(estado_afd, simbolo, estado_destino_afd)

        # Obtener los estados de aceptación del AFD
        estados_aceptacion_afd = []

        for estado_afd in afd.estados:
            for estado_aceptacion_afn in self.estadosAceptados:
                if estado_aceptacion_afn in cierre_estados[estado_afd]:
                    estados_aceptacion_afd.append(estado_afd)
                    break

        afd.estadosAceptados = estados_aceptacion_afd
        afd.estadoInicial = estado_inicial_afd

        # Imprimir la tabla de transiciones del AFD
        print("Tabla de Transiciones del AFD:")
        print(f"{'Estado Antiguo':^20} | {'Símbolo':^10} | {'Estado Nuevo':^20}")
        print('-' * 55)
        for estado_antiguo, transiciones in tabla_transiciones.items():
            for simbolo, estado_nuevo in transiciones.items():
                print(f"{estado_antiguo:^20} | {simbolo:^10} | {estado_nuevo:^20}")
        print()

        transicionAdaptada=convertir_notacion(afd.transicion)
        afd.transicion=transicionAdaptada
        return afd
    #7
    def obtenerTransiciones(self, estados, simbolo):
        nuevos_estados = set()

        for estado_afn in estados:
            if (estado_afn, simbolo) in self.transicion:
                nuevos_estados.update(self.transicion[(estado_afn, simbolo)])

        return list(nuevos_estados)
    #7
    def obtenerEstadoID(self, estados):
        estados.sort()
        return ''.join(estados)
    #PUNTOS EXTRA
    def graficar(self):
        return graficosAFN(self.alfabeto,self.estados,self.transicion,self.estadoInicial,self.estadosAceptados)
    
    #12 
    def procesarCadenaConversion(self,cadena):
        afd = self.AFNtoAFD()
        print(afd.procesarCadena(cadena))
        return(afd.procesarCadena(cadena))
    #13
    def procesarCadenaConDetallesConversion(self,cadena):
        afd = self.AFNtoAFD()
        print(afd.procesarCadenaConDetalles(cadena))
        return(afd.procesarCadenaConDetalles(cadena))
    #14
    def procesarListaCadenasConversion(self,listaCadenas,nombreArchivo, imprimirPantalla):
        afd = self.AFNtoAFD()
        afd.procesarListaCadenas(listaCadenas,nombreArchivo, imprimirPantalla)
        return(afd.procesarListaCadenas(listaCadenas,nombreArchivo, imprimirPantalla)) 
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
    
def convertir_notacion(diccionario):
    nuevo_diccionario = {}
    
    for clave, valor in diccionario.items():
        estado, simbolo = clave
        if estado not in nuevo_diccionario:
            nuevo_diccionario[estado] = {}
        nuevo_diccionario[estado][simbolo] = valor
    return nuevo_diccionario