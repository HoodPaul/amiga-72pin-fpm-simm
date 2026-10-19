#!/usr/bin/env python3
"""Colour A7's exact native silkscreen and CAD pads for an unpopulated preview.

Run with a Python environment containing pcbnew. SVG input is KiCad's current
silk-front.svg / silk-rear.svg plot, including Edge.Cuts. Raster output uses
cairosvg through the default python3 interpreter if it is not installed here.
No project, board, copper or fabrication files are changed.
"""
from pathlib import Path
import copy
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

import pcbnew

ROOT = Path(__file__).resolve().parents[1]
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def tag(name):
    return "{" + SVG_NS + "}" + name


def numbers(value):
    return [float(n) for n in re.findall(r"-?(?:\d+\.?\d*|\.\d+)", value)]


def same(a, b):
    return abs(a[0] - b[0]) < 0.0002 and abs(a[1] - b[1]) < 0.0002


def outline_path(edge_group):
    """Connect native KiCad line/arc segments without approximating curves."""
    edges = []
    for node in edge_group:
        if node.tag != tag("path"):
            continue
        data = node.attrib["d"]
        vals = numbers(data)
        start = tuple(vals[:2])
        end = tuple(vals[-2:])
        if "A" in data:
            edges.append((start, end, "A", vals[2:-2]))
        else:
            edges.append((start, end, "L", []))
    points = [p for e in edges for p in e[:2]]
    xmin, xmax = min(p[0] for p in points), max(p[0] for p in points)
    ymin, ymax = min(p[1] for p in points), max(p[1] for p in points)
    current = edges[0][0]
    start = current
    path = [f"M {current[0]} {current[1]}"]
    while edges:
        found = None
        for i, (p1, p2, kind, extra) in enumerate(edges):
            if same(p1, current):
                found = i, p2, kind, list(extra)
                break
            if same(p2, current):
                extra = list(extra)
                if kind == "A":
                    extra[-1] = 1 - extra[-1]  # Reverse the SVG sweep flag.
                found = i, p1, kind, extra
                break
        if found is None:
            raise ValueError("The native Edge.Cuts profile is not continuous")
        i, current, kind, extra = found
        edges.pop(i)
        path.append(kind + " " + " ".join(f"{v:g}" for v in extra + list(current)))
    if not same(start, current):
        raise ValueError("The native Edge.Cuts profile is not closed")
    path.append("Z")
    for node in edge_group:
        if node.tag == tag("circle"):
            x, y, r = (float(node.attrib[k]) for k in ("cx", "cy", "r"))
            path.append(f"M {x-r:g} {y:g} a {r:g} {r:g} 0 1 0 {2*r:g} 0 a {r:g} {r:g} 0 1 0 {-2*r:g} 0 Z")
    return " ".join(path), (xmin, ymin, xmax, ymax)


def recolour(element):
    for node in element.iter():
        for key in ("style", "fill", "stroke"):
            if key in node.attrib:
                node.attrib[key] = re.sub(r"#[0-9a-fA-F]{6}", "#FFFFFF", node.attrib[key])
    return element


def consolidate_triangles(element):
    """Render touching filled triangles once, avoiding raster-only seam lines."""
    for parent in element.iter():
        triangles = [node for node in parent if node.tag == tag("path")
                     and "stroke:none" in node.get("style", "")
                     and node.get("d", "").strip().endswith("Z")
                     and len(numbers(node.get("d", ""))) == 6]
        if len(triangles) < 2:
            continue
        merged = ET.Element(tag("path"), {
            "d": " ".join(node.attrib["d"] for node in triangles),
            "style": "fill:#FFFFFF;stroke:none;fill-rule:nonzero;",
        })
        for node in triangles:
            parent.remove(node)
        parent.append(merged)
    return element


def render(board, face):
    src = ET.parse(ROOT / "previews" / f"silk-{face}.svg").getroot()
    edge_groups = [g for g in src if g.tag == tag("g") and "#D0D2CD" in g.attrib.get("style", "") and any(n.tag == tag("circle") for n in g)]
    if len(edge_groups) != 1:
        raise ValueError("Expected one native Edge.Cuts SVG group")
    profile, bounds = outline_path(edge_groups[0])
    xmin, ymin, xmax, ymax = bounds
    width, height = xmax - xmin, ymax - ymin
    if abs(width - 107.95) > 0.001 or abs(height - 25.4) > 0.001:
        raise ValueError("Unexpected PCB outline dimensions")
    margin = 1.5
    svg = ET.Element(tag("svg"), {
        "version": "1.1", "width": f"{width + margin*2:g}mm",
        "height": f"{height + margin*2:g}mm",
        "viewBox": f"{xmin-margin:g} {ymin-margin:g} {width+margin*2:g} {height+margin*2:g}",
    })
    ET.SubElement(svg, tag("title")).text = f"A7 unpopulated board, {face} face"
    ET.SubElement(svg, tag("desc")).text = (
        "Illustrative black solder mask, gold exposed pads and white silkscreen. "
        "Exact native KiCad profile/silkscreen and CAD pad positions; no hidden "
        "masked tracks shown. This material-colour preview is not fabrication "
        "colour or plating control. Components are deliberately unpopulated."
    )
    ET.SubElement(svg, tag("rect"), {"x":f"{xmin-margin:g}","y":f"{ymin-margin:g}","width":f"{width+2*margin:g}","height":f"{height+2*margin:g}","fill":"#ECEFF1"})
    defs = ET.SubElement(svg, tag("defs"))
    clip = ET.SubElement(defs, tag("clipPath"), {"id": "pcb-profile"})
    ET.SubElement(clip, tag("path"), {"d":profile, "fill-rule":"evenodd", "clip-rule":"evenodd"})
    ET.SubElement(svg, tag("path"), {"d":profile, "fill":"#131719", "fill-rule":"evenodd", "stroke":"#454B4E", "stroke-width":"0.035"})
    layer = ET.SubElement(svg, tag("g"), {"clip-path":"url(#pcb-profile)"})
    # The native profile establishes the plot offset. The board outline has
    # exact physical extrema x=105..212.95, y=85.6..111, checked above.
    physical = pcbnew.SHAPE_POLY_SET()
    if not board.GetBoardPolygonOutlines(physical, False):
        raise ValueError("KiCad could not retrieve the PCB outline")
    outline = physical.Outline(0)
    xy = [outline.CPoint(i) for i in range(outline.PointCount())]
    bxmin, bxmax = min(pcbnew.ToMM(p.x) for p in xy), max(pcbnew.ToMM(p.x) for p in xy)
    bymin = min(pcbnew.ToMM(p.y) for p in xy)
    front = face == "front"
    copper = pcbnew.F_Cu if front else pcbnew.B_Cu
    mask = pcbnew.F_Mask if front else pcbnew.B_Mask
    pads = 0
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            layers = pad.GetLayerSet()
            if not layers.Contains(copper) or not layers.Contains(mask):
                continue
            if pad.GetShape() != pcbnew.PAD_SHAPE_RECT:
                raise ValueError("This renderer expects the project's rectangular SMT pads")
            pos, size = pad.GetPosition(), pad.GetSize()
            x = pcbnew.ToMM(pos.x) - bxmin + xmin if front else bxmax - pcbnew.ToMM(pos.x) + xmin
            y = pcbnew.ToMM(pos.y) - bymin + ymin
            w, h = pcbnew.ToMM(size.x), pcbnew.ToMM(size.y)
            angle = pad.GetOrientationDegrees() % 180
            if abs(angle - 90) < .001:
                w, h = h, w
            elif abs(angle) > .001:
                raise ValueError("Unexpected non-orthogonal SMT pad")
            ET.SubElement(layer, tag("rect"), {
                "x":f"{x-w/2:.6f}","y":f"{y-h/2:.6f}",
                "width":f"{w:.6f}","height":f"{h:.6f}",
                "fill":"#D9B65E",
            })
            pads += 1
    expected_pads = 176 if front else 160
    if pads != expected_pads:
        raise ValueError(f"Expected {expected_pads} exposed SMT pads on {face}, got {pads}")
    ink = "#F2EDA1" if front else "#E8B2A7"
    # KiCad10 may put filled artwork's colour on individual paths inside a
    # neutral group, while stroked text still inherits its group's colour.
    silk_groups = [g for g in src if g.tag == tag("g")
                   and any(ink.lower() in node.get("style", "").lower()
                           for node in g.iter())]
    if not silk_groups:
        raise ValueError(f"Could not locate {face} native silkscreen groups")
    for group in silk_groups:
        layer.append(consolidate_triangles(recolour(copy.deepcopy(group))))
    output = ROOT / "previews" / f"appearance-{face}.svg"
    ET.ElementTree(svg).write(output, encoding="utf-8", xml_declaration=True)
    png = output.with_suffix(".png")
    try:
        import cairosvg
        cairosvg.svg2png(url=str(output),write_to=str(png),output_width=2400)
    except ImportError:
        subprocess.run(["python3","-c", "import cairosvg,sys;cairosvg.svg2png(url=sys.argv[1],write_to=sys.argv[2],output_width=2400)",str(output),str(png)],check=True)
    print(f"{face}: {pads} pads; {len(silk_groups)} native silkscreen groups; {output.name}")


if __name__ == "__main__":
    pcb = pcbnew.LoadBoard(str(ROOT / "HY8M-SIMM.kicad_pcb"))
    for side in ("front", "rear"):
        render(pcb, side)
