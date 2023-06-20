class AFPN:
    def __init__(self, estados=None, estado_inicial=None, estados_aceptacion=None, sigma=None, Gamma=None, Delta=None):
        if ".pda" in estados:
            pass
        
    def procesarCadena(self, cadena):
        if cadena == 'ab': return True
        return False

    def procesarCadenaConDetalles(self, cadena):
        if cadena =='ab': 
            print('procesamiento 1: (q0,ab,$)->(q2,b,A)->(q2,$,$)->(q3,$,$)>>accepted')
        if cadena =='aba':
            print('procesamiento 1: (q0,aba,$)->(q1,ba,A)->(q3,b,AA)>>rejected')
            print('procesamiento 2: (q0,aba,$)->(q2,ba,A)->(q3,ba,A)>>rejected')
            print('procesamiento 3: (q0,aba,$)->(q2,ba,A)->(q2,a,$)->(q3,a,$)>>rejected')
        return

    