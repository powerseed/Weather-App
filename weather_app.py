from h2o_wave import Q, main, app, ui
import requests
import json

API_key = "f3a8554b81af781f7b0434afce72f0c6"
url = "https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={API_key}"
response_dict = None

@app('/weather')
async def serve(q: Q):        
    if not q.client.initialized:
        q.client.initialized = True
        
        q.app.city = 'London'
        response = requests.get(url.format(city = q.app.city, API_key = API_key))
        response_dict = json.loads(response.text)
        
        q.page['city_input_field'] = ui.form_card(
            box='1 1 2 2',
            items=[
                ui.textbox(name='city_input_field', label='City', trigger=True),
                ui.text(name='alert', content='')
            ]
        )
        
        q.page['city'] = ui.tall_stats_card(
            box='1 3 2 4',
            items=[
                ui.stat(name='city', label="City", value=response_dict["name"])
            ]
        )

        q.page['weather'] = ui.tall_stats_card(
            box='3 3 2 4',
            items=[
                ui.stat(name='weather', label='Weather', value=response_dict["weather"][0]["main"]),
                ui.stat(name='details', label='Details', value=response_dict["weather"][0]["description"]),
            ]
        )

        q.page['temperature'] = ui.tall_stats_card(
            box='5 3 2 4',
            items=[
                ui.stat(name='temperature', label='Temperature', value=str(response_dict["main"]["temp"])),
                ui.stat(name='feels_like', label='Feels like', value=str(response_dict["main"]["feels_like"])),
                ui.stat(name='min', label='Minimum', value=str(response_dict["main"]["temp_min"])),
                ui.stat(name='max', label='Maximum', value=str(response_dict["main"]["temp_max"])),
            ]
        )

        q.page['pressure'] = ui.tall_stats_card(
            box='7 3 2 4',
            items=[
                ui.stat(name='pressure', label='Pressure', value=str(response_dict["main"]["pressure"])),
            ]
        )

        q.page['humidity'] = ui.tall_stats_card(
            box='1 7 2 4',
            items=[
                ui.stat(name='humidity', label='Humidity', value=str(response_dict["main"]["humidity"])),
            ]
        )

        q.page['visibility'] = ui.tall_stats_card(
            box='3 7 2 4',
            items=[
                ui.stat(name='visibility', label='Visibility', value=str(response_dict["visibility"])),
            ]
        )

        q.page['wind'] = ui.tall_stats_card(
            box='5 7 2 4',
            items=[
                ui.stat(name='speed', label='Wind speed', value=str(response_dict["wind"]["speed"])),
            ]
        )
    else:
        if q.args.city_input_field and q.args.city_input_field != "":
            q.app.city = q.args.city_input_field
            response = requests.get(url.format(city = q.app.city, API_key = API_key))
            response_dict = json.loads(response.text)

            if response_dict["cod"] == 200:
                q.page['city_input_field'].alert.content = ""
                
                q.page['city'].city.value = response_dict["name"]
                
                q.page['weather'].weather.value = response_dict["weather"][0]["main"]
                q.page['weather'].details.value = response_dict["weather"][0]["description"]
                
                q.page['temperature'].temperature.value = str(response_dict["main"]["temp"])
                q.page['temperature'].feels_like.value = str(response_dict["main"]["feels_like"])
                q.page['temperature'].min.value = str(response_dict["main"]["temp_min"])
                q.page['temperature'].max.value = str(response_dict["main"]["temp_max"])
                        
                q.page['pressure'].pressure.value = str(response_dict["main"]["pressure"])
                
                q.page['humidity'].humidity.value = str(response_dict["main"]["humidity"])
                
                q.page['visibility'].visibility.value = str(response_dict["visibility"])
                
                q.page['wind'].speed.value = str(response_dict["wind"]["speed"])
            else:
                q.page['city_input_field'].alert.content = "City not found. "     
    
    await q.page.save()