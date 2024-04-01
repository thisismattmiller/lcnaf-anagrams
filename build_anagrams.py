from sys import getsizeof
import string
import unicodedata
import re
import json
count = 0
all_names = {}
collisions = {}
collisions_full = {}

with open('personal_name_labels.nt') as infile:

	for line in infile:
		count = count + 1

		lccn = line.split('<http://www.loc.gov/mads/rdf/v1#authoritativeLabel>')[0].split('/')[-1].replace('>','')
		label = line.split('<http://www.loc.gov/mads/rdf/v1#authoritativeLabel>')[1]
		label = label[2:-4]
		norm = label.translate(str.maketrans('', '', string.punctuation))
		norm = unicodedata.normalize('NFKD', norm).encode('ascii', 'ignore').decode("utf-8")
		norm = norm.lower().replace(' ','')
		norm = ''.join(sorted(norm))

		try:
			s =  re.search(r"[a-z]", norm).start()
		except:
			print(norm)
			continue

		
		first_part = norm[:s]
		second_part = norm[s:]
		norm = second_part #+ first_part

		if norm not in all_names:
			all_names[norm] = count
		else:
			if norm not in collisions:
				collisions[norm] = []
				collisions_full[norm] = []


			# if label not in collisions_full[norm]:
			# 	collisions[norm].append(norm)
			# 	collisions_full[norm].append(label)


			nodates = ''.join([i for i in label if not i.isdigit()])
			nodates = nodates.translate(str.maketrans('', '', string.punctuation)).strip()
			if nodates not in collisions[norm]:
				collisions[norm].append(nodates)
				collisions_full[norm].append({'full':label,'lccn':lccn,'flat': unicodedata.normalize('NFKD', label).encode('ascii', 'ignore').decode("utf-8").lower()    })



all_anagrams = []
for n in collisions:
	if len(collisions[n]) >= 5:
		all_anagrams.append(collisions_full[n])

json.dump(all_anagrams,open('anagram_names.json','w'),indent=2)

