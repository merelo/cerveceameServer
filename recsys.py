# -*- coding: utf-8 -*-
from openpyxl import load_workbook
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

cervAux=sys.argv[1:len(sys.argv)]
cervezas=[]

for i in range(0,len(cervAux),3):
    marca=cervAux[i][6:len(cervAux[i])]
    nombre=cervAux[i+1][7:len(cervAux[i+1])]   
    cervezas.append((marca,nombre,int(cervAux[i+2][11:len(cervAux[i+2])])))
  
I_IND=1
I_MARCA=2
I_NOMBRE=3
I_TIPO=4
I_PAIS=5
I_ALC=6
I_IBU=7
I_LUP=8
I_MALTA=9
I_CEB=10
I_TRIG=11
I_MAIZ=12
I_ARROZ=13
I_PH=14
I_CO2=15
I_oALC=16
I_GLUT=17

def lectura_datos(enlace):
    return load_workbook(enlace)

def datos_procesados(datos):
    datos = datos.values
    return list(datos)


def tipo(tipo):
    rubia={"Abadia","Barley Wine","Belgian Blonde Ale",
     "Belgian Strong Ale","Berliner Weisse (Trigo)",
     "Biere de Garde","Bitter Ale","Blond Ale",
     "Dortmunder","Kolsch","Maibock","Mild Ale",
     "Munchner Hell","Lager","Pale Ale","Pale Lager",
     "Pilsen","Red Ale","Sin Alcohol","Sparkling Ale",
     "Steam beer","Steinbier","Strong Bitter","IPA",
     "Strong Lager","Weizenbier (Trigo)","Witbier (Trigo)","Patriot Ale"}
    brown={"Brown Ale","Dubbel (Tostada)","Dunkelweizen (Tostada)",
       "Marzen","Munchner Dunkel","Old Ale","Old Brown",
       "Porter (Tostada)","Quadrupel","Rauchbier",
       "Scotch Ale","Tripel","Porter","Dunkel (Negra)"}
    negra={"Altbier","Bock","Belgian Dark Ale",
       "Dark Lager (Negra)","Doppelbock","Eisbock",
       "Schwarzbier (Negra)","Stout (Negra)",
       "Weizenbock (Trigo)"}
    frutas={"Faro","Fruit Beer","Gueuze","Kriek (Fruta)",
        "Lambic (Fruta)","Radler"}
    otros={"Con tequila","Otro"}
    if(tipo in rubia):
        return 1
    elif(tipo in brown):
        return 2
    elif(tipo in negra):
        return 3
    elif(tipo in frutas):
        return 100
    elif(tipo in otros):
        return 200
    
#Cerveza incluye todos los valores de la cerveza en datos
def calcular_distancia(cerveza,ind,est,datos,gluten):
    resultados=[]
    for i in datos:
        punt=0
        pesoAlcohol=0.2
        pesoTipo=0.4
        pesoIBU=0.1
        pesoTrigo=0.25
        pesoMaiz=0.03
        pesoArroz=0.02
        pesoGluten=0
        
        iT=tipo(i[I_TIPO])
        cT=tipo(cerveza[I_TIPO])
        if(gluten>=0.8):
            pesoGluten=0.68
            pesoTipo=0.15
            pesoTrigo=0.05
            pesoAlcohol=0.05
            pesoIBU=0.05
            pesoMaiz=0.01
            pesoArroz=0.01
            
        if(cerveza[I_GLUT]!=None and i[I_GLUT]!=None):
            punt+=pesoGluten*(1-abs(cerveza[I_GLUT]-i[I_GLUT]))*100
        #Evaluar el contenido de trigo
        if(cerveza[I_TRIG]!=None and i[I_TRIG]!=None):
            punt+=pesoTrigo*(1-abs(cerveza[I_TRIG]-i[I_TRIG]))*100
        else:
            pesoIBU+=pesoTrigo/2
            pesoAlcohol+=pesoTrigo/2        
	#Evaluar IBU
        if(cerveza[I_IBU]!=None and i[I_IBU]!=None):
            punt+=pesoIBU*(100-abs(float(cerveza[I_IBU])-float(i[I_IBU])))
        else:
            pesoAlcohol+=pesoIBU/2
            pesoTipo+=pesoIBU/2
        #Evaluar tipo
        if(abs(iT-cT)<3):
	    if(iT<50):
                punt+=pesoTipo*100*(2-abs(iT-cT))/2
            else:
                punt+=pesoTipo*100
	#ALCOHOL
        if(cerveza[I_ALC]!=None and i[I_ALC]!=None):
            valor=(7-abs(float(cerveza[I_ALC])-float(i[I_ALC])))*25/7
            if(float(cerveza[I_ALC])>=8 and float(i[I_ALC])>=8):
                valor+=75
            elif(float(cerveza[I_ALC])<8 and float(i[I_ALC])<8 and float(cerveza[I_ALC])>1 and float(i[I_ALC])>1):
                valor+=75
            else:
                valor+=75
            punt+=pesoAlcohol*valor
        #maiz y arroz
        if(cerveza[I_MAIZ]!=None and i[I_MAIZ]!=None):
            punt+=pesoMaiz*(1-abs(cerveza[I_MAIZ]-i[I_MAIZ]))*100
        if(cerveza[I_ARROZ]!=None and i[I_ARROZ]!=None):
            punt+=pesoArroz*(1-abs(cerveza[I_ARROZ]-i[I_ARROZ]))*100
            
        #Añadimos a la lista
        if(est==1):
	    punt=100-punt
        elif(est==2):
	    punt=(100-punt)*4/5
	elif(est==3):
	    punt=punt*3/5
        else:
            punt=punt*(est+15)/20
        
        resultados.append((i[I_IND],punt))
    return(resultados)

def ordenar(cervezas):
    return sorted(cervezas, key=lambda x: x[1],reverse=True)

def indice_cerveza(cerveza,datos):
    for i in datos:
        if(cerveza[0]==i[2] and cerveza[1]==i[3]):
            return i[1]
        
def porcentaje_celiaco(indices,basedatos):
    ccel=0
    nocel=0
    for i in indices:
        if(basedatos[i][I_GLUT]==1):
            nocel+=1
        else:
            ccel+=1
    return ccel/(ccel+nocel)
        
def sumar_resultados(puntuaciones, cerveza):
    resultado=[]
    if(puntuaciones==None):
        resultado=cerveza
    else:
        for i in range(len(cerveza)):
            resultado.append((cerveza[i][0],puntuaciones[i][1]+cerveza[i][1]))
    return resultado

def eliminar_repetidos(cervezas,puntuaciones,basedatos):
    index=[indice_cerveza(x,basedatos) for x in cervezas]
    return [i for i in puntuaciones if i[0] not in index]

def representar_json(cervezas,puntuaciones):
    json="{"
    for i in range(len(cervezas)):
        if(i>0):
            json=json+","
        json=json+"\""+str(i)+"\":{\"marca\":\""+cervezas[i][I_MARCA]+"\",\"nombre\":\""+cervezas[i][I_NOMBRE]+"\",\"punt\":\""+str(round(puntuaciones[i]))+"\"}"
    json=json+"}"
    return json
    
#Reads products' characteristichs
basedatos=lectura_datos("cervezas.xlsx")['Sheet1']
basedatos=datos_procesados(basedatos)

puntuaciones=None

#Gets beers' indexes
indices_cerv=[]
for cerv in cervezas:
    index=indice_cerveza(cerv,basedatos)
    indices_cerv.append(index)

#Gets percentage of gluten-free beers rated    
gluten=porcentaje_celiaco(indices_cerv,basedatos)
#For each beer we compute distance between every beer rated and the whole
for i in range(len(cervezas)):
    resultado=calcular_distancia(basedatos[indices_cerv[i]],indices_cerv[i],cervezas[i][2],basedatos[1:603],gluten)
    puntuaciones=sumar_resultados(puntuaciones,resultado)

#Delete beers already rated
puntuaciones_repetidas=eliminar_repetidos(cervezas,puntuaciones,basedatos)    

#Order by punctuation
indices_ordenado=[i[0] for i in ordenar(puntuaciones_repetidas)]
indices_ordenado=indices_ordenado[0:10]
cervezas_recomendadas=[basedatos[i] for i in indices_ordenado]
puntuaciones_recomendadas=[puntuaciones[i-1][1]/len(cervezas) for i in indices_ordenado]

#We put results in a beautiful way
def normalize(v):
    v.append(0)
    return [((x-min(v))/(max(v)-min(v))*100)-((100-max(v))/2) for x in v]

puntuaciones_recomendadas=normalize(puntuaciones_recomendadas)[0:10]

print(representar_json(cervezas_recomendadas,puntuaciones_recomendadas))
