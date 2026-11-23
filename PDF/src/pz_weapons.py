"""Weapons & Combat Equipment design sheet (user-supplied, 19 Nov 2026) → per-item concept crops + specs.
Crop boxes are pixel regions of the 1536×1024 source sheet."""
import os
from PIL import Image

SRC = r"D:\Project Zero_Roblox\Project Zero_ Nexus-01 Equipment Sheets.png"
ROOT = r"D:\Project Zero_Roblox\Project_Zero_Production_Bible"

# id, name, class, crop box, size studs (design assumption), energy cell, role, signature, meshy core
WEAPONS = [
 ("EQP-03", "ARC-7 Plasma Pulse Rifle", "Ranged", (5, 92, 378, 300), "4.6 long", "E-40", "Standard issue; stable, versatile", "orange/white body, twin cyan coil banks", "plasma pulse rifle, white and graphite body, orange accents, cyan coil chambers"),
 ("EQP-13", "VOLT-X Energy Carbine", "Ranged", (385, 92, 752, 300), "3.8 long", "E-20", "Lightweight, high mobility", "compact carbine, long scope", "compact energy carbine, scope, white graphite orange, cyan energy cell"),
 ("EQP-14", "THUNDER-9 Heavy Ion Cannon", "Ranged (heavy)", (758, 92, 1148, 300), "5.8 long", "E-100", "Heavy damage, armour penetration", "large cyan ion chamber, front ring muzzle", "heavy ion cannon, large glowing cyan core chamber, ring muzzle, orange white armor"),
 ("EQP-15", "NOVA-3 Precision Energy Rifle", "Ranged (long)", (1153, 92, 1533, 300), "6.0 long", "E-60", "Long range, high accuracy", "long barrel, big scope, cyan muzzle lens", "precision energy sniper rifle, long barrel, large scope, cyan lens, white graphite orange"),
 ("EQP-02", "PHOTON EDGE Energy Sword", "Melee", (5, 340, 390, 537), "4.6 long", "E-10", "Fast and precise", "cyan hard-light blade, orange guard", "energy sword, glowing cyan blade, graphite and orange hilt"),
 ("EQP-16", "TITAN BREAKER Heavy Hammer", "Melee (heavy)", (395, 340, 767, 537), "5.6 long", "E-50", "High impact, crowd control", "cyan-cored hammer head, long haft", "sci-fi heavy war hammer, armored head with cyan core, long graphite haft, orange bands"),
 ("EQP-17", "ARC CLAWS Retractable Blades", "Melee (wrist)", (772, 340, 1152, 537), "1.8 long (×2)", "E-15", "Wrist-mounted, retractable", "three cyan blades per gauntlet", "wrist mounted retractable energy claws, three glowing cyan blades, graphite gauntlet"),
 ("EQP-18", "SHOCK STAFF Electro-Energy Staff", "Melee (control)", (1158, 340, 1533, 537), "7.0 long", "E-30", "Non-lethal; stun and disable", "twin cyan emitter heads, segmented shaft", "electro energy staff, two glowing cyan emitter ends, segmented graphite shaft, orange rings"),
 ("EQP-06", "AEGIS-S1 Deployable Energy Shield", "Defensive", (5, 572, 422, 765), "6.0 tall deployed", "E-25", "Personal shield; absorbs energy fire", "tripod emitter + hex hard-light wall", "deployable energy shield emitter on tripod, glowing hexagonal cyan barrier"),
 ("EQP-19", "BASTION-X Heavy Riot Shield", "Defensive", (428, 572, 832, 765), "4.5 tall", "none", "Physical protection, impact resistant", "white armoured slab, cyan visor slot, gear emblem", "heavy riot shield, white armored plates, cyan visor slit, orange gear emblem"),
 ("EQP-20", "DOME-4 Portable Shield Projector", "Defensive (area)", (838, 572, 1232, 765), "2.5 wide (dome r 8)", "E-80", "Projects an area energy dome", "four-legged puck with cyan top ring", "portable shield projector drone puck on four legs, cyan ring emitter"),
 ("EQP-21", "EMP-6 Disruption Launcher", "Specialised", (5, 797, 250, 1002), "4.0 long", "E-40", "Disables electronics (temporary)", "fat barrel with cyan ring muzzle", "EMP disruption launcher, wide ring muzzle, cyan glow, orange white body"),
 ("EQP-22", "GRAVITY-8 Gravity Manipulator", "Specialised", (255, 797, 488, 1002), "4.0 long", "E-60", "Move / lift objects; combat utility", "ring emitter with orange halo", "gravity manipulator gun, large ring emitter with cyan core, orange halo"),
 ("EQP-23", "PULSE-MINE Disruption Device", "Specialised", (493, 797, 727, 1002), "1.5 wide", "E-20", "Area disable (EMP); proximity trigger", "hexapod low-profile puck", "flat hexagonal proximity mine, six legs, cyan centre light"),
 ("EQP-24", "OVERDRIVE CORE Combat Module", "Specialised", (732, 797, 978, 1002), "1.2 tall", "self", "Temporary boost; plug-in module", "caged cyan canister", "combat enhancement core canister, glowing cyan column, orange cage"),
 ("EQP-25", "SENTINEL DRONE Defensive Support", "Specialised", (985, 797, 1238, 1002), "3.0 wide", "E-40", "Auto defence, mini shield, recon", "quad-rotor with cyan eye", "defensive support drone, four rotors, central cyan eye, white graphite orange"),
 ("EQP-07", "Energy Cell System (E-10 … E-100)", "Power", (1243, 778, 1533, 1002), "0.6 – 1.5 tall", "—", "Unified swappable cells across all weapons", "six capacities, cyan columns", "energy cell canisters set, six sizes, glowing cyan columns, orange caps"),
]

def crops():
    im = Image.open(SRC).convert("RGB")
    out = {}
    for w in WEAPONS:
        aid, box = w[0], w[3]
        d = os.path.join(ROOT, "Equipment", aid); os.makedirs(d, exist_ok=True)
        c = im.crop(box); c = c.resize((c.width * 3, c.height * 3), Image.LANCZOS)
        p = os.path.join(d, "concept_crop.png"); c.save(p); out[aid] = p
    return out

BY_ID = {w[0]: w for w in WEAPONS}

if __name__ == "__main__":
    print(len(crops()), "crops")
