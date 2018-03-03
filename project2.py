###############################################################

## EECS337
## Group 3: Emily Blackman, Noah Karpinski, Kitty Liu, Yani Xie

###############################################################

import project2_preprocess as prep
import time



# right now replacing with tofu but will add other types
def toVegetarian(ingredientList, meatList):
    vegList = []
    for ingredient in ingredientList:
        for meat in meatList:
            if meat in ingredient.name:
                ingredient.name = "tofu"
                ingredient.descriptor = "none"
        vegList.append(ingredient)
    return vegList

def toVegan(ingredientList, meatList, veganSubs):
    veganList = []
    for ingredient in ingredientList:
        for meat in meatList:
            if meat in ingredient.name:
                ingredient.name = "tofu"
                ingredient.descriptor = "none"
        for nonVeg in veganSubs.keys():
            if nonVeg in ingredient.name:
                ingredient.name = veganSubs[nonVeg]
        veganList.append(ingredient)
    return veganList

def toItalian():
    print "italian"

#Main function
def main():
    start_time = time.time()
    transformation = str(raw_input("What type of transformation do you want to do to the recipe? Your options are vegetarian, vegan, healthy, easy: "))
    mod = 'html.parser'

    #scrape units
    unit_page = 'https://www.adducation.info/how-to-improve-your-knowledge/units-of-measurement/'
    unit_sp = prep.Scraper(unit_page, mod)
    units = unit_sp.scrape_unit()

    #scrape primary cooking methods:
    primarycookingmethods_page = 'https://www.thedailymeal.com/cook/15-basic-cooking-methods-you-need-know-slideshow/slide-12'
    primarycookingmethods_sp = prep.Scraper(primarycookingmethods_page,mod)
    primarycookingmethods = primarycookingmethods_sp.scrape_primarycookingmethods()
    print 'Primary cooking methods: ',primarycookingmethods

    meat_page = "http://naturalhealthtechniques.com/list-of-meats-and-poultry/"
    meatlist_sp = prep.Scraper(meat_page, mod)
    meatList = meatlist_sp.scrape_meats()
    meatList.extend(("pepperoni", "salami", "proscuitto", "sausage", "ham"))

    veganSubs = {"milk": "almond milk", "yogurt": "coconut yogurt", "eggs": "tofu", "butter": "soy margarine",
                 "honey": "agave syrup", "cheese": "nutritional yeast"}

    #test pages:
    #qpage = 'https://www.allrecipes.com/recipe/262723/homemade-chocolate-eclairs/?internalSource=staff%20pick&referringContentType=home%20page&clickId=cardslot%209'
    #qpage = 'https://www.allrecipes.com/recipe/228796/slow-cooker-barbequed-beef-ribs/?internalSource=popular&referringContentType=home%20page&clickId=cardslot%205'
    #qpage = 'http://allrecipes.com/recipe/244195/italian-portuguese-meat-loaf-fusion/?internalSource=rotd&referringContentType=home%20page&clickId=cardslot%201'

    #test bone-in chicken thighs
    #qpage = 'https://www.allrecipes.com/recipe/259101/crispy-panko-chicken-thighs/?internalSource=previously%20viewed&referringContentType=home%20page&clickId=cardslot%203'

    #test quatity&measurement conversion:
    qpage = 'https://www.allrecipes.com/recipe/217228/blood-and-sand-cocktail/?internalSource=rotd&referringId=80&referringContentType=recipe%20hub'

    #scrape recipe
    recp = prep.Scraper(qpage, mod)
    ingredients = recp.scrape_ingredients()
    print 'All ingredients:'
    print ingredients

    directions = recp.scrape_directions()
    print 'All directions:'
    print directions


    prepIngredients = []

    # Parse ingredients
    for igd in ingredients:
        prepIngredients.append(prep.Ingredients(igd, units))


    # Transform Ingredient List based on input
    if transformation == "vegetarian":
        toVegetarian(prepIngredients, meatList)
    elif transformation == "vegan":
        toVegan(prepIngredients, meatList, veganSubs)


    # Prepped ingredients
    for ingredient in prepIngredients:
        print '\n'
        print 'name: ' + ingredient.name
        print 'quantity: ' + str(ingredient.quantity)
        print 'measurement: ' + ingredient.measurement
        print 'descriptor: ' + ingredient.descriptor
        print 'preparation: ' + ingredient.preparation

    # Parse directions
    primary_cookingmethods = []
    for dir in directions:
        direction = prep.Directions(dir,primarycookingmethods)
        if direction.primaryMethods:
            primary_cookingmethods.append(direction.primaryMethods)

    #flatten a list
    primary_cookingmethods = [item for sublist in primary_cookingmethods for item in sublist]
    print '\nPrimary cooking methods:', ', '.join(set(primary_cookingmethods))

    end_time = time.time()
    print(end_time - start_time)


if __name__ == "__main__":
    main()