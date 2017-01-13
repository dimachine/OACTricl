import MySQLdb, time, random
from pickle import *

#вычисление плотности
def TDensity(Gi,Mi,Wi,I):
    nominator=0.0
    denominator=0.0
    for g in Gi:
        str_g=str(g)
        for m in Mi:
            str_m=str(m)
            for w in Wi:
                key=str_g+str_m+str(w)
                if key in I:
                    #print key
                    nominator=nominator+1
                    #print nominator
    denominator=len(Gi)*len(Mi)*len(Wi)
    #print len(I)
    return nominator/denominator

#вычисление плотности с размерами трикластера
def TSizeDensity(Gi,Mi,Wi,I):
    nominator=0.0
    denominator=0.0
    for g in Gi:
        str_g=str(g)
        for m in Mi:
            str_m=str(m)
            for w in Wi:
                key=str_g+str_m+str(w)
                if key in I:
                    #print key
                    nominator=nominator+1
                    #print nominator
    sizeGi=len(Gi)
    sizeMi=len(Mi)
    sizeWi=len(Wi)
    denominator=sizeGi*sizeMi*sizeWi
    #print len(I)
    return sizeGi,sizeMi, sizeWi, denominator, nominator/denominator



def TProbDensity(gmb,S,I):
    denominator=gmb
    nominator=0.0
    #print S
    for key in S.keys():
        #print key
        if key in I:
            #print key
            nominator=nominator+1
            #print nominator
    print nominator, denominator
    return nominator/denominator


#сохранение
def TSave(Triclusters, filename):
    f=file(filename,'w')
    f.write(str(len(Triclusters))+'\n')
    for key in Triclusters.keys():
        #print key
        f.write(str(Triclusters[key]))
        f.write('\n')
        
    f.close()
    

def MySQLConn(num_rows):
    # цепляемся
    conn = MySQLdb.connect(host="localhost",
		       user = "root",
		       passwd = "test",
		       db = "bibsonomy")
    #cursor object
    cursor = conn.cursor ()

    #umrows = int(cursor.rowcount)

    cursor.execute("SELECT user_id, tag_name, content_id from tas limit 0, "+str(num_rows))
    #cursor.execute("SELECT user_id, tag_name, content_id from tas")
    rows=cursor.fetchall ()
    print "Your data has been loaded into the memory...", len(rows)
    cursor.close ()
    conn.close ()
    return rows

def DataPowerContext():
    rows=[                    ['u1','t2','r1'],['u1','t3','r1'],
         ['u2','t1','r1'],['u2','t2','r1'],['u2','t3','r1'],
         ['u3','t1','r1'],['u3','t2','r1'],['u3','t3','r1'],
         ['u1','t1','r2'],['u1','t2','r2'],['u1','t3','r2'],
         ['u2','t1','r2'],                 ['u2','t3','r2'],
         ['u3','t1','r2'],['u3','t2','r2'],['u3','t3','r2'],
         ['u1','t1','r3'],['u1','t2','r3'],['u1','t3','r3'],
         ['u2','t1','r3'],['u2','t2','r3'],['u2','t3','r3'],
         ['u3','t1','r3'],['u3','t2','r3']                 ]
    return rows

def FirstPrimes(rows): 
#первые штрихи -- словари
    g_prime={}
    m_prime={}
    w_prime={}
    g_cnt={}
    m_cnt={}
    w_cnt={}
    I={}
#вычиляем первые штрихи для g не как пары (m,w), а как словари M_g и M_w
    for [g,m,w] in rows:
        if g not in g_prime:
            g_prime[g]=({},{})
            g_cnt[g]=0.0
        if m not in g_prime[g][0]:
            g_prime[g][0][m]=1
        if w not in g_prime[g][1]:
            g_prime[g][1][w]=1
        if m not in m_prime:
            m_prime[m]=({},{})
            m_cnt[m]=0.0
        if g not in m_prime[m][0]:   
            m_prime[m][0][g]=1
        if w not in m_prime[m][1]:        
            m_prime[m][1][w]=1
        if w not in w_prime:
            w_prime[w]=({},{})
            w_cnt[w]=0.0
        if g not in w_prime[w][0]:
            w_prime[w][0][g]=1
        if m not in w_prime[w][1]:
            w_prime[w][1][m]=1
        # считаем количество пар     
        g_cnt[g]=g_cnt[g]+1
        m_cnt[m]=m_cnt[m]+1
        w_cnt[w]=w_cnt[w]+1
    #формируем словарь c ключами 'gimiwi'
        I[str(g)+str(m)+str(w)]=(g,m,w)
          
       # print g, g_prime
       # print m, m_prime
       # print w, w_prime

    print '|G|=',len(g_cnt.keys()),'|M|=',len(m_cnt.keys()), '|B|=',len(w_cnt.keys()), len(g_cnt.keys())*len(m_cnt.keys())*len(w_cnt.keys())
    
    
    
    print "First primes have been calculated..."
    return g_prime, m_prime, w_prime, I


def TriclMain(rows, g_prime, m_prime, w_prime, time_start):  
#трикластеры хранятся в словаре   
    T={}
    cnt=0
    for [g,m,w] in rows:
        cnt=cnt+1
        #print g, g_prime
        #print m, m_prime
        #print w, w_prime
        g_primeprime=[]
        m_primeprime=[]
        w_primeprime=[]
   
        m_primeprime.extend(g_prime[g][0].keys())
        w_primeprime.extend(g_prime[g][1].keys())
    
    
        g_primeprime.extend(m_prime[m][0].keys())
        w_primeprime.extend(m_prime[m][1].keys())
  
        g_primeprime.extend(w_prime[w][0].keys())
        m_primeprime.extend(w_prime[w][1].keys())

        g_primeprime=sorted(list(set(g_primeprime)))
        m_primeprime=sorted(list(set(m_primeprime)))
        w_primeprime=sorted(list(set(w_primeprime)))

        hash_str=''
        for g1 in g_primeprime:
            hash_str=hash_str+str(g1)
        for m1 in m_primeprime:
            hash_str=hash_str+str(m1)
        for w1 in w_primeprime:
            hash_str=hash_str+str(w1)
        hash_str=hash(hash_str)        
            
        T[hash_str]=[(g_primeprime, m_primeprime, w_primeprime), 0,0,0,0,0]
        if cnt%5000==0:
            print cnt, "'th triple has been processed"
            print "time elapsed in sec:", time.clock()-time_start

    print "Calculating of triclusters is finished...Time elapsed in sec:", time.clock()-time_start
    print "Count of triclusters is ", len(T)
    
    return T

def ExhaustiveDensityCalc(I,T, time_start):
    print "Exchaustive density calculation is started"
    print "time elapsed in sec:", time.clock()-time_start
    cnt=0
    for t_key in T:
        T[t_key][1:]=TSizeDensity(T[t_key][0][0],T[t_key][0][1],T[t_key][0][2],I)
        cnt=cnt+1
        if cnt%50==0:
            print cnt, "'th triple has been processed"
            print "time elapsed in sec:", time.clock()-time_start
    return T

def ProbabDensityCalc(I,T,alpha, time_start):
    # Выбираем случайные фрагменты трикластеров
    print "Random density calculation is started"
    print "time elapsed in sec:", time.clock()-time_start

    S={}
    gmb={}
    for key in T.keys():
        sGi=len(T[key][0][0])
        sMi=len(T[key][0][1])
        sBi=len(T[key][0][2])
        gmb[key]=sGi*sMi*sBi
        print key
        print gmb[key]
        gmb[key]=int(round(gmb[key]*alpha))
        print gmb[key]
        S[key]={}
        for i in range(gmb[key]):
            g=random.choice(T[key][0][0])
            m=random.choice(T[key][0][1])
            b=random.choice(T[key][0][2])
            S[key][str(g)+str(m)+str(b)]=(g,m,b)
            #print S[key]
    print "S=",S

    cnt=0
    for t_key in T:
        T[t_key][1:]=sGi, sMi, sBi, gmb, TProbDensity(gmb[t_key],S[t_key],I)
        cnt=cnt+1
        if cnt%50==0:
            print cnt, "'th triple has been processed"
    #print "time elapsed in sec:", time.clock()-time_start
    return S

def TriclExchaust(rows, time_start):
    g_prime, m_prime, b_prime, I= FirstPrimes(rows)
    T=TriclMain(rows, g_prime, m_prime, b_prime, time_start)
    ExhaustiveDensityCalc(I,T, time_start)
    return T

def TriclProbab(rows,alpha, time_start):
    g_prime, m_prime, b_prime, I= FirstPrimes(rows)
    T=TriclMain(rows, g_prime, m_prime, b_prime, time_start)
    ProbabDensityCalc(I,T,alpha, time_start)
    return T


def Experiment1():
    time_start=time.clock()    
    I=MySQLConn(10000)
    T=TriclExchaust(I,time_start)
    print "time elapsed in sec:", time.clock()-time_start
    TSave(T,'NEWtriclusters_e_10000.txt') 
    return T

def Experiment2():
    time_start=time.clock()    
    I=MySQLConn(10000)
    T=TriclProbab(I,0.1,time_start)
    print "time elapsed in sec:", time.clock()-time_start
    TSave(T,'NEWtriclusters_p_10000.txt') 
    return T

def Experiment3():
    time_start=time.clock()    
    I=MySQLConn(10000)
    T=TriclProbab(I,0.1,time_start)
    print "time elapsed in sec:", time.clock()-time_start
    dump(T,file('NEWtriclusters_p_200k.txt','w')) 
    return T

#Experiment2()

 
Experiment1()

#Experiment1()
   

