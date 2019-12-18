# -*- coding: utf-8 -*-
"""
@author: Aleksandr Pilipenko
"""
import pylab
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize
import matplotlib.pyplot as plt

#Ввод начальных значений
# 0 - тригл \\ 1 - диглиц \\ 2- моноглиц \\ 3 - эфир \\ 4 -спирт \\ 5 - глицерин \\ 6 - катализатор  \\ 7 - вода  \\ 8 -  ffa \\ 9 - мыло
c0=[0.05,         0,           0,           0,          0.9177,          0,         0.0243,                 1,        0,           0] # мольные доли
#Константы скорости
k0=np.array([0.1,0.1    ,0.1,0.1,    0.1,0.1,      0.1,0.1,0.1,     0.1,0.1,0.1])
#Время протекания реакции
t=0,72,144,210,282,378,486,618,756   #t = np.linspace(0, 800, 320)   #sec и количество итераций
#эксперементальные значения #'MS-V 30 °C'
plt.title('Микрореактор MS-V при 30 °C')
wTexp=np.array([1,0.511,0.426,0.399,0.265,0.225,0.142,0,0.002])
wEexp=np.array([0,0.4,0.488,0.521,0.649,0.686,0.768,0.935,0.908])
wSBexp=np.array([0,0.088,0.086,0.08,0.085,0.089,0.089,0.065,0.09])

#Решение системы ДУ
def f(c,t,k):
    r1=k[0]*c[0]*c[4]*c[6]    # k(1)*T*EtOH*EtO          r(1) переэтерификация - прямая 1
    r2=k[1]*c[1]*c[3]*c[6]    # k(-1)*Di*E*EtO           r(-1)  переэтерификация - прямая 2
    r3=k[2]*c[1]*c[4]*c[6]    # k(2)*Di*EtOH*EtO         r(2)  переэтерификация - прямая 3
    r4=k[3]*c[2]*c[3]*c[6]    # k(-2)*Mo*E*EtO          r(-2)  переэтерификация - обратная 1
    r5=k[4]*c[2]*c[4]*c[6]    # k(3)*Mo*EtOH*EtO         r(3)  переэтерификация - обратная 2
    r6=k[5]*c[5]*c[3]*c[6]    # k(-3)*G*E*EtO            r(-3)  переэтерификация - обратная 3
    
    r7=k[6]*c[0]*c[7]*c[6]    # k[4] * C_trig * C_water*C_koh   прямая реакция гидрозила 1
    r8=k[7]*c[1]*c[7]*c[6]    # k[5] * C_digl * C_water*C_koh    прямая реакция гидрозила 2
    r9=k[8]*c[2]*c[7]*c[6]    # k[6] * C_monog * C_water*C_koh   прямая реакция гидрозила 3
    
    r10 = k[9]*c[7]*c[8]*c[6]  #C_koh * C_water * C_ffa --> h20 * soap побочная реакция мыло
    r11 = k[10]*c[0]*c[6]  #* C_trig * C_koh --- > G * SOAP побочная реакция мыло 2
    r12 = k[11]*c[3]*c[7]*c[6]  #* C_efir * C_water --- > ffa + eth побочная реакция гидроиз эфира ?????
    
    # диффиренциальные уравнения (мольные доли) - должны совпадать с массивом c0 по "названию" элементов
    diff0=-r1+r2  -r7  -r11                                      #триглицериды
    diff1=r1-r2-r3+r4  +r7-r8                              #диглицер
    diff2=r3-r4-r5+r6  +r8-r9                              #моноглиц
    diff3=r1-r2+r3-r4+r5-r6  - r12                                #эфир
    diff4=-r1+r2-r3+r4-r5+r6  +r9  +r12                          #спирт
    diff5=r5-r6 +r11                                            #глицерин
    diff6=-r1+r1-r2+r2-r3+r3-r4+r4-r5+r5-r6+r6+r7-r7+r8-r8+r9-r9-r10-r11-r12+r12             #катализатор
    diff7 = -r7 - r8  -r9   -r10 +r10 - r12                                   # вода
    diff8 = r7 + r8 + r9  -r10+r12                                   # FFA (свободные жирные кислоты)
    diff9 = r10+r11                                              # мыло
    diff=[diff0,diff1,diff2,diff3,diff4,diff5,diff6, diff7, diff8, diff9]
    return diff 

#Функция сравнения эксперементальных и расчетных значений
def cost_function(k):
   ode_res=odeint(f,c0,t,(k,))# результатом будет массив мольных долей
   
   wSum = ode_res[:,0] + ode_res[:,1] + ode_res[:,2]+ ode_res[:,3] # сумма элементов для того, чтобы потом разделить на неё для сохранения пропорции с экспериментальными данными

   diffmat0=abs((((ode_res[:,0]/wSum)-wTexp))**2)
   diffmat1=abs((((ode_res[:,3]/wSum)-wEexp))**2)
   diffmat2=abs((((ode_res[:,1]/wSum+ode_res[:,2]/wSum)-wSBexp))**2)
   diffmat=diffmat0,diffmat1,diffmat2
   FQS=np.sum(diffmat) # разница между экспериментальными и расчетными значениями
   return FQS

#Method L-BFGS-B работает с ограничениями
bnds = ([0, None], [0, None],[0, None], [0, None],[0, None], [0, None],       [0, None], [0, None], [0, None],       [0, None], [0, None], [0, None])
optimized=minimize(cost_function, k0,bounds=bnds,method='L-BFGS-B',options={'maxiter':1000,'gtol': 1e-6, 'eps':1e-6,'disp': True  }) 
k0=optimized.x#Присвоение новые значений вектору к

#Пересчет оптимизированных значений  и построение графиков функции
ode_g=odeint(f,c0,t,(k0,))# результатом будет массив мольных долей

# для среднеквадратичного отклонения
wSum = ode_g[:,0] + ode_g[:,1] + ode_g[:,2]+ ode_g[:,3]# сумма элементов для того, чтобы потом разделить на неё для сохранения пропорции с экспериментальными данными

T=((((ode_g[:,0]/wSum)-abs(wTexp)))**2)  # ode_g[:,0] - мольные доли триглицеридов
E=((((ode_g[:,3]/wSum)-abs(wEexp)))**2)  # ode_g[:,3] - мольные доли эфиров
SB=(((((ode_g[:,1]+ode_g[:,2])/wSum)-abs(wSBexp)))**2)  # ode_g[:,1 2] - мольные доли побочных продуктов
SSR=sum(T+E+SB)
print('Сумма среднеквадратичных отклонений:','\n Ssr=',SSR)

#Построение кинетических кривых для исходной системы ду
pylab.figure (1)
plt.xlabel('Время реакции [с]')
plt.ylabel('Массовые доли [-]')

pylab.plot(t, wTexp, "go", label="T")
pylab.plot(t, wEexp, "ro", label="E")
pylab.plot(t, wSBexp, "bo", label="SB")
pylab.plot(t, ode_g[:,0]/wSum, "g-", label="T")
pylab.plot(t, ode_g[:,3]/wSum, "r-", label="E")
pylab.plot(t, ((ode_g[:,1]+ode_g[:,2])/wSum), "b-", label="SB")

pylab.legend ( ("Масло", "Эфир", "Побочный \n продукт"))
pylab.ylim((0,1))
pylab.xlim((0,800))
pylab.grid(True)
pylab.show()

print("k =",k0)