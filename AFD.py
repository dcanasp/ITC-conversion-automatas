# from ayudasAFD import prueba,segunda #esto es lo mismo
from ayudasAFD import *
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
        self.exportar(self.nombreArchivo)
    
    def verificarCorregirCompletitudAFD(self):
        # para llamar a una funcion
        self.hallarEstadosLimbo()
        return
    
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
        print(self.transicion['q1']['a'])
        return
    
    def imprimirAFDSimplificado(self):
        return
    
    def exportar(self):
        return
    
    def procesarCadena(self,cadena):
        return
    
    def procesarCadenaConDetalles(self,cadena):
        return
    
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
    
    

    
instancia = AFD(['a','b'],['q0','q1','q2','q3'],['q0'],['q2'],{'q0':{'a':'q2','b':'q2'},'q1':{'a':'q0','b':'q0'}, 'q2':{'a':'q2','b':'q2'}, 'q3':{'a':'q2','b':'q2'}})
instancia.hallarEstadosInaccesibles()
instancia.procesarCadenaConDetalles('01010110')