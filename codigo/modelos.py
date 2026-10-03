import numpy as np
rng=np.random.default_rng(2026)
# ---------- parámetros base (fuente en anexo C)
P=40.0          # €/h, coste laboral sector K (EAES 2024: 51.862,90 € brutos; x1,31 cotizaciones; 1.700 h)
CMOD=29277.0    # €/modelo/año (Renda et al., 2021)
r,f,EL,n=0.0716,0.0272,0.020,3
def sfrac(r,n):  # saldo medio / principal, préstamo francés mensual
    i=r/12; N=int(n*12); B=1.0; pay=i/(1-(1+i)**-N); tot=0
    for _ in range(N): tot+=B; B=B*(1+i)-pay
    return tot/N
s=sfrac(r,n); print("s=",round(s,3), "salario/h check", round(51862.90*1.31/1700,1))
def m(r=r,f=f,EL=EL,n=n): return (r-f-EL)*sfrac(r,n)*n
a=0.60; trev=0.5; tx=0.1
def creg(q,a=a,trev=trev,tx=tx,P=P): return (1-a)/a*(q*trev*P + tx*P)
# integración: d = parte de obligaciones del RIA sobre solvencia ya integradas (N) o integrables (N+I+D)
d_now=8/21; d_one=None
import importlib.util,sys,io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    spec=importlib.util.spec_from_file_location("mz","matriz.py"); mz=importlib.util.module_from_spec(spec); spec.loader.exec_module(mz)
ria=[o[0] for o in mz.O if o[2]=="RIA"]
withN=[x for x in ria if "N" in mz.deg.get(x,set())]; withAny=[x for x in ria if x in mz.deg]
d_now=len(withN)/len(ria); d_one=len(withAny)/len(ria)
print("RIA oblig",len(ria),"N",len(withN),round(d_now,2),"cualquier",len(withAny),round(d_one,2))
prof={"Gran grupo":250000,"Entidad mediana":25000,"Cooperativa de crédito":2500}
print("\nm (margen x saldo x plazo) =",round(m(),4))
print("\nTabla: coste por préstamo aprobado y aumento del importe mínimo (ΔL*)")
for q,lab in ((0.10,"revisión a petición"),(1.0,"revisión previa de toda denegación")):
  for name,N in prof.items():
    for d,dl in ((0,"sin integración"),(d_now,"integración actual"),(d_one,"expediente único")):
        cm=CMOD*(1-d)/N; cr=creg(q); dL=(cm+cr)/m()
        print(f"{lab:36s}|{name:24s}|{dl:18s}| c_mod {cm:7.2f} | c_reg {cr:6.2f} | ΔL* {dL:7.0f} €")
# referencia: L* base con c_op=150
cop=150; print("\nL* sin costes regulatorios (c_op=150):", round(cop/m()))
# ---------- tornado ±20% sobre L* total, cooperativa, integración actual, q=0.1
base=dict(cop=150,CMOD=CMOD,N=2500,d=d_now,q=0.10,trev=trev,tx=tx,P=P,a=a,r=r,f=f,EL=EL,n=n)
def Lstar(p):
    cm=p['CMOD']*(1-p['d'])/p['N']; cr=(1-p['a'])/p['a']*(p['q']*p['trev']*p['P']+p['tx']*p['P'])
    return (p['cop']+cm+cr)/m(p['r'],p['f'],p['EL'],p['n'])
L0=Lstar(base); print("\nL* cooperativa base", round(L0))
res=[]
for k in base:
    lo=dict(base); hi=dict(base)
    if k=="n": lo[k]=base[k]*0.8; hi[k]=base[k]*1.2
    else: lo[k]=base[k]*0.8; hi[k]=base[k]*1.2
    res.append((k,Lstar(lo)-L0,Lstar(hi)-L0))
for k,lo,hi in sorted(res,key=lambda x:-max(abs(x[1]),abs(x[2]))): print(f"{k:5s} {lo:+7.0f} {hi:+7.0f}")
# ---------- Monte Carlo (triangulares) para ΔL* cooperativa vs gran grupo
def tri(lo,mo,hi,k): return rng.triangular(lo,mo,hi,k)
K=100000
Ps=tri(30,40,55,K); Cs=tri(15000,29277,45000,K); tr=tri(0.25,0.5,1.0,K); txs=tri(0.05,0.1,0.25,K)
ELs=tri(0.01,0.02,0.04,K); fs=tri(0.020,0.0272,0.035,K); qs=tri(0.05,0.10,0.30,K)
mm=(r-fs-ELs)*s*n
for name,N in prof.items():
  for d,dl in ((0,"sin"),(d_now,"actual"),(d_one,"único")):
    dL=(Cs*(1-d)/N + (1-a)/a*(qs*tr*Ps+txs*Ps))/mm
    print(f"MC {name:24s} {dl:7s} mediana {np.median(dL):6.0f}  P10 {np.percentile(dL,10):6.0f}  P90 {np.percentile(dL,90):6.0f}")
# ---------- monocultura
print("\nMonocultura: % de solventes rechazados por las 5 entidades")
J=5; M=400000
grp=rng.random(M)<0.20                       # 20% sin historial
qtrue=rng.standard_normal(M); solv=qtrue>np.quantile(qtrue,0.25)
sig=np.where(grp,1.0,0.6)                    # error mayor sin historial
for rho in (0,0.25,0.5,0.75,1.0):
    eps=rng.standard_normal(M); rej_all=np.ones(M,bool)
    for j in range(J):
        sc=qtrue+sig*(np.sqrt(rho)*eps+np.sqrt(1-rho)*rng.standard_normal(M))
        thr=np.quantile(sc,0.40); rej_all&=sc<thr
    tot=rej_all[solv].mean(); h=rej_all[solv&~grp].mean(); t=rej_all[solv&grp].mean()
    print(f"rho {rho:4.2f} | total {tot:6.2%} | con historial {h:6.2%} | sin historial {t:6.2%} | ratio {t/max(h,1e-9):5.1f}")
