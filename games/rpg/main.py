import sys
import numpy as np
import random
from stats import Stats
from npc import NPC


a = NPC("Peter")
b = NPC("Paul")
a.level_to(99)
a.show_stats()
b.level_to(99)
print b.cure(9999)
b.show_stats()
