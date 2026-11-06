import math
N=lambda x:0.5*(1+math.erf(x/math.sqrt(2))); n=lambda x:math.exp(-0.5*x*x)/math.sqrt(2*math.pi)
def price(cp,S,K,T,r,b,s):
    d1=(math.log(S/K)+(b+0.5*s*s)*T)/(s*math.sqrt(T)); d2=d1-s*math.sqrt(T)
    eb=math.exp((b-r)*T); er=math.exp(-r*T)
    return S*eb*N(d1)-K*er*N(d2) if cp=='c' else K*er*N(-d2)-S*eb*N(-d1)
def delta(cp,S,K,T,r,b,s,h=1e-4): return (price(cp,S+h,K,T,r,b,s)-price(cp,S-h,K,T,r,b,s))/(2*h)
S,K,T,r,b,s=30,32,21/252,0.101203,0.07,0.35
d1=(math.log(S/K)+(b+0.5*s*s)*T)/(s*math.sqrt(T)); d2=d1-s*math.sqrt(T); eb=math.exp((b-r)*T)
for cp in 'cp':
    ch_num=-(delta(cp,S,K,T+1e-5,r,b,s)-delta(cp,S,K,T-1e-5,r,b,s))/(2e-5)
    if cp=='c': ch=-eb*((b-r)*N(d1)+n(d1)*(b/(s*math.sqrt(T))-d2/(2*T)))
    else: ch=-eb*(-(b-r)*N(-d1)+n(d1)*(b/(s*math.sqrt(T))-d2/(2*T)))
    va_num=(delta(cp,S,K,T,r,b,s+1e-4)-delta(cp,S,K,T,r,b,s-1e-4))/2e-4
    va=-eb*n(d1)*d2/s
    th_num=-(price(cp,S,K,T+1e-6,r,b,s)-price(cp,S,K,T-1e-6,r,b,s))/2e-6
    th = -S*eb*n(d1)*s/(2*math.sqrt(T)) + ((-(b-r)*S*eb*N(d1)-r*K*math.exp(-r*T)*N(d2)) if cp=='c' else ((b-r)*S*eb*N(-d1)+r*K*math.exp(-r*T)*N(-d2)))
    print(cp,'charm',round(ch,5),round(ch_num,5),'vanna',round(va,5),round(va_num,5),'theta',round(th,5),round(th_num,5))
