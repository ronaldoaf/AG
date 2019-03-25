# -*- coding: cp1252 -*-
from math import exp, log
from random import random

#Funções de conversão
def intListToBinString(lista):
    n_digitos=str(len(bin(max(lista)))-2)
    formato='{0:0'+n_digitos+'b}'
    saida='';
    for item in lista: saida+=formato.format(item)
    return saida

def binStringToIntList(string,tamanho):   #tamanho do cromossomo
    n_partes=len(string)/tamanho
    return [int(string[i*tamanho:(i+1)*tamanho],2)  for i in range(n_partes)]

def floatToInt(valor,minimo,maximo,n_partes):
    intervalo=(1.0*maximo-minimo)/n_partes
    return int((valor-1.0*minimo)/intervalo)

def intToFloat(valor,minimo,maximo,n_partes):
    intervalo=(1.0*maximo-minimo)/n_partes
    return float(1.0*minimo+valor*intervalo)

class indviduo:
    def __init__(self,codigo_genetico,funcao_aptidao):
        self.codigo_genetico=codigo_genetico
        self.aptidao=funcao_aptidao(codigo_genetico)
        
    def __cmp__(self, other):
        if self.aptidao < other.aptidao: return -1
        elif self.aptidao > other.aptidao:return 1
        else: return 0

        
class populacao:    
    def __init__(self, funcao_aptidao,numero_de_cromossomos,numero_genes_por_cromossomo, tamanho_inicial=30,tamanho=30,taxa_de_mutacao=0.01,taxa_de_reproducao=0.95,metodo_de_selecao=0,elementos_por_vez=1):
        def codigo_genetico_random(numero_de_genes):
            saida=''
            for i in range(numero_de_genes): saida+=str(int(round(random(),0)))
            return saida
        
        self.funcao_aptidao=funcao_aptidao
        self.numero_de_cromossomos=numero_de_cromossomos
        self.tamanho=tamanho_inicial
        self.tamanho=tamanho
        self.numero_genes_por_cromossomo=numero_genes_por_cromossomo
        self.taxa_de_mutacao=taxa_de_mutacao
        self.taxa_de_reproducao=taxa_de_reproducao
        self.metodo_de_selecao=metodo_de_selecao
        self.elementos_por_vez=elementos_por_vez
        self.indiv=[indviduo(codigo_genetico_random(numero_de_cromossomos*numero_genes_por_cromossomo), self.funcao_aptidao if self.elementos_por_vez==1 else  self.funcao_none)  for i in range(tamanho_inicial)]

        self.selecao()

    def funcao_none(self,codigo): return None

    def selecao(self):
        #print ("### COMECOU SELECAO ###")
        if self.elementos_por_vez>1:
            self.varios_elementos_por_vez()
            
           
        #Dizimação
        if self.metodo_de_selecao==0:
            self.indiv=sorted(self.indiv,reverse=True)
            self.indiv=self.indiv[:self.tamanho]

        #Roleta
        elif self.metodo_de_selecao==1:
            def roulette_select(population, fitnesses, num):
                """ Roulette selection, implemented according to:
                    <http://stackoverflow.com/questions/177271/roulette
                    -selection-in-genetic-algorithms/177278#177278>
                """
                total_fitness = float(sum(fitnesses))
                rel_fitness = [f/total_fitness for f in fitnesses]
                # Generate probability intervals for each individual
                probs = [sum(rel_fitness[:i+1]) for i in range(len(rel_fitness))]
                # Draw new population
                new_population = []
                for n in xrange(num):
                    r = random()
                    for (i, individual) in enumerate(population):
                        if r <= probs[i]:
                            new_population.append(individual)
                            break
                return new_population

            
            populacao_atual=sorted(self.indiv,reverse=True)
            lst_aptidoes=[e.aptidao for e in populacao_atual]            
            if min(lst_aptidoes)<0:lst_aptidoes=[e.aptidao-min(lst_aptidoes) for e in populacao_atual]
            self.indiv=roulette_select(populacao_atual, lst_aptidoes, self.tamanho)


        #Torneio
        elif self.metodo_de_selecao==2:
            pop_atual=sorted(self.indiv, key=lambda x: random())
            self.indiv=[max([pop_atual[i],pop_atual[i+len(pop_atual)/2]]) for i in range(len(pop_atual)/2) ]

        self.indiv=sorted(self.indiv,reverse=True)
        #print ("### ACABOU SELECAO ###")

        
    def mutacao(self,codigo_genetico):
        codigo_genetico_alterado=''
        for bit in codigo_genetico:
            codigo_genetico_alterado+=bit if random()>self.taxa_de_mutacao else str(int(not(int(bit))))

        return codigo_genetico_alterado
        
    def varios_elementos_por_vez(self):
        def divide_lista(lista, n):
            return [lista[i*n:(i+1)*n] for i in range(len(lista)/n + (1 if len(lista) % n > 0 else 0) )]


        if self.elementos_por_vez>1:
            lista_indiv_com_indice=[ {'indice': i, 'indiv':self.indiv[i]} for i in range(len(self.indiv))]
            for sub_lista in divide_lista([e_indiv for e_indiv in lista_indiv_com_indice if e_indiv['indiv'].aptidao is None], self.elementos_por_vez):
                lista_de_fitness=self.funcao_aptidao([indiv['indiv'].codigo_genetico for indiv in sub_lista])
                lista_indices=[indiv['indice'] for indiv in sub_lista]
                for i in range(len(sub_lista)):
                    self.indiv[ lista_indices[i] ].aptidao=lista_de_fitness[i]


    def cruzamento(self):
        #print ("### INICIO CRUAZAMENTO ###")
        #Embalhara populacao
        self.indiv=sorted(self.indiv,key=lambda x: random() )
        
        for j in range(self.tamanho/2):            
            pai=self.indiv[j].codigo_genetico
            mae=self.indiv[j+self.tamanho/2].codigo_genetico
            
            n=self.numero_de_cromossomos*self.numero_genes_por_cromossomo
            
            corte=1+sorted(range(n-1),key=lambda x: random())[0]

            if random()<self.taxa_de_reproducao:
                codigo_filho1=pai[:corte]+mae[corte:corte+(n/2)]+pai[corte+(n/2):]
                codigo_filho2=mae[:corte]+pai[corte:corte+(n/2)]+mae[corte+(n/2):]   
            else:
                codigo_filho1=pai
                codigo_filho2=mae

            #Mutacao
            for codigo in [codigo_filho1,codigo_filho2]:
                self.indiv+=[indviduo(self.mutacao(codigo), self.funcao_aptidao if self.elementos_por_vez==1 else  self.funcao_none)]
        #print ("### FIM CRUAZAMENTO ###")
            


    def evolucao(self,numero_de_geracoes=1):
        for i in range(numero_de_geracoes):
            
            self.cruzamento()
            self.selecao()






