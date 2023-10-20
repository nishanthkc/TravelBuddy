# scripts/update_food_table.py
from askme.models import Food

def run():
    food_objects = Food.objects.all()
    for obj in food_objects:
        print(f"Changed: {obj.food_place}-{obj.food_id}")
        new_dict = {f"Food Recommendations for {str(obj.food_place).title()}": obj.food_result}
        new_result = str(new_dict)

        obj.food_result = new_result
        obj.save()
