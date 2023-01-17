from multiprocessing import context
from django.shortcuts import render
import json
import openai
from .forms import QuestionForm
from .models import Question
import os

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
        question=jsonfile["QCM"]["Question 1"]["Question"]
        point=jsonfile["QCM"]["Question 1"]["Points"]
        types=jsonfile["QCM"]["Question 1"]["type"]
        choix=jsonfile["QCM"]["Question 1"]["Choix"]
        reponse=jsonfile["QCM"]["Question 1"]["Reponse attendu"]
        explication=jsonfile["QCM"]["Question 1"]["Explication"]
        print(len(jsonfile["QCM"]))
        print("OUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
        context = {'question':question,'point':point,'type':types,'choix':choix,'reponse':reponse,'explication':explication}
        

    return render(request, 'main/question.html',context)

#def recup_quest()
#    return


