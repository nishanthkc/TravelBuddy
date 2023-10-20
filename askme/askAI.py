import openai
import re

def Ask(prompt):
    # prompt = sys.argv[1]
    # prompt = "who are you" here we will insert the question
    # openai.api_key = "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"
    openai.api_key = "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" # nishanth.churchmal00
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return (message)

def AskChat(prompt):
    # prompt = sys.argv[1]
    # prompt = "who are you" here we will insert the question
    # openai.api_key = "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"
    # openai.api_key = "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" # nishanth.churchmal00
    openai.api_key = "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" #thetravelbuddy.io
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt}
    ]
    )


    a = (completion.choices[0].message)["content"]
    # message = completions.choices[0].text
    return (a)

def InteractChat(prev_msg, prompt):
    # prompt = sys.argv[1]
    # prompt = "who are you" here we will insert the question
    # openai.api_key = "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"
    # openai.api_key = "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" # nishanth.churchmal00
    openai.api_key = "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" #thetravelbuddy.io

    msg_list =  [{"role": "assistant", "content":prev_msg }, {"role": "user", "content": prompt}]

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=msg_list
    )


    a = (completion.choices[0].message)["content"]
    # message = completions.choices[0].text
    return (a)


def InteractChat2(place, duration, user_inp):
    # prompt = sys.argv[1]
    # prompt = "who are you" here we will insert the question
    # openai.api_key = "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"
    # openai.api_key = "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" # nishanth.churchmal00
    openai.api_key = "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" #thetravelbuddy.io
    
    prompt = "give me "+str(duration)+" days detailed itinerary for "+place+". format for each day (a place, about it and its specialty ) Morning:, Afternoon:, Evening:, End the day with:a dinner from a popular restaurant."
    msg_list =  [{"role": "system", "content":"you are a professional and empathetic tourist guide. You take user requirements and suggest itineraries." }, 
                {"role": "user", "content": "User input: '"+user_inp+"'."+prompt}]

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=msg_list
    )
    
    a = (completion.choices[0].message)["content"]
    # message = completions.choices[0].text
    return (a)


def Clean_data(message):
    # message = message.replace("\n",". ")
    
    test = nlp(message)
    
    test_dict={}
    for i in test.ents:
        if i.label_ in test_dict.keys():
            test_dict[i.label_].append(i.text)
        else:
            test_dict[i.label_]=[i.text]

    for i in ["GPE", "LOC", "ORG", "FAC", "PERSON"]:
        if i in test_dict.keys():
            for j in test_dict[i]:            
                temp = j
                j=j.strip().replace(" ","+")
                j = '<a href="https://www.google.com/search?q='+j+'" >'+temp+'</a>'
                message = message.replace(temp,j)    

    return (message)


def Clean_data2(message, str_list):
    # message = message.replace("\n","\n ")

    mlist = str_list.split("TAGS:")
    print(mlist)
    places = mlist[1].replace("\n","").strip(" ").replace("]","").replace("[","").replace("'","").split(', ')
    print(places)

    for i in places:
        j=i.strip().replace(" ","+")
        temp = '<a href="https://www.google.com/search?q='+j+'" target="_blank" >'+i+'</a>'
        message = message.replace(i,temp)   

    for i in ["Morning:","Afternoon:","Evening:","Day","End the day with"]:
        if i in message:
            message = message.replace(i,'<b>'+i+'</b>')

    print(message) 

    return (message)


def Clean_list(message, str_list):

    places = str_list.replace("\n","").strip(" ").replace("]","").replace("[","").replace("'","").split(', ')
    print(places)

    for i in places:
        j=i.strip().replace(" ","+")
        temp = '<a href="https://www.google.com/search?q='+j+'" target="_blank" >'+i+'</a>'
        message = message.replace(i,temp)   

    for i in ["Morning:","Afternoon:","Evening:","Day","End the day with"]:
        if i in message:
            message = message.replace(i,'<b>'+i+'</b>')

    print(message) 

    return (message)


##################################################################################################################

    
def AskV2(prompt):
    # prompt = sys.argv[1]
    # prompt = "who are you" here we will insert the question
    # openai.api_key = "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"
    # openai.api_key = "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" # nishanth.churchmal00
    openai.api_key = "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" #thetravelbuddy.io V2
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": """Talk like a FUNNY and experienced travel guide. given the name of a place and duration, give an itinerary in the format for each day (a place, about it and its specialty ) Morning:, Afternoon:, Evening:, End the day with:a dinner from a popular restaurant. Don't forget to end the conversation with humour. If the place doesn't exist then end it humbly.
    MUST: In the end make a python list of all the places strictly in the format:`PLACES=['places']` with all the places in the itinerary.
    """},
        {"role": "user", "content": prompt}
    ]
    )

    return completion.choices[0].message.content

def CleanDataV2(text, place):
    text = text.replace("'","")
    note_parts = text.split('PLACES')
    if len(note_parts) == 2:
        message = note_parts[0].strip()
        str_list = note_parts[1].strip()
    else:
        message = text.strip()
        str_list=''
        
    if len(str_list)>2:
        places = str_list.split('[')[1]
        places = list(set(places.strip(" ").replace("]","").replace("'","").split(', ')))
        

        # Create a list to store the final filtered places
        filtered_places = []

        # Iterate through each place
        for p in places:
            is_substring = any(other_place != p and p in other_place for other_place in places)
            if not is_substring:
                filtered_places.append(p)
        places = filtered_places
        

        for i in places:
#             print(i)
            j=i.strip().replace(" ","+")+'+'+str(place)
            temp = '<a href="https://www.google.com/search?q='+j+'" target="_blank" >'+i+'</a>'
            message = message.replace(i,temp)   

        for i in ["Morning:","Afternoon:","Evening:","End the day with dinner"]:
            if i in message:
                message = message.replace(i,'<b>'+i+'</b>')
                
        pattern = r'Day\s\d+(\s*\w*)*\s*:'
        message = re.sub(pattern, lambda match: f'<p class="day-heading"><b>{match.group(0)}</b></p>', message)

    else:
        for i in ["Morning:","Afternoon:","Evening:","End the day with dinner"]:
            if i in message:
                message = message.replace(i,'<b>'+i+'</b>')
        pattern = r'Day\s\d+(\s*\w*)*\s*:'
        message = re.sub(pattern, lambda match: f'<p class="day-heading"><b>{match.group(0)}</b></p>', message)
    

    return (message)


def FoodV2(prompt):
    # prompt = sys.argv[1]
    # prompt = "who are you" here we will insert the question
    # openai.api_key = "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"
    # openai.api_key = "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" # nishanth.churchmal00
    openai.api_key = "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" #thetravelbuddy.io V2
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Talk like a very funny and excited Foodie who tried every food. given the name of a place give a food recommendations in that place, 5 each of famous: restaurants, cafes and local foods"},
        {"role": "user", "content": prompt}
    ]
    )

    return completion.choices[0].message.content


def CleanFoodV2(food):
    pattern = r"\n*(.*?):\s*"
    header = food.split('\n')[0]
    content = '\n'.join(food.split('\n')[1:])
    message = header+'\n'+re.sub(pattern, lambda match: f'\n<b>{match.group(0)}</b>', content)
    return message

def ChatV2(prompt, place, duration, result):
    fixed = f"{place} and {duration} days."
    heading_fixed = "Here's your "+str(duration)+"-days itinerary for "+str(place).title()
    message_list=[
        {"role": "system", "content": """Talk like a FUNNY and experienced travel guide. given the name of a place and duration, give an itinerary in the format for each day (a place, about it and its specialty ) Morning:, Afternoon:, Evening:, End the day with:a dinner from a popular restaurant. Don't forget to end the conversation with humour. If the place doesn't exist then end it humbly.
        MUST: In the end make a python list of all the places strictly in the format:`PLACES=['places']` with all the places in the itinerary.
        """}
        ]
    for heading,chat_response in result.items():
        if heading==heading_fixed:
            message_list.append({"role":"user","content":fixed})
            message_list.append({"role":"assistant","content":chat_response})
        else:
            message_list.append({"role":"user","content":fixed+heading})
            message_list.append({"role":"assistant","content":chat_response})
    message_list.append({"role":"user","content":fixed+prompt})
    
    openai.api_key = "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" #thetravelbuddy.io V2
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=message_list
    )

    return completion.choices[0].message.content


def FoodChatV2(prompt, place, result):
    fixed = f"{place}"
    heading_fixed = f"Food Recommendations for {str(place).title()}"
    message_list=[
        {"role": "system", "content": "Talk like a very funny and excited Foodie who tried every food. given the name of a place give a food recommendations in that place, 5 each of famous: restaurants, cafes and local foods"}
        ]
    for heading,chat_response in result.items():
        if heading==heading_fixed:
            message_list.append({"role":"user","content":fixed})
            message_list.append({"role":"assistant","content":chat_response})
        else:
            message_list.append({"role":"user","content":fixed+heading})
            message_list.append({"role":"assistant","content":chat_response})
    message_list.append({"role":"user","content":fixed+prompt})
    
    openai.api_key = "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" #thetravelbuddy.io V2
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=message_list
    )

    return completion.choices[0].message.content