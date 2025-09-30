# Fusion 360 script - Parametric Raspberry Pi 5 case with badge pocket
# Run inside Fusion 360 (Scripts & Add-Ins)
# Creates BaseCase, TopCover with badge pocket, and two example badges (NY & LA)
import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

        # PARAMETERS
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
        standoff_height = ensure_param('standoff_height', 5, 'mm')
        badge_width = ensure_param('badge_width', 42, 'mm')
        badge_height = ensure_param('badge_height', 28, 'mm')
        badge_depth = ensure_param('badge_depth', 1, 'mm')
        badge_clearance = ensure_param('badge_clearance', 0.3, 'mm')

        def val(p):
            return float(p.expression)

        rootComp = design.rootComponent
        allOccs = rootComp.occurrences

        # BASE CASE
        transform = adsk.core.Matrix3D.create()
        baseOcc = allOccs.addNewComponent(transform)
        baseComp = adsk.fusion.Component.cast(baseOcc.component)
        baseComp.name = 'BaseCase'
        sketches = baseComp.sketches
        xyPlane = baseComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        rec = sketch.sketchCurves.sketchLines
        L = val(case_length)
        W = val(case_width)
        sketchRect = rec.addCenterPointRectangle(adsk.core.Point3D.create(0,0,0), adsk.core.Point3D.create(L/2, W/2,0))
        prof = sketch.profiles.item(0)
        extrudes = baseComp.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(val(case_height))
        extInput.setDistanceExtent(False, distance)
        ext = extrudes.add(extInput)
        outerBody = ext.bodies.item(0)
        outerBody.name = 'OuterShell'

        # SHELL
        shellFeats = baseComp.features.shellFeatures
        shellInput = shellFeats.createInput(adsk.core.ValueInput.createByReal(val(wall_thickness)))
        shellInput.targetBodies = adsk.core.ObjectCollection.create()
        shellInput.targetBodies.add(outerBody)
        shellFeats.add(shellInput)

        # TOP COVER
        topOcc = allOccs.addNewComponent(adsk.core.Matrix3D.create())
        topComp = adsk.fusion.Component.cast(topOcc.component)
        topComp.name = 'TopCover'
        sketchesTop = topComp.sketches
        topPlane = topComp.xYConstructionPlane
        sketchTop = sketchesTop.add(topPlane)
        recTop = sketchTop.sketchCurves.sketchLines
        recTop.addCenterPointRectangle(adsk.core.Point3D.create(0,0,0), adsk.core.Point3D.create(L/2, W/2,0))
        profTop = sketchTop.profiles.item(0)
        extTopInput = topComp.features.extrudeFeatures.createInput(profTop, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extTopInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(3))
        extTop = topComp.features.extrudeFeatures.add(extTopInput)
        coverBody = extTop.bodies.item(0)
        coverBody.name = 'TopCoverBody'

        # BADGE POCKET
        sketchBadge = sketchesTop.add(coverBody.faces.item(0))
        halfW = val(badge_width)/2
        halfH = val(badge_height)/2
        sketchBadge.sketchCurves.sketchLines.addCenterPointRectangle(adsk.core.Point3D.create(0,0,0), adsk.core.Point3D.create(halfW, halfH, 0))
        profBadge = sketchBadge.profiles.item(0)
        cutInput = topComp.features.extrudeFeatures.createInput(profBadge, adsk.fusion.FeatureOperations.CutFeatureOperation)
        cutInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(val(badge_depth)))
        topComp.features.extrudeFeatures.add(cutInput)

        # TEAM BADGES
        def make_badge(name, initials):
            occ = allOccs.addNewComponent(adsk.core.Matrix3D.create())
            comp = adsk.fusion.Component.cast(occ.component)
            comp.name = name
            sk = comp.sketches.add(comp.xYConstructionPlane)
            bw = val(badge_width) - val(badge_clearance)
            bh = val(badge_height) - val(badge_clearance)
            sk.sketchCurves.sketchLines.addCenterPointRectangle(adsk.core.Point3D.create(0,0,0), adsk.core.Point3D.create(bw/2, bh/2,0))
            try:
                texts = sk.sketchTexts
                textInput = texts.createInput(initialValue=initials, position=adsk.core.Point3D.create(0,0,0), height=10)
                texts.add(textInput)
            except:
                pass
            prof = sk.profiles.item(0)
            comp.features.extrudeFeatures.add(comp.features.extrudeFeatures.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)).setDistanceExtent(False, adsk.core.ValueInput.createByReal(1.8))

        make_badge('TeamBadge_NY', 'NY')
        make_badge('TeamBadge_LA', 'LA')

        if ui:
            ui.messageBox('Parametric Pi5 case + badges created. Edit parameters or import SVG logos as needed.')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    adsk.terminate()
