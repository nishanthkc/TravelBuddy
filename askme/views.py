from django.shortcuts import render, get_list_or_404, redirect
from django.views import View
from .askAI import Ask, Clean_data, Clean_data2, AskChat, Clean_list, InteractChat
from .forms import AskForm, QForm, FForm
from .models import Queries, Data, Food, Statistics
from django.urls import reverse

from django.db.models import Sum, Count

import json
import requests
from urllib.request import urlopen

import time

# Create your views here.
class Home(View):
    def get(self, request):
        # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        # if x_forwarded_for:
        #     ip = x_forwarded_for.split(',')[0]
        # else:
        #     ip = request.META.get('REMOTE_ADDR')

        # url = 'http://ipinfo.io/json'
        # response = urlopen(url)
        # data = json.load(response)

        # ctx={'ip':ip, 'data':data}
        return render(request, "askme/main.html")
    def post(self, request):
        place = request.POST.get("place")
        duration = request.POST.get("duration")
        # prompt = "act as a tour guide and give a "+duration+" days guide to visit "+place+" as (a place, breifly about it and what a tourist can do there) for morning, afternoon and evening ( the places covered in one day should not be repeated in anyother day ) .then 'end the day with' a popular restaurant/local food places."
        # prompt = "give me "+duration+" days itinerary for "+place+". format for each day (a place, breifly about it and what a tourist can do there) Morning:, Afternoon:, Evening:, End the day with:a dinner from a popular restaurant."
        

        stats_set = Statistics.objects.filter(stat_place=place.lower().strip(), stat_duration=duration)

        if stats_set:
            updated_values = {'stat_count': stats_set[0].stat_count+1}
        else:
            updated_values = {'stat_count': 1}

        obj, created = Statistics.objects.update_or_create(
            stat_place= place.lower().strip(), stat_duration=duration,
            defaults=updated_values
        )


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
                    ctx = {"data":clean_data, "place":place, "duration":duration, "heading":heading, "extra_button":'yes'}

                    data = Data.objects.create(gpt_place= place.lower().strip(), gpt_duration=duration, gpt_result= clean_data)
                    data.save()

                    # # add session data
                    # request.session["again_place"] = place
                    # request.session["again_duration"] = duration

                    return render(request, "askme/post_ans.html", ctx)
        else:
            data = "I'm sorry, but '"+place+"' is not a known place or city. Can you provide more information or clarify the name of the destination you would like me to create an itinerary for?"
            ctx = {"data":data}
            return render(request, "askme/post_ans.html", ctx)
        # data = Clean_prompt(msg)
        ctx = {"data":data}
        return render(request, "askme/post_ans.html", ctx)

class FormHome(View):
    def get(self, request):
        form = AskForm()
        ctx = {'form':form}
        return render(request, "askme/form.html", ctx)
    def post(self, request):
        form = AskForm(request.POST)
        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, "askme/form.html", ctx)
        # If there are no errors, we would use it to get an answer
        place = request.POST.get("place")
        duration = request.POST.get("duration")

        test1 = "does the following place as it is exists on earth, tell either '1' for yes or '0' no: '"+place
        test1_data = Ask(test1)
        
        if "1" in test1_data:
            # prompt = "does the following place as it is exists on earth, tell either 1 for yes or 0 no: '"+place+"'. if yes, tell me a "+duration+" days detailed day-wise itinerary to vist "+place+" in the format: morning, afternoon and evening with places name and what we can do there in a 2 sentence format. If no output the following:Nonononono"
            # prompt = "tell me a "+duration+" days detailed day-wise itinerary to vist "+place+" in the format: morning, afternoon and evening with places name and what we can do there in a 2 sentence format"

            # prompt = "give me a "+duration+"  days point-wise detailed itinerary to visit "+place+" in the following format daywise, point-wise detailed itinerary for each day (END OF FORMAT). In the end give top rated restaurants and the food they are known for in "+place+". End with a list popular local food in "+place+". in the end generate a list of all place, restaurant and food names mentioned above on the name 'PYTHON LIST' in this format: ['place_name']"
            
            # prompt = "give me a "+duration+" days detailed itinerary to visit "+place+" in the following format daywise, point-wise itinerary for each day. also give recommended restaurants nearby(END OF FORMAT). in the end generate a list of all place names in this format:'TAGS: ['place_name']'"

            # prompt = "give me a "+duration+" days tour guide to visit "+place+" (as one place, briefly about the place and what to do there, and another nearby place and what to do there) for each morning, afternoon and evening each day."

            # prompt = "act as a tour guide and give a "+duration+" days guide to visit "+place+" as (a place, breifly about it and what a tourist can do there) for morning and afternoon.then in the evening, 'end the day with' a popular restaurant/local food places(END OF FORMAT). after all this generate a list of all place names in this format:'TAGS: [place_name]'"

            prompt = "act as a tour guide and give a "+duration+" days guide to visit "+place+" as (a place, breifly about it and what a tourist can do there) for morning and afternoon.then in the evening, 'end the day with' a popular restaurant/local food places."

            data = Ask(prompt)

            p2 = "generate a list of all place names in this format:'TAGS: ['place_name']' from the given text: "+data
            data_p2 = Ask(p2)
            
            print(data_p2)
            clean_data = Clean_data2(data, data_p2)
            # data = Clean_prompt(msg)
            ctx = {"data":clean_data}
            return render(request, "askme/post_ans.html", ctx)
        else:
            data = "I'm sorry, but '"+place+"' is not a known place or city. Can you provide more information or clarify the name of the destination you would like me to create an itinerary for?"
            ctx = {"data":data}
            return render(request, "askme/post_ans.html", ctx)

        # give me a 4 day itinerary to visit hyderabad in the following format daywise, a recommendation for breakfast, lunch and dinner then a detailed itenerary for that day
        # give me a 4 day itinerary to visit hyderabad in the following format daywise, a detailed itenerary for that day, a recommendation for breakfast, lunch and dinner for each day

        # prompt = "can you give me a "+duration+" days detailed itinerary to "+place
        # THIS IS GOOD # prompt = "give me a "+duration+"  days point-wise details itinerary to visit "+place+" in the following format daywise, point-wise detailed itinerary for each day. In the end give top rated restaurants and the food they are known for in "+place
        # prompt = "give me a "+duration+"  days point-wise detailed itinerary to visit "+place+" in the following format daywise, point-wise detailed itinerary for each day (END OF FORMAT). In the end give top rated restaurants and the food they are known for in "+place+". End with a list popular local food in "+place
        # "give me a "+duration+" days itinerary to vist "+place+"in the format: morning, afternoon and evening places to visit"
        # prompt = "assume that you are a tourist guide, tell me a "+duration+" days detailed day-wise itinerary to vist "+place+" in the format: morning, afternoon and evening"


        # "give me a 4 days point-wise detailed itinerary to visit Hyderabad in the following format daywise, point-wise detailed itinerary for each day (END OF FORMAT). In the end give top rated restaurants and the food they are known for in . End with a list popular local food in Hyderabad. in the end generate a list of all place names in this format: ['place_name']"


        # . convert the same into a json format
        
        
        # TO CHECK A PLACE EXISTS OR NOT
        # if Check_place(place):
        #     prompt = "tell me a "+duration+" days detailed day-wise itinerary to vist "+place+" in the format: morning, afternoon and evening with places name and what we can do there in a 2 sentence format"
        #     data = Ask(prompt)
        #     ctx = {"data":data}
        # else:
        #     data = "I'm sorry, but '"+place+"' is not a known place or city. Can you provide more information or clarify the name of the destination you would like me to create an itinerary for?"
        #     ctx = {"data":data}


        # "give me a 4 days detailed itinerary to visit Hyderabad in the following format daywise, point-wise itinerary for each day. also give recommended restaurants nearby(END OF FORMAT). in the end generate a list of all place names in this format: ['place_name']"



        # THIS IS ALMOST PERFECT
        # prompt = "act as a tour guide and give a "+duration+" days guide to visit "+place+" as (a place, breifly about it and what a tourist can do there) for morning and afternoon.then in the evening, 'end the day with' a popular restaurant/local food places"
        
        
        
        # prompt = "act as a tour guide and give a "+duration+" days practically doable guide to visit "+place+" as (a place, very breifly about it and what a tourist can do there) for morning and afternoon.then in the evening, 'end the day with' a popular restaurant/local food places for each day"



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
                ctx = {"data":query_set[0].gpt_result, "place":place, "duration":duration, "heading":heading, "extra_button":'yes'}
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
                    ctx = {"data":clean_data, "place":place, "duration":duration, "heading":heading, "extra_button":'yes'}

                    data = Data.objects.create(gpt_place= place.lower().strip(), gpt_duration=duration, gpt_result= clean_data)
                    data.save()

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

        change_prompt = "personalize itinerary by "+request.POST.get("personalize_prompt")
        t = Data.objects.get(gpt_place= place.lower().strip(), gpt_duration=duration)
        prev_prompt = t.gpt_result
        # print(place)
        # print(duration)

        # prompt = "act as a tour guide and give a "+duration+" days guide to visit "+place+" as (a place, breifly about it and what a tourist can do there) for morning and afternoon.then in the evening, 'end the day with' a popular restaurant/local food places. DO NOT REPEAT THE SAME PLACES TWICE."
        # prompt = "give me "+duration+" day itinerary for "+place+". format for each day (a place, about it and its specialty ) Morning:, Afternoon:, Evening:, End the day with:a dinner from a popular restaurant."
        data = InteractChat(prev_prompt, change_prompt)

        p2 = "make a python list of all the places in the format:['place'] in the below text:"+data
        data_p2 = AskChat(p2)
                
        # print(data_p2)
        clean_data = Clean_list(data, data_p2)
        heading = "Here's your "+str(duration)+"-days itinerary for "+str(place).title()
        heading2 = "Here's your "+str(duration)+"-days Personalized itinerary for "+str(place).title()
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