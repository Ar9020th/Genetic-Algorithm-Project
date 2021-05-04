import json
import requests
import numpy as np
from Population import *
from operator import attrgetter
import random
API_ENDPOINT = 'http://10.4.21.156'
MAX_DEG = 11
SECRET_KEY='nF62PuZy3oUMa3Z0E0m89iyqzOgTw66sTVwTCZ6i3Qy3fkZkVe'

initialweightvector=[0.0, -1.45799022e-12, -2.28980078e-13,  4.62010753e-11, -1.75214813e-10, -1.83669770e-15,  8.52944060e-16,  2.29423303e-05, -2.04721003e-06, -1.59792834e-08,  9.98214034e-10]
def urljoin(root, path=''):
    if path: root = '/'.join([root.rstrip('/'), path.rstrip('/')])
    return root

def send_request(id, vector, path):
    api = urljoin(API_ENDPOINT, path)
    vector = json.dumps(vector)
    response = requests.post(api, data={'id':id, 'vector':vector}).text
    if "reported" in response:
        print(response)
        exit()

    return response

def get_errors(id, vector):
    for i in vector: assert 0<=abs(i)<=10
    assert len(vector) == MAX_DEG

    return json.loads(send_request(id, vector, 'geterrors'))

def get_overfit_vector(id):
    return json.loads(send_request(id, [0], 'getoverfit'))

def submit(id, vector):
    """
    used to make official submission of your weight vector
    returns string "successfully submitted" if properly submitted.
    """
    for i in vector: assert 0<=abs(i)<=10
    assert len(vector) == MAX_DEG
    return send_request(id, vector, 'submit')

def createGenome(vec):
    newvec=[]
    for i in range(len(vec)):
        newvec.append(vec[i]+np.random.uniform(-vec[i]/1000,vec[i]/1000))
    return newvec

def createPopulation(initvector):
    population_size=7
    population_arr=[]
    for i in range(population_size):
        newvec=createGenome(initvector)
        x=Individual(get_errors(SECRET_KEY,newvec),newvec)
        x.calculateFitness()
        population_arr.append((x,x.getfitness()))
    
    return population_arr

def mate(v1,v2):
    child1=[]
    child2=[]
    # for i in range(len(v1)):
    #     rep=random.randint(0,100)
    #     if rep % 2 == 1:
    #         child1.append(v1[i])
    #         child2.append(v2[i])
    #     else:
    #         child1.append(v2[i])
    #         child2.append(v1[i])
    sp=random.randint(0,len(v1)-1)
    for i in range(sp+1):
        child1.append(v2[i])
        child2.append(v1[i])
    for i in range(sp+1,len(v1)):
        child1.append(v1[i])
        child2.append(v2[i])
    crosschilds=[child1,child2]
    for c in [child1,child2]:
        performmutation(c)
    return child1,child2,crosschilds

def crossover(childrenarr):
    nextgeneration=[]
    s1=random.randint(0,3)
    s2=s1
    while s1==s2:
        s2=random.randint(0,3)
    c1,c2,cc1=mate(childrenarr[s1],childrenarr[s2])
    nextgeneration.append(c1)
    nextgeneration.append(c2)
    arr=[i for i in range(4)]
    arr.remove(s1)
    arr.remove(s2)
    c1,c2,cc2=mate(childrenarr[arr[0]],childrenarr[arr[1]])
    nextgeneration.append(c1)
    nextgeneration.append(c2)
    ccs=[]
    ccs.append(cc1[0])
    ccs.append(cc1[1])
    ccs.append(cc2[0])
    ccs.append(cc2[1])
    return nextgeneration,ccs

def performmutation(nextgen):
    for i in range(len(nextgen)):
        probablity=random.randint(0,100)
        if probablity>=80:
            nextgen[i]+=random.uniform(-nextgen[i]/100000,nextgen[i]/100000)
    
    return nextgen

if __name__ == "__main__":
    file1 = open("generation_37.txt", "a")
    gencount=1
    file1.write(f'Generation(iteration) {gencount}\n\nInitial Population\n')
    try: 
        with open('generations.txt') as f:
            population_arr = json.load(f)
        for i in range(len(population_arr)):
            file1.write('[')
            for j in range(len(population_arr[i])-1):
                file1.write(f'{population_arr[i][j]}, ')
            file1.write(f'{population_arr[i][len(population_arr[i])-1]}]\n')
        # print(population_arr)
        poparr=[]
        for i in range(len(population_arr)):
            x=Individual(get_errors(SECRET_KEY,population_arr[i]),population_arr[i])
            x.calculateFitness()
            poparr.append((x,x.getfitness()))
        population_arr=poparr
    except:
        # print("awdawd")
        population_arr=createPopulation(initialweightvector)
    
    population_arr.sort(key=lambda x:x[1],reverse=True)
    for i in range(len(population_arr)):
        print(population_arr[i][0].geterrors())
    # childrenarr=[]
    # for i in range(4):
    #     childrenarr.append(population_arr[i].getweightvector())
    
    # next_generation=crossover(childrenarr)
    # next_generation=performmutation(next_generation)
    
    for i in range(9):
        childrenarr=[]
        for i in range(4):
            childrenarr.append(population_arr[i][0].getweightvector())
        
        population_arr1=[]
        for i in range(3):
            population_arr1.append(population_arr[i])
        file1.write('After Selection\n')
        for i in range(len(childrenarr)):
            file1.write('[')
            for j in range(len(childrenarr[i])-1):
                file1.write(f'{childrenarr[i][j]}, ')
            file1.write(f'{childrenarr[i][len(childrenarr[i])-1]}]\n')
        for i in range(len(population_arr1)):
            wv=population_arr1[i][0].getweightvector()
            file1.write('[')
            for j in range(len(wv)-1):
                file1.write(f'{wv[j]}, ')
            file1.write(f'{wv[len(wv)-1]}]\n')
        file1.write('After Crossover\n')
        next_generation,ccs=crossover(childrenarr)
        for i in range(len(ccs)):
            file1.write('[')
            for j in range(len(ccs[i])-1):
                file1.write(f'{ccs[i][j]}, ')
            file1.write(f'{ccs[i][len(ccs[i])-1]}]\n')
        for i in range(len(population_arr1)):
                wv=population_arr1[i][0].getweightvector()
                file1.write('[')
                for j in range(len(wv)-1):
                    file1.write(f'{wv[j]}, ')
                file1.write(f'{wv[len(wv)-1]}]\n')
        file1.write('After Mutation')
        for i in range(len(next_generation)):
            file1.write('[')
            for j in range(len(next_generation[i])-1):
                file1.write(f'{next_generation[i][j]}, ')
            file1.write(f'{next_generation[i][len(next_generation[i])-1]}]\n')
        for i in range(len(population_arr1)):
            wv=population_arr1[i][0].getweightvector()
            file1.write('[')
            for j in range(len(wv)-1):
                file1.write(f'{wv[j]}, ')
            file1.write(f'{wv[len(wv)-1]}]\n')
        # next_generation=performmutation(next_generation)
        file1.write('...................\n')
        gencount+=1
        file1.write(f'Generation(iteration) {gencount}\n\nInitial Population\n')
        for i in range(len(next_generation)):
            file1.write('[')
            for j in range(len(next_generation[i])-1):
                file1.write(f'{next_generation[i][j]}, ')
            file1.write(f'{next_generation[i][len(next_generation[i])-1]}]\n')
        for i in range(len(population_arr1)):
            wv=population_arr1[i][0].getweightvector()
            file1.write('[')
            for j in range(len(wv)-1):
                file1.write(f'{wv[j]}, ')
            file1.write(f'{wv[len(wv)-1]}]\n')
        population_arr=[]
        for i in range(len(next_generation)):
            x=Individual(get_errors(SECRET_KEY,next_generation[i]),next_generation[i])
            x.calculateFitness()
            population_arr.append((x,x.getfitness()))
        for p in population_arr1:
            population_arr.append(p)
        population_arr.sort(key=lambda x:x[1],reverse=True)
        for i in range(len(population_arr)):
            print(population_arr[i][0].geterrors())

    submit(SECRET_KEY,population_arr[0][0].getweightvector())
    poparr=[]
    for i in range(len(population_arr)):
        poparr.append(population_arr[i][0].getweightvector())
    with open ( 'generations.txt' , 'w' ) as dodo:
        json.dump(poparr,dodo)
