# from ayudasAFD import prueba,segunda #esto es lo mismo
from ayudasAFD import *
#NO CREAR MAS FUNCIONES EN ESTE ARCHIVO, SI SE NECESITAN IR A ayudasAFD, U OTROS ARCHIVOS COMO LOS VAYAN NECESITANDO


class AFD:
    def __init__(self,alfabeto,estados,estadoInicial,estadosAceptados,delta):
        setattr(self,'alfabeto',alfabeto)
        setattr(self,'estados',estados)
        setattr(self,'estadosInicial',estadoInicial)
        setattr(self,'estadosAceptados',estadosAceptados)
        setattr(self,'transicion',delta)
        setattr(self,'estadosLimbo','')
        setattr(self,'estadosInaccesibles','')
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
        #para cambiar un parametro
        self.estadosInaccesibles = ''
        return
    
    def pasarString(self):
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

    
instancia = AFD(['a','b'],['q0','q1','q2'],['q0'],['q2'],[['q0','q1'],['q1','q2'],['q1','q1']])
instancia.pasarString()
instancia.procesarCadenaConDetalles('01010110')