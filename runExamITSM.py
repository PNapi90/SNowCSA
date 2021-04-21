#!/usr/bin/python3
# Program to run chercher.tech Servicenow CSA mock exams in console

#import numpy as np

class Question:
    def __init__(self,pos):
        self.answers = []
        self.correct = []
        self.pos = pos
        self.amount_of_options = 0
        self.options = []
        self.QuestionCorrectlyAnswered = False
        self.is_question = True
        self.__CorrectSign = "(c)"

    def set_question(self,Q):
        self.question = Q.rstrip()
        self.is_question = False
        
    def add_option(self,option):
        if self.is_question:
            self.set_question(option)
            return
        self.options.append(option.rstrip())
        self.__checkCorrect()
        self.amount_of_options += 1
    def __checkCorrect(self):
        if self.__CorrectSign in self.options[self.amount_of_options]:
            self.options[self.amount_of_options] = self.options[self.amount_of_options].replace(self.__CorrectSign,"")
            self.correct.append(self.amount_of_options)
   
    def set_answer(self,answer):
        self.correct.sort()
        self.answers = answer.copy()
        self.answers.sort()
        same = len(self.answers) == len(self.correct)
        if same:
            for i in range(len(answer)):
                same = same and (self.answers[i] == self.correct[i])
        self.QuestionCorrectlyAnswered = same
    def checkCorrect(self):
        return self.QuestionCorrectlyAnswered

    def printQuestion(self):
        print("\n--------------------")
        print("Question #",self.pos+1)

        #check for plural or singular
        n = len(self.correct)
        plural_or_singular = "s" if n > 1 else ""
        nAnswers = "("+str(n) + " correct answer"+plural_or_singular+")"
        
        print("\n",self.question,nAnswers)
        print("\nPossible Answers:")
        for i,a in enumerate(self.options):
            print(i+1,"->",a)
    def printWrong(self):
        self.printQuestion()
        print("\n------------")
        for i,a in enumerate(self.answers):
            self.answers[i] += 1
        for i,a in enumerate(self.correct):
            self.correct[i] += 1
        print("Answers:",self.answers,"\ncorrect:",self.correct)
    def getRange(self):
        return self.amount_of_options
    def getRangeCorrect(self):
        return len(self.correct)


def checkBadAnswer(posAnswer,maxRange):
    for pA in posAnswer:
        if pA > maxRange or pA < 0:
            return True,pA
    return False,-1





def runExam(file,QuestionArray):
    points = 0
    newQuestion = False
    finished = False
    oldLine = ""
    created = False
    pos = int(0)
    for line in file:
        if line[0] == "#":
            continue
        # trigger for new question
        newQuestion = "NEW QUESTION" in line
        # trigger for end of question
        finished = "END" in line

        if newQuestion:
            #add question
            created = True
            QuestionArray.append(Question(pos))
        
        if finished:
            QuestionArray[pos].printQuestion()
            
            #input your answer
            maxRange = QuestionArray[pos].getRange()
            check = True
            while check:
                nlen = QuestionArray[pos].getRangeCorrect()
                answerString = ""
                if nlen > 1:
                    answerString = input("Answers (seperated via , ): ")
                elif nlen == 1:
                    answerString = input("Answer: ")
                #check if input string is empty
                if answerString.strip():
                    #allows single or multiple answers
                    tmpList = answerString.split(",") 
                    posAnswer = [int(t)-1 for t in tmpList]
                    #check if answer out of valid range
                    check,badPos = checkBadAnswer(posAnswer,maxRange)
                    if check:
                        print("Answer",badPos+1,"not in valid range!\n")
                else:
                    print("No answer given. Please make a valid selection.\n")
            
            QuestionArray[pos].set_answer(posAnswer)

            if QuestionArray[pos].checkCorrect():
                points += 1

            #increment position in question array
            pos += 1
            
            #close access to QuestionArray for options adding
            created = False

        #only save oldLine if line not empty (no line breaks etc.)
        line = line.rstrip()

        #add possible option to Question object
        if not(finished) and not(newQuestion) and line:
            QuestionArray[pos].add_option(line)
        
    #return points and total amount of questions (not always 60)
    return points,pos


def showWrongs(QuestionArray):
    for i,Q in enumerate(QuestionArray):
        if not(Q.checkCorrect()):
            print("")
            Q.printWrong()
            input("Press any key to continue...")



def printScore(points,total):
    print("\n=================================")
    percentage = round(points/total*100,2)
    print("Final result:",points,"/",total,"->",percentage,"%")
    passed = "Passed" if percentage >= 70 else "Failed"
    print("You",passed)
    print("=================================")




Nexam = 4
files = ["ExamsITSM/Udemy"+str(i)+".txt" for i in range(Nexam)]

print(files)

print("\n===================================")
print("CIS ITSM\n---------")
print("Which exam would you like to take?")
for i,f in enumerate(files):
    print(i,"->",f)

number = input("exam # -> ")

MADRID = int(number) == 2
NY = int(number) == 3


#check for empty input string and range
while not number.strip() or int(number) >= len(files) or int(number) < 0:
    if not number.strip() or int(number) >= len(files) or int(number) < 0:
        print("No valid exam selected. Please make a valid selection.")
        number = input("exam # -> ")

print("you choose",files[int(number)])

if MADRID:
    print("-> Madrid Delta Exam")
if NY:
    print("-> New York/Orlando Delta Exam")

fileName = files[int(number)]

#Out of scope of runExam for later access to wrong answers
QuestionArray = []

with open(fileName,"r") as file:
    points,total = runExam(file,QuestionArray)
    if points < total:
        printScore(points,total)
    showWrongs(QuestionArray)
    printScore(points,total)
