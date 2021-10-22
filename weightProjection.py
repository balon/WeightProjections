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

# range of calories to approximate and how many to skip between
rg, skp = 500, 100

# skip gain by setting to True, set limit to None to ignore
doGain = True
limit = None

# loss & gain ranges
low, lower, lowest = 125, 120, 115
high, higher, highest =  135, 140, 145

def updateBMR(weight, mul=1.0):
    """Mifflin-St Jeor equation to calculate BMR based on inputs"""
    if isMale:
        return ((10* (weight * 0.453592)) + (6.25 * startheight) - (5 * age) + 5) * mul
    else:
        return ((10* (weight * 0.453592)) + (6.25 * startheight) - (5 * age) - 161) * mul

def weightLoss(weight, bmr, mul, daily):
    dangerCheck = False
    warnCheck = False
    deficit = 0
    day = 0
    warning = 0
    danger = 0

    while weight != lowest:
        if (abs(bmr - daily) < 25):
            print("∞ days - the difference of bmr & daily is too small")
            return

        day += 1
        deficit = deficit + (bmr - daily)

        if (deficit > lb):
            weight -= 1
            bmr = updateBMR(weight, mul)
            deficit = deficit - lb

            if (weight == low) and (warnCheck is False):
                warnCheck = True      
            if (weight == lower) and (dangerCheck is False):
                dangerCheck = True
        
        if weight == low:
            warning = day
        if weight == lower:
            danger = day

    warnDate = today + datetime.timedelta(days = warning)
    badDate = today + datetime.timedelta(days = day)
    dangerDate = today + datetime.timedelta(days = danger)

    print(f"{warning} days until {low}lbs, date: {warnDate}")
    print(f"{danger} days until {lower}lbs, date: {dangerDate}")
    print(f"{day} days until {lowest}lbs, date: {badDate}")

def weightGain(weight, bmr, mul, daily):
    dangerCheck = False
    warnCheck = False
    surplus = 0
    day = 0
    warning = 0
    danger = 0

    while weight != highest:
        if (abs(bmr - daily) < 25) or (daily < bmr):
            print("∞ days - the difference of bmr & daily is too small to calculate")
            return

        day += 1
        surplus = surplus + (daily - bmr)

        if (surplus > lb):
            weight += 1
            bmr = updateBMR(weight, mul)
            surplus = surplus - lb

            if (weight == high) and (warnCheck is False):
                warnCheck = True
            if (weight == higher) and (dangerCheck is False):
                dangerCheck = True
        
        if weight == high:
            warning = day
        if weight == higher:
            danger = day

    warnDate = today + datetime.timedelta(days = warning)
    badDate = today + datetime.timedelta(days = day)
    dangerDate = today + datetime.timedelta(days = danger)

    print(f"{warning} days until {high}lbs, date: {warnDate}")
    print(f"{danger} days until {higher}lbs, date: {dangerDate}")
    print(f"{day} days until {highest}lbs, date: {badDate}")

def rounddown(x):
    return int(math.floor(x / 100.0)) * 100

def main():
    # calc initial bmr
    startbmr = updateBMR(startweight, active)

    # configure calorie-range barriers
    llow = (limit - rg) if limit != None else (rounddown(updateBMR(startweight)) - rg)
    lhigh = limit if limit != None else rounddown(updateBMR(startweight))
    glow = rounddown(updateBMR(startweight)) + skp
    ghigh = rounddown(updateBMR(startweight)) + rg
    alert = "\nWARNING: calories under 1200 can severely impact your health."

    print(f"Weight Projection; based on stats:")
    print(f"bmr = {startbmr}, activity = {[k for k, v in activity.items() if v == active][0]}, weight = {startweight}lbs, date = {str(today).split()[0]}")
    print()
    print("Calculating for loss --")
    for cals in range(llow, lhigh, skp):
        print(f"Estimating at {cals} per day... {alert if cals < 1000 else '' }")
        weightLoss(weight = startweight, bmr = startbmr, mul = active, daily = cals)
        print()
    
    if not doGain:
        return

    print("Calculating for gain --")
    for cals in range(glow, ghigh, skp):
        print(f"Estimating at {cals} per day...")
        weightGain(weight = startweight, bmr = startbmr, mul = active, daily = cals)
        print()

if __name__ == "__main__":
    main()