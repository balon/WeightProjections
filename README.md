## WeightProjections
A simple python script that projects the expected date to reach weight loss/gain goals... estimated using the Mifflin-St Jeon equation to automatically adjust TDEE. *This was a small project to help with personal goals and to help a friend struggling with their weight estimate safe calorie values to eat daily.*


### Disclaimer & Warning
This is a tool based on a mathematical equation (*Mifflin-St Jeon*), and **should not be used in replacement of medical advice** from a medical professional. The tool will estimate the amount of time it would take (in days) to reach certain weight goals, given you eat at the calories in the projection. There is no bottom-limit, so if you configure the settings to go below 1200, it will calculate that low and display a warning about the potential adverse health impact.

*All base statistics & goals provided in .py file were approved to be released by a friend who helped me in testing.*


#### Configuration:
Everything for configuration is at the top of the file. The `lb` variable defines that 1 lb of fat is equal to 3500 calories. The `activity` variable defines the different multiplier used in most TDEE calculators. The variables you must update to run the script:
```python3
# persons starting stats (height in cm, weight in lb)
startheight = 100.00          # height in cm.. as a float
startweight = 100             # weight in lbs.. as a int/float
isMale = False                # sex, defined by False if Female, or True if Male
age = 100                     # age in years.. as an int
active = activity["none"]

# rg = how many cals to go from bmr or limit, skip is how many to skip between estimations
rg, skp = 500, 100

# skip gain by setting to False, set limit to None to put a roof
doGain = False                # set this variable to False to skip the 'gain' portion
limit = None                  # if high weight, you may want to set this to a val (say if with bmr + activity your tdee is 6500.. the ranges go off this #)
# limit = 2500                # for example, if your TDEE is 5000, but want to eat at max 3000 cal per day and see estimates down to 2500, with a range of 100 per

# loss & gain ranges.. as many as you want, in any order
losses = [125, 120, 115]      # goals going down from your weight... say we start at 150... 140, 130, 120
gains =  [135, 140, 145]      # goals going up from your weight... say we start at 100... 110, 120, 130
```
