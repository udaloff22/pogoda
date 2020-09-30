import pyowm as owm
mgr = owm.OWM('000000000000000000000000000000000000').weather_manager()

running=True
while running:
    place = input('which town, brah? ')
    if place != 'exit':# условие, нужен ли выход или нет

        try:
            observation = mgr.weather_at_place(place)
            w = observation.weather
            correct =True
        except:
            correct =False
            print('wrong hood brah..')

        if correct == True:

            temper  = w.temperature('celsius')['temp']
            temper_max = w.temperature('celsius')['temp_max']
            temper_min = w.temperature('celsius')['temp_min']

            stts = w.status
            dtld_stts = w.detailed_status

            pogoda = [
            'temper in ' + str(place) + ' = ' + str(temper),
            'temper_max in ' + str(place) + ' = ' + str(temper_max),
            'temper_min in ' + str(place) + ' = ' + str(temper_min),
            'status in ' + str(place) + ' = ' + str(stts),
            'detailed_status in ' + str(place) + ' = ' + str(dtld_stts)
            ]

            pogoda_str = str(pogoda)

            file = open('pgd.txt', 'w')
            file.write(pogoda_str)
            file.close()

            print()
            print()
            print('temper in ' + str(place) + ' = ' + str(temper))
            print('temper_max in ' + str(place) + ' = ' + str(temper_max))
            print('temper_min in ' + str(place) + ' = ' + str(temper_min))
            print('status in ' + str(place) + ' = ' + str(stts))
            print('detailed_status in ' + str(place) + ' = ' + str(dtld_stts))
            print()
            print()

    else:
        print('poka, brah..')
        exit()

def exit():


    running=False
