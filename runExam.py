# Program to run chercher.tech Servicenow CSA mock exams in console

#import numpy as np

class Question:
    def __init__(self,Q,pos):
        self.question = Q.rstrip()
        self.multiple = "Select all that apply" in self.question
        self.multiAnswers = []
        self.options = []
        self.amount_of_options = 0
        self.correctAt = -1
        self.givenAnswer = -1
        self.correctAtArray = []
        self.correct = False
        self.pos = pos
    def add_option(self,option):
        self.options.append(option.rstrip())
        if self.multiple:
            self.__checkCorrectMulti()
        else:
            self.__checkCorrect()
        self.amount_of_options += 1
    def __checkCorrect(self):
        if "(Correct)" in self.options[self.amount_of_options]:
            self.options[self.amount_of_options] = self.options[self.amount_of_options][:-9]
            self.correctAt = self.amount_of_options
    def __checkCorrectMulti(self):
        if "(Correct)" in self.options[self.amount_of_options]:
            self.options[self.amount_of_options] = self.options[self.amount_of_options][:-9]
            self.correctAtArray.append(self.amount_of_options)
    def set_answer(self,answer):
        if self.multiple:
            self.correctAtArray.sort()
            self.multiAnswers = answer.copy()
            self.multiAnswers.sort()
            same = len(self.multiAnswers) == len(self.correctAtArray)
            if same:
                for i in range(len(answer)):
                    same = same and (self.multiAnswers[i] == self.correctAtArray[i])
            self.correct = same
        else:
            self.givenAnswer = answer[0]
            self.correct = self.givenAnswer == self.correctAt
    def checkCorrect(self):
        return self.correct
    def printQuestion(self):
        print("\n--------------------")
        print("Question #",self.pos+1)
        print("\n",self.question)
        print("\nPossible Answers:")
        for i,a in enumerate(self.options):
            print(i+1,"->",a)
    def printWrong(self):
        self.printQuestion()
        print("\n------------")
        if self.multiple:
            for i,a in enumerate(self.multiAnswers):
                self.multiAnswers[i] += 1
            for i,a in enumerate(self.correctAtArray):
                self.correctAtArray[i] += 1
            print("Answers:",self.multiAnswers,"\ncorrect:",self.correctAtArray)
                
        else:
            print("Answer:",self.givenAnswer+1,"\ncorrect:",self.correctAt+1)
        print("------------")
    def getRange(self):
        return self.amount_of_options


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
        # skip unwanted text
        if "ServiceNow Certified System Administrator Practice Exam" in line:
            continue

        # trigger for new question
        newQuestion = "Options are" in line
        # trigger for end of question
        finished = "Answer :" in line

        if newQuestion:
            #add question
            created = True
            QuestionArray.append(Question(oldLine,pos))
        if finished:
            QuestionArray[pos].printQuestion()
            
            #input your answer
            maxRange = QuestionArray[pos].getRange()
            check = True
            while check:
                answerString = input("Answer: ")
                #allows single or multiple answers
                tmpList = answerString.split(",") 
                posAnswer = [int(t)-1 for t in tmpList]
                #check if answer out of valid range
                check,badPos = checkBadAnswer(posAnswer,maxRange)
                if check:
                    print("Answer",badPos,"not in valid range!\n")
            
            QuestionArray[pos].set_answer(posAnswer)

            if QuestionArray[pos].checkCorrect():
                points += 1

            #increment position in question array
            pos += 1
            
            #close access to QuestionArray for options adding
            created = False

        #only save oldLine if line not empty (no line breaks etc.)
        line = line.rstrip()
        oldLine = line if line else oldLine

        #add possible option to Question object
        if not(finished) and not(newQuestion) and created and line:
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


"""
 load file and run exam 
 if you want to add exams, simply go to 
 ####
 https://chercher.tech/service-now-csa/servicenow-certified-system-administrator-practice-exam-2019-set-8
 ####
 and copy all the questions into a .txt file and add it to the files array (see below)

"""

Nexam = 5
files = ["Exam"+str(i)+".txt" for i in range(Nexam)]

print("\n===================================")
print("Which exam would you like to take?")
for i,f in enumerate(files):
    print(i,"->",f)

number = -1

while number >= len(files) or number < 0:
    number = int(input("exam # -> "))
    if number >= len(files) or number < 0:
        print(number,"not in valid range!")

print("you choose",files[number])

fileName = files[number]

#Out of scope of runExam for later access to wrong answers
QuestionArray = []

with open(fileName,"r") as file:
    points,total = runExam(file,QuestionArray)
    printScore(points,total)
    showWrongs(QuestionArray)
    printScore(points,total)
