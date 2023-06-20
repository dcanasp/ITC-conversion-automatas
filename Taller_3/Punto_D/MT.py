class MT:
    def __init__(self, estados, estadoInicial, estadosAceptacion, alfabetoEntrada, alfabetoCinta, delta):
        # Inicializar los atributos con setattr
        setattr(self, 'estados', estados)
        setattr(self, 'estadoInicial', estadoInicial)
        setattr(self, 'estadosAceptacion', estadosAceptacion)
        setattr(self, 'alfabetoEntrada', alfabetoEntrada)
        setattr(self, 'alfabetoCinta', alfabetoCinta)
        setattr(self, 'delta', delta)
    
    def procesarCadena(self, cadena):
        # Inicializar la cinta y la posición de la cabeza de lectura/escritura
        cinta = list(cadena)
        cinta.append('!')  # Agregar un símbolo de espacio en blanco al final de la cinta
        posicion = 0
        estado_actual = self.estadoInicial
        
        while True:
            # Obtener el símbolo actual en la cinta
            simbolo_actual = cinta[posicion]
            
            # Verificar si el estado actual es un estado de aceptación
            if estado_actual in self.estadosAceptacion:
                print(True)
                return True
            
            # Verificar si la transición actual está definida
            if (estado_actual, simbolo_actual) in self.delta:
                # Obtener la nueva transición y aplicarla
                nuevo_estado, nuevo_simbolo, direccion = self.delta[(estado_actual, simbolo_actual)]
                
                # Actualizar el estado actual
                estado_actual = nuevo_estado
                
                # Escribir el nuevo símbolo en la cinta
                cinta[posicion] = nuevo_simbolo
                
                # Mover la cabeza de lectura/escritura
                if direccion == '>':
                    posicion += 1
                elif direccion == '<':
                    posicion -= 1
                    
                # Expander la cinta si es necesario
                if posicion == len(cinta):
                    cinta.append('!')
                elif posicion == -1:
                    cinta.insert(0, '!')
                
            else:
                print(False)
                return False

    def toString(self):
            output = ""

            # Agregar los estados
            output += "#states\n"
            for estado in self.estados:
                output += estado + "\n"

            # Agregar el estado inicial
            output += "#initial\n"
            output += self.estadoInicial + "\n"

            # Agregar los estados de aceptación
            output += "#accepting\n"
            for estado in self.estadosAceptacion:
                output += estado + "\n"

            # Agregar el alfabeto de entrada
            output += "#inputAlphabet\n"
            for simbolo in self.alfabetoEntrada:
                output += simbolo + "\n"
            output += ";\n"

            # Agregar el alfabeto de la cinta
            output += "#tapeAlphabet\n"
            for simbolo in self.alfabetoCinta:
                output += simbolo + "\n"
            output += "_\n"

            # Agregar las transiciones
            output += "#transitions\n"
            for tupla, transicion in self.delta.items():
                estado_origen, simbolo = tupla
                estado_destino, nuevo_simbolo, direccion = transicion
                output += estado_origen + ":" + simbolo + "?" + estado_destino + ":" + nuevo_simbolo + ":" + direccion + "\n"

            print(output)
            return output

    def procesarCadenaConDetalles(self, cadena):
        # Inicializar la cinta y la posición de la cabeza de lectura/escritura
        cinta = list(cadena)
        cinta.append('!')  # Agregar un símbolo de espacio en blanco al final de la cinta
        posicion = 0
        estado_actual = self.estadoInicial
        var=True
        # Preparar el string para almacenar los detalles
        detalles = ""

        # Agregar el estado inicial y la cadena original
        detalle = f"({estado_actual}){cadena}"
        detalles += detalle

        while estado_actual not in self.estadosAceptacion:
            # Obtener el símbolo actual en la cinta
            simbolo_actual = cinta[posicion]

            # Verificar si la transición actual está definida
            if (estado_actual, simbolo_actual) in self.delta:
                # Obtener la nueva transición y aplicarla
                nuevo_estado, nuevo_simbolo, direccion = self.delta[(estado_actual, simbolo_actual)]

                # Construir la cadena procesada hasta el estado actual
                cinta[posicion] = nuevo_simbolo
                cadena_procesada = ''.join(cinta)

                # Mover la cabeza de lectura/escritura
                if direccion == '>':
                    posicion += 1
                elif direccion == '<':
                    posicion -= 1

                # Expander la cinta si es necesario
                if posicion == len(cinta):
                    cinta.append('!')
                elif posicion == -1:
                    cinta.insert(0, '!')

                # Actualizar el estado actual
                estado_actual = nuevo_estado

                # Obtener la parte izquierda y derecha de la cadena respecto al estado actual
                izquierda = ''.join(cinta[:posicion])
                derecha = ''.join(cinta[posicion:])

                # Agregar los detalles del procesamiento al string
                detalle = f"->{izquierda}({estado_actual}){derecha}"
                detalles += detalle

                # Si hemos llegado al final de la cadena, detener el bucle
                if posicion == len(cadena_procesada):
                    break
            else:
                cadena_procesada = ''.join(cinta)
                detalles += f"->{cadena_procesada}"
                detalles += " Cadena rechazada por la MT."
                var=False 
                break

        if estado_actual in self.estadosAceptacion:
            detalles += " Cadena aceptada por la MT."

        # Imprimir los detalles en la consola

        return detalles,var

    def exportar(self, nombreArchivo):
        archivo = open(nombreArchivo+".tm","w")
        archivo.write(self.toString())
        return archivo.close()

    def procesarFuncion(self, cadena):
        # Inicializar la cinta y la posición de la cabeza de lectura/escritura
        cinta = list(cadena)
        cinta.append('!')  # Agregar un símbolo de espacio en blanco al final de la cinta
        posicion = 0
        estado_actual = self.estadoInicial

        # Iterar sobre la cadena hasta llegar al estado de aceptación o rechazo
        while estado_actual not in self.estadosAceptacion:
            # Obtener el símbolo actual en la cinta
            simbolo_actual = cinta[posicion]

            # Verificar si la transición actual está definida
            if (estado_actual, simbolo_actual) in self.delta:
                # Obtener la nueva transición y aplicarla
                nuevo_estado, nuevo_simbolo, direccion = self.delta[(estado_actual, simbolo_actual)]

                # Construir la cadena procesada hasta el estado actual
                cinta[posicion] = nuevo_simbolo

                # Mover la cabeza de lectura/escritura
                if direccion == '>':
                    posicion += 1
                elif direccion == '<':
                    posicion -= 1

                # Expander la cinta si es necesario
                if posicion == len(cinta):
                    cinta.append('!')
                elif posicion == -1:
                    cinta.insert(0, '!')

                # Actualizar el estado actual
                estado_actual = nuevo_estado
            else:
                # No existe una transición definida para el estado y símbolo actual
                break

        # Obtener la última configuración instantánea
        izquierda = ''.join(cinta[:posicion])
        derecha = ''.join(cinta[posicion:])
        ultima_configuracion = f"{izquierda}{derecha}"

        # Imprimir la última configuración instantánea
        print(ultima_configuracion)

        return ultima_configuracion
    
    def procesarListaCadenas(self, listaCadenas, nombreArchivo=None, imprimirPantalla=False):
        if not nombreArchivo:
            nombreArchivo = "resultados.txt"

        try:
            archivo = open(nombreArchivo, "w")
        except IOError:
            print("No se pudo abrir el archivo de resultados.")
            return

        resultados = ""  # Variable para almacenar los detalles del procesamiento

        for cadena in listaCadenas:
            # Invocar el método procesarCadenaConDetalles para obtener los detalles del procesamiento
            detalle = self.procesarCadenaConDetalles(cadena)
            ultima = self.procesarFuncion(cadena)
            # Verificar si la cadena es aceptada o rechazada
            resultado = "yes" if detalle[1] else "no"

            # Construir la cadena de salida con el formato especificado
            salida = f"cadena: {cadena},  {resultado},  {detalle[0]}\n"

            # Agregar la salida a los resultados
            resultados += salida

            # Imprimir la salida si es necesario
            if imprimirPantalla:
                salida = f"Cadena: {cadena}, Ultima configuracion instantanea: {ultima}, Aceptada: {resultado}\n"
                print(salida)

        archivo.write(resultados)  # Guardar los resultados en el archivo
        archivo.close()

        print(f"Los resultados se han guardado en el archivo '{nombreArchivo}'.")

def construirMT(descripcion):
    lineas = descripcion.split("\n")
    estados = []
    estadoInicial = None
    estadosAceptacion = []
    alfabetoEntrada = []
    alfabetoCinta = []
    delta = {}

    for linea in lineas:
        if linea.startswith("#states"):
            estados = lineas[lineas.index(linea) + 1 : lineas.index("#initial")]
        elif linea.startswith("#initial"):
            estadoInicial = lineas[lineas.index(linea) + 1]
        elif linea.startswith("#accepting"):
            estadosAceptacion = lineas[lineas.index(linea) + 1 : lineas.index("#inputAlphabet")]
        elif linea.startswith("#inputAlphabet"):
            alfabetoEntrada = lineas[lineas.index(linea) + 1 : lineas.index("#tapeAlphabet") - 1]
        elif linea.startswith("#tapeAlphabet"):
            alfabetoCinta = lineas[lineas.index(linea) + 1 : lineas.index("#transitions") - 1]
        elif linea.startswith("#transitions"):
            transiciones = lineas[lineas.index(linea) + 1 :]

            for transicion in transiciones:
                partes = transicion.split(":")
                estado_origen = partes[0]
                simbolo = partes[1].split("?")[0]
                estado_destino = partes[1].split("?")[1]
                nuevo_simbolo = partes[2]
                direccion = partes[3]

                delta[(estado_origen, simbolo)] = (estado_destino, nuevo_simbolo, direccion)

    # Crear instancia de la clase MT
    mt = MT(estados, estadoInicial, estadosAceptacion, alfabetoEntrada, alfabetoCinta, delta)
    return mt

def construirMTDesdeArchivo(nombreArchivo):
    try:
        with open(nombreArchivo, "r") as archivo:
            descripcion = archivo.read()
            return construirMT(descripcion)
    except FileNotFoundError:
        print("No se encontró el archivo")

cadena = 'aabbcc'
# Definición de la máquina de Turing
estados = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5']
estadoInicial = 'q0'
estadosAceptacion = ['q5']
alfabetoEntrada = ['a', 'b', 'c']
alfabetoCinta = ['X', 'Y', 'Z']
delta = {
    ('q0', 'a'): ('q1', 'X', '>'),
    ('q0', 'Y'): ('q4', 'Y', '>'),
    ('q0', '!'): ('q5', '!', '-'),
    ('q1', 'b'): ('q2', 'Y', '>'),
    ('q1', 'a'): ('q1', 'a', '>'),
    ('q1', 'Y'): ('q1', 'Y', '>'),
    ('q1', 'b'): ('q2', 'Y', '>'),
    ('q2', 'b'): ('q2', 'b', '>'),
    ('q2', 'Z'): ('q2', 'Z', '>'),
    ('q2', 'c'): ('q3', 'Z', '<'),
    ('q3', 'a'): ('q3', 'a', '<'),
    ('q3', 'b'): ('q3', 'b', '<'),
    ('q3', 'Y'): ('q3', 'Y', '<'),
    ('q3', 'Z'): ('q3', 'Z', '<'),
    ('q3', 'X'): ('q0', 'X', '>'),
    ('q4', 'Y'): ('q4', 'Y', '>'),
    ('q4', 'Z'): ('q4', 'Z', '>'),
    ('q4', '!'): ('q5', '!', '-')
}

# Crear una instancia de la máquina de Turing
mt = MT(estados, estadoInicial, estadosAceptacion, alfabetoEntrada, alfabetoCinta, delta)

# Procesar una cadena de ejemplo
print("PRUEBA CONSTRUIR DESDE ARCHIVO")
mt=construirMTDesdeArchivo("prueba.tm")
print("EXPORTAR")
mt.exportar("prueba2")
print("TOSTRING")
mt.toString()
print("PROCESAR CADENA")
mt.procesarCadena(cadena)
print("PROCESAR CADENA CON DETALLES")
mt.procesarCadenaConDetalles(cadena)
print("PROCESAR FUNCION")
mt.procesarFuncion(cadena)

listaCadenas = ["abcc", "xyz", "abc", "abc"]
print("PROCESAR LISTA DE CADENAS")
# Procesar las cadenas con detalles y guardar los resultados en un archivo
mt.procesarListaCadenas(listaCadenas, nombreArchivo="resultados.txt", imprimirPantalla=True)