from email.errors import NoBoundaryInMultipartDefect
from sre_constants import REPEAT_ONE
from tkinter.messagebox import QUESTION
from xml.dom import NoModificationAllowedErr
from django.shortcuts import render
from django.shortcuts import redirect
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
    print(nombre_question)
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
    return render(request, 'main/questionnaire.html',context)


def Note(liste_reponse):
    '''prend en argument une liste de [".Correcte",".Incorrecte"] de la longueure du nombre de question
    retourne un liste avec [nombre de point, total points du questionnaire, note sur 20]'''

    with open("media/question/data.json") as json_file:
        data = json.load(json_file)

    # access the QCM section
    qcm_data = data['QCM']
    total_points = []
    bareme = 0
    reponse = 0
    for question in qcm_data.values() :
        bareme += int(question['Points'])
        if (liste_reponse[reponse]=='.\n\nCorrecte'):
            total_points.append(int(question['Points']))
        reponse += 1

    return [sum(total_points),bareme,sum(total_points)*20/bareme]

def Correction(request):
    with open("media/question/data.json") as json_file:
        jsonfile = json.load(json_file)
    nombre_question=len(jsonfile["QCM"])
    question=[]
    reponse_list=[]
    for o in range (nombre_question):
        question.append(jsonfile["QCM"]["Question {}".format(o+1)]["Question"])
    if request.method == "POST": 
        Correction=[]
        reponsePost = request.POST.dict()
        for i in range (nombre_question):
            Correction.append(CallChatGpt(question[i],reponsePost["Question{}".format(i+1)]))
        for i in range (nombre_question):
            reponse_list.append(reponsePost["Question{}".format(i+1)])
        note=Note(Correction)[2]
        ElementsQuestion=zip(question,Correction,reponse_list)
        context = {'ElementsQuestion':ElementsQuestion}
        context['note']=note
        print(Correction)
    return render(request,'main/correction.html',context)







