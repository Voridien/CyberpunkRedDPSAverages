import random
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog

Weapons = {
    "MediumPistol": [2, 2, 12],
    "HeavyPistol": [3, 2, 8],
    "VeryHeavyPistol": [4, 1, 8],
    "SMG": [2, 1, 30],
    "HeavySMG": [3, 1, 40],
    "AssaultRifle": [5, 1, 25],
    "SniperRifle": [5, 1, 4],
    "BowAndCrossbow": [4, 1, 9999]
}

averages = {}

#reflexes = 8
#weaponSkill = 6
DV = {
    "MediumPistol": [13, 15, 20, 25, 30, 30, 9999, 9999],
    "HeavyPistol": [13, 15, 20, 25, 30, 30, 9999, 9999],
    "VeryHeavyPistol": [13, 15, 20, 25, 30, 30, 9999, 9999],
    "SMG": [15, 13, 15, 20, 25, 25, 30, 9999],
    "HeavySMG": [15, 13, 15, 20, 25, 25, 30, 9999],
    "AssaultRifle": [17, 16, 15, 13, 15, 20, 25, 30],
    "SniperRifle": [30, 25, 25, 20, 15, 16, 17, 20],
    "BowAndCrossbow": [15,13,15,17,20,22,9999,9999]
}

runs = 10000

def getWeapon(getWeaponType):
    if getWeaponType == "MediumPistol":
        return 0
    elif getWeaponType == "HeavyPistol":
        return 1
    elif getWeaponType == "VeryHeavyPistol":
        return 2
    elif getWeaponType == "SMG":
        return 3
    elif getWeaponType == "HeavySMG":
        return 4
    elif getWeaponType == "AssaultRifle":
        return 5
    elif getWeaponType == "SniperRifle":
        return 6
    elif getWeaponType == "BowAndCrossbow":
        return 7

def run(weaponType, weaponRange):
    defence = DV[weaponType][weaponRange]
    tempArmor = armor
    damageTotal = 0
    total_critical_injuries = 0
    total_attacks = 0  # Initialize total attacks
    successful_attacks = 0  # Initialize successful attacks
    clipSize = Weapons[weaponType][2]
    currentClip = clipSize
    for j in range(turns):
        canCrit = True
        shouldCrit = False
        #print("weapon: " + weaponType + ", Range: " + str(weaponRange) + ", armor: " + str(tempArmor) + ", attacks/total: " + str(successful_attacks) + "/" + str(total_attacks) + ", damage: " + str(damageTotal) + ", criticals: " + str(total_critical_injuries) + ", clip: " + str(currentClip))
        critical_injuries = 0  # Initialize the critical injuries for this run
        if currentClip <= Weapons[weaponType][1]:
            currentClip = clipSize
            continue
        for i in range(Weapons[weaponType][1]):
            shouldCrit = False
            canCrit = True
            total_attacks += 1  # Increment total attacks
            currentClip -= 1
            hitRoll = random.randint(1, 10)
            if hitRoll == 10:
                hitRoll += random.randint(1, 10)
            elif hitRoll == 1:
                hitRoll -= random.randint(1, 10)
            attack = reflexes + weaponSkill + hitRoll
            damage = 0
            critical_injury = False
            if attack > defence:
                successful_attacks += 1  # Increment successful attacks
                for k in range(Weapons[weaponType][0]):
                    damage_roll = random.randint(1, 6)
                    damage += damage_roll
                    if damage_roll == 6:
                        # Check for critical injury
                        if critical_injury:
                            shouldCrit = True
                            critical_injury = False
                        else:
                            critical_injury = True
                if tempArmor > 0:
                    damage -= tempArmor
                    if damage > 0:
                        tempArmor -= 1
                    if damage < 0:
                        damage = 0
                if shouldCrit and canCrit:
                    critical_injuries += 1
                    damage += 5  # Critical injury deals 5 damage directly
                    canCrit = False
            damageTotal += damage
        total_critical_injuries += critical_injuries  # Accumulate the critical injuries for all attacks in this run
    # Calculate accuracy as the percentage of successful attacks
    accuracy = (successful_attacks / total_attacks) * 100
    return damageTotal, total_critical_injuries, accuracy  # Return accuracy in addition to other values

root = tk.Tk()
root.withdraw()  # Hide the main window

# Set default values
default_armor = 11
default_turns = 1
default_reflexes = 8
default_weapon_skill = 6

# Create labels and defaults for input
labels = ["Enemy Armor:", "Turns in Battle:", "Your Reflexes:", "Your Weapon Skill:"]
defaults = [default_armor, default_turns, default_reflexes, default_weapon_skill]

# Collect user input for armor, turns, reflexes, and weapon skill
values = []
for label, default in zip(labels, defaults):
    value = simpledialog.askinteger("Input", label, initialvalue=default)
    values.append(value)

# Now you have the values in the variables armor, turns, reflexes, and weaponSkill
armor, turns, reflexes, weaponSkill = values

print(f"Enemy Armor: {armor}")
print(f"Turns in Battle: {turns}")
print(f"Your Reflexes: {reflexes}")
print(f"Your Weapon Skill: {weaponSkill}")

for theWeaponType in Weapons:
    weapon_results = []
    for theWeaponRange in range(len(DV)):
        total_damage = 0
        weapon_total_critical_injuries = 0
        total_accuracy = 0  # Initialize total accuracy
        for _ in range(runs):
            damage, critical_injuries, accuracy = run(theWeaponType, theWeaponRange)
            total_damage += damage
            weapon_total_critical_injuries += critical_injuries
            total_accuracy += accuracy  # Accumulate accuracy
        average_damage = total_damage / runs
        average_critical_injuries = weapon_total_critical_injuries / runs
        average_accuracy = total_accuracy / runs  # Calculate average accuracy
        weapon_results.append((average_damage, average_critical_injuries, average_accuracy))
    averages[theWeaponType] = weapon_results

for anotherWeaponType, weapon_results in averages.items():
    for l, (average_damage, average_critical_injuries, average_accuracy) in enumerate(weapon_results):
        print(f"{anotherWeaponType} - Range {l} - Average Damage: {average_damage:.2f} - Average Critical Injuries: {average_critical_injuries:.2f} - Average Accuracy: {average_accuracy:.2f}%")

# Create lists to store data for the graph
x_values = []  # Labels for x-axis (e.g., weapon names)

average_damage_values = []  # Average damage values
average_critical_injuries_values = []  # Average critical injuries values
average_accuracy_values = []  # Average accuracy values

# Populate the lists with data from your "averages" dictionary
for moreWeaponType, weapon_results in averages.items():
    for m, (average_damage, average_critical_injuries, average_accuracy) in enumerate(weapon_results):
        x_values.append(f"{moreWeaponType} - Range {m}")
        average_damage_values.append(average_damage)
        average_critical_injuries_values.append(average_critical_injuries)
        average_accuracy_values.append(average_accuracy)

# Create a figure with one row and three subplots
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6))

# Subplot 1: Average Damage
ax1.bar(x_values, average_damage_values, label="Average Damage")
ax1.set_xlabel("Weapons and Ranges")
ax1.set_ylabel("Average Values")
ax1.legend()
ax1.tick_params(axis='x', rotation=90)

# Subplot 2: Average Accuracy
ax2.bar(x_values, average_accuracy_values, label="Average Accuracy")
ax2.set_xlabel("Weapons and Ranges")
ax2.set_ylabel("Average Accuracy (%)")
ax2.legend()
ax2.tick_params(axis='x', rotation=90)

# Subplot 3: Average Critical Injuries
ax3.bar(x_values, average_critical_injuries_values, label="Average Critical Injuries")
ax3.set_xlabel("Weapons and Ranges")
ax3.set_ylabel("Average Values")
ax3.legend()
ax3.tick_params(axis='x', rotation=90)

ax1.yaxis.grid(color='gray', linestyle='--', linewidth=0.5)
ax2.yaxis.grid(color='gray', linestyle='--', linewidth=0.5)
ax3.yaxis.grid(color='gray', linestyle='--', linewidth=0.5)

# Ensure labels fit within the figure boundaries
plt.tight_layout()

# Show the graph
plt.show()