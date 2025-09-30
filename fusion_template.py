# Fusion 360 script: Pi 5 case + all 30 MLB badges + STL export + CSV support
# Place team SVGs in svg_folder, create export_folder for STL outputs
# Place CSV file in svg_folder as mlb_teams.csv
# Run inside Fusion 360 (Scripts & Add-Ins)

import adsk.core, adsk.fusion, adsk.cam, traceback, os, csv

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct
        rootComp = design.rootComponent
        allOccs = rootComp.occurrences

        # ===== PARAMETERS =====
        params = design.userParameters
        def ensure_param(name, value, unit):
            try:
                return params.itemByName(name)
            except:
                return params.add(name, adsk.core.ValueInput.createByString(f"{value}{unit}"), name, '')
        case_length = ensure_param('case_length', 93, 'mm')
        case_width  = ensure_param('case_width', 64, 'mm')
        case_height = ensure_param('case_height', 30, 'mm')
        wall_thickness = ensure_param('wall_thickness', 2, 'mm')
        badge_width = ensure_param('badge_width', 42, 'mm')
        badge_height = ensure_param('badge_height', 28, 'mm')
        badge_depth = ensure_param('badge_depth', 1, 'mm')
        badge_clearance = ensure_param('badge_clearance', 0.3, 'mm')

        def val(p):
            return float(p.expression)

        # ===== FOLDERS =====
        svg_folder = "C:/Users/You/Desktop/mlb_svgs/"       # <--- CHANGE to your folder
        export_folder = "C:/Users/You/Desktop/mlb_stl/"     # <--- CHANGE to your folder
        csv_file = os.path.join(svg_folder, "mlb_teams.csv") # CSV: Team,SVG

        # ===== READ CSV =====
        teams = []
        team_svgs = {}
        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                team = row['Team']
                svg_file = row['SVG']
                teams.append(team)
                team_svgs[team] = svg_file

        # ===== BASE CASE =====
        transform = adsk.core.Matrix3D.create()
        baseOcc = allOccs.addNewComponent(transform)
        baseComp = adsk.fusion.Component.cast(baseOcc.component)
        baseComp.name = 'BaseCase'
        sketch = baseComp.sketches.add(baseComp.xYConstructionPlane)
        rec = sketch.sketchCurves.sketchLines
        L = val(case_length)
        W = val(case_width)
        rec.addCenterPointRectangle(adsk.core.Point3D.create(0,0,0), adsk.core.Point3D.create(L/2, W/2,0))
        prof = sketch.profiles.item(0)
        ext = baseComp.features.extrudeFeatures.add(baseComp.features.extrudeFeatures.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation))
        ext.setDistanceExtent(False, adsk.core.ValueInput.createByReal(val(case_height)))
        outerBody = ext.bodies.item(0)
        shellFeats = baseComp.features.shellFeatures
        shellInput = shellFeats.createInput(adsk.core.ValueInput.createByReal(val(wall_thickness)))
        shellInput.targetBodies = adsk.core.ObjectCollection.create()
        shellInput.targetBodies.add(outerBody)
        shellFeats.add(shellInput)

        # ===== TOP COVER =====
        topOcc = allOccs.addNewComponent(adsk.core.Matrix3D.create())
        topComp = adsk.fusion.Component.cast(topOcc.component)
        topComp.name = 'TopCover'
        sketchTop = topComp.sketches.add(topComp.xYConstructionPlane)
        sketchTop.sketchCurves.sketchLines.addCenterPointRectangle(adsk.core.Point3D.create(0,0,0), adsk.core.Point3D.create(L/2, W/2,0))
        profTop = sketchTop.profiles.item(0)
        extTop = topComp.features.extrudeFeatures.add(topComp.features.extrudeFeatures.createInput(profTop, adsk.fusion.FeatureOperations.NewBodyFeatureOperation))
        extTop.setDistanceExtent(False, adsk.core.ValueInput.createByReal(3))
        coverBody = extTop.bodies.item(0)

        # Badge pocket
        sketchBadge = topComp.sketches.add(coverBody.faces.item(0))
        halfW = val(badge_width)/2
        halfH = val(badge_height)/2
        sketchBadge.sketchCurves.sketchLines.addCenterPointRectangle(adsk.core.Point3D.create(0,0,0), adsk.core.Point3D.create(halfW, halfH,0))
        profBadge = sketchBadge.profiles.item(0)
        cutInput = topComp.features.extrudeFeatures.createInput(profBadge, adsk.fusion.FeatureOperations.CutFeatureOperation)
        cutInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(val(badge_depth)))
        topComp.features.extrudeFeatures.add(cutInput)

        # ===== CREATE TEAM BADGES AND EXPORT STL =====
        for team in teams:
            occ = allOccs.addNewComponent(adsk.core.Matrix3D.create())
            comp = adsk.fusion.Component.cast(occ.component)
            comp.name = f"TeamBadge_{team}"

            # Sketch badge base
            sk = comp.sketches.add(comp.xYConstructionPlane)
            bw = val(badge_width) - val(badge_clearance)
            bh = val(badge_height) - val(badge_clearance)
            sk.sketchCurves.sketchLines.addCenterPointRectangle(adsk.core.Point3D.create(0,0,0), adsk.core.Point3D.create(bw/2, bh/2,0))

            # Import SVG
            svg_file = team_svgs.get(team)
            if svg_file:
                svg_path = os.path.join(svg_folder, svg_file)
                try:
                    importMgr = app.importManager
                    importOptions = importMgr.createSVGImportOptions(svg_path)
                    importMgr.importToTarget(importOptions, sk)
                except:
                    print(f"SVG import failed for {team}")
            else:
                print(f"No SVG for {team}")

            # Extrude badge
            profs = sk.profiles
            if profs.count > 0:
                prof = profs.item(0)
                extFeat = comp.features.extrudeFeatures.add(comp.features.extrudeFeatures.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation))
                extFeat.setDistanceExtent(False, adsk.core.ValueInput.createByReal(1.8))

            # Export STL
            try:
                bodies = adsk.core.ObjectCollection.create()
                for body in comp.bodies:
                    bodies.add(body)
                exportMgr = design.exportManager
                stlOptions = exportMgr.createSTLExportOptions(bodies, os.path.join(export_folder, f"{team}.stl"))
                exportMgr.execute(stlOptions)
            except:
                print(f"Failed STL export for {team}")

        if ui:
            ui.messageBox('All MLB badges created and exported as STL!')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    adsk.terminate()
