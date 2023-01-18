from django.shortcuts import render
import json
import openai
from .forms import QuestionForm
from .models import Question
import os

openai.api_key = "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"

def CallChatGpt(question,reponse):
    questionAposer = "Partons du principe que tu es un professeur ayant realise un examen. a la question comportant la consigne : {}. ton eleve a repondu : {}. est-ce que cette réponse est correcte ou incorrecte ? Réponds uniquement en un seul mot sans utilisation de points à la fin de ta phrase".format(question,reponse)
    res = str(openai.Completion.create(
        model="text-davinci-003",
        prompt = questionAposer,
        max_tokens=5,
        temperature=0
    ))
    res = json.loads(res)
    res = res["choices"][0]["text"]
    return res

    





# def index(request):
#     if request.method == "POST": #check if request is POST
#         form = QuestionForm(request.POST, request.FILES) #get the form from the request using the model
#         if form.is_valid():
#             if os.listdir("media/question"): #check if there is a file in the folder
#                 for file in os.listdir("media/question"): 
#                     os.remove("media/question/"+file) #remove all files in the folder
#             form.save() #save the new file in the folder
#             os.rename("media/question/"+os.listdir("media/question")[0],"media/question/data.json") #rename the file to data.json
#     else :
#         form = QuestionForm()

#     return render(request, 'main/index.html', {'form': form})
def index(request):
    if request.method == "POST": #check if request is POST
        form = QuestionForm(request.POST, request.FILES) #get the form from the request using the model
        if form.is_valid():
            file = request.FILES.dict()['ListeQuestion']
            #give me the content of file in json format
            jsonfile = json.loads(file.read().decode('utf-8'))
            json_object = json.dumps(jsonfile, ensure_ascii=False, indent=4)
            with open("media/question/data.json", "w") as outfile:
                outfile.truncate(0)
                outfile.write(json_object)
            
            
    else :
        form = QuestionForm()

    return render(request, 'main/index.html', {'form': form})






def Configuration(request):
    return render(request, 'main/configuration.html')


def Questionnaire(request):
    with open("media/question/data.json") as json_file:
        jsonfile = json.load(json_file)

    nombre_question=len(jsonfile["QCM"])

    question=[]
    point=[]
    types=[]
    choix=[]
    reponse=[]
    explication=[]
    index=[]

    for o in range (nombre_question):
        question.append(jsonfile["QCM"]["Question {}".format(o+1)]["Question"])
        point.append(jsonfile["QCM"]["Question {}".format(o+1)]["Points"])
        types.append(jsonfile["QCM"]["Question {}".format(o+1)]["type"])
        choix.append(jsonfile["QCM"]["Question {}".format(o+1)]["Choix"])
        reponse.append(jsonfile["QCM"]["Question {}".format(o+1)]["Reponse attendu"])
        explication.append(jsonfile["QCM"]["Question {}".format(o+1)]["Explication"])
        index.append(o+1)
        print("hello")
        ElementsQuestion=zip(question,point,types,choix,reponse,explication,index)
        context = {'ElementsQuestion':ElementsQuestion}

    

    if request.method == "POST":
        Correction=[]
        reponses = request.POST.dict()
        for i in range (nombre_question):
            print(reponses["Question{}".format(i+1)])
            Correction.append(CallChatGpt(question[i],reponses["Question{}".format(i+1)]))
        
        #Correction = ["oui","oui"]
        #print(Correction)
        ElementsQuestion=zip(question,point,types,choix,reponse,explication,index,Correction)
        context = {'ElementsQuestion':ElementsQuestion}
    
    



    return render(request, 'main/questionnaire.html',context)









