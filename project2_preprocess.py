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
from pattern.text.en import singularize,pluralize
from nltk.corpus import stopwords
import string
import pattern.en


class Scraper:

    def __init__(self, qpage, mod):
        self.ingredients = []
        self.directions = []
        if 'http' in qpage:
            # if input page is a web page
            self.page = requests.get(qpage).text
            self.soup = BeautifulSoup(self.page, mod)
        else:
            # if input is a file
            self.page = qpage

    # Scrape recipe title
    def scrape_title(self):
        title = ''
        fullHTML = self.soup.find('title')
        title = fullHTML.text if fullHTML else 'None'
        return title



    # Scrape all ingredients
    def scrape_ingredients(self):
        ingredients = []
        fullHTML = self.soup.find_all('span', {"itemprop": 'ingredients', "data-id": lambda x: x != '0'})
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
        units = ['can', 'link', 'pinch', 'drop','sprig','package','bottle','piece','jar','dessertspoon','smidgen','dash',
                 'saltspoon','scruple','coffeespoon','fluid dram','wineglass','teacup','pottle','c','g','kg','l','ml',
                 'oz','pt','tsp','tbl','tb','tbsp','lb','gal','qt','pn','dr','ds','ssp','csp','dsp']
        fullHTML = self.soup.find_all('td')
        fullHTML = [u.find('strong') for u in fullHTML if u.find('strong')]
        for x in range(0, len(fullHTML)):
            units.append(fullHTML[x].text.strip().encode('utf-8').lower())

        return units

    # Scrape primary cooking methods
    def scrape_primarycookingmethods(self):
        pcookingmethods = []

        fullHTML = self.soup.find_all('picture', {"class": 'img-responsive'})
        for x in range(0, len(fullHTML)):
            pcookingmethods.append(fullHTML[x]['title'].encode('utf-8').lower())

        return pcookingmethods

    # Scrape general cooking methods
    def scrape_cookingmethods(self):
        cookingmethods = ['shake', 'crush', 'squeeze', 'cut']

        fullHTML = self.soup.find_all('td', {'valign': 'TOP'})
        fullHTML = [u.find_all('b') for u in fullHTML if u.find_all('b')]
        fullHTML = [item for sublist in fullHTML for item in sublist]

        for x in range(0, len(fullHTML)):
            cookingmethods.append(fullHTML[x].text.strip().split(':')[0].encode('utf-8').lower())

        return cookingmethods

    # Scrape tools
    def scrape_tools(self):
        tools = []
        with open(self.page) as fp:
            line = fp.readline()
            while line:
                tools.append(singularize(line.strip().lower()))
                line = fp.readline()
        return tools

    # Scrape meats
    def scrape_meats(self):
        meats = []
        article = self.soup.find_all('article', {"class": "tag-animal-protein-list"})
        fullHTML = []
        for art in article:
            fullHTML = art.find_all("li")
        for x in range(0, len(fullHTML)):
            meats.append(fullHTML[x].text.strip().encode('utf-8').lower())
        self.meats = meats
        meats = [singularize(m.strip()) for m in meats]
        return meats


    # Scrape seafood
    def scrape_seafood(self):
        seafood = []
        fullHTML = self.soup.find_all('li')
        for x in range(11, 98):
            seafood.append(singularize(re.sub('\(.*?\)','',fullHTML[x].text.strip().encode('utf-8').lower()).strip()))

        return seafood

    # Scrape vegetables
    def scrape_vegtables(self):
        vegetables = []
        article = self.soup.find_all('div', {"class": "mw-parser-output"})
        fullHTML = []
        for art in article:
            fullHTML = art.find_all("li")
        for x in range(0, len(fullHTML)):
            txt = fullHTML[x].text.strip().encode('utf-8').lower()
            if "legumes" not in txt and \
                    "beans" not in txt and \
                    "bean" not in txt and \
                    "peppers" not in txt and \
                    "herbs and spices" not in txt:
                finalsplitstr = txt.replace('\\', '(').replace(':', '(').replace('[', '(').split("(")
                if "\n" not in finalsplitstr[0]:
                    vegetables.append(finalsplitstr[0])
        vegetables.pop()
        vegetables.pop()
        strtRemove = False
        adjuster = 0
        for v in range(0, len(vegetables)):
            if vegetables[v + adjuster] == "anise" or vegetables[v + adjuster] == "chives" or vegetables[
                v + adjuster] == "paprika":
                strtRemove = True
            if vegetables[v + adjuster] == "arugula" or vegetables[v + adjuster] == "bell pepper" or vegetables[
                v + adjuster] == "tabasco pepper":
                strtRemove = False
            if strtRemove:
                vegetables.pop(v + adjuster)
                adjuster -= 1
        self.vegetables = vegetables

        vegetables = [singularize(v.strip()) for v in vegetables]
        return vegetables


#Class of ingredients
#Attributes: transformed_method, name, quantity, measurement, descriptor and preparation.
class Ingredients:
    def __init__(self, oneIngred, units,*kargs):

        if kargs:
            self.transformed_method = kargs[0]
        else:
            self.transformed_method = ''

        # special adj that shouldn't appear with a name
        spe_jj = ['prepared', 'fresh', 'freshly', 'plain', 'large', 'thick', 'ground','taste','small','frozen']

        # extract parentheses and elements in it
        # for example: "1 (6 ounce) can": (6 ounce) will be extracted
        words_parenth = re.search(r'\([\d*\/\d+|\d+|.| ]+[\w| ]+\)', oneIngred)
        words_parenth = words_parenth.group() if words_parenth else ''

        # remove parentheses in original string
        oneIngred = oneIngred.replace(words_parenth, '')

        # determine quantity
        # find the first number in a string, and convert str to float
        quantity_str = re.search('[\d*\/\d+|\d+| ]+|$', oneIngred).group()
        self.quantity = float("{0:.2f}".format(float(sum(Fraction(d) for d in quantity_str.split())))) \
            if quantity_str and not quantity_str is ' ' else 'none'


        # determine measurement, and update quantity if necessary
        if words_parenth:
            # if a formal measurement is used, do conversion
            # for example: "2 (6 ounce) cans" will convert to 12(quantity) ounce(measurement)
            measmt_parenth = re.search('[a-z ]+', words_parenth)
            self.measurement = singularize(measmt_parenth.group().strip()) \
                if measmt_parenth and singularize(measmt_parenth.group().strip()) in units else 'none'

            quantity_parenth = re.search('[\d*\/\d+|\d+|\d.]+', words_parenth)
            quantity_f = float("{0:.2f}".format(float(sum(Fraction(d) for d in quantity_parenth.group().split())))) \
                if quantity_parenth and not quantity_parenth is ' ' else 'none'
            self.quantity = self.quantity * quantity_f if quantity_f != 'none' else self.quantity


            next_word = oneIngred[oneIngred.find(quantity_str) + len(quantity_str):].split()[0]
            oneIngred = oneIngred.replace(next_word, '') if singularize(next_word) in units else oneIngred

            # if the unit is not the word after quantity, check if next two words is a possible unti in parentheses
            if self.measurement == 'none' and self.quantity != 'none':
                # Singularize next two words, and check if they are in units list
                word_in_paren = measmt_parenth.group().strip().split() if measmt_parenth else ['none']

                if len(word_in_paren) >= 2:
                    next_two_words_paren = word_in_paren[0] + ' ' + word_in_paren[1]
                    singularized_paren = singularize(word_in_paren[0] + ' ' + word_in_paren[1])

                    tempunit = [u for u in units if singularized_paren == u]
                    tempunit.sort(key=lambda ele: len(ele))
                    if len(tempunit) >= 1:
                        self.measurement = tempunit[len(tempunit) - 1]
                        oneIngred = oneIngred.replace(next_two_words_paren, '')
                if len(word_in_paren) >= 1 and self.measurement == 'none':
                    next_one_words_paren = word_in_paren[0]
                    singularized_paren = singularize(word_in_paren[0])

                    tempunit = [u for u in units if singularized_paren == u]
                    tempunit.sort(key=lambda ele: len(ele))
                    if len(tempunit) >= 1:
                        self.measurement = tempunit[len(tempunit) - 1]
                        oneIngred = oneIngred.replace(next_one_words_paren, '')

        else:
            # normal case: determine a measurement
            # for example: "6 ounce" will store "ounce" as measurement
            measmt = oneIngred[oneIngred.find(quantity_str) + len(quantity_str):].split()[0] \
                if quantity_str else 'none'.encode('utf-8')
            singularize_measmt = singularize(measmt)
            self.measurement = singularize_measmt if singularize_measmt in units else 'none'
            oneIngred = oneIngred.replace(measmt, '') if not self.measurement is 'none' else oneIngred

        # update ingredient string by removing quantity and measurement
        oneIngred = oneIngred.replace(quantity_str, '').strip() if not quantity_str is ' ' else oneIngred.strip()

        #if the unit is not the word after quantity, check if next two words is a possible unti in ingredient sentence
        if self.measurement == 'none' and self.quantity != 'none':
            #Singularize next two words, and check if they are in units list
            word_in_ing = oneIngred.split()
            if len(word_in_ing)>=2:
                next_two_words = word_in_ing[0]+ ' ' + word_in_ing[1]
                singularized_ing = singularize(word_in_ing[0]+ ' ' + word_in_ing[1])

                tempunit = [u for u in units if singularized_ing == u]
                tempunit.sort(key = lambda ele: len(ele))
                if len(tempunit) >= 1:
                    self.measurement = tempunit[len(tempunit)-1]
                    oneIngred = oneIngred.replace(next_two_words,'')


        # tokenization
        tokens = TweetTokenizer().tokenize(oneIngred)
        token_tag_org = nltk.pos_tag(tokens)
        token_tag = []

        # Correct common mistakes of pos tagger
        for tt in token_tag_org:
            templist = list(tt)
            if templist[0] == 'chopped':
                templist[1] = 'VBD'
            elif templist[0] == 'plain' or 'less' in templist[0] or 'ground' in templist[0] or (
                    '-' in templist[0] and len(templist[0]) > 1) or 'fresh' in templist[0]:
                templist[1] = 'JJ'
            token_tag.append(tuple(templist))

        # determine descriptor
        desp = [word for word, pos in token_tag \
                if (pos == 'JJ')]
        self.descriptor = ', '.join(map(str, desp)) if desp else 'none'

        # determine preparation
        prep = [word for word, pos in token_tag \
                if (pos == 'VBD' or pos == 'VBN' or pos == 'RB')]
        self.preparation = ' '.join(map(str, prep)) if prep else 'none'

        # determine name
        name = ''
        sent = pattern.en.parsetree(oneIngred.split(',')[0])
        for sentence in sent:
            for chunk in sentence.chunks:
                if chunk.type == 'NP':
                    namelist = [(w.string).encode('utf-8') for w in chunk.words if not w.type is 'CD'
                                and not w.string in spe_jj and not w.string in self.preparation and not '-' in w.string]
                    name = name + ' '.join(namelist) + ' '
        self.name = singularize(name.strip())

        if self.name is '':
            names = [word for word, pos in token_tag \
                     if (pos.startswith('NN')) and not word.encode('utf-8') in units]
            self.name = singularize(' '.join(map(str, names)) if names else 'none')


# Class of directions
# Attributes: primaryMethods, othermethods, tools, cookingtime
class Directions:
    def __init__(self, oneDir, cooking_methods, othercookingmethods, tools):

        # tokenization and remove stop words
        tokens = TweetTokenizer().tokenize(oneDir)
        stop = stopwords.words('english') + list(string.punctuation)
        tokens = [word.encode('utf-8') for word in tokens if not word in stop and len(word) > 2]

        # check if any primary cooking methods in this direction
        # Lemmatization is used
        self.primaryMethods = [pattern.en.lemma(word) for word in tokens if
                               pattern.en.lemma(word).encode('utf-8') in cooking_methods]
        if len(self.primaryMethods) < 1:
            self.primaryMethods = ['none']

        # check if any other cooking methods in this direction
        # Lemmatization is used
        self.otherMethods = [pattern.en.lemma(word) for word in tokens
                             if pattern.en.lemma(word) in othercookingmethods and not pattern.en.lemma(word).encode(
                'utf-8') in cooking_methods]
        if len(self.otherMethods) < 1:
            self.otherMethods = ['none']

        # check if any tool is used in this direction
        self.tools = [t for t in tools if oneDir.find(t) > 0]
        if len(self.tools) < 1:
            self.tools = ['none']

        # extract cooking times from a direction
        cookingtime = re.findall(
            r'[\d*\/\d+|\d+|\d.]+\s*\b(?:hours?\b|hrs?\b|h\b|seconds?\b|s\b|minutes?\b|min\b)*(?: to )*\b[\d*\/\d+|\d+|\d.]*\s*(?:hours?\b|hrs?\b|h\b|seconds?\b|s\b|minutes?\b|min\b)',
            oneDir)
        self.cookingtime = cookingtime if cookingtime else ['none']
        self.cookingtime = [c.strip() for c in self.cookingtime]


# Class of altCook
# Attributes: type(meat or vegetables), pm(primary cooking methods), alts(alternative cooking methods)
class AltCook:
    def __init__(self, type, pm, alts):
        self.type = type
        self.pm = pm
        self.alts = alts

    # Return alternative cooking methods
    def getAlts(self, type, pm):
        if (type == self.type and (pm == self.pm or pm == "any")):
            return self.alts
        else:
            return -1
