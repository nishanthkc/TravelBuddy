from django.shortcuts import render, get_list_or_404, redirect
from django.views import View
from .askAI import Ask, Clean_data, Clean_data2, AskChat, Clean_list, InteractChat, InteractChat2

from .askAI import AskV2, CleanDataV2, FoodV2, CleanFoodV2, ChatV2

from .forms import AskForm, QForm, FForm
import ast

# from .models import Queries, Data, Food, Statistics, Search_history
from .models import Queries, Data, Food, PersonalisedData
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .helpers import find_closest_pair, generate_urls
from django.http import HttpResponse

from django.db.models import Sum, Count

import json
import uuid
import requests
from datetime import datetime, timedelta
from urllib.request import urlopen

import time
import random

class ModelFormHome(View):
    def get(self, request):
        form = QForm()
        ctx = {'form':form}
        return render(request, "askme/index.html", ctx)
    def post(self, request):
        try:
            form = QForm(request.POST)
            if not form.is_valid() :
                ctx = {'form' : form}
                return render(request, "askme/index.html", ctx)
            # If there are no errors, we would use it to get an answer
            place = request.POST.get("place")
            duration = request.POST.get("duration")

            stats_set = Statistics.objects.filter(stat_place=place.lower().strip(), stat_duration=duration)

            if stats_set:
                updated_values = {'stat_count': stats_set[0].stat_count+1}
            else:
                updated_values = {'stat_count': 1}

            obj, created = Statistics.objects.update_or_create(
                stat_place= place.lower().strip(), stat_duration=duration,
                defaults=updated_values
            )

            query_set = Data.objects.filter(gpt_place=place.lower().strip(), gpt_duration=duration)

            if query_set:
                # print("there is a query set")
                # print(query_set[0])
                # print(query_set[0].gpt_place)
                # print(query_set[0].gpt_duration)
                # print(query_set[0].gpt_result)

                # to make it seem like we're querying hahahah
                time.sleep(5)

                heading = "Here's your "+str(duration)+"-days itinerary for "+str(place).title()
                page_link = ("https://thetravelbuddy.io/places/{}/{}".format(place,duration)).replace(" ","")
                if request.user.is_authenticated:
                    Search_history.objects.create(user=request.user, search_place=place,search_duration=duration,search_query="<h2><b>"+heading+"</b></h2>"+query_set[0].gpt_result)
                ctx = {"data":query_set[0].gpt_result, "place":place, "duration":duration, "heading":heading, "extra_button":'yes', 'page_link':page_link}
                return render(request, "askme/post_ans.html", ctx)
            
            else:
                test1 = "answer '0' if the place doesnt exist or '1' if it does: "+place
                test1_data = AskChat(test1)
                
                if "1" in test1_data:

                    # prompt = "act as a tour guide and give a "+duration+" days guide to visit "+place+" as (a place, breifly about it and what a tourist can do there) for morning, afternoon and evening .then 'end the day with' a popular restaurant/local food places."
                    prompt = "give me "+duration+" day itinerary for "+place+". format for each day (a place, about it and its specialty ) Morning:, Afternoon:, Evening:, End the day with:a dinner from a popular restaurant."
                    data = AskChat(prompt)

                    p2 = "make a python list of all the places in the format:['place'] in the below text:"+data
                    data_p2 = AskChat(p2)
                    
                    # print(data_p2)
                    clean_data = Clean_list(data, data_p2)
                    heading = "Here's your "+str(duration)+"-days itinerary for "+str(place).title()
                    page_link = ("https://thetravelbuddy.io/places/{}/{}".format(place,duration)).replace(" ","")
                    ctx = {"data":clean_data, "place":place, "duration":duration, "heading":heading, "extra_button":'yes', 'page_link':page_link}

                    data = Data.objects.create(gpt_place= place.lower().strip(), gpt_duration=duration, gpt_result= clean_data)
                    data.save()

                    if request.user.is_authenticated:
                        Search_history.objects.create(user=request.user, search_place=place,search_duration=duration,search_query="<h2><b>"+heading+"</b></h2>"+clean_data)

                    # # add session data
                    # request.session["again_place"] = place
                    # request.session["again_duration"] = duration

                    return render(request, "askme/post_ans.html", ctx)
                else:
                    data = "I'm sorry, but '"+place+"' is not a known place or city. Can you provide more information or clarify the name of the destination you would like me to create an itinerary for?"
                    ctx = {"data":data}
                    return render(request, "askme/post_ans.html", ctx)
        except:
            data = "Something went wrong. Can you please try again."
            ctx = {"data":data}
            return render(request, "askme/error.html", ctx)

class AskAgain(View):
    def get(self, request):
        return redirect(reverse('askme:askme_mform'))
    def post(self, request):

        # print("in ASK AGAIN VIEW")

        place = request.POST.get("again_place")
        duration = request.POST.get("again_duration")
        
        # print(place)
        # print(duration)

        # prompt = "act as a tour guide and give a "+duration+" days guide to visit "+place+" as (a place, breifly about it and what a tourist can do there) for morning and afternoon.then in the evening, 'end the day with' a popular restaurant/local food places. DO NOT REPEAT THE SAME PLACES TWICE."
        prompt = "give me "+duration+" day itinerary for "+place+". format for each day (a place, about it and its specialty ) Morning:, Afternoon:, Evening:, End the day with:a dinner from a popular restaurant."
        data = AskChat(prompt)

        p2 = "make a python list of all the places in the format:['place'] in the below text:"+data
        data_p2 = AskChat(p2)
                
        # print(data_p2)
        clean_data = Clean_list(data, data_p2)
        heading = "Here's your "+str(duration)+"-days itinerary for "+str(place).title()
        ctx = {"data":clean_data, "place":place, "duration":duration, "heading":heading, "extra_button":'yes'}

        # t = Data.objects.get(gpt_place= place, gpt_duration=duration)
        # t.gpt_result = clean_data  # change field
        # t.save()

        updated_values = {'gpt_result': clean_data}

        obj, created = Data.objects.update_or_create(
            gpt_place= place.lower().strip(), gpt_duration=duration,
            defaults=updated_values
        )

        # obj, created = Data.objects.get_or_create(gpt_place=place.lower().strip(), gpt_duration=duration, gpt_result=clean_data)
        # obj.save()

        # data = Data.objects.create(gpt_place= place.lower().strip(), gpt_duration=duration, gpt_result= clean_data)
        # data.save()

        return render(request, "askme/post_ans.html", ctx)

class FoodView(View):
    def post(self, request):
        place = request.POST.get("food_place")
        heading = "Food Recommendations for "+str(place).title()
        query_set = Food.objects.filter(gpt_place=place.lower().strip())

        if query_set:
            time.sleep(3.5)
            ctx = {"data":query_set[0].gpt_result, "place":place, "heading":heading}
            return render(request, "askme/post_ans.html", ctx)

        # prompt = "give me popular restaurant recommendation in "+place+" and also the popular local foods"
        prompt = "give me food recommendations in "+place+". also popular restaurants, cafes and local foods "
        # print(prompt)

        data = AskChat(prompt)
        ctx = {"data":data, "place":place, "heading":heading}

        data = Food.objects.create(gpt_place= place.lower().strip(), gpt_result= data)
        data.save()

        # data = Data.objects.create(gpt_place= place.lower().strip(), gpt_duration=duration, gpt_result= clean_data)
        # data.save()

        return render(request, "askme/post_ans.html", ctx)


class MostSearched(View):
    def get(self, request):
        q = (Statistics.objects.values('stat_place').annotate(total = Sum('stat_count')))
        sorted_list = sorted(q, key=lambda x:x['total'], reverse=True)
        ctx = {'data':sorted_list[:3], 'heading':"Top 3 Most Searched Destinations"}
        return render(request, "askme/most_searched.html", ctx)

class PlaceView(View):
    def get(self, request, place_name):
        q = Data.objects.filter(gpt_place=place_name)
        ctx = {'data':q, 'heading':"Different Itineraries of "+place_name.title()}
        return render(request, "askme/place_view.html", ctx)

class PlaceDayView(View):
    def get(self, request, place_name, d):
        q = Data.objects.filter(gpt_place=place_name, gpt_duration=d)
        ctx = {'data':q[0].gpt_result, 'heading':str(d)+"-days Itinerary for "+place_name.title(), 'place':place_name, 'duration':d}
        return render(request, "askme/place_day_view.html", ctx)


class FoodRecommender(View):
    def get(self, request):
        form = FForm()
        ctx = {'form':form}
        return render(request, "askme/food_form.html", ctx)
    def post(self, request):
        
        place = request.POST.get("gpt_place")
        heading = "Food Recommendations for "+str(place).title()
        query_set = Food.objects.filter(gpt_place=place.lower().strip())

        if query_set:
            time.sleep(3.5)
            ctx = {"data":query_set[0].gpt_result, "place":place, "heading":heading}
            return render(request, "askme/post_food.html", ctx)

        # prompt = "give me popular restaurant recommendation in "+place+" and also the popular local foods"
        prompt = "give me 10 food recommendations in "+place+" at Popular Restaurants:, Cafes: and local foods: "
        # print(prompt)

        data = AskChat(prompt)
        ctx = {"data":data, "place":place, "heading":heading}

        data = Food.objects.create(gpt_place= place.lower().strip(), gpt_result= data)
        data.save()

        # data = Data.objects.create(gpt_place= place.lower().strip(), gpt_duration=duration, gpt_result= clean_data)
        # data.save()

        return render(request, "askme/post_food.html", ctx)


class Chat(View):
    def get(self, request):
        return redirect(reverse('askme:askme_mform'))
    def post(self, request):
        place = request.POST.get("again_place")
        duration = request.POST.get("again_duration")
        change_prompt = request.POST.get("personalize_prompt")
        
        t = Data.objects.get(gpt_place= place.lower().strip(), gpt_duration=duration)
        prev_prompt = t.gpt_result
        # print(place)
        # print(duration)

        # prompt = "act as a tour guide and give a "+duration+" days guide to visit "+place+" as (a place, breifly about it and what a tourist can do there) for morning and afternoon.then in the evening, 'end the day with' a popular restaurant/local food places. DO NOT REPEAT THE SAME PLACES TWICE."
        # prompt = "give me "+duration+" day itinerary for "+place+". format for each day (a place, about it and its specialty ) Morning:, Afternoon:, Evening:, End the day with:a dinner from a popular restaurant."
        data = InteractChat2(place, duration, user_inp=change_prompt)

        p2 = "make a python list of all the places in the format:['place'] in the below text:"+data
        data_p2 = AskChat(p2)
                
        # print(data_p2)
        clean_data = Clean_list(data, data_p2)
        heading = "Here's your "+str(duration)+"-days itinerary for "+str(place).title()
        heading2 = "Here's your "+str(duration)+"-days Personalized itinerary for "+str(place).title()
        
        
        if request.user.is_authenticated:
            latest_search = Search_history.objects.filter(user=request.user, search_place=place,search_duration=duration)[0]
            updated_values = {'search_query': "<h2><b>"+heading+"</b></h2>"+prev_prompt+"<h2><b>"+heading2+"</b></h2>"+clean_data}
            obj, created = Search_history.objects.update_or_create(
                    pk =latest_search.id, user=request.user, search_place=place,search_duration=duration,
                    defaults=updated_values
                )

        ctx = {"data":prev_prompt, "place":place, "duration":duration, "heading":heading, "extra_button":'yes', 'heading2':heading2, 'personalised':clean_data}

        # t = Data.objects.get(gpt_place= place, gpt_duration=duration)
        # t.gpt_result = clean_data  # change field
        # t.save()

        # updated_values = {'gpt_result': clean_data}

        # obj, created = Data.objects.update_or_create(
        #     gpt_place= place.lower().strip(), gpt_duration=duration,
        #     defaults=updated_values
        # )

        # obj, created = Data.objects.get_or_create(gpt_place=place.lower().strip(), gpt_duration=duration, gpt_result=clean_data)
        # obj.save()

        # data = Data.objects.create(gpt_place= place.lower().strip(), gpt_duration=duration, gpt_result= clean_data)
        # data.save()

        return render(request, "askme/post_ans.html", ctx)


class ItinerariesView(LoginRequiredMixin, View):
    def get(self, request):
        search_results = Search_history.objects.filter(user=request.user)
        ctx={'itineraries':search_results}
        print(ctx)
        return render(request, 'askme/itineraries.html',ctx)

class SingleItineraryView(LoginRequiredMixin, View):
    def get(self, request, i_id):
        search_results = Search_history.objects.get(pk=i_id)
        ctx={'itinerary':search_results}
        return render(request, 'askme/single_itinerary.html',ctx)


def flights(request):
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')
    dest = request.POST.get('destination')
    pair = find_closest_pair(latitude, longitude,dest.lower().strip())
    flight = generate_urls(pair[0], pair[1])
    # (hotel,flight) = generate_urls(find_closest_pair(latitude,longitude)[0],dest.lower().strip())
    return redirect(flight)

def hotel(request,place):
    today = datetime.today()
    today_date = str(today.year)+'-'+str(today.month)+'-'+str(today.day)
    tomorrow = today + timedelta(days=1)
    tomorrow_date = str(tomorrow.year)+'-'+str(tomorrow.month)+'-'+str(tomorrow.day)
    hotel = "https://www.expedia.co.in/Hotel-Search?destination={}&selected=&d1={}&startDate={}&d2={}&endDate={}&adults=2".format(str(place), today_date, today_date, tomorrow_date, tomorrow_date)
    return redirect(hotel)






# ------------------------------------------------------------------------------------------------------------------------------------------------
class Health(View):
    def get(self, request):
        return HttpResponse(status=200)


class Privacy(View):
    def get(self, request):
        return render(request, 'askme/privacy.html')


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

from django.http import JsonResponse
import json

def testing(request):
    data = {'message': 'This is an Ajax response!'}
    return JsonResponse(data)


def chatbot(request):
    print("working chatbot")
    if request.method == "POST":
        user_input = request.POST.get("user_input", "")
        # user_input += "<div class='user-message'>" + user_input + "</div>"
        chat_history = request.POST.get("chat_history", "")
        # Process user input and chat history, get bot response
        bot_response = "CHATBOT RESPONCE: "+user_input
        chat_history += bot_response
        print(chat_history)
        return JsonResponse({"bot_response": bot_response})
    return JsonResponse({"error": "Invalid request method"})

class Test(View):
    def get(self, request):
        return render(request, 'askme/test_view.html')




# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



class Home(View):
    def get(self, request):
        form = QForm()
        ctx = {'form':form}
        if request.user.is_authenticated:
            return redirect('askme:personal_home')
        else:
            return render(request, "askme/index.html", ctx)


def requestItinerary(request):
    start = datetime.now()
    place = request.GET.get('place', '').strip().lower()
    duration = request.GET.get('duration', '').strip()
    print(f"working itinerary: {place} for {str(duration)} days")
    query_set = Data.objects.filter(gpt_place=place, gpt_duration=duration)
    if query_set:
        print("present in database: "+str(query_set))
        if len(query_set)<2:
            print("has less than 2 instances")
            guid = str(uuid.uuid4()).split('-')[-1]
            heading = "Here's your "+str(duration)+"-days itinerary for "+str(place).title()
            result = {heading:AskV2(f"{place} and {duration}")}
            result = str(result)
            data = Data.objects.create(itinerary_id=guid, gpt_place=place, gpt_duration=duration, gpt_result=result)
            data.save()
            # query_set = Data.objects.filter(gpt_place=place, gpt_duration=duration)
            print("added "+str(data))
            iti_id = guid
        else:
            print("has exactly 2 instances")
            iti_id = query_set[random.randint(0,len(query_set)-1)].itinerary_id
    else:
        print("NOT in DATABASE")
        guid = str(uuid.uuid4()).split('-')[-1]
        heading = "Here's your "+str(duration)+"-days itinerary for "+str(place).title()
        result = {heading:AskV2(f"{place} and {duration}")}
        result = str(result)
        data = Data.objects.create(itinerary_id=guid, gpt_place=place, gpt_duration=duration, gpt_result=result)
        data.save()
        # query_set = Data.objects.filter(gpt_place=place, gpt_duration=duration)
        print("added "+str(data))
        iti_id = guid
    end = datetime.now()
    print(f"Took {end-start} sec")
    return redirect('askme:getItinerary', place_name=place,  iti_id=iti_id)

def hotel(request, place):
    today = datetime.today() + timedelta(days=1)
    today_date = str(today.year)+'-'+str(today.month)+'-'+str(today.day)
    tomorrow = today + timedelta(days=1)
    tomorrow_date = str(tomorrow.year)+'-'+str(tomorrow.month)+'-'+str(tomorrow.day)
    hotel = f"https://www.expedia.co.in/Hotel-Search?destination={str(place)}&selected=&d1={today_date}&startDate={today_date}&d2={tomorrow_date}&endDate={tomorrow_date}&adults=2"
    return redirect(hotel)

class GetItinerary(View):
    def get(self, request, place_name, iti_id):
        data_set = Data.objects.filter(itinerary_id=iti_id)[0]
        place = data_set.gpt_place.title()
        duration = int(data_set.gpt_duration)
        iti_dic = ast.literal_eval(data_set.gpt_result)
        data = {k:CleanDataV2(v, place) for k,v in iti_dic.items()}
        base_url = request.build_absolute_uri('/')+'itinerary/'+str(iti_id)
        ctx = {'place':place, 'data':data, 'base_url':base_url, 'iti_id':iti_id, 'duration':duration}
        return render(request, 'askme/post_ans.html', ctx)


# ERROR PAGES


def page_not_found(request, exception):
    print("404 error")
    return render(request, 'askme/404.html', status=404)

def server_error(request):
    print("500 error")
    return render(request, 'askme/500.html', status=500)


# FOOD RECOMMENDER

class FoodRecommender(View):
    def get(self, request):
        form = FForm()
        ctx = {'form':form}
        return render(request, "askme/food_form.html", ctx)
    


def requestFood(request):
    place = request.GET.get('food_place', '').strip().lower()
    print(f"working food: {place}")
    query_set = Food.objects.filter(food_place=place)
    if query_set:
        print("present in FOOD database: "+str(query_set))
        food_id = query_set[random.randint(0,len(query_set)-1)].food_id
    else:
        print("NOT in DATABASE")
        guid = str(uuid.uuid4()).split('-')[-1]

        result = FoodV2(f"{place}")      
        data = Food.objects.create(food_id=guid, food_place=place, food_result=result)
        data.save()
        # query_set = Data.objects.filter(gpt_place=place, gpt_duration=duration)
        print("added "+str(data))
        food_id = guid

    return redirect('askme:getFood', place_name=place, food_id=food_id)
    
class GetFoodfromItinerary(View):
    def get(self, request, place):
        place = place.strip().lower()
        print(f"working food: {place}")
        query_set = Food.objects.filter(food_place=place)
        if query_set:
            print("present in FOOD database: "+str(query_set))
            food = query_set[random.randint(0,len(query_set)-1)]
        else:
            print("NOT in DATABASE")
            guid = str(uuid.uuid4()).split('-')[-1]

            result = FoodV2(f"{place}")      
            food = Food.objects.create(food_id=guid, food_place=place, food_result=result)
            food.save()
            # query_set = Data.objects.filter(gpt_place=place, gpt_duration=duration)
            print("added "+str(food))

        heading = f"Food Recommendations for {str(food.food_place).title()}"
        ctx = {'heading':heading, 'data':CleanFoodV2(food.food_result)}
        return redirect('askme:getFood', place_name=place, food_id=food.food_id)
        
class GetFood(View):
    def get(self, request, place_name, food_id):
        data_set = Food.objects.filter(food_id=food_id)[0]
        heading = f"Food Recommendations for {str(data_set.food_place).title()}"
        ctx = {'heading':heading, 'data':CleanFoodV2(data_set.food_result)}
        return render(request, 'askme/post_food.html', ctx)



# PERSONALISATION AND CHAT

class PersonalHome(LoginRequiredMixin, View):
    def get(self, request):
        form = QForm()
        ctx = {'form':form}
        if request.user.is_authenticated:
            return render(request, 'askme/personal_index.html', ctx)
        else:
            return redirect('askme:home')

def requestPersonalItinerary(request):
    start = datetime.now()
    place = request.GET.get('place', '').strip().lower()
    duration = request.GET.get('duration', '').strip()
    my_user = request.user
    print(f"Requesting Personal itinerary: {place} for {str(duration)} days")
    query_set = Data.objects.filter(gpt_place=place, gpt_duration=duration)
    print("Checking in DATA DB")
    if query_set:
        print("present in DATA DB: "+str(query_set))
        iti_id = query_set[random.randint(0,len(query_set)-1)].itinerary_id
    else:
        print("NOT in DATA DB, hence creating an instance")
        guid = str(uuid.uuid4()).split('-')[-1]
        heading = "Here's your "+str(duration)+"-days itinerary for "+str(place).title()
        result = {heading:AskV2(f"{place} and {duration}")}
        result = str(result)
        data = Data.objects.create(itinerary_id=guid, gpt_place=place, gpt_duration=duration, gpt_result=result)
        data.save()
        # query_set = Data.objects.filter(gpt_place=place, gpt_duration=duration)
        print("added "+str(data))
        iti_id = guid
    end = datetime.now()
    print(f"Took {end-start} sec")
    return redirect('askme:createPID', iti_id=iti_id)
        

def createPID(request, iti_id):
    iti_data = Data.objects.get(itinerary_id=iti_id)
    guid = str(uuid.uuid4()).split('-')[-1]
    data = PersonalisedData.objects.create(user=request.user ,p_itinerary_id=guid, p_gpt_place=iti_data.gpt_place, p_gpt_duration=iti_data.gpt_duration, p_gpt_result=iti_data.gpt_result)
    data.save()
    return redirect('askme:getPersonalItinerary', piti_id=guid)

class GetPersonalItinerary(LoginRequiredMixin, View):
    def get(self, request, piti_id):
        data_set = PersonalisedData.objects.get(p_itinerary_id=piti_id)
        place = data_set.p_gpt_place.title()
        duration = int(data_set.p_gpt_duration)
        iti_dic = ast.literal_eval(data_set.p_gpt_result)
        data = {k:CleanDataV2(v, place) for k,v in iti_dic.items()}
        base_url = request.build_absolute_uri('/')+'itinerary/'+str(piti_id)
        ctx = {'place':place, 'data':data, 'base_url':base_url, 'iti_id':piti_id, 'duration':duration}
        return render(request, 'askme/post_ans.html', ctx)

def goto_personal_itinerary_section(request, piti_id):
    data_set = PersonalisedData.objects.get(p_itinerary_id=piti_id)
    result = ast.literal_eval(data_set.p_gpt_result)
    redirect_url = f"{request.build_absolute_uri(reverse('askme:getPersonalItinerary', args=[piti_id]))}#{len(result)}"
    #return redirect(redirect_url)
    return redirect('askme:getPersonalItinerary', piti_id=piti_id)

def interact(request, place, duration, iti_id):
    personalize_prompt = request.GET.get('personalize_prompt', '').strip()
    print(f"personalizing itinerary: {personalize_prompt}")

    data_set = PersonalisedData.objects.get(p_itinerary_id=iti_id)
    result = ast.literal_eval(data_set.p_gpt_result)
    result[personalize_prompt] = ChatV2(personalize_prompt, place, duration, result)
    data_set.p_gpt_result = result
    data_set.save()
    
    redirect_url = f"{request.build_absolute_uri(reverse('askme:getPersonalItinerary', args=[iti_id]))}#{len(result)}"

    #return redirect(redirect_url)
    return redirect('askme:getPersonalItinerary', piti_id=iti_id)
    


# query_set = Data.objects.filter(gpt_place=place, gpt_duration=duration)
    # if query_set:
    #     print("present in database: "+str(query_set))
    #     if len(query_set)<2:
    #         print("has less than 2 instances")
    #         guid = str(uuid.uuid4()).split('-')[-1]
    #         heading = "Here's your "+str(duration)+"-days itinerary for "+str(place).title()
    #         result = {heading:AskV2(f"{place} and {duration}")}
    #         result = str(result)
    #         data = Data.objects.create(itinerary_id=guid, gpt_place=place, gpt_duration=duration, gpt_result=result)
    #         data.save()
    #         # query_set = Data.objects.filter(gpt_place=place, gpt_duration=duration)
    #         print("added "+str(data))
    #         iti_id = guid
    #     else:
    #         print("has exactly 2 instances")
    #         iti_id = query_set[random.randint(0,len(query_set)-1)].itinerary_id
    # else:
    #     print("NOT in DATABASE")
    #     guid = str(uuid.uuid4()).split('-')[-1]
    #     heading = "Here's your "+str(duration)+"-days itinerary for "+str(place).title()
    #     result = {heading:AskV2(f"{place} and {duration}")}
    #     result = str(result)
    #     data = Data.objects.create(itinerary_id=guid, gpt_place=place, gpt_duration=duration, gpt_result=result)
    #     data.save()
    #     # query_set = Data.objects.filter(gpt_place=place, gpt_duration=duration)
    #     print("added "+str(data))
    #     iti_id = guid
    # end = datetime.now()
    # print(f"Took {end-start} sec")
    # return redirect('askme:getItinerary', iti_id=iti_id)


    # PERSONAL ITINERARY ETC

class ItinerariesView(View):
    def get(self, request):
        query_set = PersonalisedData.objects.filter(user = request.user)
        if len(query_set)>0:
            iti_list = [ (i.p_gpt_place, list(ast.literal_eval(i.p_gpt_result).keys())[-1], i.p_itinerary_id) for i in query_set]
            res = [(p,h,i) if h.split(" ")[0]!="Here's" else (p,"",i) for p,h,i in iti_list]
            ctx = {'itineraries':res}
            return render(request, 'askme/itineraries.html', ctx)
        else:
            ctx = {'none':True}
            return render(request, 'askme/itineraries.html', ctx)
            
