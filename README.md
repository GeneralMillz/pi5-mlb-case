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
