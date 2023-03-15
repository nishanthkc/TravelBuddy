import openai

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




    