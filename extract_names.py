


with open('names.madsrdf.nt') as infile:

	current = None
	dates = []
	types = []
	
	label = ""
	for line in infile:

		if '# BEGIN' in line:
			current = line.split('/')[-1].strip()
			dates = []
			types = []
			label = ""
		
		if len(current) < 5:
			current = "NONONONONONONOON"


		if '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>' in line and current in line:
			rdftype = line.split("> <")[2].replace('> .','').strip()
			types.append(rdftype)


		if '<http://www.loc.gov/mads/rdf/v1#authoritativeLabel>' in line and current in line:
			label = line




			
		if '<http://id.loc.gov/ontologies/RecordInfo#recordChangeDate>' in line:
			dates.append(line.split("> ")[1].split("^^")[0].replace('"',''))

		if '# END' in line:

			created = sorted(dates)[0]
			if len(types) > 0:
				if 'http://www.loc.gov/mads/rdf/v1#PersonalName' in types or 'http://www.loc.gov/mads/rdf/v1#CorporateName' in types:
					# print(created, types)
					if label.strip() != '':
						print(label.strip())

