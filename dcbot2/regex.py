import re

proba = [".pti", "asd", "123"]
for p in proba:
	if re.search(r"\.[a-z]", p):
		print("Torolni kell {}".format(p))
	else:
		print("Nem kell torolni {}".format(p))