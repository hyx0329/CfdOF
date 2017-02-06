# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2015 - Bernd Hahnebach <bernd@bimstatik.org>            *
# *   Copyright (c) 2017 - CSIR, South Africa                               *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

__title__ = "Fluid boundary object"
__author__ = ""
__url__ = "http://www.freecadweb.org"

## @package CfdFluidBoundary
#  \ingroup CFD

import FreeCAD
import Part

class PartFeature:
    "Part containing CfdFluidBoundary faces"
    def __init__(self, obj):
        obj.Proxy = self

class _CfdFluidBoundary(PartFeature):
    "The CfdFluidBoundary object"
    def __init__(self, obj):
        PartFeature.__init__(self, obj)

        obj.Proxy = self
        self.Type = "CfdFluidBoundary"
        obj.addProperty("App::PropertyPythonObject", "References")
        obj.addProperty("App::PropertyPythonObject", "BoundarySettings")

        # obj.addProperty("App::PropertyPythonObject","partNameList").partNameList = []
        obj.addProperty("App::PropertyLinkList","faceList")

        # Default settings
        obj.References = []
        obj.BoundarySettings = {"BoundaryType": "wall",
                                "BoundarySubtype": "fixed",
                                "VelocityIsCartesian": True,
                                "Ux": "0 m/s",    # Units.Quantity not JSON serialisable, so use string
                                "Uy": "0 m/s",
                                "Uz": "0 m/s",
                                "VelocityMag": "0 m/s",
                                "DirectionFace": "",
                                "ReverseNormal": False,
                                "Pressure": "0 kg*m/s^2",
                                "SlipRatio": "0",
                                "VolFlowRate": "0.0 m^3/s",
                                "MassFlowRate": "0.0 kg/s",
                                "TurbulenceSpecification": "intensity&DissipationRate",
                                "ThermalBoundaryType": "fixedValue"}

    def execute(self, obj):
        '''Create compound part at recompute'''
        docName = str(obj.Document.Name)
        doc = FreeCAD.getDocument(docName)
        listOfFaces = []
        for i in range(len(obj.References)):
            ref = obj.References[i]
            selection_object = doc.getObject(ref[0]) # Check that object is always stored in [0] and what happens if it is a compound.
            listOfFaces.append(selection_object.Shape.getElement(ref[1]))
        if len(listOfFaces)>0:
            obj.Shape = Part.makeCompound(listOfFaces)
        self.updateBoundaryColors(obj)
        return

    def updateBoundaryColors(self,obj):
        vobj = obj.ViewObject
        vobj.Transparency = 20
        if obj.BoundarySettings['BoundaryType'] == 'wall':
            vobj.ShapeColor = (0.1, 0.1, 0.1)  # Dark grey
        elif obj.BoundarySettings['BoundaryType'] == 'inlet':
            vobj.ShapeColor = (0.0, 1.0, 0.0)  # Green
        elif obj.BoundarySettings['BoundaryType'] == 'outlet':
            vobj.ShapeColor = (1.0, 0.0, 0.0)  # Red
        elif obj.BoundarySettings['BoundaryType'] == 'interface':
            vobj.ShapeColor = (0.0, 0.0, 1.0)  # Blue
        else:
            vobj.ShapeColor = (1.0, 1.0, 1.0)  # White

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None