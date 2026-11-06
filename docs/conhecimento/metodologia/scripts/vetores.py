import math
N=lambda x:0.5*(1+math.erf(x/math.sqrt(2)))
n=lambda x:math.exp(-0.5*x*x)/math.sqrt(2*math.pi)

def gbs(cp,S,K,T,r,b,sig):
    # generalized BS: b = cost of carry (b=r-q BSM-Merton, b=0 Black-76, b=rd-rf GK)
    d1=(math.log(S/K)+(b+0.5*sig*sig)*T)/(sig*math.sqrt(T)); d2=d1-sig*math.sqrt(T)
    e1=math.exp((b-r)*T); e2=math.exp(-r*T)
    if cp=='c':
        p=S*e1*N(d1)-K*e2*N(d2); delta=e1*N(d1)
        theta=-S*e1*n(d1)*sig/(2*math.sqrt(T))-(b-r)*S*e1*N(d1)-r*K*e2*N(d2)
        rho=T*K*e2*N(d2)
    else:
        p=K*e2*N(-d2)-S*e1*N(-d1); delta=-e1*N(-d1)
        theta=-S*e1*n(d1)*sig/(2*math.sqrt(T))+(b-r)*S*e1*N(-d1)+r*K*e2*N(-d2)
        rho=-T*K*e2*N(-d2)
    gamma=e1*n(d1)/(S*sig*math.sqrt(T)); vega=S*e1*n(d1)*math.sqrt(T)
    return dict(preco=p,delta=delta,gamma=gamma,vega=vega,theta=theta,rho=rho,d1=d1,d2=d2)

def iv_newton(cp,P,S,K,T,r,b,s0=0.3):
    s=s0
    for i in range(50):
        g=gbs(cp,S,K,T,r,b,s); diff=g['preco']-P
        if abs(diff)<1e-12: return s,i
        s-=diff/g['vega']
        s=max(s,1e-4)
    return s,50
def iv_brent_bisect(cp,P,S,K,T,r,b,lo=1e-4,hi=5.0):
    f=lambda s:gbs(cp,S,K,T,r,b,s)['preco']-P
    a,bb=lo,hi
    for i in range(200):
        m=0.5*(a+bb)
        if f(a)*f(m)<=0: bb=m
        else: a=m
        if bb-a<1e-12: break
    return 0.5*(a+bb)

print("== BSM acao (sem dividendo, convencao B3) ==")
S,K,DU,DI,sig=30.0,32.0,21,0.1065,0.35
T=DU/252; r=math.log(1+DI)
for cp in 'cp':
    g=gbs(cp,S,K,T,r,r,sig)
    print(cp,{k:round(v,6) for k,v in g.items()})
    print('  escalas: vega/1pp',round(g['vega']/100,6),'theta/DU',round(g['theta']/252,6),'theta/DC',round(g['theta']/365,6),'rho/1pp',round(g['rho']/100,6),
          'gamma1%',round(g['gamma']*S*0.01,6),'cashgamma(S^2*0.01)',round(g['gamma']*S*S*0.01,6),'pnl1%',round(0.5*g['gamma']*(0.01*S)**2,6))
    P=g['preco']; print('  IV newton',iv_newton(cp,P,S,K,T,r,r),'bissecao',round(iv_brent_bisect(cp,P,S,K,T,r,r),10))
c=gbs('c',S,K,T,r,r,sig)['preco']; p=gbs('p',S,K,T,r,r,sig)['preco']
print(' paridade C-P =',round(c-p,8),' S-K e^-rT =',round(S-K*math.exp(-r*T),8))

print("== BSM com dividendo discreto (escrowed) e strike protegido ==")
D=1.0; DUex=10; tex=DUex/252
Sstar=S-D*math.exp(-r*tex)
c_prot=gbs('c',Sstar,K-D,T,r,r,sig)['preco']
c_nodiv=gbs('c',S,K,T,r,r,sig)['preco']
c_unprot=gbs('c',Sstar,K,T,r,r,sig)['preco']
print(' protegida (S*-escrow, K-D):',round(c_prot,6),' B3 BS sem div (S,K):',round(c_nodiv,6),' nao protegida (S*,K):',round(c_unprot,6))
print(' diferenca forward residual D(e^{r(T-tex)}-1)=',round(D*(math.exp(r*(T-tex))-1),6))

print("== Black-76 (IND futuro) ==")
F,K2,DU2,sig2=130000.0,132000.0,15,0.20
T2=DU2/252
for cp in 'cp':
    g=gbs(cp,F,K2,T2,r,0.0,sig2); print(cp,{k:round(v,6) for k,v in g.items()})
    print('  GEX por contrato (mult 1, x F^2 x 0.01):',round(g['gamma']*1*F*F*0.01,4))

print("== Garman-Kohlhagen (dolar a vista, convencao B3) ==")
S3,K3,DU3,DC3,sig3,cupom=5.40,5.50,20,28,0.14,0.05
T3=DU3/252; rd=math.log(1+DI); q=(252/DU3)*math.log(1+cupom*DC3/360)
for cp in 'cp':
    g=gbs(cp,S3,K3,T3,rd,rd-q,sig3); print(cp,{k:round(v,6) for k,v in g.items()})
F3=S3*math.exp((rd-q)*T3); print(' forward implicito F=S e^{(r-q)T} =',round(F3,6))
gb=gbs('c',F3,K3,T3,rd,0.0,sig3)['preco']; print(' Black-76 com F:',round(gb,8),' (igual ao GK call)')

print("== BGT move: sqrt(2|Theta_dia|/Gamma) vs S*sigma/sqrt(252) com r=q=0 ==")
g=gbs('c',100.0,100.0,30/252,0.0,0.0,0.30)
th=g['theta']/252; print(' BGT=',round(math.sqrt(2*abs(th)/g['gamma']),6),' S*sig/sqrt252=',round(100*0.30/math.sqrt(252),6))
g=gbs('c',100.0,100.0,30/252,r,r,0.30)
th=g['theta']/252; print(' com r=ln(1.1065): BGT=',round(math.sqrt(2*abs(th)/g['gamma']),6))

print("== Max Pain (2 metodos) ==")
calls={28:1000,30:5000,32:8000,34:3000}
puts={26:2000,28:6000,30:4000,32:1000}
strikes=sorted(set(calls)|set(puts))
def dor(X): return sum(oi*max(X-k,0) for k,oi in calls.items())+sum(oi*max(k-X,0) for k,oi in puts.items())
def itm(X): return sum(oi for k,oi in calls.items() if X>k)+sum(oi for k,oi in puts.items() if X<k)
for X in strikes: print(' X',X,'dor R$',dor(X),'contratos ITM',itm(X))
print(' MaxPain A =',min(strikes,key=dor),' MaxPain B =',min(strikes,key=itm))
# condicao de 1a ordem
for X in strikes:
    dl=sum(oi for k,oi in calls.items() if k<X)-sum(oi for k,oi in puts.items() if k>=X)
    dr=sum(oi for k,oi in calls.items() if k<=X)-sum(oi for k,oi in puts.items() if k>X)
    print('  X',X,'derivada esq',dl,'dir',dr)

print("== Estruturas x CDI ==")
DUe=21; cdi=0.1065
fator_cdi=(1+cdi)**(DUe/252)-1
S,Ka,Pask,Cbid=30.0,30.0,1.20,1.65
custo=S+Pask-Cbid; rp=Ka/custo-1
aa=(1+rp)**(252/DUe)-1
dcdi=(1+cdi)**(1/252)-1
pct_cetip=((1+rp)**(1/DUe)-1)/dcdi
print(' box3: custo',round(custo,4),'r_periodo',round(rp,6),'a.a.',round(aa,6),'%CDI razao',round(rp/fator_cdi,4),'%CDI diario',round(pct_cetip,4))
print("== escrowed com sigma ajustado ==")
S,K,sig=30.0,32.0,0.35; T=21/252
sadj=sig*S/Sstar
print(' sigma_adj',round(sadj,6),' protegida c/ sigma_adj:',round(gbs('c',Sstar,K-D,T,r,r,sadj)['preco'],6),' B3 sem div:',round(gbs('c',S,K,T,r,r,sig)['preco'],6))
# IV implicita do preco protegido no modelo B3
Pp=gbs('c',Sstar,K-D,T,r,r,sig)['preco']
print(' IV no modelo B3 do preco protegido(sigma 35%):',round(iv_newton('c',Pp,S,K,T,r,r)[0],6))
