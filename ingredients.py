import project2_preprocess as prep
import time


mod = 'html.parser'

unit_page = 'https://www.adducation.info/how-to-improve-your-knowledge/units-of-measurement/'
unit_sp = prep.Scraper(unit_page, mod)
units = unit_sp.scrape_unit()


# Meat Replacements
tofu = prep.Ingredients('1 cup sliced tofu', units, 'seared')
tempeh = prep.Ingredients('1/2 cup sliced temeph', units, 'steamed')
texturedvegprote = prep.Ingredients('1/2 cup textured vegetable protein', units, 'boil')
jackfruit = prep.Ingredients('1 cup jackfruit', units, 'boil')
mushrooms = prep.Ingredients('1 cup chopped mushrooms', units, 'sautee')
lentils = prep.Ingredients('3/4 cup lentils', units, 'boil')

# Vegan Replacements
almondmilk = prep.Ingredients('1/2 cup almond milk', units)
coconutyogurt = prep.Ingredients('1/2 cup coconut yogurt', units)
soymarg = prep.Ingredients("2 tablespoon soy margarine", units)
agave = prep.Ingredients("1 tablespoon agave syrup", units)
nutyeast = prep.Ingredients("1/4 cup nutritional yeast", units)
agar = prep.Ingredients("3 tablespoons agar", units)
silktofu = prep.Ingredients('1 cup chopped silken tofu pieces', units)

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

# Italian Spices
oregano = prep.Ingredients('1 teaspoon dried oregano', units)
thyme = prep.Ingredients('1 teaspoon dried thyme', units)
rosemary = prep.Ingredients('1 teaspoon rosemary', units)
sage = prep.Ingredients('1 teaspoon dried sage', units)
basil = prep.Ingredients('1 teaspoon chopped basil', units)
marjoram = prep.Ingredients('1 teaspoon dried marjoram', units)

# Italian Sauces
tomatosauce = prep.Ingredients('3 tablespoons tomato sauce', units)
alfredosauce = prep.Ingredients('2 tablespoons alfredo sauce', units)
pestosauce = prep.Ingredients('2 tablespoons pesto sauce', units)
balsamicvinegar = prep.Ingredients('2 tablespoons balsamic vinegar', units)

#Healthy replacements
turkeybacon = prep.Ingredients('1 piece turkey bacon', units)
wholegrainbread = prep.Ingredients('2 slices of bread', units)
rolledoats = prep.Ingredients('1 cup rolled oats', units)
fatfreebutterspread = prep.Ingredients('3 tablespoon fat-free butter spread', units)
cookingspray = prep.Ingredients('1 tablespoon', units)
halfandhalf = prep.Ingredients('3 tablespoon fat-free half and half', units)
fatfreecreamcheese = prep.Ingredients('1 cup fat-free cream cheese', units)
eggwhites = prep.Ingredients('3 egg whites', units)
wholewheatflour = prep.Ingredients('3 cups whole-wheat flour', units)
leanbeef = prep.Ingredients('1 pound lean ground beef', units)
arugula = prep.Ingredients('2 cups arugula', units)
reducedfatmayo = prep.Ingredients('1 cup reduced-fat mayonnaise', units)
evaporatedskim = prep.Ingredients('6 ounces evaporated skim milk', units)
fatfreemilk = prep.Ingredients('1 cup fat-free milk', units)
brownrice = prep.Ingredients('1 cup brown rice', units)
fatfreedressing = prep.Ingredients('1/2 cup dressing', units)
fatfreesourcream = prep.Ingredients('1 cup fat-free sour cream', units)

