# Raspberry Pi 5 MLB Case - Parametric Template

## Contents
- fusion_template.py — Fusion 360 script
- freecad_macro.py — FreeCAD macro
- README.md — instructions

## Usage (Fusion 360)
1. Open Fusion 360 → Scripts & Add-Ins → + → Add `fusion_template.py`.
2. Run script → generates:
   - BaseCase
   - TopCover with badge pocket
   - TeamBadge_NY and TeamBadge_LA
3. Edit parameters: Modify → Change Parameters
4. To add logos: open TeamBadge sketch → Insert SVG or use Text → Extrude

## Usage (FreeCAD)
1. Open FreeCAD → Macros → Create new macro → paste `freecad_macro.py`
2. Run → creates base case + two badges
3. Edit parameters at top or use Spreadsheet
4. Import SVG logos into badge plates as needed

## Tips
- Clearance: 0.2–0.3 mm for badges
- Magnet pockets or snap tabs possible for removable badges
- Check port/vent clearances after generation


Raspberry Pi 5 MLB Case — Parametric Template

A fully parametric Raspberry Pi 5 case with:

Base case

Top cover with removable badge pocket

30 MLB team badges (one per team)

All badges are generated automatically from SVG logos and exported as STL files for 3D printing.

📂 Repository Structure
pi5-mlb-case/
│
├── fusion_template.py          # Main Fusion 360 script (creates case + badges + exports STL)
├── freecad_macro.py            # Optional FreeCAD macro
├── README.md                   # This file
├── mlb_teams.csv               # CSV mapping team initials → SVG filenames
└── mlb_svgs/                   # Folder containing 30 SVG logos (or placeholders)

🛠 Requirements

Fusion 360 installed (Download Here
)

mlb_teams.csv (included in repo)

SVG logos for each MLB team in mlb_svgs/

Folder for STL exports (must exist before running the script)

The script automatically reads the CSV, imports each SVG, extrudes badges, and exports STL files. No manual work needed.

📁 Folder Setup

Create folder for SVGs:

C:/Users/Partner/Desktop/mlb_svgs/


Place all 30 team SVG logos and mlb_teams.csv in this folder.

Create folder for STL exports:

C:/Users/Partner/Desktop/mlb_stl/


You can adjust these paths directly in fusion_template.py if needed.

⚡ Step-by-Step Instructions

Open Fusion 360 → Scripts & Add-Ins.

Load fusion_template.py.

Confirm CSV and SVG files are in the correct folder (mlb_svgs/).

Ensure the STL export folder exists (mlb_stl/).

Click Run.

What happens automatically:

Base case + top cover + badge pocket created.

30 MLB badges generated from SVGs.

Each badge exported as an STL to the export folder.

🖨 Printing Tips

If a badge doesn’t fit perfectly, adjust badge_clearance in fusion_template.py.

Badges can be printed in different colors using printer pauses or dual extrusion.

Check SVG quality — clean SVGs will print sharper.

⚙ Optional Enhancements

Add magnet pockets for removable badges.

Add fillets or rounded edges for smoother prints.

Replace placeholder SVGs with official logos or custom designs.

🔧 Example Paths (Beginner-Friendly)
SVG folder:      C:/Users/Partner/Desktop/mlb_svgs/
Export folder:   C:/Users/Partner/Desktop/mlb_stl/
CSV file:        C:/Users/Partner/Desktop/mlb_svgs/mlb_teams.csv


Make sure these folders exist. If your partner wants, they can edit the paths directly in fusion_template.py to match their system.

✅ Quick Start Summary

Download this repo.

Put SVGs and CSV in mlb_svgs/.

Create STL export folder.

Open Fusion 360 → Load fusion_template.py → Run.

Print STL files from export folder.

All 30 MLB badges ready with minimal setup.
