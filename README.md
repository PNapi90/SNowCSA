# python3 scripts to run ServiceNow CSA/CIS-ITSM mock exams

Prerequisites: `python3`

### CSA exams from chercher.tech

To run the programm, simply run `python3 runExamCSA.py` in your terminal.  
If you want to add additional exams, simply copy the exam text from chercher.tech into a .txt file and add it to the file list in the `Exams` folder (in incrementing order).
##### Warning
The answers marked as correct do not necessarily have to be correct!

##### About the exams (from chercher.tech):

Exams 1 - 11 are from the ServiceNow Certified System Administrator 2019 Set, with the corresponding numbering
Exam 0 is the ServiceNow - CSA - Mock test



### CIS-ITSM exams

The program `runExamITSM.py` is written in such a way that exams with the format

```
NEW QUESTION
<Exam question>
<Answer1>
<Answer2> (c)
<Answer3>
<Answer4> (c)
END
```

where `(c)` signifies the correct answer(s). The questions themselves are not part of the repository due to potential copyright issues.
