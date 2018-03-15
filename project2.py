###############################################################

## EECS337
## Group 3: Emily Blackman, Noah Karpinski, Kitty Liu, Yani Xie

###############################################################

import project2_preprocess as prep
import time
import copy
from pattern.text.en import pluralize,singularize
import ingredients as ingred
import requests

checkedIng = []


# Update directions when any ingredient changes. Replace original ingredient to new ingredient
def updateDirections_ingredients(directions, org_ingredient, new_ingredient):
    if any(org_ingredient in dir for dir in directions):
        if (new_ingredient in checkedIng):
            return directions
        directions = [dir.replace(org_ingredient, new_ingredient) for dir in directions]
        checkedIng.append(new_ingredient)

    # edge case where the new ingredient includes the name of the original ingredient
    if org_ingredient in new_ingredient or org_ingredient[:-1] in new_ingredient or new_ingredient in org_ingredient:
        return directions  # stop here to prevent name from being replaced multiple times

    if org_ingredient[-1:] is "s":
        if any(org_ingredient[:-1] in dir for dir in directions):
            directions = [dir.replace(org_ingredient[:-1], new_ingredient) for dir in directions]

    # edge case when the ingredient name changes and only part of the name appears in the directions
    original = org_ingredient.split()
    for name in original:
        for i in xrange(len(directions)):
            if name in directions[i]:
                directions[i] = directions[i].replace(name, new_ingredient)
    return directions


# Transformation: toVegetarian
def toVegetarian(ingredientList, meatList, meatSubs, directions):
    vegList = []
    i = 0
    for ingredient in ingredientList:
        name = ingredient.name.split()
        for word in name:
            if word in meatList:
                tempquantity = ingredient.quantity
                directions = updateDirections_ingredients(directions, ingredient.name, meatSubs[i].name)
                ingredient = meatSubs[i]
                ingredient.quantity = tempquantity
                i += 1
                break
        vegList.append(ingredient)
    # for meat in meatList:
    for j in xrange(len(directions)):
        directions[j] = directions[j].replace("meat", "tofu")
        directions[j] = directions[j].replace("bone", "middle")
    return vegList, directions


# Transformation: toNonVegetarian
def toNonVegetarian(ingredientList, commonMeatList, meatSubs, directions):
    nonVegList = []
    i = 0
    for ingredient in ingredientList:
        for meatsub in meatSubs:
            if ingredient.name in meatsub.name:
                directions = updateDirections_ingredients(directions, ingredient.name, commonMeatList[i])
                ingredient.name = commonMeatList[i]
                i += 1
                break
        nonVegList.append(ingredient)
    return nonVegList, directions


# Transformation: toVegan
def toVegan(ingredientList, meatList, meatSubs, veganSubs, directions):
    veganList = []
    i = 0
    for ingredient in ingredientList:
        name = ingredient.name.split()
        for word in name:
            if word in meatList:
                tempquantity = ingredient.quantity
                directions = updateDirections_ingredients(directions, ingredient.name, meatSubs[i].name)
                ingredient = meatSubs[i]
                ingredient.quantity = tempquantity
                i += 1
                break
        for nonVeg in veganSubs.keys():
            if nonVeg in ingredient.name:
                directions = updateDirections_ingredients(directions, ingredient.name, veganSubs[nonVeg].name)
                ingredient.name = veganSubs[nonVeg].name
        veganList.append(ingredient)
    # for meat in meatList:
    for j in xrange(len(directions)):
        directions[j] = directions[j].replace("meat", "tofu")
        directions[j] = directions[j].replace("bone", "middle")
        directions[j] = directions[j].replace("crack", "add")
    return veganList, directions


# Transformation: toNonVegan
def toNonVegan(ingredientList, commonMeatList, meatSubs, veganSubs, directions):
    nonVeganList = []
    nonVeganRepl = {y: x for x, y in veganSubs.iteritems()}
    i = 0
    for ingredient in ingredientList:
        for meatsub in meatSubs:
            if ingredient.name in meatsub.name:
                directions = updateDirections_ingredients(directions, ingredient.name, commonMeatList[i])
                ingredient.name = commonMeatList[i]
                i += 1
                break
        for veg in nonVeganRepl.keys():
            if veg.name in ingredient.name:
                directions = updateDirections_ingredients(directions, ingredient.name, veganSubs[veg].name)
                ingredient.name = veganSubs[veg].name
        nonVeganList.append(ingredient)
    return nonVeganList, directions


# Transformation: toHealthy
def toHealthy(ingredientList, healthySubsDict, directions):
    healthyList = []

    for ingredient in ingredientList:
        name = ingredient.name.split()
        # for word in name:
        for ing in healthySubsDict.keys():
            if ing in ingredient.name:
                if ing == "sugar":
                    ingredient.quantity = ingredient.quantity / 2
                if "chocolate" in ing:
                    # for word in ingredient.name:
                    if "chips" in ing:
                        directions = updateDirections_ingredients(directions, ingredient.name,
                                                                  healthySubsDict[ing].name)
                        ingredient.name = healthySubsDict[ing].name
                        ingredient.descriptor = healthySubsDict[ing].descriptor

                    break
                #    break #to prevent chocolate ingredients other than chocolate chips from being replaced with chips
                else:
                    directions = updateDirections_ingredients(directions, ingredient.name, healthySubsDict[ing].name)
                    ingredient.name = healthySubsDict[ing].name
                    ingredient.descriptor = healthySubsDict[ing].descriptor
                break

        healthyList.append(ingredient)
    return healthyList, directions


def toUnhealthy(ingredientList, healthySubsDict, unhealthySubsDict, directions, seafoodList):
    unhealthyList = []
    unhealthyRepl = {y: x for x, y in healthySubsDict.iteritems()}
    for ingredient in ingredientList:
        name = ingredient.name.split()
        # for word in name:
        for ing in unhealthyRepl.keys():
            # ingName = ing.name.split()
            # for part in ingName:
            if ing.name in ingredient.name:
                if ing.name == "sugar":
                    ingredient.quantity = ingredient.quantity * 2  # double the amount of sugar for any type
                directions = updateDirections_ingredients(directions, ingredient.name, unhealthyRepl[ing])
                ingredient.name = unhealthyRepl[ing]
                ingredient.descriptor = "none"  # clear previous descriptors
                if unhealthyRepl[ing] == "flour":
                    ingredient.descriptor = "all-purpose"
                break
        for word in name:
            if word in seafoodList:
                directions = updateDirections_ingredients(directions, ingredient.name, unhealthySubsDict["fish"].name)
                ingredient.name = unhealthySubsDict["fish"].name
        for ing in unhealthySubsDict.keys():
            if "whole turkey" in ingredient.name:
                break  # don't change anything if it is a whole turkey
            if ing in ingredient.name:
                directions = updateDirections_ingredients(directions, ingredient.name, unhealthySubsDict[ing].name)
                ingredient.name = unhealthySubsDict[ing].name
                ingredient.descriptor = unhealthySubsDict[ing].descriptor

        unhealthyList.append(ingredient)
    return unhealthyList, directions


# Transformation: DIY to easy (OPTIONAL)
def toEasy(ingredientList, commonSpices, typicalSpices, directions):
    count = 0
    subcount = 0
    replacements = []
    spiceSizes = ["pinch", "tablespoon", "tablespoons", "teaspoon", "teaspoons", "to taste", "dash", "drops"]
    ingrls = []
    ingnames = []
    for ings in ingredientList:
        ingnames.append(ings.name)
    maxed = False
    for ingredient in ingredientList:
        common = False
        for spice in commonSpices:
            if spice in ingredient.name:
                common = True
        if not common and ingredient.measurement in spiceSizes:
            replaced = False
            while not replaced and not maxed:
                if subcount < len(typicalSpices):
                    if typicalSpices[subcount].name not in ingnames:
                        replacements.append([ingredient, typicalSpices[subcount]])
                        replaced = True
                else:
                    maxed = True
                subcount += 1
            if not replaced:
                olding = copy.deepcopy(ingredientList[count])
                olding.name = olding.name + "&REMOVED&"
                directions = updateDirections_ingredients(directions, ingredient.name, olding.name)
                ingredient = olding
        ingrls.append(ingredient)
        count += 1
    for r in replacements:
        directions = updateDirections_ingredients(directions, r[0].name, r[1].name)
        tempquantity = r[0].quantity
        r[0] = r[1]
        r[0].quantity = tempquantity
    return ingredientList, directions


# Transformation: toAltMethod
def toAltMethod(ingredientList, vegetableList, meatList, altMethods, pm, directions):
    altlt = []
    if len(pm) == 1:
        pm = pm[0].encode('utf-8')
    else:
        altlt.append("")
        return altlt, directions, ''
    for ingredient in ingredientList:
        for meat in meatList:
            if meat in ingredient and "broth" not in ingredient:
                for alt in altMethods:
                    res = alt.getAlts("meat", pm)
                    if res != -1:
                        altlt = res
                        return altlt, directions, pm
    # Meat has priority since it is more important if meat is cooked properly
    for ingredient in ingredientList:
        for veg in vegetableList:
            if veg in ingredient:
                for alt in altMethods:
                    res = alt.getAlts("veg", pm)
                    if res != -1:
                        altlt = res
                        return altlt, directions, pm

    altlt.append("")
    return altlt, directions, ''


# Transformation: toChinese (Style of cuisine)
def toChinese(ingredientList, chineseIngredients, commonSpices, commonSauces, directions):
    chList = []
    spiceSizes = ["pinch", "tablespoon", "tablespoons", "teaspoon", "teaspoons", "to taste", "dash", "drops"]
    i = 0
    z = 0
    for ingredient in ingredientList:
        if ingredient.name in commonSauces and z < len(chineseIngredients[1]):
            directions = updateDirections_ingredients(directions, ingredient.name, chineseIngredients[1][z].name)
            tempquantity = ingredient.quantity
            ingredient = chineseIngredients[1][z]
            ingredient.quantity = tempquantity
            z += 1
        elif ingredient.name not in commonSpices and ingredient.measurement in spiceSizes and i < len(
                chineseIngredients[0]):
            directions = updateDirections_ingredients(directions, ingredient.name, chineseIngredients[0][i].name)
            tempquantity = ingredient.quantity
            ingredient = chineseIngredients[0][i]
            ingredient.quantity = tempquantity
            i += 1
        for j in chineseIngredients[2].keys():
            if j in ingredient.name or ingredient.name in j:
                directions = updateDirections_ingredients(directions, ingredient.name, chineseIngredients[2][j].name)
                ingredient = chineseIngredients[2][j]
        chList.append(ingredient)
    return chList, directions


# Transformation: toItalian (Style of cuisine)
def toItalian(ingredientList, italianIngredients, commonSpices, commonSauces, commonOils, directions):
    itList = []
    spiceSizes = ["pinch", "tablespoon", "tablespoons", "teaspoon", "teaspoons", "to taste", "dash", "drops"]
    i = 0
    j = 0
    oilReplaced = False
    for ingredient in ingredientList:
        if ingredient.name in commonSauces and j < len(italianIngredients[1]):
            directions = updateDirections_ingredients(directions, ingredient.name, italianIngredients[1][j].name)
            tempquantity = ingredient.quantity
            ingredient = italianIngredients[1][j]
            ingredient.quantity = tempquantity
            j += 1
        elif ingredient.name in commonOils and not oilReplaced:
            olding = copy.deepcopy(ingredient)
            olding.name = italianIngredients[2][0].name
            directions = updateDirections_ingredients(directions, ingredient.name, olding.name)
            ingredient = olding
            oilReplaced = True
        elif ingredient.name not in commonSpices and ingredient.measurement in spiceSizes and i < len(
                italianIngredients[0]):
            directions = updateDirections_ingredients(directions, ingredient.name, italianIngredients[0][i].name)
            tempquantity = ingredient.quantity
            ingredient = italianIngredients[0][i]
            ingredient.quantity = tempquantity
            i += 1
        itList.append(ingredient)

    return itList, directions


# Main function
def main():
    start_time = time.time()

    qpage = str(raw_input("Enter a recipe link from AllRecipes website: ")).strip()
    while not 'https://' in qpage or requests.get(qpage).status_code != 200:
        qpage = str(raw_input("Invalid link - Enter a recipe link from AllRecipes website again: ")).strip()

        # Ask for a user input
    transformation = str(raw_input(
        "What type of transformation do you want to do to the recipe?\n Your options are vegetarian, nonvegetarian, vegan, nonvegan, healthy, unhealthy, altmethod, easy, chinese, italian: "))

    options = ['vegetarian', 'nonvegetarian', 'vegan', 'nonvegan', 'healthy', 'unhealthy', 'altmethod', 'easy',
               'chinese', 'italian']
    if transformation in options:
        print 'Transforming to ' + transformation + '...\n'
    else:
        print ' Your option(' + transformation + ') is not available. Analyzing original recipe...\n'

    # Scrape necessary lists: including units, primary cooking methods, other cooking methods, tools, meat,vegetable
    mod = 'html.parser'

    # scrape units
    unit_page = 'https://www.adducation.info/how-to-improve-your-knowledge/units-of-measurement/'
    unit_sp = prep.Scraper(unit_page, mod)
    units = unit_sp.scrape_unit()

    # scrape primary cooking methods:
    primarycookingmethods_page = 'https://www.thedailymeal.com/cook/15-basic-cooking-methods-you-need-know-slideshow/slide-12'
    primarycookingmethods_sp = prep.Scraper(primarycookingmethods_page, mod)
    primarycookingmethods = primarycookingmethods_sp.scrape_primarycookingmethods()
    primarycookingmethods = [pc for pc in primarycookingmethods if not 'fry' in pc]
    primarycookingmethods.append('fry')

    # scrape other cooking methods:
    othercookingmethods_page = 'https://www.d.umn.edu/~alphanu/cookery/glossary_cooking.html'
    othercookingmethods_page_sp = prep.Scraper(othercookingmethods_page, mod)
    othercookingmethods = othercookingmethods_page_sp.scrape_cookingmethods()

    # scrape tools.txt
    tools_page = 'tools.txt'
    tools_sp = prep.Scraper(tools_page, '')
    tools = tools_sp.scrape_tools()

    # VEGETARIAN
    # scrape meat
    meat_page = "http://naturalhealthtechniques.com/list-of-meats-and-poultry/"
    meatlist_sp = prep.Scraper(meat_page, mod)
    meatList = meatlist_sp.scrape_meats()
    meatList.extend(
        ("pepperoni", "salami", "proscuitto", "sausage", "ham", "chorizo", "rib", "steak", "bone", "thigh"))

    seafood_page = "https://en.wikipedia.org/wiki/List_of_types_of_seafood"
    seafoodlist_sp = prep.Scraper(seafood_page, mod)
    seafoodList = seafoodlist_sp.scrape_seafood()
    meatList.extend(seafoodList)

    meatSubs = [ingred.tofu, ingred.tempeh, ingred.texturedvegprote, ingred.mushrooms, ingred.jackfruit, ingred.lentils]
    commonMeatList = ["chicken", "pork", "beef", "lamb", "salmon", "tuna", "duck", "turkey", "ham"]
    # VEGAN
    veganSubs = {"milk": ingred.almondmilk, "cream": ingred.almondmilk, "yogurt": ingred.coconutyogurt,
                 "egg": ingred.silktofu, "butter": ingred.soymarg,
                 "honey": ingred.agave, "cheese": ingred.nutyeast, "gelatin": ingred.agar}

    # Healthy Substitutions
    unhealthySubsDict = {"turkey": ingred.beef, "chicken": ingred.breadedchicken, "fish": ingred.beef}
    healthySubsDict = {"sugar": ingred.sugar, "bacon": ingred.turkeybacon, "bread": ingred.wholegrainbread,
                       "bread crumb": ingred.rolledoats, "butter": ingred.fatfreebutterspread,
                       "cream": ingred.halfandhalf,
                       "cream cheese": ingred.fatfreecreamcheese, "egg": ingred.eggwhites,
                       "flour": ingred.wholewheatflour, "beef": ingred.leanbeef, "lettuce": ingred.arugula,
                       "mayonnaise": ingred.reducedfatmayo, "evaporated milk": ingred.evaporatedskim,
                       "milk": ingred.fatfreemilk, "rice": ingred.brownrice, "dressing": ingred.fatfreedressing,
                       "sour cream": ingred.fatfreesourcream, "chocolate chip": ingred.unsweetenedchips}

    # Alt Methods
    altList = []
    pm_list = []
    # Simmer, Stew, and Braise too situational
    br = "broil"
    bake = "bake"
    sr = "sear"
    gr = "grill"
    rt = "roast"
    f = "fry"
    sa = "saute"
    st = "steam"
    any = "any"
    altMethods = []
    altMethods.append(prep.AltCook("meat", bake, [br, rt, gr, sr, f]))
    altMethods.append(prep.AltCook("meat", br, [bake]))
    altMethods.append(prep.AltCook("meat", sa, [bake, f]))
    altMethods.append(prep.AltCook("meat", sr, [bake, gr, rt, f]))
    altMethods.append(prep.AltCook("meat", gr, [bake, sr, rt, f]))
    altMethods.append(prep.AltCook("meat", rt, [bake, sr, gr, f]))
    altMethods.append(prep.AltCook("veg", any, [st]))

    vegetable_page = "https://simple.wikipedia.org/wiki/List_of_vegetables"
    vegetableList_sp = prep.Scraper(vegetable_page, mod)
    vegetableList = vegetableList_sp.scrape_vegtables()

    # CUISINE TRANSFORMATION LISTS
    commonSpices = ["salt", "pepper", "garlic powder", "onion powder", "water", "butter", "olive oil", "oil"]

    commonSauces = ["barbecue", "bbq", "gravy", "buffalo", "tabasco", "sriracha", "mustard",
                    "ketchup", "salsa"]
    commonOils = ["canola oil", "vegtable oil", "coconut oil", "peanut oil", "lard", "cooking spray"]

    typicalSpices = [ingred.salt, ingred.pepper, ingred.garlicpowder, ingred.onionpowder]

    # Chinese Ingredients
    chineseSpices = [ingred.ginger, ingred.star_anise, ingred.five_spice, ingred.cilantro, ingred.chinesecinnamon,
                     ingred.cloves, ingred.fennelseed, ingred.corianderseed, ingred.chilipowder, ingred.peppercorn]
    chineseSauces = [ingred.fishsauce, ingred.soysauce, ingred.oystersauce, ingred.chilipaste]
    chineseVegetables = {"bell pepper": ingred.whiteradish, "asparagu": ingred.bambooshoots, "pea": ingred.beanspouts,
                         "lettuce": ingred.bokchoy, "brussel sprout": ingred.chives, "kale": ingred.chinesecabbage}
    chineseIngredients = [chineseSpices, chineseSauces, chineseVegetables]


    # Italian Ingredients
    italianSpices = [ingred.oregano, ingred.thyme, ingred.rosemary, ingred.sage, ingred.basil,
                     ingred.marjoram]

    italianSauces = [ingred.tomatosauce, ingred.alfredosauce, ingred.pestosauce]

    italianOils = [ingred.oliveoil]

    italianIngredients = [italianSpices, italianSauces, italianOils]

    # scrape recipe
    recp = prep.Scraper(qpage, mod)
    ingredients = recp.scrape_ingredients()
    directions = recp.scrape_directions()

    prepIngredients = []

    # Parse ingredients
    for igd in ingredients:
        prepIngredients.append(prep.Ingredients(igd, units))

    # Parse directions
    primary_cookingmethods_list = []
    other_cookingmethods = []
    used_tools = []
    steps_time = []

    for dir in directions:
        direction = prep.Directions(dir, primarycookingmethods, othercookingmethods, tools)
        if direction.primaryMethods:
            primary_cookingmethods_list.append(direction.primaryMethods)
        if direction.tools:
            used_tools.append(direction.tools)
        if direction.otherMethods:
            other_cookingmethods.append(direction.otherMethods)
        if direction.cookingtime:
            steps_time.append(direction.cookingtime)

    # analyze ingredients in each step for toAltMethods
    stepIngredients = []
    igd_for_dir = set([ing.name for ing in prepIngredients for word in ing.name.split(' ') if word in directions[0]])
    stepIngredients.append(igd_for_dir)
    for i in range(1, len(directions)):
        igd_for_dir = set(
            [ing.name for ing in prepIngredients for word in ing.name.split(' ') if word in directions[i]])
        if len(igd_for_dir) < 1:
            stepIngredients.append(stepIngredients[i - 1])
        else:
            stepIng = ', '.join(igd_for_dir)
            stepIngredients.append(stepIng.split(', '))

    # Transform Ingredient List based on input
    primary_cookingmethods = [item for sublist in primary_cookingmethods_list for item in sublist if not item is 'none']
    if transformation == "vegetarian":
        prepIngredients, directions = toVegetarian(prepIngredients, meatList, meatSubs, directions)
    elif transformation == "nonvegetarian":
        prepIngredients, directions = toNonVegetarian(prepIngredients, commonMeatList, meatSubs, directions)
    elif transformation == "vegan":
        prepIngredients, directions = toVegan(prepIngredients, meatList, meatSubs, veganSubs, directions)
    elif transformation == "nonvegan":
        prepIngredients, directions = toNonVegan(prepIngredients, commonMeatList, meatSubs, veganSubs, directions)
    elif transformation == "easy":
        prepIngredients, directions = toEasy(prepIngredients, commonSpices, typicalSpices, directions)
    elif transformation == "healthy":
        prepIngredients, directions = toHealthy(prepIngredients, healthySubsDict, directions)
    elif transformation == "unhealthy":
        prepIngredients, directions = toUnhealthy(prepIngredients, healthySubsDict, unhealthySubsDict, directions,
                                                  seafoodList)

    elif transformation == "altmethod":
        count1 = 0
        for pm in primary_cookingmethods_list:
            altmethods_list, directions, org_method = toAltMethod(stepIngredients[count1], vegetableList, meatList,
                                                                  altMethods, pm, directions)
            altList.append(altmethods_list)
            pm_list.append(org_method)
            count1 += 1
    elif transformation == "chinese":
        prepIngredients, directions = toChinese(prepIngredients, chineseIngredients, commonSpices, commonSauces,
                                                directions)
    elif transformation == "italian":
        prepIngredients, directions = toItalian(prepIngredients, italianIngredients, commonSpices, commonSauces,
                                                commonOils, directions)

    # Steps: analyze each direction
    steps = []
    all_altermethod = []
    for i in range(len(directions)):
        igd_for_dir = set(
            [ing.name for ing in prepIngredients for word in ing.name.split(' ') if word in directions[i]])
        if len(igd_for_dir) < 1:
            igd_for_dir = ['none']
        alttxt = ""
        if altList and altList[i][0] != "":
            alttxt = "Alternate Cooking Method: " + pm_list[i] + ' --> ' + ', '.join(altList[i])
            all_altermethod.append(pm_list[i] + ' --> ' + ' ,'.join(altList[i]))
            alttxt += ' | '
        steps.append('Step ' + str(i + 1) + ': | ' + 'Ingredients: ' + ', '.join(set(igd_for_dir)) + ' | ' + 'Tools: ' +
                     ', '.join(set(used_tools[i])) + ' | ' + 'Primary Cooking Methods: ' + ', '.join(
            set(primary_cookingmethods_list[i]))
                     + ' | ' + alttxt + 'Other Cooking Methods: ' + ', '.join(
            set(other_cookingmethods[i])) + ' | ' + 'Time: ' +
                     ', '.join(steps_time[i]) + ' | ' + 'Details/Directions: ' + directions[i])

    # Output: transformed ingredients
    print 'Ingredients:'
    for ingredient in prepIngredients:
        print 'name: ' + ingredient.name
        print 'quantity: ' + str(ingredient.quantity)
        print 'measurement: ' + ingredient.measurement if ingredient.quantity <= 1 or ingredient.measurement is 'none' \
            else 'measurement: ' + pluralize(ingredient.measurement)
        print 'descriptor: ' + ingredient.descriptor
        print 'preparation: ' + ingredient.preparation
        print '\n'

    # Output: tools
    used_tools = [item for sublist in used_tools for item in sublist if not item is 'none']
    print 'Tools:\n', ', '.join(set(used_tools)) if len(used_tools) > 0 else 'none'

    # Output: methods
    print '\nMethods:'
    print '\tPrimary cooking methods:', ', '.join(set(primary_cookingmethods)) \
        if len(primary_cookingmethods) > 0 else 'none'
    if transformation == "altmethod":
        if all_altermethod:
            print "\tAlternate Cooking Methods: " + ', '.join(set(all_altermethod))
        else:
            print "\tAlternate Cooking Methods: No alternate cooking method is available for this recipe."

    other_cookingmethods = [item for sublist in other_cookingmethods for item in sublist if not item is 'none']
    print '\tOther cooking methods:', ', '.join(set(other_cookingmethods)) if len(other_cookingmethods) > 0 else 'none'

    # Output: steps
    print '\nSteps:'
    for s in steps:
        print '\n'.join(s.split(' | '))
        print '\n'

    # Calculate running time
    end_time = time.time()
    print 'Running time: ' + str(end_time - start_time)

    # HTML Output: transformed ingredients
    f = open("results.html", "w")
    f.write("<html><body><h2>Ingredients:</h2><br/>")
    for ingredient in prepIngredients:
        if str(ingredient.quantity) != "none":
            f.write(str(ingredient.quantity) + " ")
        else:
            f.write("")
        if ingredient.measurement is 'none':
            f.write("")
        elif ingredient.quantity <= 1:
            f.write(" " + ingredient.measurement)
        else:
            f.write(" " + pluralize(ingredient.measurement))
        f.write(" " + ingredient.name + "<br/>")
        # f.write('descriptor: ' + ingredient.descriptor + "<br/>")
        # f.write('preparation: ' + ingredient.preparation + "<br/><br/>")

    # HTML Output: tools
    f.write('<h2>Tools:</h2><br/>')
    f.write(', '.join(set(used_tools)) if len(used_tools) > 0 else 'none')
    f.write('<br/>')
    # HTML Output: methods
    f.write('<br/><h2>Methods:</h2><br/>')
    f.write('Primary cooking methods: ')
    f.write(', '.join(set(primary_cookingmethods)) if len(primary_cookingmethods) > 0 else 'none')
    f.write("<br/>")
    if transformation == "altmethod":
        if all_altermethod:
            f.write("Alternate Cooking Methods: " + ', '.join(set(all_altermethod)))
            f.write("<br/>")
        else:
            f.write("Alternate Cooking Methods: No alternate cooking method is available for this recipe.")
            f.write("<br/>")
    f.write('Other cooking methods: ')
    f.write(', '.join(set(other_cookingmethods)) if len(other_cookingmethods) > 0 else 'none')

    # HTML Output: steps
    f.write('<h2>Steps:</h2><br/>')
    for s in steps:
        f.write('<br/>'.join(s.split(' | ')))
        f.write('<br/><br/>')


if __name__ == "__main__":
    main()
