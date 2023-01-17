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
    return render(request, 'main/question.html')





