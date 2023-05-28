from Punto_B.AFD import AFD
from Punto_C.AFN import AFN
from graficar import graficosAFNLambda
class AFNLambda:
    def obtenerAlfabeto(alfabeto):
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

    def hallarEstadosInaccesibles(self):
        estados=self.estados
        delta=self.Delta
        for estado in estados:
            i=0
            encontrado=False
            while i < len(delta):
                subcadena=self.leer_desde_subcadena(">",delta[i])
                if subcadena.find(estado)!=-1:
                    encontrado=True
                    break
                i+=1
            if encontrado==False:
                self.estadosInaccesibles.append(estado)
        return self.estadosInaccesibles
    
    def __init__(self, alfabeto=None, estados=None, estadoInicial=None, estadosAceptacion=None, Delta=None):
        if ".nfe" in alfabeto or ".NFe" in alfabeto or ".NFE" in alfabeto:
            with open('./Punto_D/'+alfabeto, 'r') as file:
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
            #Obtener el alfabeto
            alfabeto=AFNLambda.obtenerAlfabeto(partes[0])
            #Obtener los estados
            estados=partes[1].split(',')
            #Obtener el estado inicial
            estadoInicial=partes[2]
            #Obtener los estados de aceptacion
            estadosAceptacion=partes[3].split(',')
            #Obtener la funcion de transicion
            Delta=partes[4].split(',')

        self.alfabeto = alfabeto
        self.estados = estados
        self.estadoInicial = estadoInicial
        self.estadosAceptacion = estadosAceptacion
        self.Delta = Delta
        self.estadosInaccesibles = []

        for transicion in self.Delta:
            if transicion.find(";"):
                inicio=self.leer_hasta_subcadena(":",transicion)
                medio=self.leer_desde_subcadena(":",transicion)
                medio=self.leer_hasta_subcadena(">",medio)
                final=self.leer_desde_subcadena(">",transicion)
                transiciones=final.split(";")
                for valor in transiciones:
                    transicionCompleta=inicio+":"+medio+">"+valor
                    self.Delta.append(transicionCompleta)
                self.Delta.remove(transicion)
        self.Delta=list(set(self.Delta))
        self.Delta.sort()

    def imprimirAFNLSimplificado(self):
        representation = ""
        representation += "#!nfe\n"
        representation += "#alphabet\n"
        for letra in self.alfabeto:
            representation += letra + "\n"
        representation += "#states\n"
        for estado in self.estados:
            representation += estado + "\n"
        representation += "#initial\n"
        representation += self.estadoInicial + "\n"
        representation += "#accepting\n"
        for estado in self.estadosAceptacion:
            representation += estado + "\n"
        representation += "#transitions\n"
        for transicion in self.Delta:
            representation += transicion + "\n"
        representation + "#unreachable\n"
        return representation
    
    def __str__(self):
        texto = self.imprimirAFNLSimplificado()
        texto += "#unreachable\n"
        for estado in self.estadosInaccesibles:
            texto += estado + "\n"
        return texto

    def calcularLambdaClausura(self, estado):
        estados = []
        if ',' in estado:
            estados = estado.split(',')
        else:
            estados.append(estado)
        listaEstados = []
        for estado_actual in estados:
            if estado_actual in self.estados:
                listaEstados.extend(self.calcularClausuraLambdaRecursiva(estado_actual))
        listaEstados = list(set(listaEstados))
        return listaEstados

    def calcularClausuraLambdaRecursiva(self, estado):
        estadosVisitados = set()
        colaEstados = [estado]
        listaEstados = []
        while colaEstados:
            estado_actual = colaEstados.pop(0)
            if estado_actual in estadosVisitados:
                continue
            estadosVisitados.add(estado_actual)
            listaEstados.append(estado_actual)
            for transicion in self.Delta:
                estadoCadena = self.leer_hasta_subcadena(":", transicion)
                transiciones = self.leer_desde_subcadena(":", transicion)
                if estadoCadena == estado_actual and transiciones[0] == '$':
                    estadosDestino = transiciones[2:].split(';')
                    colaEstados.extend(estadosDestino)
        listaEstados = list(set(listaEstados))
        listaEstados.sort()
        return listaEstados

    def leer_desde_subcadena(self,subcadena, cadena):
        posicion = cadena.find(subcadena)
        if posicion != -1:
            contenido_leido = cadena[posicion+1:]
            return contenido_leido
        else:
            return "None"
        
    def leer_hasta_subcadena(self,subcadena, cadena):
        posicion = cadena.find(subcadena)
        if posicion != -1:
            contenido_leido = cadena[:posicion]
            return contenido_leido
        else:
            return "None"
    
    def exportar(nombre_archivo, contenido):
        nombre_archivo_con_extension = nombre_archivo + ".nfe"
        with open(nombre_archivo_con_extension, 'w') as archivo:
            archivo.write(contenido)

    def comprobarCadena(self,cadena):
        cadena = cadena
        i=0
        while i < len(cadena):
            if cadena[i] not in self.alfabeto:
                print("La cadena no es valida")
                return False
            i+=1
    
    def procesarCadenaConDetalles(self, cadena):
        print("Procesando símbolo: $")
        lambda_clausura_actual = self.calcularLambdaClausura(self.estadoInicial)

        for simbolo in cadena:
            nueva_lambda_clausura = []

            print("---Estado actual:", lambda_clausura_actual, "---")
            print("Procesando símbolo:", simbolo)

            for estado in lambda_clausura_actual:
                print("Estado:", estado)

                for transicion in self.Delta:
                    estadoCadena = self.leer_hasta_subcadena(":", transicion)
                    transiciones = self.leer_desde_subcadena(":", transicion)

                    if estadoCadena == estado and transiciones[0] == simbolo:
                        if transiciones[2:] not in nueva_lambda_clausura:
                            if transiciones[2:].find(";") != -1:
                                nueva_lambda_clausura.extend(transiciones[2:].split(";"))
                            else:
                                nueva_lambda_clausura.append(transiciones[2:])

                        print(estado, "--", simbolo, "->", transiciones[2:])

            lambda_clausura_actual = list(set(nueva_lambda_clausura))
            print("Lambda Clausura actualizada:", lambda_clausura_actual)

        print("Los estados a los que se llega son:", lambda_clausura_actual)

        for estado in lambda_clausura_actual:
            if estado in self.estadosAceptacion:
                return True

        return False
    
    def exportar(self,nombre_archivo):
        nombre_archivo_con_extension = nombre_archivo + ".nfe"
        with open(nombre_archivo_con_extension, 'w') as archivo:
            archivo.write(self.imprimirAFNLSimplificado())
            archivo.write("#unreachable\n")
            for estado in self.estadosInaccesibles:
                archivo.write(estado + "\n")
    
    def procesarCadena(self,cadena):
        lambda_clausura_actual = self.calcularLambdaClausura(self.estadoInicial)
        for simbolo in cadena:
            nueva_lambda_clausura = []
            for estado in lambda_clausura_actual:
                for transicion in self.Delta:
                    estadoCadena=self.leer_hasta_subcadena(":",transicion)
                    transiciones=self.leer_desde_subcadena(":",transicion)
                    if estadoCadena == estado and transiciones[0] == simbolo:
                        if transiciones[2:] not in nueva_lambda_clausura:
                            if transiciones[2:].find(";")!=-1:
                                nueva_lambda_clausura.extend(transiciones[2:].split(";"))
                            else:
                                nueva_lambda_clausura.append(transiciones[2:])
            lambda_clausura_actual = []
            for estado_nuevo in nueva_lambda_clausura:
                lambda_clausura_actual.extend(self.calcularLambdaClausura(estado_nuevo))
                if estado_nuevo not in lambda_clausura_actual:
                    lambda_clausura_actual.append(estado_nuevo)
            lambda_clausura_actual = list(set(lambda_clausura_actual))
        for estado in lambda_clausura_actual:
            if estado in self.estadosAceptacion:
                return True
        return False
    
    def computarTodosLosProcesamientos(self, cadena, nombreArchivo):
        procesamientos_aceptados = []
        procesamientos_rechazados = []
        procesamientos_abortados = []

        def procesar_cadena_recursivo(cadena_actual, estados_actuales):
            if not cadena_actual:
                if any(estado in self.estadosAceptacion for estado in estados_actuales):
                    return True
                return False
            simbolo_actual = cadena_actual[0]
            cadena_restante = cadena_actual[1:]

            nueva_lambda_clausura = []
            for estado in estados_actuales:
                for transicion in self.Delta:
                    estado_cadena = self.leer_hasta_subcadena(":", transicion)
                    transiciones = self.leer_desde_subcadena(":", transicion)
                    if estado_cadena == estado and (transiciones[0] == simbolo_actual or transiciones[0] == "$"):
                        if transiciones[2:] not in nueva_lambda_clausura:
                            if transiciones[2:].find(";") != -1:
                                nueva_lambda_clausura.extend(transiciones[2:].split(";"))
                            else:
                                nueva_lambda_clausura.append(transiciones[2:])

            if not nueva_lambda_clausura:
                procesamientos_abortados.append((estados_actuales, cadena_actual))
                return False

            for estado_nuevo in nueva_lambda_clausura:
                nuevos_estados_actuales = self.calcularLambdaClausura(estado_nuevo)
                if estado_nuevo not in nuevos_estados_actuales:
                    nuevos_estados_actuales.append(estado_nuevo)

                if procesar_cadena_recursivo(cadena_restante, nuevos_estados_actuales):
                    procesamientos_aceptados.append((estados_actuales, cadena_actual))
                    return True

            procesamientos_rechazados.append((estados_actuales, cadena_actual))
            return False

        procesar_cadena_recursivo(cadena, [self.estadoInicial])

        nombre_archivo_aceptadas = nombreArchivo + "Aceptadas.txt"
        nombre_archivo_rechazadas = nombreArchivo + "Rechazadas.txt"
        nombre_archivo_abortadas = nombreArchivo + "Abortadas.txt"

        with open(nombre_archivo_aceptadas, "w") as archivo_aceptadas:
            archivo_aceptadas.write("Procesamientos Aceptados:\n")
            for estados, cadena in procesamientos_aceptados:
                archivo_aceptadas.write(f"Estados: {estados}, Cadena: {cadena}\n")

        with open(nombre_archivo_rechazadas, "w") as archivo_rechazadas:
            archivo_rechazadas.write("Procesamientos Rechazados:\n")
            for estados, cadena in procesamientos_rechazados:
                archivo_rechazadas.write(f"Estados: {estados}, Cadena: {cadena}\n")

        with open(nombre_archivo_abortadas, "w") as archivo_abortadas:
            archivo_abortadas.write("Procesamientos Abortados:\n")
            for estados, cadena in procesamientos_abortados:
                archivo_abortadas.write(f"Estados: {estados}, Cadena: {cadena}\n")

        print("Procesamientos Aceptados:")
        for estados, cadena in procesamientos_aceptados:
            print(f"Estados: {estados}, Cadena: {cadena}")

        print("Procesamientos Rechazados:")
        for estados, cadena in procesamientos_rechazados:
            print(f"Estados: {estados}, Cadena: {cadena}")

        print("Procesamientos Abortados:")
        for estados, cadena in procesamientos_abortados:
            print(f"Estados: {estados}, Cadena: {cadena}")

    def procesarListaCadenas(self, listaCadenas, nombreArchivo, imprimirPantalla):
        # Verificar si el nombre de archivo es válido
        if nombreArchivo == "" or nombreArchivo is None:
            # Asignar un nombre por defecto si el nombre de archivo no es válido
            nombreArchivo = "resultados_procesamiento.txt"

        # Abrir el archivo en modo escritura
        archivo_resultados = open(nombreArchivo, "w")

        # Variables para contar los resultados
        num_procesamientos_aceptados = 0
        num_procesamientos_rechazados = 0
        num_procesamientos_abortados = 0

        # Recorrer cada cadena en la lista de cadenas
        for cadena in listaCadenas:
            # Procesar la cadena con detalles
            procesamiento_detalles = self.procesarCadenaConDetalles(cadena)

            # Obtener los resultados del procesamiento
            cadena_aceptada = procesamiento_detalles  # El resultado es la propia variable procesamiento_detalles
            procesamientos = []  # Inicializar como una lista vacía, ya que no hay procesamientos en este caso


            # Contar los resultados
            if cadena_aceptada:
                num_procesamientos_aceptados += 1
            elif procesamientos == []:
                num_procesamientos_rechazados += 1
            else:
                num_procesamientos_abortados += 1

            # Escribir los resultados en el archivo
            archivo_resultados.write(f"Cadena: {cadena}\n")
            archivo_resultados.write(f"Procesamientos:\n")
            for procesamiento in procesamientos:
                archivo_resultados.write(f"{procesamiento}\n")
            archivo_resultados.write(f"Número de posibles procesamientos: {len(procesamientos)}\n")
            archivo_resultados.write(f"Número de procesamientos de aceptación: {num_procesamientos_aceptados}\n")
            archivo_resultados.write(f"Número de procesamientos abortados: {num_procesamientos_abortados}\n")
            archivo_resultados.write(f"Número de procesamientos de rechazo: {num_procesamientos_rechazados}\n")
            archivo_resultados.write(f"Aceptada: {'Sí' if cadena_aceptada else 'No'}\n\n")
            print("\n")

            # Imprimir en pantalla si es necesario
            if imprimirPantalla:
                print(f"Cadena: {cadena}")
                print(f"Procesamientos:")
                for procesamiento in procesamientos:
                    print(procesamiento)
                print(f"Número de posibles procesamientos: {len(procesamientos)}")
                print(f"Número de procesamientos de aceptación: {num_procesamientos_aceptados}")
                print(f"Número de procesamientos abortados: {num_procesamientos_abortados}")
                print(f"Número de procesamientos de rechazo: {num_procesamientos_rechazados}")
                print(f"Aceptada: {'Sí' if cadena_aceptada else 'No'}\n")
                print("\n")

        # Cerrar el archivo
        archivo_resultados.close()

    def obtenerTransiciones(self,estadoActual, simbolo):
        estadoActual = estadoActual
        simbolo = simbolo
        transiciones = []
        for transicion in self.Delta:
            estadoInicial = self.leer_hasta_subcadena(":", transicion)
            simbolos = self.leer_desde_subcadena(":", transicion)
            simboloActual = simbolos[0]
            estadoFinal = simbolos[2:]
            if estadoActual==estadoInicial and simboloActual==simbolo:
                transiciones.append(estadoFinal)
        i=0
        while i < len(transiciones):
            if transiciones[i].find(";")!=-1:
                transiciones.extend(transiciones[i].split(";"))
                transiciones.pop(i)
            i+=1
        return transiciones

    def calcularTransicion(self,estadoActual, simbolo):
        estadoActual = estadoActual
        simbolo = simbolo
        transiciones = []
        for transicion in self.Delta:
            estadoInicial = self.leer_hasta_subcadena(":", transicion)
            simbolos = self.leer_desde_subcadena(":", transicion)
            simboloActual = simbolos[0]
            estadoFinal = simbolos[2:]
            if estadoActual==estadoInicial and simboloActual==simbolo:
                transiciones.append(estadoFinal)
        transiciones=list(set(transiciones))
        transiciones.sort()
        return transiciones
        
    def unirEstados(self, transiciones):
        estadosUnidos = {}
        for transicion in transiciones:
            estadoOrigen = self.leer_hasta_subcadena(":", transicion)
            simbolo = self.leer_desde_subcadena(":", transicion)
            transicionesDestino = self.leer_desde_subcadena(">", transicion)
            if estadoOrigen not in estadosUnidos:
                estadosUnidos[estadoOrigen] = {simbolo: set(transicionesDestino.split(";"))}
            else:
                estadosUnidos[estadoOrigen][simbolo] |= set(transicionesDestino.split(";"))

        transicionesUnidas = []
        for estado, transiciones in estadosUnidos.items():
            transicionesEstado = []
            for simbolo, destinos in transiciones.items():
                transicionesEstado.append(estado + ":" + simbolo + ">" + ";".join(destinos))
            transicionesUnidas.append(";".join(transicionesEstado))

        return transicionesUnidas
    
    def actualizarEstados(self,listaTransiciones):
        estadosNuevos=[]
        estados=self.estados
        for transicion in listaTransiciones:
            medio=self.leer_desde_subcadena(":",transicion)
            medio=self.leer_hasta_subcadena(">",medio)
            final=self.leer_desde_subcadena(">",transicion)
            for estado in estados:
                if estado in final:
                    estadosNuevos.append(estado)
        if self.estadoInicial not in estadosNuevos:
            estadosNuevos.append(self.estadoInicial)
        estadosNuevos=list(set(estadosNuevos))
        estadosNuevos.sort()
        return estadosNuevos
    
    def actualizarAceptacion(self,estados):
        estadosAceptacion=[]
        for estado in estados:
            clambda=self.calcularLambdaClausura(estado)
            for estadoActual in clambda:
                if estadoActual in self.estadosAceptacion:
                    estadosAceptacion.append(estado)
        estadosAceptacion=list(set(estadosAceptacion))
        estadosAceptacion.sort()
        return estadosAceptacion
    
    def convertirListaADiccionario(self,listaTransiciones):
        transiciones=listaTransiciones
        diccionario = {}
        for transicion in transiciones:
            partes = transicion.split(':')
            estado_actual = partes[0].strip()
            simbolo = partes[1].split('>')[0].strip()
            estados_siguientes = partes[1].split('>')[1].strip()
            if (estado_actual, simbolo) in diccionario:
                diccionario[(estado_actual, simbolo)].append(estados_siguientes)
            else:
                diccionario[(estado_actual, simbolo)] = [estados_siguientes]
        return diccionario

    def AFN_LambdaToAFN(self):
        estadoInicial=self.estadoInicial
        estados=self.estados
        lambdaClausuraInicial=self.calcularLambdaClausura(estadoInicial)
        transicionesFinales=[]
        for estado in estados:
            lambdaClausuraInicial=self.calcularLambdaClausura(estado)
            if estado not in lambdaClausuraInicial:
                lambdaClausuraInicial.append(estado)
            lambdaClausuraInicial=list(set(lambdaClausuraInicial))
            for simbolo in self.alfabeto:
                for estado2 in lambdaClausuraInicial:
                    estadosProvisional=[]
                    estadosProvisional=self.calcularTransicion(estado2,simbolo)
                    for estadoActual in estadosProvisional:
                        if estadoActual!=None:
                            for transicion in self.calcularLambdaClausura(estadoActual):
                                transicionesFinales.append(estado+":"+simbolo+">"+transicion)
        transicionesFinales=list(set(transicionesFinales))
        transicionesFinales.sort()
        transiciones=self.convertirListaADiccionario(transicionesFinales)
        estadosFinales=self.actualizarEstados(transicionesFinales)
        estadosFinales.sort()
        estadosAceptacion=self.actualizarAceptacion(estadosFinales)
        nuevoAFN=AFN(self.alfabeto,estadosFinales,estadoInicial,estadosAceptacion,transiciones)
        return nuevoAFN

    def AFN_LambdaToAFD(self):
        nuevoAFD=self.AFN_LambdaToAFN().AFNtoAFD()
        return nuevoAFD
    
    def procesarCadenaConversion(cadena):
        AFD = AFNLambda.AFN_LambdaToAFD()
        return AFD.procesarCadena(cadena)
    
    def procesarCadenaConDetallesConversion(cadena):
        AFD = AFNLambda.AFN_LambdaToAFD()
        return AFD.procesarCadenaConDetalles(cadena)
    
    def procesarListaCadenasConversion(listaCadenas, nombreArchivo, imprimirPantalla):
        AFD = AFNLambda.AFN_LambdaToAFD()
        AFD.procesarListaCadenas(listaCadenas, nombreArchivo, imprimirPantalla)
    
    def graficar(self):
        return graficosAFNLambda(self.alfabeto,self.estados,self.Delta,self.estadoInicial,self.estadosAceptacion)
        