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

def toEasy(ingredientList, commonSpices):
    count = 0
    indexes = []
    for ingredient in ingredientList:
        common = False
        for spice in commonSpices:
            if spice in ingredient.name:
                common = True
        if not common and (ingredient.measurement == "teaspoon" or ingredient.measurement == "tablespoon"):
            indexes.append(count)
        count += 1
    adj = 0
    print indexes
    for index in indexes:
        ingredientList.pop(index + adj)
        adj -= 1
    return ingredientList

def toAltMethod(ingredientList, meatList, altMethods, pm, altList):
    for ingredient in ingredientList:
        for meat in meatList:
            if meat in ingredient.name:
                for alt in altMethods:
                    res = alt.getAlts("meat",pm)
                    if res != -1:
                        altList = res
                        break
    return altList

def toItalian():
    print "italian"


#Main function
def main():
    start_time = time.time()
    transformation = str(raw_input("What type of transformation do you want to do to the recipe?\n Your options are vegetarian, vegan, healthy, altmethod, easy: "))
    mod = 'html.parser'

    #scrape units
    unit_page = 'https://www.adducation.info/how-to-improve-your-knowledge/units-of-measurement/'
    unit_sp = prep.Scraper(unit_page, mod)
    units = unit_sp.scrape_unit()

    #scrape primary cooking methods:
    primarycookingmethods_page = 'https://www.thedailymeal.com/cook/15-basic-cooking-methods-you-need-know-slideshow/slide-12'
    primarycookingmethods_sp = prep.Scraper(primarycookingmethods_page,mod)
    primarycookingmethods = primarycookingmethods_sp.scrape_primarycookingmethods()


    #scrape other cooking methods:
    othercookingmethods_page = 'https://www.d.umn.edu/~alphanu/cookery/glossary_cooking.html'
    othercookingmethods_page_sp = prep.Scraper(othercookingmethods_page,mod)
    othercookingmethods = othercookingmethods_page_sp.scrape_cookingmethods()


    #scrape tools.txt
    tools_page = 'tools.txt'
    tools_sp = prep.Scraper(tools_page, '')
    tools = tools_sp.scrape_tools()


    #scrape meat
    meat_page = "http://naturalhealthtechniques.com/list-of-meats-and-poultry/"
    meatlist_sp = prep.Scraper(meat_page, mod)
    meatList = meatlist_sp.scrape_meats()
    meatList.extend(("pepperoni", "salami", "proscuitto", "sausage", "ham"))

    veganSubs = {"milk": "almond milk", "yogurt": "coconut yogurt", "eggs": "tofu", "butter": "soy margarine",
                 "honey": "agave syrup", "cheese": "nutritional yeast"}

    #Easy change
    commonSpices = ["salt", "pepper", "garlic"]

    #Alt Methods
    altList = []
    pf = "pan fry"
    bake = "bake"
    mw = "microwave"
    df = "deepfry"
    altMethods = []
    altMethods.append(prep.AltCook("meat",bake,[pf, mw]))
    altMethods.append(prep.AltCook("meat", pf, [df, bake, mw]))
    altMethods.append(prep.AltCook("meat", mw, [pf, bake]))
    altMethods.append(prep.AltCook("meat", df, [pf, bake]))
    #test pages:
    #qpage = 'https://www.allrecipes.com/recipe/262723/homemade-chocolate-eclairs/?internalSource=staff%20pick&referringContentType=home%20page&clickId=cardslot%209'
    #qpage = 'https://www.allrecipes.com/recipe/228796/slow-cooker-barbequed-beef-ribs/?internalSource=popular&referringContentType=home%20page&clickId=cardslot%205'
    #qpage = 'http://allrecipes.com/recipe/244195/italian-portuguese-meat-loaf-fusion/?internalSource=rotd&referringContentType=home%20page&clickId=cardslot%201'

    #test bone-in chicken thighs
    qpage = 'https://www.allrecipes.com/recipe/259101/crispy-panko-chicken-thighs/?internalSource=previously%20viewed&referringContentType=home%20page&clickId=cardslot%203'

    #test quatity&measurement conversion:
    #qpage = 'https://www.allrecipes.com/recipe/217228/blood-and-sand-cocktail/?internalSource=rotd&referringId=80&referringContentType=recipe%20hub'

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

    # Parse directions
    primary_cookingmethods = []
    other_cookingmethods = []
    used_tools = []

    for dir in directions:
        direction = prep.Directions(dir, primarycookingmethods, othercookingmethods, tools)
        if direction.primaryMethods:
            primary_cookingmethods.append(direction.primaryMethods)
        if direction.tools:
            used_tools.append(direction.tools)
        if direction.otherMethods:
            other_cookingmethods.append(direction.otherMethods)

    # Transform Ingredient List based on input
    primary_cookingmethods = [item for sublist in primary_cookingmethods for item in sublist]
    pm = ''.join(set(primary_cookingmethods))
    if transformation == "vegetarian":
        toVegetarian(prepIngredients, meatList)
    elif transformation == "vegan":
        toVegan(prepIngredients, meatList, veganSubs)
    elif transformation == "easy":
        ingredientList = toEasy(prepIngredients, commonSpices)
    elif transformation == "altmethod":
        altList = toAltMethod(prepIngredients, meatList, altMethods, pm, altList)

    # Prepped ingredients
    for ingredient in prepIngredients:
        print '\n'
        print 'name: ' + ingredient.name
        print 'quantity: ' + str(ingredient.quantity)
        print 'measurement: ' + ingredient.measurement
        print 'descriptor: ' + ingredient.descriptor
        print 'preparation: ' + ingredient.preparation



    #flatten a list
    print '\nPrimary cooking methods:', ', '.join(set(primary_cookingmethods))

    if len(altList) != 0:
        print '\nAlternative cooking methods:', ', '.join(set(altList))

    other_cookingmethods = [item for sublist in other_cookingmethods for item in sublist]
    print '\nOther cooking methods:', ', '.join(set(other_cookingmethods))

    used_tools = [item for sublist in used_tools for item in sublist]
    print '\nTools:', ', '.join(set(used_tools))



    end_time = time.time()
    print(end_time - start_time)



if __name__ == "__main__":
    main()
