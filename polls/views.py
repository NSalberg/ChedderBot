from django.shortcuts import render , get_object_or_404
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpRequest
from phonenumber_field.formfields import PhoneNumberField
import requests
from .models import Question, Choice, PhoneNumber
from django.urls import reverse
from django.views import generic
from django import forms

class PhoneForm(forms.Form):
    phone = PhoneNumberField(region="US")

class IndexView(generic.ListView):
    template_name = "polls/indext.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def phone_input(request):
    if request.method == "POST":
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone"]
            request.session["phone_number"] = str(phone_number)
            try: 
                PhoneNumber.objects.get(phone_number=phone_number)
            except PhoneNumber.DoesNotExist:
                number = PhoneNumber(phone_number=phone_number)
                number.save()
            
            return render(request, "polls/thanks.html", {"phone_number": phone_number})
    else:
        form = PhoneForm()
    return render(request, "polls/phone_input.html", {"form": form})

def thanks(request):
    return render(request, "polls/thanks.html")

def delete(request, phone_number, UID):
    if request.method == "GET":
        phone_number = "+1"+str(phone_number)
        form = PhoneForm({"phone": phone_number})

        if form.is_valid():
            number = form.cleaned_data["phone"]
        else:
            return JsonResponse({"error": "Invalid phone number"}, status=400)
        
        try:
            PhoneNumber.objects.get(phone_number=number, UID=UID).delete()
            return render(request, "polls/delete.html", {"phone_number": phone_number})
        except PhoneNumber.DoesNotExist:
            return JsonResponse({"error": "Phone number does not exist"}, status=404)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try: 
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice",
            }
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
