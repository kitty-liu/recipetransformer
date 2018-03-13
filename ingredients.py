import project2_preprocess as prep
import time


mod = 'html.parser'

unit_page = 'https://www.adducation.info/how-to-improve-your-knowledge/units-of-measurement/'
unit_sp = prep.Scraper(unit_page, mod)
units = unit_sp.scrape_unit()



# Meat Replacements



# Chinese Spices
ginger = prep.Ingredients('1 tablespoon minced ginger', units)
star_anise = prep.Ingredients('2 star anise', units)
five_spice = prep.Ingredients('1 teaspoon fivespice', units)
cilantro = prep.Ingredients('1/2 cup chopped cilantro', units)
peppercorn = prep.Ingredients('2 teaspoon peppercorns', units)
chinesecinnamon = prep.Ingredients('1 teaspoon ground chinese cinnamon', units)
corianderseed = prep.Ingredients('1 tablespoon coriander seeds', units)
fennelseed = prep.Ingredients('1 tablespoon fennel seeds', units)
cloves = prep.Ingredients('3 cloves', units)
chilipowder = prep.Ingredients('1/2 tablespoon chili powder', units)


# Chinese Sauces
sesameoil = prep.Ingredients('1 tablespoon sesame oil', units)
ricevinegar = prep.Ingredients('2 tablespoon rice vinegar', units)
soysauce = prep.Ingredients('2 tablespoon soy sauce', units)
chilipaste = prep.Ingredients('1 tablespoon chili paste', units)
fishsauce = prep.Ingredients('1 tablespoon fish sauce', units)
oystersauce = prep.Ingredients('1 tablespoon oyster sauce', units)

# Chinese Vegetables
bokchoy = prep.Ingredients('2 bok choy', units)
chinesecabbage = prep.Ingredients('1 cup chopped chinese cabbage', units)
beanspouts = prep.Ingredients('1 cup bean sprouts', units)
whiteradish = prep.Ingredients('1 cup chopped white radish', units)
bambooshoots = prep.Ingredients('1/2 cup bamboo shoots', units)
chives = prep.Ingredients('1 cup chopped chives', units)
greenonion = prep.Ingredients('1/2 cup chopped green onion', units)