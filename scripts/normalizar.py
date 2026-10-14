#!/usr/bin/env python3
"""Limpia un informe pegado desde ChatGPT sin tocar su contenido.

Uso:
    python3 _sistema/scripts/normalizar.py <entrada.md> <salida.md>

Quita los artefactos de la interfaz (citas internas, entidades, caracteres de uso privado) y los
envoltorios HTML, y avisa de lo que no puede arreglar solo (Mermaid, frontmatter previo). Nunca
reescribe texto: lo que cambie de contenido va a la revisión, no aquí. Ver
_sistema/convenciones.md#normalización-de-informes.
"""
import re
import sys
from pathlib import Path

# ChatGPT delimita sus marcas con \ue200 (inicio), \ue202 (separador) y \ue201 (fin)
ENTIDAD = re.compile("\ue200entity\ue202(\\[.*?\\])\ue201", re.S)
MARCA = re.compile("[ \t]?\ue200[a-z_]*\ue202.*?\ue201", re.S)
RESTO_CITA = re.compile(r"\s?(?:file)?cite(?:turn\d+\w+?\d+)+")
USO_PRIVADO = re.compile("[\ue000-\uf8ff]")
CORCHETES = re.compile("【[^】]*】")
HTML_VACIO = re.compile(r'<div style="page-break[^"]*"></div>\n?|</?(?:div|span|figure|sup)[^>]*>\n?', re.I)
FIGCAPTION = re.compile(r"<figcaption>(.*?)</figcaption>", re.S)
BR = re.compile(r"<br\s*/?>", re.I)
UTM = re.compile(r"([?&])utm_source=chatgpt\.com&?")


def nombre_entidad(m):
    # entity["tipo","Nombre visible",...] → Nombre visible
    partes = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
    return partes[1] if len(partes) > 1 else ""


def normalizar(texto):
    cambios = {}

    def contar(nombre, patron, repl, t):
        nuevo, n = patron.subn(repl, t)
        if n:
            cambios[nombre] = cambios.get(nombre, 0) + n
        return nuevo

    t = contar("entidades", ENTIDAD, nombre_entidad, texto)
    t = contar("marcas de cita", MARCA, "", t)
    t = contar("restos de cita", RESTO_CITA, "", t)
    t = contar("caracteres de uso privado", USO_PRIVADO, "", t)
    t = contar("citas 【】", CORCHETES, "", t)
    t = contar("figcaption", FIGCAPTION, r"*\1*", t)
    t = contar("HTML", HTML_VACIO, "", t)
    t = contar("<br>", BR, "  \n", t)
    t = contar("utm_source=chatgpt.com", UTM, r"\1", t)
    t = re.sub(r"[?&]\)", ")", t)
    t = re.sub(r"[ \t]+\n", "\n", t)
    avisos = []
    if "```mermaid" in t:
        avisos.append("contiene Mermaid (se deja; anotarlo en la revisión)")
    if t.startswith("---\n"):
        avisos.append("ya trae frontmatter: se sustituirá por el del sistema")
    return t, cambios, avisos


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    texto = Path(sys.argv[1]).read_text(encoding="utf-8")
    limpio, cambios, avisos = normalizar(texto)
    Path(sys.argv[2]).write_text(limpio, encoding="utf-8")
    for nombre, n in cambios.items():
        print(f"- eliminado/sustituido: {n} × {nombre}")
    for a in avisos:
        print(f"- AVISO: {a}")
    if not cambios:
        print("- sin artefactos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
