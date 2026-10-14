#!/usr/bin/env bash
# Crea un proyecto de investigaciones (repo contenedor) con este motor como submódulo en _sistema/.
#
# Uso:
#   crear-proyecto.sh <carpeta-del-proyecto> [url-del-motor]
#
# Sin url, usa el remoto "origin" del motor desde el que se ejecuta el script (o el repo público).
# La carpeta no debe existir o debe estar vacía. No crea remoto ni sube nada.
set -euo pipefail

URL_POR_DEFECTO="https://github.com/davidbp845/deep-research-sistema.git"

if [ $# -lt 1 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'
  exit 1
fi

destino="$1"
motor="$(cd "$(dirname "$0")/.." && pwd)"
url="${2:-$(git -C "$motor" remote get-url origin 2>/dev/null || echo "$URL_POR_DEFECTO")}"

if [ -e "$destino" ] && [ -n "$(ls -A "$destino" 2>/dev/null)" ]; then
  echo "error: $destino ya existe y no está vacía" >&2
  exit 1
fi

mkdir -p "$destino"
cd "$destino"
nombre="$(basename "$(pwd)")"

git init -q
git submodule add -q "$url" _sistema

mkdir -p investigaciones .claude/commands .obsidian/snippets
touch investigaciones/.gitkeep

# Comandos de Claude Code: symlinks al motor, para que se actualicen con él
for comando in _sistema/.claude/commands/*.md; do
  ln -s "../../$comando" ".claude/commands/$(basename "$comando")"
done

# Archivos del contenedor a partir de las plantillas
sed "s/{{proyecto}}/$nombre/g" _sistema/plantillas/proyecto/CLAUDE.md > CLAUDE.md
sed "s/{{proyecto}}/$nombre/g" _sistema/plantillas/proyecto/README.md > README.md
cp _sistema/plantillas/proyecto/gitignore .gitignore

# Configuración de partida de Obsidian (copia: cada vault la ajusta a su gusto)
cp _sistema/obsidian/*.json .obsidian/
cp _sistema/obsidian/snippets/*.css .obsidian/snippets/

git add -A
git commit -q -m "Proyecto de investigaciones creado con deep-research-sistema"

cat <<FIN
Proyecto creado en $(pwd)

Siguientes pasos:
  1. pip install pyyaml            (lo necesita el validador)
  2. Abre la carpeta como vault en Obsidian (opcional, pero es como mejor se lee).
  3. cd "$(pwd)" && claude
  4. /nueva-investigacion <slug>   (te entrevista para el contexto y crea las fases)
FIN
