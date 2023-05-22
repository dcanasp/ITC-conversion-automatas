#!nfe
#1) Constructor(alfabeto, estados, estadoInicial, estadosAceptacion,Delta) de la clase para inicializar los atributos.
class AFNLambda:
    #Función para obtener el alfabeto de un input
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
        estados=Automata.estados
        delta=Automata.Delta
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
                Automata.estadosInaccesibles.append(estado)
        return Automata.estadosInaccesibles
    
    def __init__(self, alfabeto=None, estados=None, estadoInicial=None, estadosAceptacion=None, Delta=None):
        if ".txt" in alfabeto:
            with open(alfabeto, 'r') as file:
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
            #Remover el final de cada partes[i] desde la ultima coma
            i=0
            while i < len(partes):
                f = len(partes[i])-1
                while f > 0:
                    if partes[i][f]==",":
                        partes[i]=partes[i][:f]
                        break
                    f-=1
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
                for transicion in self.Delta:
                    estadoCadena=self.leer_hasta_subcadena(":",transicion)
                    transiciones=self.leer_desde_subcadena(":",transicion)
                    if estadoCadena == estado_actual and transiciones[0] == '$':
                        listaEstados.append(transiciones[2:])
        i = 0
        while i < len(listaEstados):
            if listaEstados[i].find(';'):
                listaEstados.extend(listaEstados[i].split(';'))
                listaEstados.pop(i)
            i+=1
        i = 0
        while i < len(listaEstados):
            if listaEstados[i] in listaEstados[:i]:
                listaEstados.pop(i)
            else:
                i+=1
        listaEstados = list(set(listaEstados))
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

    def comprobarCadena(cadena):
        cadena = cadena
        i=0
        while i < len(cadena):
            if cadena[i] not in Automata.alfabeto:
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
            archivo.write(Automata.imprimirAFNLSimplificado())
            archivo.write("#unreachable\n")
            for estado in Automata.estadosInaccesibles:
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

Automata = AFNLambda("PruebaITC.txt")
#Automata.hallarEstadosInaccesibles()
#print(Automata.calcularLambdaClausura("s3"))
#print("Estados inaccesibles",Automata.estadosInaccesibles)
#print(Automata)
#print(Automata.imprimirAFNLSimplificado())
#print(Automata.procesarCadenaConDetalles("bbc"))
#Automata.exportar("PruebaITC")
#print(Automata.computarTodosLosProcesamientos("bbc", "Cadenas"))
Automata.procesarListaCadenas(["bbc", "ab"], "Cadenas", True)