# Program to run chercher.tech Servicenow CSA mock exams in console


class Question:
    def __init__(self,Q):
        self.question = Q.rstrip()
        self.options = []
        self.amount_of_options = 0
        self.correctAt = -1
        self.givenAnswer = -1
        self.correct = False
    def add_option(self,option):
        self.options.append(option.rstrip())
        self.__checkCorrect()
        self.amount_of_options += 1
    def __checkCorrect(self):
        if "(Correct)" in self.options[self.amount_of_options]:
            self.options[self.amount_of_options] = self.options[self.amount_of_options][:-9]
            self.correctAt = self.amount_of_options
    def set_answer(self,answer):
        self.givenAnswer = answer
        self.correct = self.givenAnswer == self.correctAt
    def checkCorrect(self):
        return self.correct

    def printQuestion(self,pos):
        print("\n--------------------")
        print("Question #",pos+1)
        print("\n",self.question)
        print("\nPossible Answers:")
        for i,a in enumerate(self.options):
            print(i+1,"->",a)




def runExam(file):
    points = 0
    QuestionArray = []
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
            QuestionArray.append(Question(oldLine))
        if finished:
            QuestionArray[pos].printQuestion(pos)
            
            #input your answer
            posAnswer = int(input("Answer: "))-1
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




"""
 load file and run exam 
 if you want to add exams, simply go to 
 ####
 https://chercher.tech/service-now-csa/servicenow-certified-system-administrator-practice-exam-2019-set-8
 ####
 and copy all the questions into a .txt file and add it to the files array (see below)

"""

files = ["Exam1.txt","Exam2.txt"]


print("Which exam would you like to take?")
for i,f in enumerate(files):
    print(i,"->",f)

number = int(input("exam # -> "))

if number >= len(files) or number < 0:
    print(number,"not in valid range!")

else:
    print("you choose",files[number])

fileName = files[number]

with open(fileName,"r") as file:
    points,total = runExam(file)
    print("\n=================================")
    percentage = round(points/total*100,2)
    print("Final result:",points,"/",total,"->",percentage,"%")
    passed = "Passed" if percentage >= 70 else "Failed"
    print("You",passed)
    print("=================================")
