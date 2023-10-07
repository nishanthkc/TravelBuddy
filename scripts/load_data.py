from askme.models import Data
import csv
import uuid
# import pandas as pd

def run():
    # with open('askme/data.csv') as file:
    with open('askme/Final_chatGPT_data_V2_freq-2.csv') as file:
        # reader = csv.reader(file)
        reader = csv.DictReader(file)
        next(reader)  # Advance past the header

        Data.objects.all().delete()
        count = 0
        
        for row in reader:
            # print(row)

            # data = Data.objects.create(gpt_place=row[1],
            #             gpt_duration=row[2],
            #             gpt_result=row[3])
            try:
                print("loading row number "+str(count))
                count += 1
                guid = "pre"+str(uuid.uuid4()).split('-')[-1]
                heading = "Here's your "+str(row['duration'])+"-days itinerary for "+str(row['place']).title()
                result = {heading:row['result']}
                result = str(result)
                data = Data.objects.create(itinerary_id=guid,
                            gpt_place=row['place'],
                            gpt_duration=row['duration'],
                            gpt_result=result)
                
                data.save()
            except:
                print("FAIL")
                print(row['duration'])
                pass

# def run():
#     # with open('askme/data.csv') as file:
#     # with open('askme/FINAL_DATA.csv') as file:
#         # reader = csv.reader(file)
#     df = pd.read_csv('askme/FINAL_DATA.csv')
        
#     for i in range(len(df)):
#         print("i is: "+str(i))
#         print(df['place'][i]+'('+str(df['duration'][i])+')')
#         place = df['place'][i]
#         duration = df['duration'][i]
#         result = df['result'][i]

#         Data.objects.all().delete()

#         data = Data.objects.create(gpt_place=place,
#                         gpt_duration=duration,
#                         gpt_result=result)
            
#         data.save()