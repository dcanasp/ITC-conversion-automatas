import matplotlib.pyplot as plt
import networkx as nx
from itertools import zip_longest
from array import array

def graficos(alfabeto,estados,transicion,estadoInicial,estadosAceptados,estadosLimbo):
    G = nx.DiGraph()

    pila = []
    pila.append(estadoInicial[0])
    estados_graficados = []
    selfLoops = []
    estados_graficados.append(estadoInicial[0])
    # Recorrer los estados y simular las transiciones a través del alfabeto
    G.add_node(estadoInicial[0])
    G.add_nodes_from(estados)
    simbolosUsadosEnOrden = []
    simbolosSelfLoopsEnOrden = []
    while pila != []:
        estado = pila.pop()
        for simbolo in alfabeto:
            # Obtener el estado al que se transita desde el estado actual y con el símbolo actual
            try:
                estado_siguiente = transicion[estado][simbolo]
                G.add_edge(estado,estado_siguiente)
                simbolosUsadosEnOrden.append(simbolo)
                if estado == estado_siguiente:
                    selfLoops.append(estado_siguiente)
                    simbolosSelfLoopsEnOrden.append(simbolo)
            except KeyError:
                estado_siguiente = None

            # Si el estado siguiente no está en la lista de estados accesibles,
            # agregarlo a la lista para futuras iteraciones
            if estado_siguiente not in estados_graficados:
                estados_graficados.append(estado_siguiente)
                pila.append(estado_siguiente)
    
    
    # pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility
    # # nodes
    # nx.draw_networkx_nodes(G, pos, node_size=700)
    # # edges
    # nx.draw_networkx_edges(G, pos, width=6)
    # nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    # # edge weight labels
    # edge_labels = nx.get_edge_attributes(G, "weight")
    # nx.draw_networkx_edge_labels(G, pos, edge_labels)
    # weight = 0.1
    # G.add_weighted_edges_from(list(('q0', n, weight) for n in G.nodes))
    # G.add_weighted_edges_from([('q0','q1',3.0),('q2','q3',7.5)])
    
    # Create positions of all nodes and save them
    pos = nx.spring_layout(G)
    # Draw the graph according to node positions
    # Create edge labels

    labels = {e: y for e,y in zip(G.edges,simbolosUsadosEnOrden)}
    # print(labels) 
    # Draw edge labels according to node positions
    colors = []
    for node in G.nodes:
        if node in estadosAceptados:
            colors.append('r')
            continue
        colors.append('b')
    #annotar en self loops 
    
    
    # pos[estadoInicial[0]] = (-1, 0.01)

    
    # Calculate the position for the label
    # Add the label using annotate
    nx.draw(G, pos,with_labels=True,node_color=colors)
    # nx.draw(G, with_labels=True, node_color=colors)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    flechaEstadoInicial = ((pos[estadoInicial[0]][0]-0.15,pos[estadoInicial[0]][1]),(pos[estadoInicial[0]][0]-0.01,pos[estadoInicial[0]][1]))
    
    plt.annotate('',xy=(flechaEstadoInicial[1]), xycoords='data',
            xytext=(flechaEstadoInicial[0]), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),)
    bandera = False
    for i in range(len(selfLoops)):
        if bandera==True:
            bandera=False
            continue
        if i+1<len(selfLoops) and selfLoops[i]==selfLoops[i+1]:
            label_pos = (pos[selfLoops[i]][0],pos[selfLoops[i]][1]+0.08)
            plt.annotate('a,b', xy=(label_pos), xytext=label_pos,)
            bandera=True
            continue
        label_pos = (pos[selfLoops[i]][0],pos[selfLoops[i]][1]+0.08)
        plt.annotate(simbolosSelfLoopsEnOrden[i], xy=(label_pos), xytext=label_pos,)

    # nx.draw(G,with_labels=True)
    plt.show()

