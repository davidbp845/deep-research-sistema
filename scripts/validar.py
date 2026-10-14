#!/usr/bin/env python3
"""Valida las investigaciones de un proyecto de deep-research y muestra su tablero de avance.

Uso:
    python3 _sistema/scripts/validar.py [slug] [--estado]

Sin slug recorre todas las carpetas de investigaciones/. Con --estado imprime además el
tablero de fases y el recuento de registros. Sale con código 1 si hay errores (los avisos no
cuentan). Las reglas que comprueba están descritas en _sistema/convenciones.md.
"""
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]
INVESTIGACIONES = RAIZ / "investigaciones"

FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID_REF = re.compile(r"(?<![\w-])([CHDPE])-(\d{2,3})(?![\w-])")
ITEM = re.compile(r"^### ([CHDP])-(\d{2,3}) — .+$", re.M)
CAMPO = re.compile(r"^- (\w+): ?(.*)$")
FILA_DATO = re.compile(r"^\|\s*(E-\d{2,3})\s*\|", re.M)
NOMBRE_ITER = re.compile(r"^(F\d{2})-(i\d{2})-(prompt|informe|revision)\.md$")
ARTEFACTOS = [
    (re.compile("[\ue000-\uf8ff]"), "caracteres de uso privado (marcas de cita de ChatGPT)"),
    (re.compile(r"\bcite\w*turn\d|turn\d+(search|view|fetch)\d+"), "marcadores de cita de ChatGPT"),
    (re.compile("【[^】]*】"), "citas 【…】"),
    (re.compile(r"<(div|figure|figcaption|span|sup|br|p)\b", re.I), "HTML"),
]

ESTADOS_FASE = {"pendiente", "preparada", "en-investigacion", "en-revision", "consolidada", "reabierta", "descartada"}
EJECUTORES = {"chatgpt-deep-research", "claude-code", "promotor"}
CLASES = {"inicial", "ampliacion", "repeticion", "verificacion"}
ESTADOS_PROMPT = {"borrador", "enviado", "respondido", "descartado"}
VEREDICTOS = {"pendiente", "aceptado", "aceptado-parcial", "rechazado"}
CONFIANZAS = {"alta", "media-alta", "media", "baja"}

REQUERIDOS = {
    "contexto": [],
    "estado": ["fase_actual", "proximo_paso"],
    "registro": ["registro"],
    "fase": ["fase", "titulo", "estado", "ejecutor", "depende_de", "iteracion_aceptada"],
    "prompt": ["fase", "iteracion", "clase", "estado", "destino"],
    "informe": ["fase", "iteracion", "origen", "fecha_recepcion", "veredicto"],
    "revision": ["fase", "iteracion", "veredicto", "puntuacion"],
    "sintesis": ["fase", "iteraciones_consolidadas", "confianza_global"],
}
ENUMS = {
    ("fase", "estado"): ESTADOS_FASE,
    ("fase", "ejecutor"): EJECUTORES,
    ("prompt", "clase"): CLASES,
    ("prompt", "estado"): ESTADOS_PROMPT,
    ("informe", "veredicto"): VEREDICTOS,
    ("revision", "veredicto"): VEREDICTOS,
    ("sintesis", "confianza_global"): CONFIANZAS,
}
REGISTROS = {
    "conclusiones": ("C", ["estado", "confianza", "origen"], {"solida", "provisional", "debilitada", "invalidada"}),
    "hipotesis": ("H", ["estado", "confianza", "origen"], {"abierta", "apoyada", "refutada", "descartada", "validada"}),
    "decisiones": ("D", ["estado", "origen"], {"propuesta", "adoptada", "revocada"}),
    "preguntas": ("P", ["estado", "prioridad", "responde"], {"abierta", "respondida", "descartada"}),
}


class Informe:
    def __init__(self):
        self.errores, self.avisos = [], []

    def error(self, ruta, msg):
        self.errores.append(f"{ruta}: {msg}")

    def aviso(self, ruta, msg):
        self.avisos.append(f"{ruta}: {msg}")


def leer(ruta):
    """Devuelve (frontmatter, cuerpo); frontmatter es None si falta o no es YAML válido."""
    texto = ruta.read_text(encoding="utf-8")
    if not texto.startswith("---\n"):
        return None, texto
    partes = texto.split("\n---\n", 1)
    if len(partes) < 2:
        return None, texto
    try:
        fm = yaml.safe_load(partes[0][4:]) or {}
    except yaml.YAMLError:
        return None, texto
    return fm, partes[1]


def items_registro(cuerpo):
    """{(prefijo, num): {campo: valor}} de los elementos ### de un registro."""
    items = {}
    bloques = ITEM.split(cuerpo)
    # split devuelve [preambulo, prefijo, num, resto, prefijo, num, resto...]
    for i in range(1, len(bloques) - 2, 3):
        campos = {}
        for linea in bloques[i + 2].splitlines():
            m = CAMPO.match(linea)
            if m:
                campos[m.group(1)] = m.group(2).strip()
        items[(bloques[i], bloques[i + 1])] = campos
    return items


def validar_investigacion(inv, inf):
    rel = lambda p: p.relative_to(RAIZ)
    proyecto = inv / "00_proyecto"
    definidos = set()
    registros = {}

    for nombre in ["01-contexto", "02-estado", "03-datos-clave", "04-hipotesis", "05-conclusiones", "06-decisiones", "07-preguntas"]:
        if not (proyecto / f"{nombre}.md").exists():
            inf.error(rel(proyecto), f"falta {nombre}.md")

    docs = [p for p in inv.rglob("*.md") if "_archivo" not in p.relative_to(inv).parts]
    for ruta in sorted(docs):
        fm, cuerpo = leer(ruta)
        if fm is None:
            inf.error(rel(ruta), "sin frontmatter YAML válido")
            continue
        tipo = fm.get("tipo")
        if tipo not in REQUERIDOS:
            inf.error(rel(ruta), f"tipo desconocido: {tipo!r}")
            continue
        if fm.get("investigacion") != inv.name:
            inf.error(rel(ruta), f"investigacion debe ser {inv.name!r}")
        if not FECHA.match(str(fm.get("fecha_actualizacion", ""))):
            inf.error(rel(ruta), "fecha_actualizacion ausente o no AAAA-MM-DD")
        for campo in REQUERIDOS[tipo]:
            if campo not in fm:
                inf.error(rel(ruta), f"falta el campo {campo!r}")
        for (t, campo), valores in ENUMS.items():
            if t == tipo and campo in fm and fm[campo] not in valores:
                inf.error(rel(ruta), f"{campo}={fm[campo]!r} no es uno de {sorted(valores)}")

        if tipo == "revision" and not (isinstance(fm.get("puntuacion"), int) and 0 <= fm["puntuacion"] <= 20):
            inf.error(rel(ruta), "puntuacion debe ser un entero 0–20")

        if ruta.parent.parent.name == "fases":
            fase_dir = ruta.parent.name[:3]
            if fm.get("fase") not in (None, fase_dir):
                inf.error(rel(ruta), f"fase={fm.get('fase')!r} no coincide con la carpeta {fase_dir}")
            m = NOMBRE_ITER.match(ruta.name)
            if m:
                if m.group(1) != fase_dir:
                    inf.error(rel(ruta), "el prefijo del nombre no coincide con la carpeta")
                if fm.get("iteracion") != m.group(2):
                    inf.error(rel(ruta), f"iteracion={fm.get('iteracion')!r} no coincide con el nombre")
                if m.group(3) != tipo:
                    inf.error(rel(ruta), f"el nombre dice {m.group(3)} pero tipo={tipo}")
            elif ruta.name not in ("ficha.md", "sintesis.md"):
                inf.aviso(rel(ruta), "nombre fuera de convención (FXX-iNN-prompt|informe|revision.md)")

        if tipo == "informe":
            for patron, desc in ARTEFACTOS:
                if patron.search(cuerpo):
                    inf.error(rel(ruta), f"contiene {desc}: normalízalo con /ingerir-informe")

        if tipo == "registro":
            reg = fm.get("registro")
            registros[reg] = (ruta, cuerpo)
            if reg == "datos":
                ids = FILA_DATO.findall(cuerpo)
                for dup in [i for i, n in Counter(ids).items() if n > 1]:
                    inf.error(rel(ruta), f"{dup} duplicado")
                definidos.update(ids)
                continue
            if reg not in REGISTROS:
                inf.error(rel(ruta), f"registro desconocido: {reg!r}")
                continue
            prefijo, req, estados = REGISTROS[reg]
            for (pre, num), campos in items_registro(cuerpo).items():
                ident = f"{pre}-{num}"
                if pre != prefijo:
                    inf.error(rel(ruta), f"{ident} no pertenece a este registro (prefijo {prefijo}-)")
                definidos.add(ident)
                for campo in req:
                    if not campos.get(campo):
                        inf.error(rel(ruta), f"{ident}: falta {campo}")
                if campos.get("estado") and campos["estado"] not in estados:
                    inf.error(rel(ruta), f"{ident}: estado {campos['estado']!r} no es uno de {sorted(estados)}")
                if "confianza" in req and campos.get("confianza") and campos["confianza"] not in CONFIANZAS:
                    inf.error(rel(ruta), f"{ident}: confianza {campos['confianza']!r} no válida")
            # items_registro fusiona los duplicados en un dict; se cuentan sobre el texto
            for ident, n in Counter(re.findall(r"^### ([CHDP]-\d{2,3}) — ", cuerpo, re.M)).items():
                if n > 1:
                    inf.error(rel(ruta), f"{ident} duplicado")

    # Referencias a IDs inexistentes (informes excluidos: el investigador puede citar los suyos)
    for ruta in sorted(docs):
        fm, cuerpo = leer(ruta)
        if not fm or fm.get("tipo") == "informe":
            continue
        for pre, num in set(ID_REF.findall(cuerpo)):
            if f"{pre}-{num}" not in definidos:
                inf.aviso(rel(ruta), f"cita {pre}-{num}, que no existe en su registro")

    fases = inv / "fases"
    for carpeta in sorted(p for p in fases.iterdir() if p.is_dir()) if fases.exists() else []:
        if not re.match(r"^F\d{2}-[a-z0-9-]+$", carpeta.name):
            inf.error(rel(carpeta), "nombre de carpeta de fase fuera de convención (FXX-slug)")
        if not (carpeta / "ficha.md").exists():
            inf.error(rel(carpeta), "falta ficha.md")
            continue
        fm, _ = leer(carpeta / "ficha.md")
        acept = (fm or {}).get("iteracion_aceptada")
        if acept and not (carpeta / f"{carpeta.name[:3]}-{acept}-informe.md").exists():
            inf.error(rel(carpeta / "ficha.md"), f"iteracion_aceptada={acept} sin informe")
        for informe in carpeta.glob("F*-i*-informe.md"):
            if not informe.with_name(informe.name.replace("-informe", "-revision")).exists():
                inf.aviso(rel(informe), "informe sin revisión: ejecuta /ingerir-informe")
    return registros


def tablero(inv, registros):
    print(f"\n## {inv.name}\n")
    fm_estado, _ = leer(inv / "00_proyecto" / "02-estado.md") if (inv / "00_proyecto" / "02-estado.md").exists() else ({}, "")
    print("| Fase | Título | Estado | Ejecutor | Prompts | Informes | Aceptada |")
    print("|---|---|---|---|---|---|---|")
    fases = inv / "fases"
    for carpeta in sorted(p for p in fases.iterdir() if p.is_dir()) if fases.exists() else []:
        fm, _ = leer(carpeta / "ficha.md") if (carpeta / "ficha.md").exists() else ({}, "")
        fm = fm or {}
        informes = sorted(carpeta.glob("F*-i*-informe.md"))
        veredictos = []
        for i in informes:
            fi, _ = leer(i)
            veredictos.append(f"{i.name[4:7]}:{(fi or {}).get('veredicto', '?')}")
        print(f"| {carpeta.name[:3]} | {fm.get('titulo', '?')} | {fm.get('estado', '?')} | {fm.get('ejecutor', '?')} "
              f"| {len(list(carpeta.glob('F*-i*-prompt.md')))} | {', '.join(veredictos) or '—'} "
              f"| {fm.get('iteracion_aceptada') or '—'} |")
    print()
    for reg in ["conclusiones", "hipotesis", "decisiones", "preguntas"]:
        if reg in registros:
            estados = Counter(c.get("estado", "?") for c in items_registro(registros[reg][1]).values())
            print(f"- {reg}: " + ", ".join(f"{n} {e}" for e, n in sorted(estados.items())))
    if "datos" in registros:
        print(f"- datos: {len(FILA_DATO.findall(registros['datos'][1]))} filas")
    if fm_estado:
        print(f"\nFase actual: {fm_estado.get('fase_actual')} · Próximo paso: {fm_estado.get('proximo_paso')}")


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    invs = [INVESTIGACIONES / args[0]] if args else sorted(p for p in INVESTIGACIONES.iterdir() if p.is_dir())
    inf = Informe()
    for inv in invs:
        if not inv.is_dir():
            print(f"No existe la investigación {inv.name}")
            return 1
        registros = validar_investigacion(inv, inf)
        if "--estado" in argv:
            tablero(inv, registros)
    print()
    for a in inf.avisos:
        print(f"AVISO  {a}")
    for e in inf.errores:
        print(f"ERROR  {e}")
    print(f"\n{len(inf.errores)} errores, {len(inf.avisos)} avisos.")
    return 1 if inf.errores else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
