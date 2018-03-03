###############################################################

## EECS337
## Group 3: Emily Blackman, Noah Karpinski, Kitty Liu, Yani Xie

###############################################################

import requests
from bs4 import BeautifulSoup
import re
from fractions import Fraction
import nltk
from nltk.tokenize import TweetTokenizer
from pattern.text.en import singularize
from nltk.corpus import stopwords
import string
import pattern.en

class Scraper:

    def __init__(self,qpage, mod):
        self.ingredients = []
        self.directions = []
        self.page = requests.get(qpage).text
        self.soup = BeautifulSoup(self.page,mod)


    # Scrape all ingredients
    def scrape_ingredients(self):
        ingredients = []
        fullHTML =self.soup.find_all('span', {"itemprop": 'ingredients',"data-id" : lambda x: x != '0'})
        for x in range(0, len(fullHTML)):
            ingredients.append(fullHTML[x].text.strip().encode('utf-8').lower())
        self.ingredients = ingredients
        return ingredients


    # Scrape all directions
    def scrape_directions(self):
        directions = []
        fullHTML = self.soup.find_all(class_="step")
        for x in range(0, len(fullHTML)):
            directions.append(fullHTML[x].text.strip().encode('utf-8').lower())

            directions = filter(None, directions)
        self.directions = directions
        return directions

    # Scrape units
    def scrape_unit(self):
        units = ['can','link','pinch','drop']
        fullHTML = self.soup.find_all('td')
        fullHTML = [u.find('strong') for u in fullHTML if u.find('strong')]
        for x in range(0, len(fullHTML)):
            units.append(fullHTML[x].text.strip().encode('utf-8').lower())

        return units

    # Scrape primary cooking methods
    def scrape_primarycookingmethods(self):
        cookingmethods = ['stir']

        fullHTML = self.soup.find_all('picture',{"class": 'img-responsive'})
        for x in range(0, len(fullHTML)):
            cookingmethods.append(fullHTML[x]['title'].encode('utf-8').lower())

        return cookingmethods

    def scrape_meats(self):
        meats = []
        article = self.soup.find_all('article', {"class": "tag-animal-protein-list"})
        fullHTML = []
        for art in article:
            fullHTML = art.find_all("li")
        for x in range(0, len(fullHTML)):
            meats.append(fullHTML[x].text.strip().encode('utf-8').lower())
        self.meats = meats
        return meats


class Ingredients:
    def __init__(self,oneIngred,units):
        #special adj that shouldn't appear with a name
        spe_jj = ['prepared']


        #extract parentheses and elements in it
        # for example: "1 (6 ounce) can": (6 ounce) will be extracted
        words_parenth = re.search(r'\(\d.*\w\)',oneIngred)
        words_parenth = words_parenth.group() if words_parenth else ''

        #remove parentheses in original string
        oneIngred = re.sub(r'\(.*\)', '',oneIngred)

        # determine quantity
        # find the first number in a string, and convert str to float
        quantity_str = re.search('[\d*\/\d+|\d+| ]+|$', oneIngred).group()
        self.quantity = float(sum(Fraction(d) for d in quantity_str.split())) \
            if quantity_str and not quantity_str is ' ' else 'none'

        # determine measurement, and update quantity if necessary
        if words_parenth:
            # if a formal measurement is used, do conversion
            # for example: "2 (6 ounce) cans" will convert to 12(quantity) ounce(measurement)
            measmt_parenth = re.search('[a-z]+',words_parenth)
            self.measurement = singularize(measmt_parenth.group()) \
                if measmt_parenth and singularize(measmt_parenth.group()) in units else 'none'
            quantity_parenth = re.search('[\d*\/\d+|\d+|\d.]+', words_parenth)
            self.quantity = self.quantity*float(quantity_parenth.group()) if quantity_parenth else self.quantity
            oneIngred = oneIngred.replace(oneIngred[oneIngred.find(quantity_str) + len(quantity_str):].split()[0],'')
        else:
            # normal case: determine a measurement
            # for example: "6 ounce" will store "ounce" as measurement
            measmt = oneIngred[oneIngred.find(quantity_str) + len(quantity_str):].split()[0] \
            if quantity_str else 'none'.encode('utf-8')
            singularize_measmt = singularize(measmt)
            self.measurement = singularize_measmt if singularize_measmt in units else 'none'
            oneIngred = oneIngred.replace(measmt,'') if not self.measurement is 'none' else oneIngred

        #update ingredient string by removing quantity and measurement
        oneIngred = oneIngred.replace(quantity_str,'') if not quantity_str is ' ' else oneIngred

        # determine name
        name = ''
        sent = pattern.en.parsetree(oneIngred.split(',')[0])
        for sentence in sent:
            for chunk in sentence.chunks:
                if chunk.type == 'NP':
                    namelist = [(w.string).encode('utf-8') for w in chunk.words if not w.type is 'CD' and not w.string in spe_jj ]
                    name = name + ' '.join(namelist) + ' '
        self.name = name.rstrip()

        # tokenization
        tokens = TweetTokenizer().tokenize(oneIngred)
        token_tag = nltk.pos_tag(tokens)

        #determine descriptor
        # tag lookup: https://pythonprogramming.net/natural-language-toolkit-nltk-part-speech-tagging/
        desp = [word for word, pos in token_tag \
                 if (pos == 'JJ')]
        self.descriptor = ' '.join(map(str, desp)) if desp else 'none'

        # determine preparation
        prep = [word for word, pos in token_tag \
                 if (pos == 'VBD' or pos == 'VBN' or pos == 'RB')]
        self.preparation = ' '.join(map(str, prep)) if prep else 'none'


class Directions:
    def __init__(self,oneDir,cooking_methods):

        # tokenization and remove stop words
        tokens = TweetTokenizer().tokenize(oneDir)
        stop = stopwords.words('english') + list(string.punctuation)
        tokens = [word.encode('utf-8') for word in tokens if not word in stop and len(word) > 2]

        # check if any primary cooking methods in this direction
        self.primaryMethods = [pattern.en.lemma(word) for word in tokens if pattern.en.lemma(word) in cooking_methods]


