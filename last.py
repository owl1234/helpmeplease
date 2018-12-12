import sys
import requests
import pygame
import os
import math

screen_height = 650
screen_width = 450
pygame.init()
screen = pygame.display.set_mode((screen_height, screen_width))
screen.fill((255, 255, 0))

font_for_text = pygame.font.Font(None, 60)
text1 = font_for_text.render('Введите две координаты:', 1, (0, 0, 0))
text2 = font_for_text.render("широту и долготу", 0, (0, 0, 0))

screen.blit(text1, (50, 225))
screen.blit(text2, (150, 260))

pygame.display.flip()

#list_of_spn = ["50,50", "45,45", "40,40", "35,35", "30,30", "25,25", "20,20", "15,15", "10,10", "5,5", "1,1", "0.5,0.5", "0.1,0.1", "0.01,0.01", "0.04,0.04", "0.07,0.07"]
list_of_spn = ["10,10", "0.1,0.1", "0.01,0.01", "0.005,0.005"]
list_of_spn1 = ["24.13,-17", "0.43,-0.20", "0.025,-0.015", "0.014,-0.006"]
index = 3
z = 14
class Label:
    def __init__(self, rect, text, fcolor = "gray", bcolor = "white"):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.bgcolor = bcolor
        self.font_color = pygame.Color(fcolor)
        # Рассчитываем размер шрифта в зависимости от высоты
        self.font = pygame.font.Font(None, self.rect.height - 10)
        self.rendered_text = None
        self.rendered_rect = None


    def render(self, surface):
        if self.bgcolor != -1:
            surface.fill(pygame.Color(self.bgcolor), self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
            # выводим текст
        surface.blit(self.rendered_text, self.rendered_rect)
lon = None
lat = None
flag_of_search = None
flag_of_mouse = 0
flag_of_index = 0
flag_flag = 0
flag_of_org = 0

class Button(Label):
    def __init__(self, rect, text):
        super().__init__(rect, text)
        self.font = pygame.font.Font(None, self.rect.height - 20)
        self.bgcolor = pygame.Color("black")
        self.text = text
        # при создании кнопка не нажата
        self.pressed = False

    def render(self, surface):
        global flag_of_mouse
        surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        if not self.pressed:
            color1 = pygame.Color("gray")
            color2 = pygame.Color("black")
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 5, centery=self.rect.centery)
        else:
            flag_of_mouse = 0
            color1 = pygame.Color("gray")
            color2 = pygame.Color("white")
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 7, centery=self.rect.centery + 2)

        # рисуем границу
        pygame.draw.rect(surface, color1, self.rect, 2)
        pygame.draw.line(surface, color2, (self.rect.right - 1, self.rect.top), (self.rect.right - 1, self.rect.bottom), 2)
        pygame.draw.line(surface, color2, (self.rect.left, self.rect.bottom - 1),
                         (self.rect.right, self.rect.bottom - 1), 2)
        # выводим текст
        surface.blit(self.rendered_text, self.rendered_rect)

    def get_event(self, event):
        global lon, lat, flag_of_search, text_out, flag_of_index, flag_flag, flag_of_start_use, map_params
        try:
            self.pressed = self.rect.collidepoint(event.pos)
        except:
            pass
        if self.pressed == True or flag_flag != 0:
            if self.text == "Найти" and (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or flag_flag != 0):
                #self.pressed = self.rect.collidepoint(event.pos)
                # послать запрос
                search_str = text_in.text

                #print(search_str)
                try:
                    coordinates, address, postal_code = coordinates_of_object("https://geocode-maps.yandex.ru/1.x/?geocode=" + search_str + "&format=json")
                except:
                    print("Error (Button)")
                    sys.exit()
                if not coordinates:
                    print("Error (Button)")
                    sys.exit()
                #print("".join(coordinates).split())
                coordinates = "".join(coordinates).split()
                lon = coordinates[1]
                lat = coordinates[0]

                #print(lat + "," + lon)
                #print(address)
                #print(postal_code)

                flag_of_search = 1
                #address = address_of_object
                if flag_of_index == 1 or flag_flag == 1:
                    address += ", " + postal_code
                #elif flag_flag == -1:

                #print(address)
                text_out = TextBox((325, 0, 320, 50), address)
                #print(flag_of_start_use)
                if flag_of_start_use == 0:
                    map_params = {
                        "ll": lat + "," + lon,
                        "size": "{0},{1}".format(str(screen_height), str(screen_width)),
                        "l": "map",
                        "spn": list_of_spn[index],
                        "pt": lat + "," + lon
                    }
                    flag_of_start_use = -1
                #print(flag_of_start_use)

            elif self.text == "Найти" and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.pressed = False

            if self.text == "Сброс" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                flag_of_search = 0
                flag_flag = 0

            elif self.text == "Сброс" and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.pressed = False


class GUI:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def render(self, surface):
        for element in self.elements:
            render = getattr(element, "render", None)
            if callable(render):
                element.render(surface)

    def update(self):
        for element in self.elements:
            update = getattr(element, "update", None)
            if callable(update):
                element.update()

    def get_event(self, event):
        for element in self.elements:
            get_event = getattr(element, "get_event", None)
            if callable(get_event):
                element.get_event(event)

class TextBox(Label):
    def __init__(self, rect, text):
        super().__init__(rect, text)
        self.active = True
        self.blink = True
        self.blink_timer = 0

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                pass
            elif event.key == pygame.K_BACKSPACE:
                if len(self.text) > 0:
                    self.text = self.text[:-1]
            else:
                self.text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)

    def update(self):
        if pygame.time.get_ticks() - self.blink_timer > 200:
            self.blink = not self.blink
            self.blink_timer = pygame.time.get_ticks()

    def render(self, surface):
        super(TextBox, self).render(surface)
        if self.blink and self.active:
            pygame.draw.line(surface, pygame.Color("black"),
                             (self.rendered_rect.right + 2, self.rendered_rect.top + 2),
                             (self.rendered_rect.right + 2, self.rendered_rect.bottom - 2))

gui = GUI()
b1 = Button((10, 65, 100, 60), "Найти")
b2 = Button((110, 65, 100, 60), "Сброс")
# "нажмем" одну для демонстрации
b1.pressed = True
b2.pressed = True
gui.add_element(b1)
gui.add_element(b2)
text_in = TextBox((0, 0, 315, 50), '')
text_out = None

def get_town(search):
    response = None
    try:
        response = requests.get(search)
        if response:
            # Преобразуем ответ в json-объект
            json_response = response.json()

            # Получаем первый топоним из ответа геокодера.
            # Согласно описанию ответа он находится по следующему пути:
            begin = json_response["response"]["GeoObjectCollection"]
            #print(1)
            found = begin["metaDataProperty"]["GeocoderResponseMetaData"]["found"]
            #print(2)
            if found == 0:
                print("Не удалось найти требуемый объект. Проверьте правильность названия объекта и выполните запрос ещё раз.")
                return
            #address_of_object = begin["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]
            #print(3)
            found_town = begin["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"][4]['name']
            #print(found_town)

            return found_town
        else:
            print("Ошибка выполнения запроса (coordinates_of_object):")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            return
    except:
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет (coordinates_of_object).")
        return

def lonlat_distance(a, b):

    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b

    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    distance = math.sqrt(dx * dx + dy * dy)

    return distance

def find_first_organisation(lat, lon):
    global flag_of_index
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "3c4a592e-c4c0-4949-85d1-97291c87825c"
    #print("latlon", lat, lon)
    address_ll = "{0},{1}".format(lon, lat)
    #print(address_ll)
    #print("https://geocode-maps.yandex.ru/1.x/?geocode=" + address_ll + "&format=json")
    our_town = get_town("https://geocode-maps.yandex.ru/1.x/?geocode=" + address_ll + "&format=json")
    #return
    #address_ll = "41.404429,52.769208"

    search_params = {
        "apikey": api_key,
        #"text": our_town,
        "lang": "ru_RU",
        #"rspn": 1,
        "results": 500,
        "ll": address_ll,
        "type": "biz"
    }



    response = requests.get(search_api_server, params=search_params)
    if not response:
        return -1


    # Преобразуем ответ в json-объект
    json_response = response.json()

    # Получаем первую найденную организацию.
    try:
        #print(json_response["features"])
        organization = json_response["features"][0]["properties"]["CompanyMetaData"]
        #print(json_response["features"])
        #print()
        #print(json_response["features"][0])
        #print()
        #print(json_response["features"][0]["properties"])
        #print()
        #print(json_response["features"][0]["properties"]["id"])
        #print()
        print(json_response["features"][0]["properties"]["CompanyMetaData"])

        minn = 0
        minn_index = 0
        ch = 0
        flagg = 0
        for i in json_response["features"]:
            j = i["properties"]["CompanyMetaData"]

            #coordd = "response":{"GeoObjectCollection":{"metaDataProperty":{"GeocoderResponseMetaData":{"request":"41.44973233333333,52.721885666666665","found":"7","results":"10","Point":{"pos"
            coordd = i["geometry"]["coordinates"]
            #print(coordd)
            #print(float(coordd[0]), float(coordd[1]))
            #print(lonlat_distance((lon, lat), (float(coordd[0]), float(coordd[1]))))
            if lonlat_distance((lon, lat), (float(coordd[0]), float(coordd[1]))) < 50:
                minn = lonlat_distance((lon, lat), (float(coordd[0]), float(coordd[1])))
                minn_index = ch
                flagg = 1
                break
            #print(coordd)
            ch += 1
        if flagg == 0:
            return -1
        #print(minn_index)
        #org_address = json_response["features"][minn_index]["properties"]["CompanyMetaData"]["address"]
        #print(json_response["features"])
        #print(json_response["features"][minn_index]["properties"]["CompanyMetaData"])
        #print(json_response["features"][minn_index]["properties"]["CompanyMetaData"]["address"])
        #print(json_response["features"][minn_index]["properties"]['References'])
        #print(json_response["features"][minn_index]["geometry"])

        #if flag_of_index == 1:
        #    org_address += ', ' + organization["postalCode"]
        #print(our_town)
        #print(json_response["features"][minn_index]["properties"]["CompanyMetaData"]["address"])
        #print(str(our_town + ', ' + json_response["features"][minn_index]["properties"]["CompanyMetaData"]["address"]))
        #print(json_response["features"][minn_index]["geometry"]["coordinates"])
        return [our_town + ', ' + json_response["features"][minn_index]["properties"]["CompanyMetaData"]["address"], json_response["features"][minn_index]["geometry"]["coordinates"], json_response["features"][minn_index]["properties"]["CompanyMetaData"]["name"]]
    except:
        pass

def coordinates_of_mouse(mouse_pos, lon, lat):
    global index
    #print(list_of_spn[index])
    coeffic_x = float(list_of_spn1[index].split(',')[0]) / screen_height
    coeffic_y = float(list_of_spn1[index].split(',')[1]) / screen_width
    begin_x = float(lat) - screen_height // 2 * coeffic_x
    begin_y = float(lon) - screen_width // 2 * coeffic_y
    now_x = begin_x + coeffic_x * mouse_pos[0]
    now_y = begin_y + coeffic_y * mouse_pos[1]
    #print('mouse:', mouse_pos)
    #print('coeff_x:', coeffic_x, 'coeff_y:', coeffic_y, "begin_x:", begin_x, "begin_y:", begin_y, 'now_x:', now_x, 'now_y:', now_y)
    #print(now_x, now_y)
    return [now_x, now_y]

def coordinates_of_object(search):
    response = None
    try:
        response = requests.get(search)
        if response:
            # Преобразуем ответ в json-объект
            json_response = response.json()

            # Получаем первый топоним из ответа геокодера.
            # Согласно описанию ответа он находится по следующему пути:
            begin = json_response["response"]["GeoObjectCollection"]
            found = begin["metaDataProperty"]["GeocoderResponseMetaData"]["found"]
            print(found)
            if found == 0:
                print("Не удалось найти требуемый объект. Проверьте правильность названия объекта и выполните запрос ещё раз.")
                return
            address_of_object = begin["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]
            toponym_index = ""
            try:
                toponym_index = begin["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
                print(toponym_index)
            except:
                print("У поискового объекта нет индекса. Уточните адрес для получения полной информации.")

            print(address_of_object)
            toponym = begin["featureMember"][0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            return [toponym_coodrinates, address_of_object, toponym_index]
        else:
            print("Ошибка выполнения запроса (coordinates_of_object):")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            return
    except:
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет (coordinates_of_object).")
        return

#def address(ser)

map_file = None
def get_image(map_params):
    global map_file, flag_of_start_use
    try:
        os.remove(map_file)
    except:
        pass

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)


lat, lon = None, None
flag_of_start_use = 0

running = True
lat1, lon1 = None, None
spn = "0.05,0.05"
type_of_map = "map"
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and flag_of_start_use ** 2 == 1:
            if event.key == pygame.K_PAGEUP:
                if index < 3:
                    index += 1
                if index == 2:
                    z = 15
                if index == 3:
                    z = 16
                if index == 1:
                    z = 11
                if index == 0:
                    z = 5
                    #break
            elif event.key == pygame.K_PAGEDOWN:
                if index > -1:
                    index -= 1
                if index == 2:
                    z = 15
                if index == 3:
                    z = 16
                if index == 1:
                    z = 11
                if index == 0:
                    z = 5
                    #break
            elif event.key == pygame.K_RIGHT:
                move_lat = 360 / (2 ** (z + 8)) * 575
                if float(lat) + move_lat <= 90:
                    lat = str(float(lat) + move_lat)

            elif event.key == pygame.K_LEFT:
                move_lat = 360 / (2 ** (z + 8)) * 575
                if float(lat) - move_lat >= 0:
                    lat = str(float(lat) - move_lat)

            elif event.key == pygame.K_UP:
                move_lon = math.cos(math.radians(float(lon))) * 180 / (2 ** (z + 8)) * 800
                if float(lon) + move_lon <= 180:
                    lon = str(float(lon) + move_lon)

            elif event.key == pygame.K_DOWN:
                move_lon = math.cos(math.radians(float(lon))) * 180 / (2 ** (z + 8)) * 800
                if float(lon) - move_lon >= 0:
                    lon = str(float(lon) - move_lon)

            elif event.key == pygame.K_F1:
                type_of_map = "map"
            elif event.key == pygame.K_F2:
                type_of_map = "sat"
            elif event.key == pygame.K_F3:
                type_of_map = "sat,skl"

            elif event.key == pygame.K_1:
                flag_of_index = 1
                flag_flag = 1
            elif event.key == pygame.K_0:
                flag_of_index = 0
                flag_flag = -1

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and flag_of_start_use ** 2 == 1:
            mouse_pos = pygame.mouse.get_pos()
            lat1, lon1 = coordinates_of_mouse(mouse_pos, lon, lat)
            #print(lon, lat)
            flag_of_mouse = 1
            search_str = "{0},{1}".format(lat1, lon1)
            try:
                coordinatess, address_mouse, postal_codes = coordinates_of_object("https://geocode-maps.yandex.ru/1.x/?geocode=" + search_str + "&format=json")
                #print(address_mouse)
            except:
                print("Error (while)")
                sys.exit()
            if not coordinatess:
                print("Error (while)")
                sys.exit()
                #print("".join(coordinates).split())
            #coordinates = "".join(coordinates).split()
            #lon = coordinates[1]
            #lat = coordinates[0]
                #print(lat + "," + lon)
            #flag_of_search = 1
                #address = address_of_object

            if flag_of_index == 1 or flag_flag == 1:
                address += ", " + postal_codes
                #elif flag_flag == -1:

            #print(address_mouse)
            text_out = TextBox((325, 0, 320, 50), address_mouse)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and flag_of_start_use ** 2 == 1:
            mouse_pos = pygame.mouse.get_pos()
            lat2, lon2 = lat, lon
            lat1, lon1 = coordinates_of_mouse(mouse_pos, lon, lat)
            #print(lat1, lon1)
            flag_of_org = 1
            #print(find_first_organisation(lon1, lat1))
            try:
                organiz_address, coorrdd, name_of_org = find_first_organisation(lon1, lat1)
                print("!!!", organiz_address)
            except:
                flag_of_org = 0
                lan1, lon1 = lat2, lon2
                print("К заданной точке не нашлось ближайших организаций.")
            else:
            #print(organiz_address, coorrdd)
            #print(organiz_address)

                if flag_of_index == 1 or flag_flag == 1:
                    addess += ", " + indexx
                    #elif flag_flag == -1:

                #print(address_mouse)
                print("По адресу {0} расположена организация {1}".format(organiz_address, name_of_org))
                text_out = TextBox((325, 0, 320, 50), organiz_address)



        #print(pygame.mouse.get_pressed())
        text_in.get_event(event)
        try:
            text_out.get_event(event)
        except:
            pass
        b1.get_event(event)
        b2.get_event(event)


        if map_file == None and flag_of_start_use == 1:
            print("Ошибка")
            sys.exit()

    #print(flag_of_start_use)
    text_in.render(screen)
    try:
        text_out.render(screen)
    except:
        pass

    b1.render(screen)
    b2.render(screen)

    text_in.update()
    try:
        text_out.update()
    except:
        pass

    if  flag_of_start_use ** 2 == 1:
        if flag_of_mouse == 1 or flag_of_org == 1:
            map_params = {
                "ll": lat + "," + lon,
                "size": "{0},{1}".format(str(screen_height), str(screen_width)),
                "l": type_of_map,
                "spn": list_of_spn[index],
                "pt": str(lat1) + "," + str(lon1)
            }
            get_image(map_params)
        elif flag_of_search == 1:
            map_params = {
                "ll": lat + "," + lon,
                "size": "{0},{1}".format(str(screen_height), str(screen_width)),
                "l": type_of_map,
                "spn": list_of_spn[index],
                "pt": lat + "," + lon
            }
            get_image(map_params)
        else:
            map_params = {
                "ll": lat + "," + lon,
                "size": "{0},{1}".format(str(screen_height), str(screen_width)),
                "l": type_of_map,
                "spn": list_of_spn[index]
            }
            get_image(map_params)

        if flag_of_start_use == -1:
            flag_of_start_use = 1



    pygame.display.flip()
    if flag_of_start_use ** 2 == 1:
        screen.blit(pygame.image.load(map_file), (0, 0))
