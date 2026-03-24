#!/usr/bin/env python3
"""
generateur_fiches.py
--------------------
Génère une feuille HTML format A4 épurée (fond blanc) à partir d'un fichier
d'instructions pour l'activité débranchée "Système d'Exploitation Humain".

Usage :
    python generateur_fiches.py <fichier_instructions> [-o sortie.html]

Format du fichier d'entrée :
    PID: <numero>
    PRIORITE: <1|2|3>
    (ligne vide optionnelle)
    INSTRUCTION_1
    INSTRUCTION_2
    ...
    ---          <- séparateur entre deux fiches

Instructions reconnues :
    PRENDRE(Couleur)
    POSER(Couleur)
    DESSINER(Couleur, [Cases...])
"""

import argparse
import sys
import re
from pathlib import Path
from html import escape
from datetime import datetime


# ---------------------------------------------------------------------------
# Couleurs associées aux marqueurs
# ---------------------------------------------------------------------------
COULEUR_CSS = {
    "ROUGE": "#d32f2f",
    "BLEU":  "#1565c0",
    "VERT":  "#2e7d32",
    "NOIR":  "#212121",
}

COULEUR_BG = {
    "ROUGE": "#ffebee",
    "BLEU":  "#e3f2fd",
    "VERT":  "#e8f5e9",
    "NOIR":  "#f5f5f5",
}

# Niveau de priorite -> libelle + couleur badge
PRIORITE_INFO = {
    1: {"label": "HAUTE",   "color": "#d32f2f", "bg": "#ffebee"},
    2: {"label": "MOYENNE", "color": "#f57c00", "bg": "#fff3e0"},
    3: {"label": "BASSE",   "color": "#388e3c", "bg": "#e8f5e9"},
}


# ---------------------------------------------------------------------------
# Parsing du fichier d'instructions
# ---------------------------------------------------------------------------
def parse_instruction_file(filepath: str) -> list:
    """
    Lit le fichier et retourne une liste de processus.
    Chaque processus est un dict {'pid': str, 'priorite': int, 'instructions': [str]}.
    """
    text = Path(filepath).read_text(encoding="utf-8")

    # Separer les blocs de fiches
    raw_blocks = re.split(r"^\s*---+\s*$", text, flags=re.MULTILINE)

    processes = []
    for block in raw_blocks:
        lines = [l.rstrip() for l in block.splitlines()]
        # Supprimer lignes vides et commentaires
        lines = [l for l in lines if l and not l.startswith("#")]

        if not lines:
            continue

        pid          = None
        priorite     = 2       # valeur par defaut
        instructions = []

        for line in lines:
            m_pid  = re.match(r"(?i)PID\s*:\s*(\S+)", line)
            m_prio = re.match(r"(?i)PRIORITE\s*:\s*(\d+)", line)

            if m_pid:
                pid = m_pid.group(1)
            elif m_prio:
                p = int(m_prio.group(1))
                priorite = max(1, min(3, p))   # borne [1,3]
            else:
                # Normaliser l'instruction : espaces superflus
                inst = re.sub(r"\s+", " ", line).strip()
                if inst:
                    instructions.append(inst)

        if pid is None:
            print("AVERTISSEMENT : Bloc sans PID ignore.", file=sys.stderr)
            continue
        if not instructions:
            print(f"AVERTISSEMENT : PID {pid} : aucune instruction trouvee.", file=sys.stderr)
            continue

        processes.append({"pid": pid, "priorite": priorite, "instructions": instructions})

    return processes


# ---------------------------------------------------------------------------
# Rendu d'une instruction : icone + texte colore
# ---------------------------------------------------------------------------
def render_instruction(instruction: str) -> str:
    """Retourne le HTML interne d'une ligne d'instruction."""

    m_prendre  = re.match(r"(?i)(PRENDRE)\((\w+)\)", instruction)
    m_poser    = re.match(r"(?i)(POSER)\((\w+)\)", instruction)
    m_dessiner = re.match(
        r"(?i)(DESSINER)\((\w+)\s*,\s*\[([^\]]*)\]\s*\)", instruction
    )

    if m_prendre:
        verb, couleur = m_prendre.group(1).upper(), m_prendre.group(2).upper()
        color = COULEUR_CSS.get(couleur, "#333")
        bg    = COULEUR_BG.get(couleur, "#fafafa")
        icon  = "&#x2B07;"   # fleche bas
        detail = (
            f'<span class="verb">{verb}</span>'
            f'(<span class="couleur" style="color:{color};background:{bg};">'
            f'{couleur}</span>)'
        )

    elif m_poser:
        verb, couleur = m_poser.group(1).upper(), m_poser.group(2).upper()
        color = COULEUR_CSS.get(couleur, "#333")
        bg    = COULEUR_BG.get(couleur, "#fafafa")
        icon  = "&#x2B06;"   # fleche haut
        detail = (
            f'<span class="verb">{verb}</span>'
            f'(<span class="couleur" style="color:{color};background:{bg};">'
            f'{couleur}</span>)'
        )

    elif m_dessiner:
        verb    = m_dessiner.group(1).upper()
        couleur = m_dessiner.group(2).upper()
        cases   = m_dessiner.group(3)
        color   = COULEUR_CSS.get(couleur, "#333")
        bg      = COULEUR_BG.get(couleur, "#fafafa")
        icon    = "&#x270F;"  # crayon
        case_list  = [c.strip() for c in cases.split(",") if c.strip()]
        cases_html = " ".join(
            f'<span class="case-badge" style="border-color:{color};color:{color};">'
            f'{escape(c)}</span>'
            for c in case_list
        )
        detail = (
            f'<span class="verb">{verb}</span>'
            f'(<span class="couleur" style="color:{color};background:{bg};">'
            f'{couleur}</span>, [{cases_html}])'
        )

    else:
        # Instruction generique non reconnue
        icon   = "&bull;"
        detail = f'<span class="verb-generic">{escape(instruction)}</span>'

    return f'<span class="inst-icon">{icon}</span>{detail}'


# ---------------------------------------------------------------------------
# Generation HTML d'une fiche A4
# ---------------------------------------------------------------------------
def render_process_card(proc: dict) -> str:
    """Retourne le HTML d'une fiche pour un processus (bloc A4)."""
    pid      = escape(str(proc["pid"]))
    priorite = proc["priorite"]
    pinfo    = PRIORITE_INFO.get(priorite, PRIORITE_INFO[2])

    rows = []
    for i, inst in enumerate(proc["instructions"], start=1):
        inst_html = render_instruction(inst)
        rows.append(f"""        <tr>
            <td class="col-num">{i}</td>
            <td class="col-check"><span class="checkbox"></span></td>
            <td class="col-inst">{inst_html}</td>
        </tr>""")

    rows_html = "\n".join(rows)
    today     = datetime.today().strftime("%d/%m/%Y")

    return f"""
    <div class="fiche page-break">

        <header class="fiche-header">
            <div class="pid-block">
                <span class="pid-label">PID</span>
                <span class="pid-value">{pid}</span>
            </div>
            <div class="title-block">
                <span class="activity-label">Activit&#233; D&#233;branch&#233;e</span>
                <span class="activity-sub">Syst&#232;me d&#8217;Exploitation</span>
            </div>
            <div class="prio-block"
                 style="background:{pinfo['bg']};border-color:{pinfo['color']};">
                <span class="prio-label" style="color:{pinfo['color']};">PRIORIT&#201;</span>
                <span class="prio-num"   style="color:{pinfo['color']};">{priorite}</span>
                <span class="prio-text"  style="color:{pinfo['color']};">{pinfo['label']}</span>
            </div>
        </header>

        <div class="rules-strip">
            <span>&#x2B07; <strong>PRENDRE</strong> le feutre</span>
            <span>&#x270F; <strong>DESSINER</strong> les cases</span>
            <span>&#x2B06; <strong>POSER</strong> le feutre</span>
            <span class="rule-quantum">Quantum&nbsp;: <strong>1&nbsp;ligne&nbsp;/ tour</strong></span>
        </div>

        <table class="inst-table">
            <thead>
                <tr>
                    <th class="col-num">#</th>
                    <th class="col-check">&#x2713;</th>
                    <th class="col-inst">Instruction</th>
                </tr>
            </thead>
            <tbody>
{rows_html}
            </tbody>
        </table>

        <footer class="fiche-footer">
            <div class="footer-hint">
                &#x2714; Coche la case <strong>uniquement</strong> si l&#8217;action est
                <strong>termin&#233;e</strong>.&nbsp;
                Si <em>PRENDRE</em> &#233;choue &#8594; va en file <strong>BLOQU&#201;</strong> (droite).
            </div>
            <div class="footer-meta">PID&nbsp;{pid} &mdash; {today}</div>
        </footer>

    </div>"""


# ---------------------------------------------------------------------------
# Document HTML complet
# ---------------------------------------------------------------------------
def build_html_document(processes: list) -> str:
    cards_html = "\n".join(render_process_card(p) for p in processes)

    return """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fiches Processus &#8212; Activit&#233; D&#233;branch&#233;e SE</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;700&family=IBM+Plex+Sans:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        /* ============================================================
           RESET & BASE
        ============================================================ */
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            background: #d8d8d8;
            font-family: 'IBM Plex Sans', Arial, sans-serif;
            color: #111;
            padding: 20px;
        }

        /* ============================================================
           FORMAT A4
        ============================================================ */
        .fiche {
            width: 210mm;
            min-height: 297mm;
            background: #ffffff;
            margin: 0 auto 28px auto;
            padding: 14mm 16mm 12mm 16mm;
            display: flex;
            flex-direction: column;
            box-shadow: 0 4px 24px rgba(0,0,0,.20);
            position: relative;
        }

        /* ============================================================
           EN-TETE
        ============================================================ */
        .fiche-header {
            display: flex;
            align-items: stretch;
            border: 3px solid #111;
            border-radius: 6px;
            overflow: hidden;
            margin-bottom: 10px;
        }

        .pid-block {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 12px 22px;
            background: #111;
            color: #fff;
            min-width: 90px;
            gap: 2px;
        }
        .pid-label {
            font-size: 8.5pt;
            letter-spacing: 3px;
            font-weight: 700;
            opacity: .65;
            text-transform: uppercase;
        }
        .pid-value {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 30pt;
            font-weight: 700;
            line-height: 1;
        }

        .title-block {
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 12px 22px;
            flex: 1;
            border-left: 3px solid #111;
            border-right: 3px solid #111;
        }
        .activity-label {
            font-size: 14pt;
            font-weight: 700;
            letter-spacing: .5px;
            color: #111;
        }
        .activity-sub {
            font-size: 8.5pt;
            color: #666;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: 4px;
        }

        .prio-block {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 12px 22px;
            min-width: 100px;
            gap: 1px;
        }
        .prio-label {
            font-size: 7pt;
            letter-spacing: 2px;
            font-weight: 700;
            text-transform: uppercase;
        }
        .prio-num {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 28pt;
            font-weight: 700;
            line-height: 1;
        }
        .prio-text {
            font-size: 7.5pt;
            font-weight: 600;
            letter-spacing: 1px;
        }

        /* ============================================================
           BANDEAU REGLES
        ============================================================ */
        .rules-strip {
            display: flex;
            align-items: center;
            gap: 0;
            background: #f4f4f4;
            border: 1.5px solid #ccc;
            border-radius: 5px;
            padding: 7px 14px;
            font-size: 8pt;
            color: #333;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }
        .rules-strip span {
            padding: 0 12px;
            border-right: 1px solid #bbb;
        }
        .rules-strip span:first-child { padding-left: 0; }
        .rules-strip span:last-child  { border-right: none; }
        .rule-quantum {
            margin-left: auto;
            background: #111;
            color: #fff;
            padding: 3px 12px;
            border-radius: 20px;
            border-right: none !important;
            white-space: nowrap;
        }

        /* ============================================================
           TABLE D'INSTRUCTIONS
        ============================================================ */
        .inst-table {
            width: 100%;
            border-collapse: collapse;
            flex: 1;
        }
        .inst-table thead tr {
            background: #111;
            color: #fff;
        }
        .inst-table th {
            padding: 8px 10px;
            font-size: 8.5pt;
            letter-spacing: 1px;
            text-transform: uppercase;
            font-weight: 700;
        }
        .inst-table tbody tr {
            border-bottom: 1.5px solid #e4e4e4;
        }
        .inst-table tbody tr:last-child {
            border-bottom: none;
        }
        .inst-table tbody tr:nth-child(even) {
            background: #fafafa;
        }
        .inst-table tbody tr:hover {
            background: #f0f4ff;
        }

        /* Colonnes */
        .col-num {
            width: 36px;
            text-align: center;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 9pt;
            color: #999;
            padding: 11px 6px;
        }
        .col-check {
            width: 48px;
            text-align: center;
            padding: 11px 4px;
        }
        .col-inst {
            padding: 11px 14px;
            font-size: 11.5pt;
            line-height: 1.5;
        }

        /* Case a cocher dessinee en CSS pur */
        .checkbox {
            display: inline-block;
            width: 24px;
            height: 24px;
            border: 2.5px solid #444;
            border-radius: 4px;
            background: #fff;
            vertical-align: middle;
        }

        /* Rendu des instructions */
        .verb {
            font-family: 'IBM Plex Mono', monospace;
            font-weight: 700;
            font-size: 10.5pt;
            color: #111;
        }
        .verb-generic {
            font-family: 'IBM Plex Mono', monospace;
            color: #555;
        }
        .couleur {
            font-family: 'IBM Plex Mono', monospace;
            font-weight: 700;
            font-size: 10pt;
            padding: 2px 8px;
            border-radius: 4px;
            margin: 0 2px;
        }
        .case-badge {
            display: inline-block;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 8.5pt;
            font-weight: 700;
            border: 1.5px solid;
            border-radius: 3px;
            padding: 1px 5px;
            margin: 1px 2px;
        }
        .inst-icon {
            display: inline-block;
            width: 22px;
            text-align: center;
            font-size: 11pt;
            margin-right: 6px;
            opacity: .55;
        }

        /* ============================================================
           PIED DE PAGE
        ============================================================ */
        .fiche-footer {
            margin-top: 14px;
            padding-top: 10px;
            border-top: 2px dashed #d0d0d0;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            gap: 20px;
        }
        .footer-hint {
            font-size: 8pt;
            color: #555;
            line-height: 1.6;
            max-width: 75%;
        }
        .footer-meta {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 7.5pt;
            color: #bbb;
            text-align: right;
            white-space: nowrap;
        }

        /* ============================================================
           IMPRESSION
        ============================================================ */
        @media print {
            body { background: white; padding: 0; }
            .fiche {
                box-shadow: none;
                margin: 0;
                page-break-after: always;
            }
            .fiche:last-child { page-break-after: auto; }
        }

        .page-break       { page-break-after: always; }
        .page-break:last-child { page-break-after: auto; }
    </style>
</head>
<body>

""" + cards_html + """

</body>
</html>"""


# ---------------------------------------------------------------------------
# Point d'entree
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Genere des fiches HTML A4 pour l'activite debranchee SE.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "input",
        metavar="FICHIER_INSTRUCTIONS",
        help="Fichier texte contenant les fiches (ex: instructions.txt)",
    )
    parser.add_argument(
        "-o", "--output",
        metavar="SORTIE",
        default=None,
        help="Fichier HTML de sortie (defaut : <input>_fiches.html)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERREUR : Fichier introuvable : {args.input}", file=sys.stderr)
        sys.exit(1)

    output_path = (
        Path(args.output) if args.output
        else input_path.with_name(input_path.stem + "_fiches.html")
    )

    print(f"Lecture de : {input_path}")
    processes = parse_instruction_file(str(input_path))

    if not processes:
        print("ERREUR : Aucun processus valide trouve dans le fichier.", file=sys.stderr)
        sys.exit(1)

    print(f"{len(processes)} fiche(s) trouvee(s) : {[p['pid'] for p in processes]}")

    html = build_html_document(processes)
    output_path.write_text(html, encoding="utf-8")

    print(f"Fichier genere : {output_path}")


if __name__ == "__main__":
    main()
