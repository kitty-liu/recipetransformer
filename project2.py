###############################################################

## EECS337
## Group 3: Emily Blackman, Noah Karpinski, Kitty Liu, Yani Xie

###############################################################

import project2_preprocess as prep
import time
from pattern.text.en import pluralize


#Update directions when any ingredient changes. Replace original ingredient to new ingredient
def updateDirections(directions,org_ingredient,new_ingredient):
    return [dir.replace(org_ingredient,new_ingredient) for dir in directions]

# right now replacing with tofu but will add other types
def toVegetarian(ingredientList, meatList,directions):
    vegList = []
    for ingredient in ingredientList:
        for meat in meatList:
            if meat in ingredient.name:
                directions = updateDirections(directions,ingredient.name,'tofu')
                ingredient.name = "tofu"
                ingredient.descriptor = "none"
                ingredient.measurement = "ounce"
        vegList.append(ingredient)
    return vegList,directions

def toVegan(ingredientList, meatList, veganSubs,directions):
    veganList = []
    for ingredient in ingredientList:
        for meat in meatList:
            if meat in ingredient.name:
                directions = updateDirections(directions,ingredient.name,'tofu')
                ingredient.name = "tofu"
                ingredient.descriptor = "none"
                ingredient.measurement = "ounce"
        for nonVeg in veganSubs.keys():
            if nonVeg in ingredient.name:
                directions = updateDirections(directions,ingredient.name,veganSubs[nonVeg])
                ingredient.name = veganSubs[nonVeg]
        veganList.append(ingredient)
    return veganList,directions

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

    options = ['vegetarian','vegan', 'healthy', 'altmethod', 'easy']
    if transformation in options:
        print 'Transforming to ' + transformation + '...\n'
    else:
        print 'Your option(' + transformation + ') is not available. Analyzing original recipe...\n'

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
    #qpage = 'https://www.allrecipes.com/recipe/259101/crispy-panko-chicken-thighs/?internalSource=previously%20viewed&referringContentType=home%20page&clickId=cardslot%203'

    #test quatity&measurement conversion:
    #qpage = 'https://www.allrecipes.com/recipe/217228/blood-and-sand-cocktail/?internalSource=rotd&referringId=80&referringContentType=recipe%20hub'

    qpage = 'https://www.allrecipes.com/recipe/20545/bruschetta-iii/?internalSource=hub%20recipe&referringContentType=search%20results&clickId=cardslot%2022'

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
    primary_cookingmethods_list = []
    other_cookingmethods = []
    used_tools = []
    steps_time = []
    #steps_test = []

    for dir in directions:
        direction = prep.Directions(dir, primarycookingmethods, othercookingmethods, tools,)
        if direction.primaryMethods:
            primary_cookingmethods_list.append(direction.primaryMethods)
        if direction.tools:
            used_tools.append(direction.tools)
        if direction.otherMethods:
            other_cookingmethods.append(direction.otherMethods)
        if direction.cookingtime:
            steps_time.append(direction.cookingtime)
        #if direction.step:
            #steps_test.append(direction.step)

    # Transform Ingredient List based on input
    primary_cookingmethods = [item for sublist in primary_cookingmethods_list for item in sublist if not item is 'none']
    pm = ''.join(set(primary_cookingmethods))
    if transformation == "vegetarian":
        prepIngredients,directions = toVegetarian(prepIngredients, meatList,directions)
    elif transformation == "vegan":
        prepIngredients,directions = toVegan(prepIngredients, meatList, veganSubs,directions)
    elif transformation == "easy":
        prepIngredients = toEasy(prepIngredients, commonSpices)
    elif transformation == "altmethod":
        altList = toAltMethod(prepIngredients, meatList, altMethods, pm, altList)

    # Prepped ingredients
    for ingredient in prepIngredients:
        print '\n'
        print 'name: ' + ingredient.name
        print 'quantity: ' + str(ingredient.quantity)
        print 'measurement: ' + ingredient.measurement if ingredient.quantity <= 1 or ingredient.measurement is 'none' \
            else 'measurement: ' + pluralize(ingredient.measurement)
        print 'descriptor: ' + ingredient.descriptor
        print 'preparation: ' + ingredient.preparation


    steps = []
    for i in range(len(directions)):

        igd_for_dir = set([ing.name for ing in prepIngredients for word in ing.name.split(' ') if word in directions[i]])
        if len(igd_for_dir) < 1:
            igd_for_dir = ['none']
        steps.append('Step ' + str(i+1) + ': | ' + 'Ingredients: ' + ', '.join(igd_for_dir) + ' | ' + 'Tool: ' +
                     ', '.join(used_tools[i]) + ' | ' + 'Primary Cooking Methods: ' + ', '.join(primary_cookingmethods_list[i])
                     + ' | ' + 'Other Cooking Methods: ' + ', '.join(other_cookingmethods[i]) + ' | ' + 'Time: ' +
                     ', '.join(steps_time[i]))



    used_tools = [item for sublist in used_tools for item in sublist if not item is 'none']
    print '\nTools:\n', ', '.join(set(used_tools)) if len(used_tools) > 0 else 'none'

    print '\nMethods:'
    print '\tPrimary cooking methods:', ', '.join(set(primary_cookingmethods))

    if len(altList) != 0:
        print '\tAlternative cooking methods:', ', '.join(set(altList))

    other_cookingmethods = [item for sublist in other_cookingmethods for item in sublist if not item is 'none']
    print '\tOther cooking methods:', ', '.join(set(other_cookingmethods)) if len(other_cookingmethods) > 0 else 'none'

    print '\nSteps:'
    for s in steps:
        print '\n'.join(s.split(' | '))
        print '\n'




    end_time = time.time()
    print(end_time - start_time)



if __name__ == "__main__":
    main()
