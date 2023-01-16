from django.shortcuts import render

# Create your views here.
def index(request):
    if request.method == "POST":
        print("POST")
        print(request.POST.get("jsonUpload"))
    return render(request, 'main/index.html')