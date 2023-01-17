from contextvars import Context
from multiprocessing import context
from tkinter.messagebox import QUESTION
from django.shortcuts import render
import json
import openai
from .forms import QuestionForm
from .models import Question
import os
#from django.views.generic.base import TemplateView
#from configparser import ConfigParser

# openai.api_key = ""

def CallChatGpt(question,reponse):
    questionAposer = "the question is {}, and the answer is {}. does the answer is right?".format(question,reponse)
    res = str(openai.Completion.create(
        model="text-davinci-003",
        prompt = questionAposer,
        max_tokens=10,
        temperature=0
    ))
    res = json.loads(res)
    res = res["choices"][0]["text"]
    return res
        # Reponse = CallChatGpt(jsonUpload["question"],jsonUpload["reponse"])



# Create your views here.
def index(request):
    if request.method == "POST":
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            if os.listdir("media/question"):
                for file in os.listdir("media/question"):
                    os.remove("media/question/"+file)
            form.save()
            os.rename("media/question/"+os.listdir("media/question")[0],"media/question/data.json")

            

    else :
        form = QuestionForm()

    return render(request, 'main/index.html', {'form': form})




def question(request):
    if request.method == "GET" :
        with open("media/question/data.json") as json_file:
            print(json_file)
            jsonfile = json.load(json_file)
        #parser = ConfigParser()
        #test= parser.read('Format_ini.ini')
        #print(test)
        #print(parser.get('Question 1', 'type'))
        nombre_question=len(jsonfile["QCM"])
        question=[]
        point=[]
        types=[]
        choix=[]
        reponse=[]
        explication=[]
        
        toute=[]
        #context = {'nombre_question':nombre_question}
        for o in range (nombre_question):
            question.append(jsonfile["QCM"]["Question {}".format(o+1)]["Question"])
            toute.append(jsonfile["QCM"]["Question {}".format(o+1)]["Question"])
            #context['question{}'.format(o)]=question[o]

            point.append(jsonfile["QCM"]["Question {}".format(o+1)]["Points"])
            toute.append(jsonfile["QCM"]["Question {}".format(o+1)]["Points"])
            #context['point{}'.format(o)]=point[o]

            types.append(jsonfile["QCM"]["Question {}".format(o+1)]["type"])
            toute.append(jsonfile["QCM"]["Question {}".format(o+1)]["type"])
            #context['types{}'.format(o)]=types[o]

            choix.append(jsonfile["QCM"]["Question {}".format(o+1)]["Choix"])
            toute.append(jsonfile["QCM"]["Question {}".format(o+1)]["Choix"])
            #context['choix{}'.format(o)]=choix[o]

            reponse.append(jsonfile["QCM"]["Question {}".format(o+1)]["Reponse attendu"])
            toute.append(jsonfile["QCM"]["Question {}".format(o+1)]["Reponse attendu"])
            #context['reponse{}'.format(o)]=reponse[o]

            explication.append(jsonfile["QCM"]["Question {}".format(o+1)]["Explication"])
            toute.append(jsonfile["QCM"]["Question {}".format(o+1)]["Explication"])
            #context['explication{}'.format(o)]=explication[o]

        zipp=zip(question,point,types,choix,reponse,explication)
        print(toute)
        context = {'question':question,'point':point,'types':types,'choix':choix,'reponse':reponse,'explication':explication,'toute':toute,'zipp':zipp}
        context['nombre_question']=nombre_question


    return render(request, 'main/question.html',context)




