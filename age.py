# -*- coding: utf-8 -*-

import sys
import os

if len(sys.argv) == 1:
	os.system("result=$(date +%s); python ./my-script.py $result")
	exit(0)

age_sec = float(sys.argv[1])
death_sec = 2473257600

age = (age_sec - 43300800) / 31557600
print()
print("Today's age:          ", round(age, 10))
print("Day of my death:       2048 May 17 (assuming death @ 77)")
print("Must build AGI before: 2023 May 17 (assuming 25 years of tech diffusion)")
print()

secs_left = death_sec - age_sec
print("Total seconds left = ", int(secs_left))

days_left = secs_left / (24*60*60)
print("Total days left = ", round(days_left, 2))

years_left = days_left / 365.25
print("Total years left = ", round(years_left, 2))
print("Years left allowing for 25 years' AI diffusion = ", round(years_left - 25, 2))

print
# 17 May 2003 = 1053100800 = 32nd birthday
age32_sec = age_sec - 1053100800
age32_day = age32_sec / (24*60*60)
age32_year = age32_day / 365.25
print("Years elapsed since 32nd birthday = ", round(age32_year, 2))

print()

print("Counting from 32 birthday (2003 May 17),")
print("I have 45 years of life left = 16436 days")		# 16436.25 days
print("Minus 25 years of AI diffusion = 20 years")

print()

exit(0)

print("Remaining since 32nd birthday (2003 May 17):")
print("days of 16437")
print("weeks of 2348")
print("months of 539")
print("years of 45")
print("%")
print
print("Elapsed since 32nd birthday (2003 May 17):")
print("days of 16437")
print("weeks of 2348")
print("months of 539")
print("years of 45")
print("%")
print
print("Allowing for 25 years of AI diffusion")
print("25 years = 6631 days")
print
print("Remaining since 32nd birthday (2003 May 17):")
print("days of 16437")
print("weeks of 2348")
print("months of 539")
print("years of 45")
print("%")
print
print("Elapsed since 32nd birthday (2003 May 17):")
print("days of 16437")
print("weeks of 2348")
print("months of 539")
print("years of 45")
print("%")
print
