from django.shortcuts import render
import json
import openai

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



# Create your views here.
def index(request):
    Reponse = ""
    if request.method == "POST":
        print("POST")
        jsonUpload = request.POST.get("jsonUpload")
        jsonUpload = json.loads(jsonUpload)
        print(jsonUpload)
        print(jsonUpload["question"])
        Reponse = CallChatGpt(jsonUpload["question"],jsonUpload["reponse"])
        print(Reponse)
    context = {'name':Reponse}
    return render(request, 'main/index.html',context)

def question(request):
    return render(request, 'main/question.html')





