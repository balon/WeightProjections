import datetime
import math

# globals
today = datetime.datetime.now()
lb = 3500

# activity level mutiplier based on: https://www.k-state.edu/paccats/Contents/PA/PDF/Physical%20Activity%20and%20Controlling%20Weight.pdf
activity = dict()
activity["penalty"] = 0.8           # assuming you 'believe' in starvation mode
activity["none"] = 1.0              # base BMR
activity["sedentary"] = 1.2         # desk job / little activity
activity["light"] = 1.375           # 15-30min activity daily
activity["moderate"] = 1.55
activity["fairly"] = 1.725
activity["very"] = 1.9

# persons starting stats (height in cm, weight in lb)
startheight = 170.18
startweight = 130
isMale = False
age = 19
active = activity["none"]

# rg = how many cals to go from tdee or limit, skip is how many to skip between estimations
rg, skp = 500, 100

# skip gain by setting to False, set limit to None to put a roof
doGain = False
limit = None

# loss & gain ranges.. as many as you want, in any order
losses = [125, 120, 115]
gains =  [135, 140, 145]

def updateTDEE(weight, mul=1.0):
    """Mifflin-St Jeor equation to calculate TDEE based on inputs"""
    if isMale:
        return ((10* (weight * 0.453592)) + (6.25 * startheight) - (5 * age) + 5) * mul
    else:
        return ((10* (weight * 0.453592)) + (6.25 * startheight) - (5 * age) - 161) * mul

def weightProjection(weight, tdee, mul, daily, goals, gainMode = False):
    """Project the days-until weight, based on defined goals"""
    cals, day = 0, 0
    goalDays = list()
    currentGoal = 0

    # ensure goals are increasing if gain mode
    if gainMode is True:
        goals = sorted(goals, reverse = False)
    else:
        goals = sorted(goals, reverse = True)
    
    # go until we get to the goal
    while weight != goals[-1]:
        if (abs(tdee - daily) < 25) or ((gainMode is True) and (daily < tdee)):
            print("∞ days - tdee & daily delta cannot be calculated")
            return

        # add to the day, and calc the cals
        day += 1
        cals = cals + (daily - tdee) if gainMode else (cals + (tdee - daily))

        # when our cals pass the lbs, add or subtract from weight
        if (cals > lb):
            weight = weight + 1 if gainMode else weight - 1
            tdee = updateTDEE(weight, mul)
            cals = cals - lb

            # if we pass a goal.. let the user know
            if (weight == goals[currentGoal]):
                goalDays.append(day)
                currentGoal += 1

    # add the last one
    goalDays.append(day)

    # find the date we will reach each goal
    goalDates = list()
    for goalDay in goalDays:
        goalDates.append(str(today + datetime.timedelta(days = goalDay)).split()[0])

    # print it all to the user
    for days, lbs, date in zip(goalDays, goals, goalDates):
        print(f"{days} days until {lbs}lbs, date: {date}")

def rounddown(x):
    """Returns the number, rounded down"""
    return int(math.floor(x / 100.0)) * 100

def main():
    # calc initial tdee
    starttdee = updateTDEE(startweight, active)

    # configure calorie-range barriers
    llow = (limit - rg) if limit != None else (rounddown(updateTDEE(startweight)) - rg)
    lhigh = limit if limit != None else rounddown(updateTDEE(startweight))
    glow = rounddown(updateTDEE(startweight)) + skp
    ghigh = rounddown(updateTDEE(startweight)) + rg
    alert = "\nWARNING: calories under 1200 can severely impact your health."

    # start calculating and displaying results
    print(f"Weight Projection; based on stats:")
    print(f"tdee = {starttdee}, activity = {[k for k, v in activity.items() if v == active][0]}, weight = {startweight}lbs, date = {str(today).split()[0]}")
    print()
    print("Calculating for loss --")
    for kcals in range(llow, lhigh, skp):
        print(f"Estimating at {kcals} cals per day... {alert if kcals < 1200 else '' }")
        weightProjection(weight = startweight, tdee = starttdee, mul = active, daily = kcals, goals = losses, gainMode = False)
        print()
    
    if not doGain:
        return

    print("Calculating for gain --")
    for kcals in range(glow, ghigh, skp):
        print(f"Estimating at {kcals} cals per day...")
        weightProjection(weight = startweight, tdee = starttdee, mul = active, daily = kcals, goals = gains, gainMode = True)
        print()

if __name__ == "__main__":
    main()