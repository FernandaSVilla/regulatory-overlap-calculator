# Figuras a partir de la matriz, los modelos y los datos de datos_figuras/
# Uso: python3 graficos.py   (las imágenes se guardan en esta carpeta)
# Las figuras de la matriz y de los modelos se calculan con matriz.py y modelos.py (semilla 2026).
# El calendario, las cuentas básicas rechazadas, los estados del alta y las posiciones de la red se leen de datos_figuras/.
import numpy as np, matplotlib, matplotlib.patheffects, matplotlib.dates, matplotlib.ticker, io, contextlib, importlib.util, os, collections, csv, datetime as dt
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__)); DATOS = os.path.join(HERE, "datos_figuras")
os.chdir(os.path.join(HERE, "..", "codigo"))

# ---- Estilo ------------------------------------------------------------------
# Letra: Carlito (métrica idéntica a Calibri); si no está, Calibri; si no, la sans por defecto.
disp = {f.name for f in font_manager.fontManager.ttflist}
LETRA = next((f for f in ("Carlito", "Calibri") if f in disp), "DejaVu Sans")
MARINO, AZUL, CELESTE = "#1B3A5C", "#3E6A93", "#9DB3CB"
OCRE, OCRE_CL, GRANATE = "#C9A227", "#E6D18E", "#7A2E2E"
GRIS, VACIO, TINTA, SUAVE, EJE = "#D9D9D9", "#F1F1EE", "#222222", "#5A5A5A", "#8A8A8A"
plt.rcParams.update({
    "font.family": LETRA, "font.size": 11, "figure.dpi": 300, "savefig.dpi": 300,
    "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": EJE, "axes.linewidth": 0.8,
    "axes.labelcolor": SUAVE, "axes.titleweight": "bold", "axes.titlesize": 11.5, "axes.titlelocation": "left",
    "xtick.color": SUAVE, "ytick.color": TINTA, "xtick.major.width": 0.8, "ytick.major.width": 0.8,
    "legend.frameon": False, "legend.fontsize": 10.5, "text.color": TINTA, "axes.unicode_minus": True})

def es(x, dec=0):
    s = f"{x:,.{dec}f}"; return s.replace(",", "X").replace(".", ",").replace("X", ".")
def save(f, name):
    f.savefig(os.path.join(HERE, name + ".png"), bbox_inches="tight", facecolor="white"); plt.close(f)
def lee(n):
    with open(os.path.join(DATOS, n + ".csv"), encoding="utf-8") as f: return list(csv.DictReader(f))
def caja(ax, rects, **kw):
    ax.legend(handles=[Rectangle((0, 0), 1, 1, color=c) for c, _ in rects], labels=[l for _, l in rects], **kw)

with contextlib.redirect_stdout(io.StringIO()):
    s1 = importlib.util.spec_from_file_location("mz", "matriz.py"); mz = importlib.util.module_from_spec(s1); s1.loader.exec_module(mz)
    s2 = importlib.util.spec_from_file_location("md", "modelos.py"); md = importlib.util.module_from_spec(s2); s2.loader.exec_module(md)

# ---- calendario -----------------------------------------------------
ev = [(r["hito"], dt.date.fromisoformat(r["fecha"])) for r in lee("calendario")]
f, ax = plt.subplots(figsize=(10, 3.9))
ax.axvspan(dt.date(2025, 1, 1), dt.date(2027, 12, 31), ymin=0, ymax=0.9, color="#E9EEF4", lw=0)
for i, (lab, x) in enumerate(ev):
    hi = x >= dt.date(2025, 1, 1); col = MARINO if hi else EJE
    ax.plot([dt.date(2018, 1, 1), x], [i, i], color="#E2E2E2", lw=0.8, zorder=1)
    ax.plot(x, i, "D" if hi else "o", color=col, ms=6.5 if hi else 7, zorder=2)
    ax.text(x + dt.timedelta(days=45), i, f"{x.day}.{x.month}.{x.year}", va="center", fontsize=10, color=col)
ax.text(dt.date(2026, 7, 1), -1.15, "2025-2027: cuatro marcos\nentran en aplicación", ha="center", va="bottom",
        fontsize=10.5, color=MARINO, linespacing=1.1)
ax.set_yticks(range(len(ev))); ax.set_yticklabels([l for l, _ in ev], fontsize=10.5)
ax.set_ylim(len(ev) - 0.4, -2.0); ax.set_xlim(dt.date(2018, 1, 1), dt.date(2029, 1, 1))
ax.xaxis.set_major_locator(matplotlib.dates.YearLocator()); ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y"))
ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
save(f, "calendario")

# ---- mapa de superposición -------------------------------------------
fr = ["RIA", "RGPD", "CCD2", "EBA/GL/2020/06", "DORA", "Dir. 2014/92/UE", "RDL 19/2017", "Ley 10/2010", "EBA/GL/2023/04", "AMLR"]
fr_lab = ["Reglamento\nde IA", "RGPD", "Directiva\n2023/2225", "EBA/GL/\n2020/06", "DORA", "Directiva\n2014/92/UE",
          "RDL\n19/2017", "Ley\n10/2010", "EBA/GL/\n2023/04", "AMLR"]
funcs = []
for dec in "SA":
    for o in mz.O:
        if o[1] == dec and (dec, o[4]) not in funcs: funcs.append((dec, o[4]))
M = np.zeros((len(funcs), len(fr)))
for o in mz.O: M[funcs.index((o[1], o[4])), fr.index(o[2])] += 1
f, ax = plt.subplots(figsize=(10, 9))
for i in range(len(funcs)):
    varios = (M[i] > 0).sum() > 1
    for j in range(len(fr)):
        col = VACIO if M[i, j] == 0 else (MARINO if varios else GRIS)
        ax.add_patch(Rectangle((j + 0.05, i + 0.08), 0.9, 0.84, color=col, lw=0))
        if M[i, j] > 1:
            ax.text(j + 0.5, i + 0.5, int(M[i, j]), ha="center", va="center", fontsize=11, fontweight="bold",
                    color="white" if varios else TINTA)
ns = sum(1 for d_, _ in funcs if d_ == "S")
ax.plot([-0.05, 11.9], [ns, ns], color=TINTA, lw=1, clip_on=False)
ax.text(10.25, ns / 2, "Evaluación\nde solvencia", va="center", fontsize=11.5, fontweight="bold")
ax.text(10.25, ns + (len(funcs) - ns) / 2, "Alta de\ncuenta", va="center", fontsize=11.5, fontweight="bold")
ax.set_xlim(0, len(fr)); ax.set_ylim(len(funcs), 0)
ax.xaxis.tick_top(); ax.set_xticks(np.arange(len(fr)) + 0.5); ax.set_xticklabels(fr_lab, fontsize=10, color=SUAVE)
ax.set_yticks(np.arange(len(funcs)) + 0.5); ax.set_yticklabels([fn for _, fn in funcs], fontsize=10.5)
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0)
caja(ax, [(MARINO, "Función regulada por dos o más marcos"), (GRIS, "Función regulada por un solo marco")],
     loc="upper center", bbox_to_anchor=(0.5, -0.01), ncol=2, fontsize=10.5)
save(f, "mapa_superposicion")

# ---- asimetría -------------------------------------------------------
def grupo(k):
    a, b = mz.orient(k[0]), mz.orient(k[1]); return a if a == b else "mixta"
G = {g: collections.Counter(v for k, v in mz.R.items() if grupo(k) == g) for g in ("interna", "persona", "mixta")}
labels = {"interna": "Obligaciones internas", "persona": "De cara a la persona",
          "mixta": "Pares mixtos (supervisión\ninterna y derecho de la persona)"}
cats = [("N", MARINO, "Integrada por norma expresa", "white"), ("I", CELESTE, "Equivalente o compatible", TINTA),
        ("D", OCRE, "Definición distinta", TINTA), ("C", GRANATE, "En tensión", "white")]
f, ax = plt.subplots(figsize=(9.7, 3.9))
for i, g in enumerate(("interna", "persona", "mixta")):
    c = G[g]; tot = sum(c.values()); left = 0
    for k, col, _, tc in cats:
        w = 100 * c[k] / tot
        if w > 0:
            ax.barh(i, w, left=left, color=col, height=0.55, edgecolor="white", linewidth=1.5)
            if w > 7: ax.text(left + w / 2, i, f"{c[k]} ({es(w)} %)", ha="center", va="center", color=tc, fontsize=11, fontweight="bold")
        left += w
ax.set_yticks(range(3)); ax.set_yticklabels([f"{labels[g]}\n({sum(G[g].values())} relaciones)" for g in ("interna", "persona", "mixta")], fontsize=10.5)
ax.invert_yaxis(); ax.set_xlim(0, 100); ax.set_xlabel("% de las relaciones entre marcos")
ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
caja(ax, [(c[1], c[2]) for c in cats], ncol=4, loc="upper center", bbox_to_anchor=(0.45, -0.25))
save(f, "asimetria_integracion")

# ---- recorrido de la persona -----------------------------------------
f = plt.figure(figsize=(10, 5)); ax = f.add_axes([0, 0, 1, 1]); ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(5, 101)
def box(x, y, w, h, t, ec, fc, bold=False, fs=11.5):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=1.3))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal", linespacing=1.25)
AZ_F, OC_F = "#E6ECF3", "#F7EDCC"
box(2, 82, 33, 12, "Alta de cuenta de pago básica", TINTA, "white", True, 13)
box(45, 82, 33, 12, "Solicitud de crédito al consumo", TINTA, "white", True, 13)
ax.annotate("", xy=(44.2, 88), xytext=(35.8, 88), arrowprops=dict(arrowstyle="-|>", color=SUAVE, lw=1.1, mutation_scale=14))
ax.text(40, 96, "semanas\ndespués", ha="center", va="center", fontsize=10, color=SUAVE)
for k, (t, ec, fc) in enumerate([("AMLR, art. 76.5\nintervención humana significativa", MARINO, AZ_F),
                                 ("RGPD, art. 22\nintervención e impugnación", MARINO, AZ_F),
                                 ("RDL 19/2017, arts. 4-5\ndenegación escrita y motivada", "#9C7C12", OC_F)]):
    box(2, 60 - 20 * k, 33, 13, t, ec, fc)
for k, t in enumerate(["Reglamento de IA, arts. 14 y 26.2\nsupervisión humana del sistema",
                       "Directiva 2023/2225, art. 18.8\nintervención, explicación y revisión",
                       "RGPD, arts. 15.1.h y 22\nexplicación e intervención"]):
    box(45, 60 - 20 * k, 33, 13, t, MARINO, AZ_F)
box(82, 30, 17, 40, "Para la persona:\n\n4 estándares de\nrevisión humana\n\n3 canales de\nreclamación\n\n3 constancias de\nuna denegación",
    MARINO, "#F4F6F9", fs=11)
ax.text(2, 9, "Azul: intervención o revisión humana.    Ocre: comunicación de la denegación.", fontsize=10.5, color=SUAVE, va="center")
save(f, "recorrido_persona")

# ---- composición del coste por préstamo ------------------------------
prof = [("Gran grupo", 250000), ("Entidad mediana", 25000), ("Cooperativa", 2500)]
ints = [(0, "Sin\nintegración"), (md.d_now, "Integración\nactual"), (md.d_one, "Expediente\núnico")]
f, axs = plt.subplots(1, 3, figsize=(10.4, 4.1), sharey=True); cr = md.creg(0.10)
for ax, (pn, N) in zip(axs, prof):
    cm = [md.CMOD * (1 - d) / N for d, _ in ints]; x = np.arange(3)
    ax.bar(x, [cr] * 3, color=GRIS, width=0.6, label="Coste por decisión (revisión a petición)")
    ax.bar(x, cm, bottom=[cr] * 3, color=MARINO, width=0.6, label="Coste por modelo")
    for xi, v in zip(x, cm): ax.text(xi, cr + v + 0.25, f"{es(cr + v, 1)} €", ha="center", fontsize=10.5)
    ax.set_xticks(x); ax.set_xticklabels([l for _, l in ints], fontsize=10, color=SUAVE)
    ax.set_title(f"{pn} (N = {es(N)})", fontsize=12)
axs[0].set_ylabel("€ por préstamo concedido"); axs[0].set_ylim(0, 18); axs[0].set_yticks(range(0, 19, 2))
for ax in axs: ax.tick_params(axis="y", colors=SUAVE)
axs[0].legend(loc="upper left", fontsize=10.5)
f.tight_layout(); save(f, "coste_por_prestamo")

# ---- ΔL* ---------------------------------------------------------------
f, axs = plt.subplots(1, 2, figsize=(9.7, 4.3), sharey=True); cols = [GRANATE, AZUL, CELESTE]
names = ["Sin integración", "Integración actual", "Expediente único"]
for ax, (q, tt) in zip(axs, ((0.10, "Revisión a petición"), (1.0, "Revisión previa de toda denegación"))):
    x = np.arange(3); w = 0.26
    for k, (d, _) in enumerate(ints):
        v = [(md.CMOD * (1 - d) / N + md.creg(q)) / md.m() for _, N in prof]
        ax.bar(x + (k - 1) * w, v, width=w, color=cols[k], edgecolor="white", label=names[k])
        for xi, vi in zip(x + (k - 1) * w, v): ax.text(xi, vi + 10, es(vi), ha="center", fontsize=10)
    ax.set_xticks(x); ax.set_xticklabels(["Gran grupo", "Entidad\nmediana", "Cooperativa"], color=SUAVE)
    ax.set_title(tt, fontsize=12); ax.tick_params(axis="y", colors=SUAVE)
axs[0].set_ylabel("Aumento del importe mínimo rentable, ΔL* (€)"); axs[0].set_ylim(0, 800)
axs[1].legend(loc="upper left", fontsize=10.5)
f.tight_layout(); save(f, "importe_minimo_rentable")

# ---- tornado (cooperativa, integración actual, revisión a petición) ----
base = dict(cop=150, CMOD=md.CMOD, N=2500, d=md.d_now, q=0.10, trev=0.5, tx=0.1, P=40.0, a=0.6, r=md.r, f=md.f, EL=md.EL, n=md.n)
nm = {"r": "Tipo del préstamo", "f": "Coste de financiación", "n": "Plazo", "EL": "Pérdida esperada", "cop": "Coste operativo de originación",
      "a": "Tasa de aprobación", "N": "Préstamos por modelo", "CMOD": "Coste anual por modelo", "d": "Descuento por integración",
      "P": "Coste por hora", "tx": "Tiempo de explicación", "q": "Denegaciones revisadas", "trev": "Tiempo de revisión"}
REG = {"a", "N", "CMOD", "d", "P", "tx", "q", "trev"}; L0 = md.Lstar(base); rows = []
for k in nm:
    lo = dict(base); hi = dict(base); lo[k] *= 0.8; hi[k] *= 1.2; rows.append((k, md.Lstar(lo) - L0, md.Lstar(hi) - L0))
rows.sort(key=lambda r: max(abs(r[1]), abs(r[2])))
f, ax = plt.subplots(figsize=(9.7, 4.3))
for i, (k, lo, hi) in enumerate(rows):
    reg = k in REG
    ax.barh(i, lo, color=(OCRE_CL if reg else OCRE), height=0.6); ax.barh(i, hi, color=(CELESTE if reg else MARINO), height=0.6)
    ax.text(max(lo, hi, 0) + 90, i, f"{'+' if lo >= 0 else '−'}{es(abs(lo))} / {'+' if hi >= 0 else '−'}{es(abs(hi))} €", va="center", fontsize=10)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([("● " if k in REG else "") + nm[k] for k, _, _ in rows], fontsize=10.5)
ax.axvline(0, color=EJE, lw=0.8); ax.set_xlim(-2200, 7600); ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: es(v).replace("-", "−")))
ax.set_xlabel("Cambio del importe mínimo rentable (€) al mover cada parámetro un 20 %")
caja(ax, [(OCRE, "Parámetro −20 %"), (MARINO, "Parámetro +20 %"), (OCRE_CL, "● Parámetro regulatorio −20 %"),
          (CELESTE, "● Parámetro regulatorio +20 %")], loc="lower right", fontsize=10)
save(f, "sensibilidad"); print("L0", round(L0))

# ---- Monte Carlo (mismas extracciones que modelos.py) -------------------
rng = np.random.default_rng(2026); K = 100000; tri = lambda a, b, c: rng.triangular(a, b, c, K)
Ps = tri(30, 40, 55); Cs = tri(15000, 29277, 45000); tr = tri(0.25, 0.5, 1.0); txs = tri(0.05, 0.1, 0.25)
ELs = tri(0.01, 0.02, 0.04); fs = tri(0.020, 0.0272, 0.035); qs = tri(0.05, 0.10, 0.30)
mm = (md.r - fs - ELs) * md.s * md.n
cases = [("Gran grupo, integración actual", 250000, md.d_now), ("Entidad mediana, integración actual", 25000, md.d_now),
         ("Cooperativa, expediente único", 2500, md.d_one), ("Cooperativa, integración actual", 2500, md.d_now),
         ("Cooperativa, sin integración", 2500, 0)]
f, ax = plt.subplots(figsize=(9.7, 3.6)); mcres = []
for i, (lab, N, d) in enumerate(cases):
    v = (Cs * (1 - d) / N + (1 - md.a) / md.a * (qs * tr * Ps + txs * Ps)) / mm
    p10, p25, p50, p75, p90 = np.percentile(v, [10, 25, 50, 75, 90]); det = (md.CMOD * (1 - d) / N + md.creg(0.10)) / md.m()
    ax.plot([p10, p90], [i, i], color=CELESTE, lw=8, solid_capstyle="butt"); ax.plot([p25, p75], [i, i], color=AZUL, lw=8, solid_capstyle="butt")
    ax.plot(p50, i, "o", color=MARINO, ms=7.5); ax.plot([det, det], [i - 0.27, i + 0.27], color=OCRE, lw=2.4)
    ax.text(p90 + 18, i, f"mediana {es(p50)} €  [{es(p10)}-{es(p90)}]", va="center", fontsize=10.5)
    mcres.append((lab, round(p50), round(p10), round(p90)))
ax.set_yticks(range(len(cases))); ax.set_yticklabels([c[0] for c in cases], fontsize=10.5); ax.invert_yaxis()
ax.set_xlim(0, 1500); ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: es(v)))
ax.set_xlabel("Aumento del importe mínimo rentable, ΔL* (€), revisión a petición")
ax.legend([Line2D([0], [0], color=CELESTE, lw=8), Line2D([0], [0], color=AZUL, lw=8), Line2D([0], [0], marker="o", color=MARINO, lw=0, ms=7.5),
           Line2D([0], [0], color=OCRE, lw=2.4)], ["Percentiles 10 a 90", "Percentiles 25 a 75", "Mediana", "Caso base"],
          ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.24), fontsize=10.5)
save(f, "montecarlo"); print("MC", mcres)

# ---- cuentas de pago básicas rechazadas, 2023 ----------------------------
rows = lee("cuentas_basicas")
def tasa(r):
    if not r["abiertas_2023"] or not r["rechazadas_2023"]: return None
    a, b = float(r["abiertas_2023"]), float(r["rechazadas_2023"]); return 100 * b / (a + b)
ue = tasa(next(r for r in rows if r["pais"] == "Unión Europea")); rows = [r for r in rows if r["pais"] != "Unión Europea"]
f, ax = plt.subplots(figsize=(9.5, 6.2))
for i, r in enumerate(rows):
    t = tasa(r)
    if t is None:
        ax.text(0.15, i, "n. d.", va="center", fontsize=10, color=EJE)
    else:
        ax.barh(i, t, color=MARINO, height=0.6); ax.text(t + 0.25, i, f"{es(t, 1)} %", va="center", fontsize=10)
ax.axvline(ue, color=GRANATE, ls=(0, (3, 2)), lw=1.2)
ax.text(ue + 0.15, -1.1, f"Unión Europea: {es(ue, 1)} %", color=GRANATE, fontsize=10.5, va="center")
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r["pais"] for r in rows], fontsize=10.5)
ax.set_ylim(len(rows) - 0.4, -1.8); ax.set_xlim(0, 18.5); ax.set_xticks(range(0, 19, 2))
ax.set_xticklabels([f"{x} %" for x in range(0, 19, 2)]); ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
ax.set_xlabel("Solicitudes de cuenta de pago básica rechazadas, 2023 (% de las solicitudes resueltas)")
save(f, "cuentas_basicas_rechazadas")

# ---- estados del alta de cuenta -----------------------------------------
rows = lee("estados_alta_cuenta")
estados = list(dict.fromkeys(r["estado"] for r in rows)); marcos10 = list(dict.fromkeys(r["marco"] for r in rows))
lab10 = {"Cuenta básica": "Cuenta\nbásica", "Directrices EBA": "Directrices\nEBA", "Reglamento de IA": "Reglamento\nde IA",
         "Atención al cliente": "Atención\nal cliente"}
col10 = {"E": MARINO, "C": CELESTE, "G": GRIS, "0": VACIO}
f, ax = plt.subplots(figsize=(10, 4.7))
for r in rows:
    i, j, c = int(r["fila"]) - 1, int(r["columna"]) - 1, r["codigo"]
    ax.add_patch(Rectangle((j + 0.05, i + 0.09), 0.9, 0.82, color=col10[c], lw=0))
    if c != "0": ax.text(j + 0.5, i + 0.5, c, ha="center", va="center", fontsize=11, fontweight="bold", color="white" if c == "E" else TINTA)
vacia = [k for k, e in enumerate(estados) if all(r["codigo"] == "0" for r in rows if r["estado"] == e)]
for k in vacia: ax.add_patch(Rectangle((0, k), len(marcos10), 1, fill=False, ec=GRANATE, lw=1.6, clip_on=False))
ax.set_xlim(0, len(marcos10)); ax.set_ylim(len(estados), 0)
ax.xaxis.tick_top(); ax.set_xticks(np.arange(len(marcos10)) + 0.5); ax.set_xticklabels([lab10.get(m, m) for m in marcos10], fontsize=10.5, color=SUAVE)
ax.set_yticks(np.arange(len(estados)) + 0.5); ax.set_yticklabels(estados, fontsize=10.5)
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0)
caja(ax, [(MARINO, "E: exige evidencia del estado"), (CELESTE, "C: cobertura condicional"), (GRIS, "G: gobierna el dato o el canal"),
          (VACIO, "0: sin obligación identificada")], ncol=4, loc="upper center", bbox_to_anchor=(0.45, -0.01), fontsize=10.5)
save(f, "estados_alta_cuenta")

# ---- monocultura (aprobación 75 %, igual a la proporción de solventes) ----
rho = [0, 0.25, 0.5, 0.75, 1.0]
def mono(appr):
    r2 = np.random.default_rng(2026); [r2.triangular(0, 1, 2, 100000) for _ in range(7)]
    M = 400000; grp = r2.random(M) < 0.20; qtrue = r2.standard_normal(M); solv = qtrue > np.quantile(qtrue, 0.25)
    sig = np.where(grp, 1.0, 0.6); out = []
    for rh in rho:
        eps = r2.standard_normal(M); rej = np.ones(M, bool)
        for j in range(5):
            sc = qtrue + sig * (np.sqrt(rh) * eps + np.sqrt(1 - rh) * r2.standard_normal(M)); rej &= sc < np.quantile(sc, 1 - appr)
        out.append((100 * rej[solv].mean(), 100 * rej[solv & ~grp].mean(), 100 * rej[solv & grp].mean()))
    return np.array(out)
m75 = mono(0.75); m60 = mono(0.60); print("mono75", m75.round(2).tolist()); print("mono60", m60.round(2).tolist())
f, ax = plt.subplots(figsize=(9.7, 4.4))
ax.yaxis.grid(True, color="#EEEEEE"); ax.set_axisbelow(True)
ax.plot(rho, m75[:, 1], "-o", color=MARINO, lw=2, ms=7, label="Con historial")
ax.plot(rho, m75[:, 2], "-o", color=OCRE, lw=2, ms=7, label="Sin historial")
ax.plot(rho, m75[:, 0], color=EJE, lw=1.8, ls=(0, (3, 2)), label="Total")
ax.annotate(f"{es(m75[-1, 2], 1)} %", (1, m75[-1, 2]), textcoords="offset points", xytext=(10, -4), fontsize=11, color=OCRE, fontweight="bold")
ax.annotate(f"{es(m75[-1, 1], 1)} %", (1, m75[-1, 1]), textcoords="offset points", xytext=(10, -4), fontsize=11, color=MARINO, fontweight="bold")
ax.text(0.25, 14.6, f"Con modelos independientes (ρ = 0): {es(m75[0, 1], 2)} % con historial\ny {es(m75[0, 2], 2)} % sin historial. "
        "Aprobación del 75 %, igual a la\nproporción de solventes.", fontsize=10.5, color=SUAVE, va="top")
ax.set_xticks(rho); ax.set_xticklabels(["0\nmodelos\nindependientes", "0,25", "0,50", "0,75", "1\nun mismo\nmodelo"], color=SUAVE)
ax.set_xlabel("Correlación entre los modelos de las cinco entidades (ρ)"); ax.set_ylabel("% de solventes rechazados por las cinco")
ax.set_ylim(0, 18); ax.set_yticks(range(0, 19, 2)); ax.tick_params(axis="y", colors=SUAVE); ax.legend(loc="upper left")
save(f, "monocultura")

# ---- red de obligaciones y relaciones de la matriz ------------
pos = {r["id"]: r for r in lee("red_posiciones")}
nombre_marco = {"RIA": "Reglamento de IA", "RGPD": "RGPD", "CCD2": "Directiva (UE) 2023/2225", "DORA": "DORA",
                "EBA/GL/2020/06": "EBA/GL/2020/06", "Dir. 2014/92/UE": "Directiva 2014/92/UE", "RDL 19/2017": "RDL 19/2017",
                "Ley 10/2010": "Ley 10/2010", "EBA/GL/2023/04": "EBA/GL/2023/04", "AMLR": "AMLR"}
colB = {"RIA": "#0D3B8C", "RGPD": "#2F6FD0", "CCD2": "#6AA8E8", "DORA": "#1B7FA8", "EBA/GL/2020/06": "#A9C9EE",
        "Dir. 2014/92/UE": "#0E5A3A", "RDL 19/2017": "#2E8B57", "Ley 10/2010": "#6CBF86", "EBA/GL/2023/04": "#1F7A6B", "AMLR": "#A6D8B2"}
estilo = {"N": dict(color=TINTA, lw=3.2, ls="-"), "D": dict(color="#8F949B", lw=1.6, ls=(0, (5, 3))),
          "I": dict(color="#8F949B", lw=1.6, ls="-"), "C": dict(color="#4A4F56", lw=2.0, ls=(0, (1, 3)))}
f = plt.figure(figsize=(11, 9.3)); ax = f.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1600); ax.set_ylim(1310, 10); ax.axis("off")
ax.plot([1110, 1110], [20, 1050], color="#C9CDD2", lw=0.8, ls=(0, (3, 4)))
ax.text(40, 38, f"Crédito (evaluación de solvencia): {sum(1 for o in mz.O if o[1] == 'S')} obligaciones", fontsize=15, fontweight="bold", va="center")
ax.text(1140, 38, f"Alta de cuenta: {sum(1 for o in mz.O if o[1] == 'A')} obligaciones", fontsize=15, fontweight="bold", va="center")
for (a, b), r in mz.R.items():
    pa, pb = pos[a], pos[b]
    ax.plot([float(pa["x"]), float(pb["x"])], [float(pa["y"]), float(pb["y"])], solid_capstyle="round", dash_capstyle="round", zorder=1, **estilo[r])
for o in mz.O:
    p = pos[o[0]]; x, y = float(p["x"]), float(p["y"]); c = colB[o[2]]
    if mz.orient(o[0]) == "persona": ax.plot(x, y, "o", ms=11, mfc="white", mec=c, mew=3.2, zorder=3)
    else: ax.plot(x, y, "o", ms=13, mfc=c, mec="white", mew=1.6, zorder=3)
    ax.text(x + float(p["etiqueta_dx"]), y + float(p["etiqueta_dy"]) - 6, o[0], fontsize=13.5, va="center",
            ha={"start": "left", "end": "right", "middle": "center"}[p["alineacion"]], zorder=4)
ly = 1120; paso = 33
ax.plot([40, 1560], [ly - 40, ly - 40], color="#C9CDD2", lw=0.8)
for x, t in ((40, "TIPO DE OBLIGACIÓN"), (480, "RELACIÓN ENTRE NORMAS"), (930, "NORMA")):
    ax.text(x, ly, t, fontsize=11.5, fontweight="bold", color=SUAVE, va="center")
ax.plot(62, ly + 36, "o", ms=13, mfc=colB["RIA"], mec="white"); ax.plot(62, ly + 36 + paso, "o", ms=11, mfc="white", mec=colB["RIA"], mew=3.2)
ax.text(96, ly + 36, "Punto relleno: interna del banco", fontsize=12.5, va="center")
ax.text(96, ly + 36 + paso, "Anillo: de cara a la persona", fontsize=12.5, va="center")
for k, (r, t) in enumerate([("N", "N  integrada por norma expresa"), ("D", "D  mismo fin, definición distinta"),
                            ("I", "I  equivalente o compatible"), ("C", "C  en tensión")]):
    yy = ly + 36 + k * paso
    ax.plot([482, 524], [yy, yy], dash_capstyle="round", **estilo[r]); ax.text(536, yy, t, fontsize=12.5, va="center")
for k, m in enumerate(nombre_marco):
    x = 930 if k < 5 else 1265; yy = ly + 36 + (k % 5) * paso
    ax.plot(x + 22, yy, "o", ms=13, mfc=colB[m], mec="white"); ax.text(x + 56, yy, nombre_marco[m], fontsize=12.5, va="center")
save(f, "red_obligaciones")

# ---- red agrupada por orientación (figura del apartado 4.2) ------------
posO = {r["id"]: r for r in lee("red_posiciones_orientacion")}
X0, AW, Y0, AH = 40, 1520, 95, 960
f = plt.figure(figsize=(11, 8.9)); ax = f.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1600); ax.set_ylim(1285, 10); ax.axis("off")
xd = X0 + 0.6 * AW
ax.plot([xd, xd], [20, Y0 + AH], color="#C9CDD2", lw=0.8, ls=(0, (3, 4)))
n_int = sum(1 for o in mz.O if mz.orient(o[0]) == "interna"); n_per = len(mz.O) - n_int
ax.text(X0 + 0.30 * AW, 38, f"Obligaciones internas del banco: {n_int}", fontsize=15, fontweight="bold", va="center", ha="center")
ax.text(X0 + 0.80 * AW, 38, f"De cara a la persona: {n_per}", fontsize=15, fontweight="bold", va="center", ha="center")
def xy(i): p = posO[i]; return X0 + float(p["x_rel"]) * AW, Y0 + float(p["y_rel"]) * AH
for (a, b), r in mz.R.items():
    (xa, ya), (xb, yb) = xy(a), xy(b)
    ax.plot([xa, xb], [ya, yb], solid_capstyle="round", dash_capstyle="round", zorder=1, **estilo[r])
for o in mz.O:
    x, y = xy(o[0]); c = colB[o[2]]
    if mz.orient(o[0]) == "persona": ax.plot(x, y, "o", ms=11, mfc="white", mec=c, mew=3.2, zorder=3)
    else: ax.plot(x, y, "o", ms=13, mfc=c, mec="white", mew=1.6, zorder=3)
    izq = posO[o[0]]["etiqueta_izquierda"] == "1"
    ax.text(x + (-17 if izq else 17), y, o[0], fontsize=12.5, va="center", ha="right" if izq else "left", zorder=4,
            path_effects=[matplotlib.patheffects.withStroke(linewidth=3, foreground="white")])
ly = 1105; paso = 31
ax.plot([40, 1560], [ly - 38, ly - 38], color="#C9CDD2", lw=0.8)
for x, t in ((40, "TIPO DE OBLIGACIÓN"), (480, "RELACIÓN ENTRE NORMAS"), (930, "NORMA")):
    ax.text(x, ly, t, fontsize=11.5, fontweight="bold", color=SUAVE, va="center")
ax.plot(62, ly + 34, "o", ms=13, mfc=colB["RIA"], mec="white"); ax.plot(62, ly + 34 + paso, "o", ms=11, mfc="white", mec=colB["RIA"], mew=3.2)
ax.text(96, ly + 34, "Punto relleno: interna del banco", fontsize=12.5, va="center")
ax.text(96, ly + 34 + paso, "Anillo: de cara a la persona", fontsize=12.5, va="center")
for k, (r, t) in enumerate([("N", "N  integrada por norma expresa"), ("D", "D  mismo fin, definición distinta"),
                            ("I", "I  equivalente o compatible"), ("C", "C  en tensión")]):
    yy = ly + 34 + k * paso
    ax.plot([482, 524], [yy, yy], dash_capstyle="round", **estilo[r]); ax.text(536, yy, t, fontsize=12.5, va="center")
for k, m in enumerate(nombre_marco):
    x = 930 if k < 5 else 1265; yy = ly + 34 + (k % 5) * paso
    ax.plot(x + 22, yy, "o", ms=13, mfc=colB[m], mec="white"); ax.text(x + 56, yy, nombre_marco[m], fontsize=12.5, va="center")
save(f, "red_orientacion")
print("Figuras guardadas en", HERE)
