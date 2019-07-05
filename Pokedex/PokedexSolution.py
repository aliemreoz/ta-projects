__author__ = "aliemre"

import pickle
import time
from Tkinter import *
import ttk
from PIL import ImageTk, Image
from bs4 import BeautifulSoup
import urllib
import urllib2

class Pokemon():

    def __init__(self, name, idd, typee, img_link, height, weight, category, ability, weakness):

        """
        init method for Pokemon Class
        :param name:
        :param idd:
        :param typee:
        :param img_link:
        :param height:
        :param weight:
        :param category:
        :param ability:
        :param weakness:
        """

        self.name = name
        self.id = idd
        self.type = typee
        self.img_link = img_link
        self.height = height
        self.weight = weight
        self.category = category
        self.ability = ability
        self.weakness = weakness

    def make_dict(self):

        """
        create dictionary for Pokemon Object.
        :return: pokemon dict with attributes
        """

        self.pokemon_temp_dict = {}
        str_poketype = [x.encode("utf-8") for x in self.type]
        str_weakness = [x.encode("utf-8") for x in self.weakness]
        self.pokemon_temp_dict["number"] = self.id
        self.pokemon_temp_dict["image_link"] = self.img_link
        self.pokemon_temp_dict["type"] = str_poketype
        self.pokemon_temp_dict["height"] = self.height
        self.pokemon_temp_dict["weight"] = self.weight
        self.pokemon_temp_dict["category"] = self.category
        self.pokemon_temp_dict["abilities"] = self.ability
        self.pokemon_temp_dict["weakness"] = str_weakness

        return self.pokemon_temp_dict

    def get_name(self):

        """
        get Pokemon Object's name
        :return:
        """

        return self.name



class GUI(Frame):


    def __init__(self, parent):
        """
        init method for GUI class.
        :param parent:
        """
        Frame.__init__(self, parent)
        self.parent = parent

        self.scale = 10
        self.color_dict = {'Steel': 'snow2',
                           'Ghost': 'honeydew2',
                           'Electric': 'yellow',
                           'Ice': 'aquamarine2',
                           'Normal': 'lavender',
                           'Fire': 'orange',
                           'Psychic': 'magenta2',
                           'Flying': 'turquoise',
                           'Poison': 'hot pink',
                           'Dragon': 'red2',
                           'Water': 'CadetBlue1',
                           'Fighting': 'papaya whip',
                           'Rock': 'dark khaki',
                           'Fairy': 'deep pink',
                           'Grass': 'OliveDrab1',
                           'Bug': 'green yellow',
                           'Ground': 'sandy brown'}

        self.type_list = ['Electric',
                          'Water',
                          'Psychic',
                          'Grass',
                          'Poison',
                          'Ground',
                          'Dragon',
                          'Normal',
                          'Flying',
                          'Fire',
                          'Rock',
                          'Steel',
                          'Fairy',
                          'Bug',
                          'Fighting',
                          'Ghost',
                          'Ice']


        self.pokemon_dict = {}
        self.pokemon_list = []

        self.init_ui()


    def init_ui(self):

        """
        GUI widgets for Pokedex
        :return: None
        """
        #################################################################################################

        self.frame_big_left = Frame(self, bg="#fb0505", height=10*self.scale, width=40*self.scale)

        self.frame_big_left.pack(side=LEFT,
                             fill=BOTH)

        self.frame_left_first = Frame(self.frame_big_left,
                                      bg="#fb0505",
                                      height=7*self.scale,
                                      width=40*self.scale,
                                      highlightbackground="black",
                                      highlightthickness=2)

        self.frame_left_first.pack(side=TOP,
                                 fill=BOTH)

        self.frame_left_second = Frame(self.frame_big_left,
                                       bg="#fb0505",
                                       height=12*self.scale,
                                       width=40*self.scale,
                                       highlightbackground="black",
                                       highlightthickness=2)

        self.frame_left_second.pack(side=TOP,
                                 fill=BOTH)

        self.frame_left_third = Frame(self.frame_big_left,
                                      bg="#fb0505",
                                      height=24*self.scale,
                                      width=40*self.scale,
                                      highlightbackground="black",
                                      highlightthickness=2)

        self.frame_left_third.pack(side=TOP,
                                   fill=BOTH,
                                   ipady=self.scale)

        self.frame_left_fourth = Frame(self.frame_big_left,
                                       bg="#fb0505",
                                       height=24 * self.scale,
                                       width=40 * self.scale,
                                       highlightbackground="black",
                                       highlightthickness=2)

        self.frame_left_fourth.pack(side=TOP,
                                    fill=BOTH)

        self.frame_big_right = Frame(self, bg="#fb0505", height=10*self.scale, width=60*self.scale,
                                       highlightbackground="black",
                                       highlightthickness=2)

        #################################################################################################

        self.app_label = Label(text="POKEDEX",
                               fg='white',
                               bg="#fb0505",
                               font='helvetica 25')

        self.app_label.pack(in_=self.frame_left_first,
                            fill=X)

        #################################################################################################

        self.fetch_pokemon_data = Button(text="Fetch Pokemon\nData",
                                         bg="yellow",
                                         font="Helvetica 8",
                                         fg="black")

        self.fetch_pokemon_data.configure(command=self.fetch)

        self.fetch_pokemon_data.pack(in_=self.frame_left_second,
                                     side=LEFT,
                                     pady=self.scale*2,
                                     padx=self.scale)


        self.progress_bar = Canvas(self,  width=200, height=20, relief='sunken')

        self.progress_bar.pack(in_=self.frame_left_second,
                               side=LEFT,
                               pady=self.scale * 2,
                               padx=self.scale)

        #################################################################################################

        self.searching_filtering_label = Label(width=int(self.scale*2.5),
                                               text="Searching&Filtering",
                                               bg="#fb0505",
                                               font="Helvetica 14")

        self.searching_filtering_label.grid(in_=self.frame_left_third,
                                           row=0,
                                           column=0,
                                           columnspan=2,
                                           padx=self.scale*4,
                                           sticky=W)


        self.search_entry = Entry(width=self.scale*3,
                                  font="Helvetica 12",
                                  justify=CENTER,
                                  borderwidth=3)

        self.search_entry.grid(in_=self.frame_left_third,
                               row=1,
                               column=0,
                               columnspan=2,
                               padx=self.scale*4,
                               pady=self.scale,
                               sticky=W)


        self.filter_label = Label(text="Filter by type",
                                  bg="#fb0505",
                                  font="Helvetica 12")

        self.filter_label.grid(in_=self.frame_left_third,
                               row=2,
                               column=0,
                               columnspan=2,
                               padx=self.scale,
                               sticky=W)


        self.filter_combobox = ttk.Combobox(width=self.scale*3)

        self.filter_combobox.grid(in_=self.frame_left_third,
                                 row=3,
                                 column=0,
                                 padx=self.scale,
                                 sticky=W)


        self.search_button = Button(text="SEARCH",
                                    bg="yellow",
                                    font="Helvetica 11",
                                    fg="black")

        self.search_button.configure(command=self.search)

        self.search_button.grid(in_=self.frame_left_third,
                                row=3,
                                column=1,
                                padx=self.scale,
                                sticky=W)

        #################################################################################################

        self.result_label = Label(width=self.scale*3,
                                  text="Total number of result",
                                  bg="#fb0505",
                                  font="Helvetica 14")

        self.result_label.grid(in_=self.frame_left_fourth,
                               row=0,
                               column=0,
                               columnspan=2,
                               padx=self.scale,
                               pady=self.scale,
                               sticky=W)


        self.result_listbox = Listbox(width=self.scale * 3)

        self.result_listbox.grid(in_=self.frame_left_fourth,
                                 row=1,
                                 column=0,
                                 padx=self.scale,
                                 pady=self.scale,
                                 sticky=W)


        self.get_button = Button(text="Get Pokemon\nData",
                                    bg="yellow",
                                    font="Helvetica 11",
                                    fg="black")

        self.get_button.configure(command=self.get_pokemon_data)

        self.get_button.grid(in_=self.frame_left_fourth,
                                row=1,
                                column=1,
                                padx=self.scale,
                                pady=self.scale)

        #################################################################################################

        self.pokemon_name_label = Label(width=self.scale*3,
                                        text="CHARMANDER",
                                        bg="#fb0505",
                                        font="Arial 25")

        self.pokemon_name_label.grid(in_=self.frame_big_right,
                                     row=0,
                                     column=0,
                                     pady=self.scale)


        self.pokemon_number_label = Label(width=self.scale * 3,
                                        text="#004",
                                        bg="#fb0505",
                                        font="Arial 15")

        self.pokemon_number_label.grid(in_=self.frame_big_right,
                                     row=1,
                                     column=0)


        self.type_label_data = Label(width=10,
                                     text="FIRE",
                                bg="orange",
                                fg="black",
                                font="Helvetica 12")

        self.type_label_data.grid(in_=self.frame_big_right,
                             row=3,
                             column=0)


        self.type_label_data2 = Label(width=10,
                                      text="FLYING",
                                      bg="cyan",
                                      fg="black",
                                      font="Helvetica 12")

        self.type_label_data2.grid(in_=self.frame_big_right,
                                   row=4,
                                   column=0)


        self.height_label = Label(text="Height  : ",
                                bg="#fb0505",
                                font="Helvetica 12")

        self.height_label.grid(in_=self.frame_big_right,
                             row=5,
                             column=0)


        self.weight_label = Label(text="Weight  : ",
                                  bg="#fb0505",
                                  font="Helvetica 12")

        self.weight_label.grid(in_=self.frame_big_right,
                               row=6,
                               column=0)


        self.category_label = Label(text="Category  : ",
                                  bg="#fb0505",
                                  font="Helvetica 12")

        self.category_label.grid(in_=self.frame_big_right,
                               row=7,
                               column=0)


        self.abilities_label = Label(text="Abilities  : ",
                                    bg="#fb0505",
                                    font="Helvetica 12")

        self.abilities_label.grid(in_=self.frame_big_right,
                                 row=8,
                                 column=0)


        self.weakness_label = Label(text="Weakness  : ",
                                     bg="#fb0505",
                                     font="Helvetica 12")

        self.weakness_label.grid(in_=self.frame_big_right,
                                  row=9,
                                  column=0)

        #################################################################################################

        self.pack()


    def get_pokemon_list(self):

        """
        Create list of pokemons from txt file.
        :return: List of Pokemons
        """

        file = open("all_pokemon.txt", "r")

        for line in file:
            self.pokemon_list.append(line.split()[0])

        return self.pokemon_list


    def fill_dict(self, pokemon):

        """
        Crawl given pokemon data with beautiful soup
        Create Pokemon object from crawled data
        Fill dictionary with Pokemons and their datas.
        :param pokemon:
        :return: None
        """

        base_link = "https://www.pokemon.com/us/pokedex/"
        link = base_link + pokemon

        response = urllib2.urlopen(link)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")

        name = pokemon.upper()
        number = (soup.find(class_="pokedex-pokemon-pagination-title").span.text).encode("utf-8")
        image_link = (soup.find(class_="profile-images").img["src"]).encode("utf-8")
        pokemon_type = soup.find(class_="dtm-type").text.split()[1:]
        height = (soup.find_all(class_="attribute-value")[0].text).encode("utf-8")
        weight = (soup.find_all(class_="attribute-value")[1].text).encode("utf-8")
        category = (soup.find_all(class_="attribute-value")[3].text).encode("utf-8")
        abilities = (soup.find_all(class_="attribute-value")[4].text).encode("utf-8")
        weakness = soup.find(class_="dtm-weaknesses").text.split()[1:]

        temp_pokemon_object = Pokemon(name,number,pokemon_type,image_link,height,weight,category,abilities,weakness)
        pokemon_name = temp_pokemon_object.get_name()
        temp_poke_dict = temp_pokemon_object.make_dict()
        self.pokemon_dict[pokemon_name] = temp_poke_dict


    def fetch(self):

        """
        Try:
            open database if exist.
            Handle with progress bar.
            Fill filter combobox.
        Except: there is no database.
            Call fill_dict for all pokemons.
            Create db for future use.
            Handle with progress bar.
            Fill filter combobox.
        :return: None
        """

        try:

            file = open("pokemons.db", "rb")
            self.pokemon_dict = pickle.load(file)

            self.progress_bar.create_rectangle(0, 0, 101*2, 25, fill="green")
            self.progress_bar.create_text(100,12,text="FINISHED",fill="black")

            self.type_list.insert(0,"All Types")
            self.type_list.sort()
            self.filter_combobox["values"]=self.type_list
            self.filter_combobox.current(0)

        except:

            index = 0.0

            self.pokemon_list = self.get_pokemon_list()

            for i in self.pokemon_list:
                index = index + 1.0
                count = (index * 100) / len(self.pokemon_list)
                self.progress_bar.create_rectangle(0, 0, int(count) * 2, 25, fill="green")
                self.update_idletasks()
                time.sleep(0.04)
                self.fill_dict(i)
            self.progress_bar.create_text(100, 12, text="FINISHED", fill="black")

            file_object = open("pokemons.db", "wb")
            pickle.dump(self.pokemon_dict, file_object)
            file_object.close()


            dosya = open("pokemons.db", "rb")
            self.pokemon_dict = pickle.load(dosya)

            self.type_list.insert(0,"All Types")
            self.type_list.sort()
            self.filter_combobox["values"]=self.type_list
            self.filter_combobox.current(0)


    def search(self):

        """
        Clean result listbox.
        Get query.
        Get filter type.
        First search, then filter.
        Fill result listbox.
        Manipulate result count label.
        :return: None
        """

        self.result_listbox.delete(0,END)

        self.query = self.search_entry.get()
        self.query=self.query.upper()

        self.search_result = []
        self.filtered_result = []

        if self.search_entry.get()=="":
            for i in self.pokemon_dict.keys():
                self.search_result.append(i)

        else:
            for i in self.pokemon_dict.keys():
                if i.find(self.query) != -1:
                    self.search_result.append(i)

        try:
            self.selected_type = self.filter_combobox.get()

            for i in self.search_result:
                if self.selected_type == "All Types":
                    self.filtered_result.append(i)

                else:
                    if self.selected_type in self.pokemon_dict[i]["type"]:
                        self.filtered_result.append(i)

        except:
            print "Please select type."

        self.filtered_result.sort()
        for i in self.filtered_result:
            self.result_listbox.insert(END,i)

        self.result_label.configure(text="Total : "+str(len(self.filtered_result))+" Result")


    def get_pokemon_data(self):

        """
        Manipulate labels for selected pokemon.
        :return: None
        """

        self.frame_big_right.pack(side=LEFT, fill=BOTH)

        selected_pokemon_index = self.result_listbox.curselection()
        selected_pokemon = self.result_listbox.get(selected_pokemon_index)

        self.pokemon_name_label.configure(text=selected_pokemon)


        image_url = self.pokemon_dict[selected_pokemon]["image_link"] #get image link
        self.image = urllib.urlretrieve(image_url, "temp_pokemon.png") #download image as temp_pokemon.png
        self.opened_image = Image.open("temp_pokemon.png") #open image with PIL
        self.width, self.height = self.opened_image.size #get width and height of image
        self.new_width = int(float(self.width) * 0.5) #recalculate width
        self.new_height = int(float(self.height) * 0.5) #recalculate height
        self.new_image = self.opened_image.resize((self.new_width, self.new_height)) #resize image
        self.project_image = ImageTk.PhotoImage(self.new_image) #open image in ImageTk
        self.maincanvas = Canvas(bg='#fb0505', width=self.new_width, height=self.new_height,
                                 highlightbackground='#fb0505') #create canvas
        self.maincanvas.create_image(0, 0, image=self.project_image, anchor='nw') #add image to canvas

        self.maincanvas.grid(in_=self.frame_big_right,
                             row=2,
                             column=0)

        self.pokemon_number_label.configure(text=self.pokemon_dict[selected_pokemon]["number"])

        type0 = self.pokemon_dict[selected_pokemon]["type"][0]
        self.type_label_data.configure(text=type0,bg=self.color_dict[type0])

        # check for is there any second type for selected pokemon
        try: #there is second type
            type1 = self.pokemon_dict[selected_pokemon]["type"][1]
            self.type_label_data2.configure(text=type1, bg=self.color_dict[type1])

        except: #there is not second type
            self.type_label_data2.configure(text="")
            self.type_label_data2.configure(bg='#fb0505')

        self.height_label.configure(text="Height  :  "+self.pokemon_dict[selected_pokemon]["height"])
        self.weight_label.configure(text="Weight  :  "+self.pokemon_dict[selected_pokemon]["weight"])
        self.category_label.configure(text="Category  :  "+self.pokemon_dict[selected_pokemon]["category"])
        self.abilities_label.configure(text="Abilities  :  "+self.pokemon_dict[selected_pokemon]["abilities"])
        self.weakness_as_str = ", ".join(self.pokemon_dict[selected_pokemon]["weakness"])
        self.weakness_label.configure(text="Weakness  :  "+self.weakness_as_str)


def main():
    root = Tk()
    root.title("POKEDEX")
    root.geometry()
    root.resizable(width=FALSE, height=FALSE)
    app = GUI(root)
    root.mainloop()

main()
