#  Littlewood MorningMile Certificate

This repo helps generate Certificate of Achievement for morning mile runners

## Prereqs

- WSL installed in windows (or comparable shell environment, e.g. MacOS terminal might work).
- Inkscape installed on the command line: `sudo apt install inkscape`
- Pypdf2 installed: `sudo apt install python3-pypdf2`
- MATURA font installed: `mkdir -p ~/.local/share/fonts/;  cp MATURASC.TTF ~/.local/share/fonts/`

## Preparing the Data

Open up the data sheet and generate two columns Name, Miles

I made a “certificates” tab and made a range with the query:

```
=FILTER(FILTER(AllStudents, (TeacherMarkers <> "x") * (TotalMiles >= CertMilesCutoff )), {0,1,0,0,0,1})
```

This is similar to the query we’re using on the "Student Stats" sheet, but not sorted so that it is still grouped by Teacher > alphabetical.

Copy all the data into a `students.tsv` file. I selected the cells of data (student name and miles), copied them, and then opened `students.tsv` in vscode and pasted in the data overwriting everything that’s there.

## Prepare the Certificate template

Open up the template and ensure everything looks good: `inkscape "Morning Mile Certificate - template.svg" &`

1. Check for “Certificate of Achievement” should be a fancy script and centered, if it is a plain sanserif and running off the right you’re missing the MATURA font.
1. School Year is fixed
1. Save it

## Run a Test Generation

Since generating for all students takes a little while it is good to do it for a small handful first to ensure everything is working alright.

First 10 students: `head -n 10 students.tsv | python templatecerts.py`

Look at the generated file, `output.pdf`, and ensure everything is happy.

Generate certs for all students

```
cat students.tsv | python templatecerts.py
```
