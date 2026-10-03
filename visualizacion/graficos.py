import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import io, contextlib, importlib.util, os
HERE=os.path.dirname(os.path.abspath(__file__)); os.chdir(os.path.join(HERE,"..","codigo"))
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10.5,"axes.spines.top":False,"axes.spines.right":False,
 "axes.edgecolor":"#5b6872","axes.labelcolor":"#18232b","xtick.color":"#18232b","ytick.color":"#18232b",
 "axes.titlesize":12.5,"axes.titleweight":"bold","axes.titlelocation":"left","figure.dpi":200})
INK="#18232b"; MUT="#5b6872"; ACC="#145c6e"; ACC2="#5fa8b8"; PUR="#7d3b8a"; ORA="#b5651d"; GRY="#c9d0d3"
def save(f,name): f.savefig(os.path.join(HERE,f"{name}.png"),bbox_inches="tight",facecolor="white"); plt.close(f)
with contextlib.redirect_stdout(io.StringIO()):
    spec=importlib.util.spec_from_file_location("mz","matriz.py"); mz=importlib.util.module_from_spec(spec); spec.loader.exec_module(mz)
    spec2=importlib.util.spec_from_file_location("md","modelos.py"); md=importlib.util.module_from_spec(spec2); spec2.loader.exec_module(md)

# 1 Calendario
ev=[("2018-05-25","RGPD"),("2023-03-31","Directrices EBA/GL/2023/04 (acceso)"),("2024-08-01","Reglamento de IA: entrada en vigor"),
    ("2025-01-17","DORA: aplicación"),("2026-06-11","Sentencia Jenec (C-81/24)"),("2026-07-24","Reglamento 2026/1744 (Ómnibus de IA)"),
    ("2026-11-20","Directiva 2023/2225: aplicación"),("2027-07-10","AMLR: aplicación"),("2027-12-02","Reglamento de IA: obligaciones del anexo III")]
import datetime as dt
f,ax=plt.subplots(figsize=(10,4.4))
for i,(s_,l) in enumerate(ev):
    x=dt.date.fromisoformat(s_); hi=x>=dt.date(2025,1,1)
    ax.plot([dt.date(2017,6,1),x],[i,i],color=GRY,lw=0.8)
    ax.plot(x,i,"D" if hi else "o",color=ACC if hi else MUT,ms=7)
    ax.text(x+dt.timedelta(days=45),i,f"{x.day}.{x.month}.{x.year}",va="center",fontsize=8.6,color=ACC if hi else MUT,fontweight="bold" if hi else "normal")
ax.axvspan(dt.date(2025,1,1),dt.date(2027,12,31),color=ACC,alpha=0.07)
ax.text(dt.date(2026,7,1),-1.1,"2025-2027",ha="center",fontsize=9,color=ACC,fontweight="bold")
ax.set_yticks(range(len(ev))); ax.set_yticklabels([l for _,l in ev],fontsize=9); ax.invert_yaxis()
ax.set_ylim(len(ev)-0.4,-1.6)
ax.set_xlim(dt.date(2017,6,1),dt.date(2029,3,1)); ax.spines["left"].set_visible(False); ax.tick_params(axis="y",length=0)
ax.set_title("Entre 2025 y 2027 coinciden cuatro marcos sobre las mismas decisiones automatizadas")
save(f,"f1_calendario")

# 2 Mapa de superposición: función x marco, por decisión
O=mz.O; deg=mz.deg
fr_order=["RIA","RGPD","CCD2","EBA/GL/2020/06","DORA","Dir. 2014/92/UE","RDL 19/2017","Ley 10/2010","EBA/GL/2023/04","AMLR"]
fr_lab=["Regl. IA","RGPD","Dir. 2023/2225","EBA/GL/2020/06","DORA","Dir. 2014/92","RDL 19/2017","Ley 10/2010","EBA/GL/2023/04","AMLR"]
funcs=[]
for dec in "SA":
    for o in O:
        k=(dec,o[4])
        if o[1]==dec and k not in funcs: funcs.append(k)
M=np.zeros((len(funcs),len(fr_order)))
for o in O:
    i=funcs.index((o[1],o[4])); j=fr_order.index(o[2]); M[i,j]+=1
f,ax=plt.subplots(figsize=(10,8.4))
for i,(dec,fn) in enumerate(funcs):
    nfr=(M[i]>0).sum()
    for j in range(len(fr_order)):
        if M[i,j]>0:
            ax.add_patch(plt.Rectangle((j+0.08,i+0.08),0.84,0.84,color=ACC if nfr>1 else GRY,alpha=0.9 if nfr>1 else 0.8))
            if M[i,j]>1: ax.text(j+0.5,i+0.55,int(M[i,j]),ha="center",va="center",color="white" if nfr>1 else INK,fontsize=8.5,fontweight="bold")
ax.set_xlim(0,len(fr_order)); ax.set_ylim(len(funcs),0)
ax.set_xticks(np.arange(len(fr_order))+0.5); ax.set_xticklabels(fr_lab,rotation=40,ha="right",fontsize=9)
ax.set_yticks(np.arange(len(funcs))+0.5); ax.set_yticklabels([fn for _,fn in funcs],fontsize=8.8)
ns=sum(1 for d_,_ in funcs if d_=="S")
ax.axhline(ns,color=INK,lw=1)
ax.text(len(fr_order)+0.15,ns/2,"Evaluación\nde solvencia",va="center",fontsize=9.5,color=INK,fontweight="bold")
ax.text(len(fr_order)+0.15,ns+(len(funcs)-ns)/2,"Alta de\ncuenta",va="center",fontsize=9.5,color=INK,fontweight="bold")
for s in ["left","bottom"]: ax.spines[s].set_visible(False)
ax.tick_params(length=0)
ax.legend(handles=[plt.Rectangle((0,0),1,1,color=ACC),plt.Rectangle((0,0),1,1,color=GRY)],
          labels=["Función regulada por dos o más marcos","Función regulada por un solo marco"],loc="upper center",bbox_to_anchor=(0.45,-0.16),ncol=2,frameon=False,fontsize=9)
ax.set_title("17 de las 24 funciones de las dos decisiones las regulan dos o más marcos")
save(f,"f2_mapa")

# 3 Asimetría
cats=["N","I","D","C"]; lab={"N":"Integrada por norma expresa","I":"Equivalente o compatible","D":"Definición distinta","C":"En tensión"}
col={"N":ACC,"I":ACC2,"D":ORA,"C":PUR}
import collections
P=mz.PERS
def cnt(test): 
    c=collections.Counter(v for k,v in mz.R.items() if test(mz.ids[k[0]][4])); return c
data={"Obligaciones internas\n(19 relaciones)":cnt(lambda f_: f_ not in P),"De cara a la persona\n(13 relaciones)":cnt(lambda f_: f_ in P)}
f,ax=plt.subplots(figsize=(10,3.2))
for i,(name,c) in enumerate(data.items()):
    tot=sum(c.values()); left=0
    for k in cats:
        w=100*c[k]/tot
        ax.barh(i,w,left=left,color=col[k],height=0.55)
        if w>6: ax.text(left+w/2,i,f"{c[k]} ({w:.0f} %)",ha="center",va="center",color="white",fontsize=9,fontweight="bold")
        left+=w
ax.set_yticks([0,1]); ax.set_yticklabels(list(data.keys())); ax.invert_yaxis()
ax.set_xlim(0,100); ax.set_xlabel("% de las relaciones entre marcos")
ax.legend([plt.Rectangle((0,0),1,1,color=col[k]) for k in cats],[lab[k] for k in cats],ncol=4,loc="upper center",bbox_to_anchor=(0.5,-0.3),frameon=False,fontsize=9)
ax.set_title("La integración ya escrita protege los procesos del banco, no los derechos de la persona")
save(f,"f3_asimetria")

# 4 Composición del coste por préstamo
prof=[("Gran grupo",250000),("Entidad mediana",25000),("Cooperativa",2500)]
ints=[(0,"Sin integr."),(md.d_now,"Actual"),(md.d_one,"Exp. único")]
f,axs=plt.subplots(1,3,figsize=(10,3.6),sharey=True)
for ax,(pn,N) in zip(axs,prof):
    cm=[md.CMOD*(1-d)/N for d,_ in ints]; cr=md.creg(0.10)
    x=np.arange(3)
    ax.bar(x,[cr]*3,color=GRY,width=0.6,label="Por decisión (revisión a petición)")
    ax.bar(x,cm,bottom=[cr]*3,color=ACC,width=0.6,label="Por modelo")
    for xi,v in zip(x,cm): ax.text(xi,cr+v+0.3,f"{cr+v:.1f} €".replace(".",","),ha="center",fontsize=8.8)
    ax.set_xticks(x); ax.set_xticklabels([l for _,l in ints],fontsize=8.8); ax.set_title(f"{pn} (N = {N:,})".replace(",","."),fontsize=10)
axs[0].set_ylabel("€ por préstamo concedido")
axs[0].legend(loc="upper left",frameon=False,fontsize=8.5)
f.suptitle("En la cooperativa domina el coste por modelo; en el gran grupo, el coste por decisión",x=0.01,ha="left",fontweight="bold",fontsize=12.5)
f.tight_layout()
save(f,"f4_coste")

# 5 ΔL* con Monte Carlo
rng=np.random.default_rng(2026); K=100000
tri=lambda a,b,c: rng.triangular(a,b,c,K)
Ps=tri(30,40,55); Cs=tri(15000,29277,45000); tr=tri(0.25,0.5,1.0); txs=tri(0.05,0.1,0.25); ELs=tri(0.01,0.02,0.04); fs=tri(0.020,0.0272,0.035)
mm=(md.r-fs-ELs)*md.s*md.n
f,ax=plt.subplots(figsize=(10,4.2))
w=0.13; x=np.arange(3)
for k,(d,dl) in enumerate(ints):
    for q,qlab,qq,hatch in ((0.10,"a petición",tri(0.05,0.10,0.30),None),(1.0,"previa",np.ones(K),"//")):
        det=[(md.CMOD*(1-d)/N+md.creg(q))/md.m() for _,N in prof]
        mc=[(Cs*(1-d)/N+(1-md.a)/md.a*(qq*tr*Ps+txs*Ps))/mm for _,N in prof]
        pos=x+(k*2+(0 if q<1 else 1)-2.5)*w
        c=[ACC,ACC2,"#9cc9d3"][k]
        ax.bar(pos,det,width=w,color=c,hatch=hatch,edgecolor="white",label=f"{dl}, revisión {qlab}")
        lo=[np.percentile(v,10) for v in mc]; hi=[np.percentile(v,90) for v in mc]
        if q<1: ax.errorbar(pos,det,yerr=[np.maximum(0,np.array(det)-lo),np.maximum(0,np.array(hi)-det)],fmt="none",ecolor=MUT,elinewidth=0.9,capsize=2)
ax.set_xticks(x); ax.set_xticklabels([p for p,_ in prof])
ax.set_ylabel("Aumento del importe mínimo rentable (€)")
ax.legend(ncol=3,fontsize=8.2,frameon=False,loc="upper left")
ax.set_ylim(0,1100)
ax.set_title("Revisar de antemano toda denegación eleva el umbral unos 300 € en cualquier entidad")
ax.text(0,-0.2,"Barras: caso base. Bigotes (revisión a petición): percentiles 10 y 90 de 100.000 simulaciones de Monte Carlo.",transform=ax.transAxes,fontsize=8.5,color=MUT)
save(f,"f5_deltaL")

# 6 Tornado
base=dict(cop=150,CMOD=md.CMOD,N=2500,d=md.d_now,q=0.10,trev=0.5,tx=0.1,P=40,a=0.6,r=md.r,f=md.f,EL=md.EL,n=md.n)
names={"r":"Tipo del préstamo","f":"Coste de financiación","n":"Plazo","EL":"Pérdida esperada","cop":"Coste operativo","a":"Tasa de aprobación","N":"Préstamos por modelo","CMOD":"Coste por modelo","d":"Descuento por integración","P":"Coste por hora","tx":"Horas de explicación","q":"Denegaciones revisadas","trev":"Horas por revisión"}
L0=md.Lstar(base); rows=[]
for k in names:
    lo=dict(base); hi=dict(base); lo[k]*=0.8; hi[k]*=1.2
    rows.append((names[k],md.Lstar(lo)-L0,md.Lstar(hi)-L0,k in("a","N","CMOD","d","P","tx","q","trev")))
rows.sort(key=lambda r:max(abs(r[1]),abs(r[2])))
f,ax=plt.subplots(figsize=(10,5))
for i,(nm,lo,hi,reg) in enumerate(rows):
    ax.barh(i,lo,color=PUR,height=0.6); ax.barh(i,hi,color=ACC,height=0.6)
    ax.text(max(lo,hi)+90,i,f"{lo:+,.0f} / {hi:+,.0f} €".replace(",","."),va="center",fontsize=8.3,color=MUT)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([("● " if r[3] else "")+r[0] for r in rows],fontsize=9)
ax.axvline(0,color=INK,lw=0.8); ax.set_xlim(-2200,7600)
ax.set_xlabel("Cambio del importe mínimo rentable (€) al mover cada parámetro un 20 %")
ax.legend([plt.Rectangle((0,0),1,1,color=PUR),plt.Rectangle((0,0),1,1,color=ACC)],["Parámetro −20 %","Parámetro +20 %"],frameon=False,loc="lower right",fontsize=9)
ax.text(0,-0.14,"● parámetro regulatorio. Cooperativa con integración actual y revisión a petición; importe mínimo base: 4.143 €.",transform=ax.transAxes,fontsize=8.5,color=MUT)
ax.set_title("El tipo de interés y el plazo mueven el umbral mucho más que cualquier parámetro regulatorio")
save(f,"f6_tornado")

# 7 Monocultura
rh=[0,0.25,0.5,0.75,1.0]; tot=[1.81,4.10,7.16,11.60,23.92]; con=[1.92,4.15,7.06,11.21,22.78]; sin=[1.39,3.93,7.58,13.19,28.49]
f,ax=plt.subplots(figsize=(10,4))
ax.plot(rh,con,"-o",color=ACC,label="Con historial"); ax.plot(rh,sin,"-o",color=PUR,label="Sin historial"); ax.plot(rh,tot,"--",color=MUT,lw=1,label="Total")
for xs,ys,c in ((rh,con,ACC),(rh,sin,PUR)):
    ax.annotate(f"{ys[-1]:.1f} %".replace(".",","),(1,ys[-1]),textcoords="offset points",xytext=(-40,6),fontsize=8.6,color=c,fontweight="bold")
ax.set_xticks(rh); ax.set_xticklabels(["0\nmodelos\nindependientes","0,25","0,50","0,75","1\nun mismo\nmodelo"])
ax.set_xlabel("Correlación entre los modelos de las cinco entidades (ρ)"); ax.set_ylabel("% de solventes rechazados por las cinco")
ax.text(0.0,16.5,"Con modelos independientes (ρ = 0):\n1,9 % con historial y 1,4 % sin historial",fontsize=8.6,color=MUT)
ax.legend(frameon=False,loc="upper left")
ax.set_title("Sin historial, la monocultura multiplica por veinte el rechazo sistémico de solventes")
save(f,"f7_monocultura")

# 8 Recorrido de la persona
f,ax=plt.subplots(figsize=(10,4.6)); ax.axis("off"); ax.set_xlim(0,100); ax.set_ylim(0,50)
def box(x,y,w,h,t,fc="white",ec=MUT,bold=False,fs=8.8):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.4,rounding_size=1.2",fc=fc,ec=ec,lw=1.1))
    ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=fs,fontweight="bold" if bold else "normal",color=INK)
box(2,36,20,8,"Solicitud de\ncuenta básica",bold=True)
box(54,36,20,8,"Solicitud de\ncrédito al consumo",bold=True)
ax.annotate("",xy=(53,40),xytext=(23,40),arrowprops=dict(arrowstyle="->",color=MUT))
ax.text(38,41.5,"semanas después",ha="center",fontsize=8,color=MUT)
alta=[("AMLR, art. 76.5\nintervención significativa",PUR),("RGPD, art. 22\nintervención e impugnación",PUR),("RDL 19/2017, arts. 4-5\nnegativa escrita motivada",ORA)]
cred=[("Regl. IA, arts. 14 y 26.2\nsupervisión del sistema",PUR),("Dir. 2023/2225, art. 18.8\nintervención y revisión",PUR),("RGPD, arts. 15 y 22\nexplicación e intervención",PUR)]
for i,(t,c) in enumerate(alta):
    box(1+i*0.0,26-i*9.5,24,7,t,ec=c,fs=8); ax.plot([12,12],[36,33],color=MUT,lw=0.8)
for i,(t,c) in enumerate(cred):
    box(53,26-i*9.5,24,7,t,ec=c,fs=8); ax.plot([64,64],[36,33],color=MUT,lw=0.8)
box(81,14,17.5,22,"Para ella:\n\n4 estándares de\nrevisión humana\n\n3 canales de\nreclamación\n\n3 constancias de\nuna denegación",fc="#e3eef0",ec=ACC,fs=8.6)
ax.text(28,2,"Morado: intervención o revisión humana. Naranja: comunicación de la denegación.",fontsize=8.3,color=MUT)
ax.set_title("Una persona, dos decisiones y ninguna regla que integre sus derechos",loc="left")
save(f,"f8_recorrido")
print("ok")
