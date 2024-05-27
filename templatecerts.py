#!/usr/bin/env python


from pathlib import Path
import io
import subprocess
import PyPDF2
import sys


inputfile = Path("students.tsv")

TEMPLATEFILE = "Morning Mile Certificate - template.svg"


def readstudents(p="/dev/stdin"):
    p = Path(p)
    lines = p.read_text().split("\n")
    for idx, l in enumerate(lines):
        if l == "":
            return
        parts = l.split("\t")
        name = parts[0].strip()
        miles = parts[1].strip()
        # miles=str(round(float(miles)))
        print(f"{idx: 3}: writing {name!r} \t{miles}", file=sys.stderr)
        yield {"name": name, "miles": miles}


def readtemplate(p=TEMPLATEFILE):
    return Path(p).read_text()


def subst(templ, name, miles):
    return templ.replace("STUDENTNAME", name).replace("MILES", miles)


def writecert(outputdir, name, miles):
    outputdir = Path(outputdir)
    outputdir.mkdir(exist_ok=True)
    outfile = outputdir / name
    outfile.write_text(subst(TEMPLATE, name, miles))


def svgToPDF(svg):
    return subprocess.run(
        ["inkscape", "--pipe", "-o", "-", "--export-type=pdf"],
        input=bytes(svg, "utf-8"),
        capture_output=True,
        check=True,
    ).stdout


def mergepdfs(pdfs, outputfilename):
    m = PyPDF2.PdfFileMerger()
    for p in pdfs:
        m.append(io.BytesIO(p))
    m.write(outputfilename)


if __name__ == "__main__":

    outfile="output.pdf"
    data = readstudents()
    templ = readtemplate()
    pdfs = (svgToPDF(subst(templ, **student)) for student in data)
    mergepdfs(pdfs, outfile)
    print(f"finished generating {outfile!r}", file=sys.stderr)