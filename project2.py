###############################################################

## EECS337
## Group 3: Emily Blackman, Noah Karpinski, Kitty Liu, Yani Xie

###############################################################

import project2_preprocess as prep
import time
from pattern.text.en import pluralize
import ingredients as ingred


#Update directions when any ingredient changes. Replace original ingredient to new ingredient
def updateDirections_ingredients(directions,org_ingredient,new_ingredient):
    if any(org_ingredient in dir for dir in directions):
        return [dir.replace(org_ingredient, new_ingredient) for dir in directions]
    else:  #edge case when the ingredient name changes and only part of the name appears in the directions
        original = org_ingredient.split()
        for name in original:
            for i in xrange(len(directions)):
                if name in directions[i]:
                    directions[i] = directions[i].replace(name, new_ingredient)
                    print directions[i]
                    return directions
        return directions



#Update directions when any cooking method changes. Replace original cooking method to new cooking method and update
# cooking appliances
def updateDirections_methods(directions,org_method,new_method):
    newdir = []
    for dir in directions:
        dir = dir.replace(org_method, new_method)
        if org_method == 'bake':
            dir = dir.replace('oven','pan')
        newdir.append(dir)
    return newdir

def toVegetarian(ingredientList, meatList, meatSubs, directions):
    vegList = []
    i = 0
    for ingredient in ingredientList:
        name = ingredient.name.split()
        for word in name:
            if word in meatList:
                directions = updateDirections_ingredients(directions, ingredient.name, meatSubs[i].name)
                # directions = updateDirections_methods(directions, ingredient., meatSubs[i].transformed_method)
                ingredient = meatSubs[i]
                i += 1
                break
        vegList.append(ingredient)
    directions = [dir.replace("meat", "") for dir in directions]
    return vegList, directions

def toVegan(ingredientList, meatList, veganSubs,directions):
    veganList = []
    for ingredient in ingredientList:
        for meat in meatList:
            if meat in ingredient.name:
                directions = updateDirections_ingredients(directions,ingredient.name,'tofu')
                ingredient.name = "tofu"
                ingredient.descriptor = "none"
                ingredient.measurement = "ounce"
        for nonVeg in veganSubs.keys():
            if nonVeg in ingredient.name:
                directions = updateDirections_ingredients(directions,ingredient.name,veganSubs[nonVeg])
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

def toAltMethod(ingredientList, vegetableList, meatList, altMethods, pm, directions):
    altlt = []
    for ingredient in ingredientList:
        for meat in meatList:
            if meat in ingredient:
                for alt in altMethods:
                    res = alt.getAlts("meat",pm)
                    if res != -1:
                        #directions = updateDirections_methods(directions,pm,' or '.join(set(res)))
                        altlt = res
                        return altlt,directions,pm
    # Meat has priority since it is more important if meat is cooked properly
    for ingredient in ingredientList:
        for veg in vegetableList:
            if veg in ingredient:
                for alt in altMethods:
                    res = alt.getAlts("veg",pm)
                    if res != -1:
                        #directions = updateDirections_methods(directions, pm, ' or '.join(set(res)))
                        altlt = res
                        return altlt, directions,pm

    altlt.append("")
    return altlt,directions,''

def toChinese(ingredientList, chineseIngredients, commonSpices, directions):
    chList = []
    spiceSizes = ["pinch", "tablespoon", "tablespoons", "teaspoon", "teaspoons", "to taste", "dash", "drops"]
    i = 0
    for ingredient in ingredientList:
        if ingredient.name not in commonSpices and ingredient.measurement in spiceSizes:
            directions = updateDirections_ingredients(directions, ingredient.name, chineseIngredients[0][i].name)
            tempquantity = ingredient.quantity
            ingredient = chineseIngredients[0][i]
            ingredient.quantity = tempquantity
            i += 1
        chList.append(ingredient)
    return chList,directions

#Main function
def main():
    start_time = time.time()
    transformation = str(raw_input("What type of transformation do you want to do to the recipe?\n Your options are vegetarian, vegan, healthy, altmethod, easy, chinese: "))

    options = ['vegetarian','vegan', 'healthy', 'altmethod', 'easy', 'chinese']
    if transformation in options:
        print 'Transforming to ' + transformation + '...\n'
    else:
        print ' Your option(' + transformation + ') is not available. Analyzing original recipe...\n'

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


    # VEGETARIAN
    #scrape meat
    meat_page = "http://naturalhealthtechniques.com/list-of-meats-and-poultry/"
    meatlist_sp = prep.Scraper(meat_page, mod)
    meatList = meatlist_sp.scrape_meats()
    meatList.extend(("pepperoni", "salami", "proscuitto", "sausage", "ham", "chorizo", "ribs", "steak"))
    print "Meat List" ,meatList

    meatSubs = [ingred.tofu, ingred.tempeh, ingred.texturedvegprote, ingred.mushrooms,ingred.jackfruit, ingred.lentils]
    vegetable_page = "https://simple.wikipedia.org/wiki/List_of_vegetables"
    vegetableList_sp = prep.Scraper(vegetable_page, mod)
    vegetableList = vegetableList_sp.scrape_vegtables()

    # VEGAN
    veganSubs = {"milk": "almond milk", "yogurt": "coconut yogurt", "eggs": "tofu", "butter": "soy margarine",
                 "honey": "agave syrup", "cheese": "nutritional yeast"}

    #Easy change
    commonSpices = ["salt", "pepper", "garlic"]

    #Alt Methods
    altList = []
    pm_list = []
    pf = "pan fry"
    bake = "bake"
    mw = "microwave"
    df = "deepfry"
    st = "steam"
    any = "any"
    altMethods = []
    altMethods.append(prep.AltCook("meat",bake,[pf, mw]))
    altMethods.append(prep.AltCook("meat", pf, [df, bake, mw]))
    altMethods.append(prep.AltCook("meat", mw, [pf, bake]))
    altMethods.append(prep.AltCook("meat", df, [pf, bake]))
    altMethods.append(prep.AltCook("veg", any, [st]))

    # CUISINE TRANSFORMATION LISTS
    commonSpices = ["salt", "pepper", "garlic powder", "onion powder", "water", "butter", "olive oil", "oil"]

    commonVegetables = ['potato', 'corn', 'green bean', 'broccoli', 'carrot', 'tomato', 'cucumber', 'onion',
                        'spinach', 'sweet potato', 'mushroom', 'cauliflower', 'celery', 'zucchini', 'jalapeno',
                        'eggplant', 'yam', 'leek']
    commonOther = ["olive oil", "water", "sugar", "butter"]


    #Chinese Ingredients
    chineseSpices = [ingred.ginger, ingred.star_anise, ingred.five_spice, ingred.cilantro, ingred.peppercorn, ingred.chinesecinnamon,
                     ingred.cloves, ingred.fennelseed, ingred.corianderseed, ingred.chilipowder]
    chineseSauces = [ingred.ricevinegar, ingred.soysauce, ingred.sesameoil, ingred.chilipaste]
    chineseVegetables = [ingred.bokchoy, ingred.chives, ingred.greenonion, ingred.chinesecabbage, ingred.beanspouts, ingred.whiteradish, ingred.bambooshoots]
    # chineseSauces = {"oil": "sesame oil", "vinegar": "rice vinegar", "sauce": "soy sauce", "chili": "chili paste"}
    chineseIngredients = [chineseSpices, chineseSauces, chineseVegetables]

    #example to add a cooking method for ginger
    # gingertest = prep.Ingredients('1 tablespoon chopped ginger', units,'stir fry')
    # print gingertest.transformed_method

    #test pages:
    # qpage = 'https://www.allrecipes.com/recipe/262723/homemade-chocolate-eclairs/?internalSource=staff%20pick&referringContentType=home%20page&clickId=cardslot%209'
    # qpage = 'https://www.allrecipes.com/recipe/228796/slow-cooker-barbequed-beef-ribs/?internalSource=popular&referringContentType=home%20page&clickId=cardslot%205'
    # qpage = 'http://allrecipes.com/recipe/244195/italian-portuguese-meat-loaf-fusion/?internalSource=rotd&referringContentType=home%20page&clickId=cardslot%201'

    #test bone-in chicken thighs
    #qpage = 'https://www.allrecipes.com/recipe/259101/crispy-panko-chicken-thighs/?internalSource=previously%20viewed&referringContentType=home%20page&clickId=cardslot%203'

    #test quatity&measurement conversion:
    #qpage = 'https://www.allrecipes.com/recipe/217228/blood-and-sand-cocktail/?internalSource=rotd&referringId=80&referringContentType=recipe%20hub'

    #qpage = 'https://www.allrecipes.com/recipe/20545/bruschetta-iii/?internalSource=hub%20recipe&referringContentType=search%20results&clickId=cardslot%2022'
    #qpage = 'https://www.allrecipes.com/recipe/262622/indian-chicken-tikka-masala/?internalSource=previously%20viewed&referringContentType=home%20page&clickId=cardslot%203'
    #qpage = 'https://www.allrecipes.com/recipe/73634/colleens-slow-cooker-jambalaya/?internalSource=previously%20viewed&referringContentType=home%20page&clickId=cardslot%2014'

    qpage = 'https://www.allrecipes.com/recipe/245362/chef-johns-shakshuka/'
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


    stepIngredients = []
    igd_for_dir = set([ing.name for ing in prepIngredients for word in ing.name.split(' ') if word in directions[0]])
    stepIngredients.append(igd_for_dir)
    for i in range(1,len(directions)):
        igd_for_dir = set([ing.name for ing in prepIngredients for word in ing.name.split(' ') if word in directions[i]])
        if len(igd_for_dir) < 1:
            stepIngredients.append(stepIngredients[i-1])
        else:
            stepIng = ', '.join(igd_for_dir)
            stepIngredients.append(stepIng.split(', '))


    # Transform Ingredient List based on input
    primary_cookingmethods = [item for sublist in primary_cookingmethods_list for item in sublist if not item is 'none']
    if transformation == "vegetarian":
        prepIngredients,directions = toVegetarian(prepIngredients, meatList, meatSubs, directions)
    elif transformation == "vegan":
        prepIngredients,directions = toVegan(prepIngredients, meatList, veganSubs,directions)
    elif transformation == "easy":
        prepIngredients = toEasy(prepIngredients, commonSpices)
    elif transformation == "altmethod":
        count1 = 0
        for pm in primary_cookingmethods_list:
            altmethods_list, directions,org_method = toAltMethod(stepIngredients[count1], vegetableList, meatList, altMethods, pm[0].encode('utf-8'),directions)
            altList.append(altmethods_list)
            pm_list.append(org_method)
            count1 += 1
    elif transformation == "chinese":
        prepIngredients,directions = toChinese(prepIngredients, chineseIngredients, commonSpices, directions)

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
    all_altermethod = []
    for i in range(len(directions)):
        igd_for_dir = set([ing.name for ing in prepIngredients for word in ing.name.split(' ') if word in directions[i]])
        if len(igd_for_dir) < 1:
            igd_for_dir = ['none']
        alttxt = ""
        if altList and altList[i][0] != "":
            alttxt = "Alternate Cooking Method: " + pm_list[i] + ' --> '+', '.join(altList[i])
            all_altermethod.append(pm_list[i] + ' --> ' + ' ,'.join(altList[i]))
            alttxt += ' | '
        steps.append('Step ' + str(i+1) + ': | ' + 'Ingredients: ' + ', '.join(set(igd_for_dir)) + ' | ' + 'Tools: ' +
                     ', '.join(set(used_tools[i])) + ' | ' + 'Primary Cooking Methods: ' + ', '.join(set(primary_cookingmethods_list[i]))
                     + ' | '+ alttxt + 'Other Cooking Methods: ' + ', '.join(set(other_cookingmethods[i])) + ' | ' + 'Time: ' +
                     ', '.join(steps_time[i]) + ' | ' + 'Details: ' + directions[i])



    used_tools = [item for sublist in used_tools for item in sublist if not item is 'none']
    print '\nTools:\n', ', '.join(set(used_tools)) if len(used_tools) > 0 else 'none'

    print '\nMethods:'
    print '\tPrimary cooking methods:', ', '.join(set(primary_cookingmethods))
    if transformation == "altmethod":
        if all_altermethod:
            print "\tAlternate Cooking Methods: " + ', '.join(set(all_altermethod))
        else:
            print "\tAlternate Cooking Methods: No alternate cooking method is available for this recipe."

    #if len(altList) != 0:
        #print '\tAlternative cooking methods:', ', '.join(set(altList))

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
