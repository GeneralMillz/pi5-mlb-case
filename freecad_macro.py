# FreeCAD macro - Parametric Raspberry Pi 5 case + badge pocket
from FreeCAD import Base
import FreeCAD, Part, Draft

doc = FreeCAD.newDocument("Pi5_MLB_Case")

# PARAMETERS
case_length = 93.0
case_width  = 64.0
case_height = 30.0
wall_thickness = 2.0
badge_width = 42.0
badge_height = 28.0
badge_depth = 1.0
badge_clearance = 0.3

# BASE CASE
base = Part.makeBox(case_length, case_width, case_height)
base.translate(Base.Vector(-case_length/2, -case_width/2, 0))
inner = Part.makeBox(case_length - 2*wall_thickness, case_width - 2*wall_thickness, case_height - wall_thickness)
inner.translate(Base.Vector(-case_length/2 + wall_thickness, -case_width/2 + wall_thickness, wall_thickness))
hollow = base.cut(inner)
part = doc.addObject("Part::Feature", "BaseCase")
part.Shape = hollow

# TOP COVER
cover_thickness = 3.0
cover = Part.makeBox(case_length, case_width, cover_thickness)
cover.translate(Base.Vector(-case_length/2, -case_width/2, case_height))
cover_part = doc.addObject("Part::Feature", "TopCover")
cover_part.Shape = cover

# BADGE POCKET
pocket = Part.makeBox(badge_width, badge_height, badge_depth)
pocket.translate(Base.Vector(-badge_width/2, -badge_height/2, case_height + cover_thickness - badge_depth))
cover_part.Shape = cover_part.Shape.cut(pocket)

# TEAM BADGES (NY + LA)
badge_thickness = 1.8
badge_NY = Part.makeBox(badge_width - badge_clearance, badge_height - badge_clearance, badge_thickness)
badge_NY.translate(Base.Vector(- (badge_width - badge_clearance)/2, - (badge_height - badge_clearance)/2, case_height + cover_thickness - badge_thickness))
badgeNY_obj = doc.addObject("Part::Feature", "TeamBadge_NY")
badgeNY_obj.Shape = badge_NY

badge_LA = Part.makeBox(badge_width - badge_clearance, badge_height - badge_clearance, badge_thickness)
badge_LA.translate(Base.Vector(- (badge_width - badge_clearance)/2, - (badge_height - badge_clearance)/2, case_height + cover_thickness - badge_thickness))
badgeLA_obj = doc.addObject("Part::Feature", "TeamBadge_LA")
badgeLA_obj.Shape = badge_LA

# Add simple text placeholders
textNY = Draft.makeText(['NY'], point=Base.Vector(-10, -5, case_height + cover_thickness - 0.2), screen=False)
textLA = Draft.makeText(['LA'], point=Base.Vector(-10, -5, case_height + cover_thickness - 0.2), screen=False)

doc.recompute()
print('FreeCAD macro created base case and two badge plates. Import SVG logos as needed.')
