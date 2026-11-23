#!/usr/bin/env python3
"""Render every diagram onto one PDF page each (for visual checking): python3 tools/preview_diagrams.py out.pdf [name ...]"""
import sys, pathlib   # standard library
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))   # import sibling module
import diagrams   # the diagram registry
from reportlab.graphics import renderPDF   # drawing -> PDF
from reportlab.pdfgen import canvas   # PDF canvas
names = sys.argv[2:] or sorted(diagrams.DIAGRAMS)   # diagrams to render
cv = canvas.Canvas(sys.argv[1])   # output file
for n in names:   # one page per diagram
    d = diagrams.DIAGRAMS[n]()   # build the drawing
    cv.setPageSize((d.width + 20, d.height + 20))   # page fits the drawing
    renderPDF.draw(d, cv, 10, 10)   # draw with a small margin
    cv.showPage()   # next page
cv.save()   # write the file
