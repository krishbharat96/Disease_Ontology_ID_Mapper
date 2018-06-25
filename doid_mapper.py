import pronto
import cStringIO
import urllib

do_slim_file = 'https://raw.githubusercontent.com/DiseaseOntology/HumanDiseaseOntology/master/src/ontology/doid-non-classified.obo'
do_link = 'https://sourceforge.net/p/diseaseontology/code/HEAD/tree/trunk/HumanDO.obo?format=raw'

def create_do_ontology(do_link):
    do_file = cStringIO.StringIO(urllib.urlopen(do_link).read())
    alternate_dict = dict()
    all_types_dicts = dict()
    do_ont = pronto.Ontology(do_file)
    for term in do_ont:
        term_id = term.id
        term_xrefs = []
        try:
            for alt_id in term.other['xref']:
                term_xrefs.append(alt_id)
        except:
            term_xrefs = []
        alternate_dict.update({term_id:term_xrefs})
        for xref in term_xrefs:
            term_type = xref.split(":")[0]
            if not term_type in all_types_dicts.keys():
                all_types_dicts.update({term_type:{}})
            all_types_dicts[term_type].update({xref:term_id})

    do_ont_2 = pronto.Ontology(do_slim_file)
    for term in do_ont_2:
        term_id = term.id
        term_xrefs = []
        try:
            for alt_id in term.other['xref']:
                term_xrefs.append(alt_id)
        except:
            term_xrefs = []
        if not term_id in alternate_dict.keys():
            alternate_dict.update({term_id:term_xrefs})
        else:
            old_arr = alternate_dict[term_id]
            new_arr = list(set(old_arr + term_xrefs))
            alternate_dict[term_id] = new_arr

            for xref in new_arr:
                term_type = xref.split(":")[0]
                if not term_type in all_types_dicts.keys():
                    all_types_dicts.update({term_type:{}})
                all_types_dicts[term_type].update({xref:term_id})            
    print "Dictionaries created!"
    return alternate_dict, all_types_dicts
    
def create_slim_do_ontology(do_slim_file):
    alternate_dict = dict()
    all_types_dicts = dict()
    do_ont = pronto.Ontology(do_slim_file)
    for term in do_ont:
        term_id = term.id
        term_xrefs = []
        try:
            for alt_id in term.other['xref']:
                term_xrefs.append(alt_id)
        except:
            term_xrefs = []
        alternate_dict.update({term_id:term_xrefs})
        for xref in term_xrefs:
            term_type = xref.split(":")[0]
            if not term_type in all_types_dicts.keys():
                all_types_dicts.update({term_type:{}})
            all_types_dicts[term_type].update({xref:term_id})
    print "Dictionaries created!"
    return alternate_dict, all_types_dicts

def get_snomed(keys):
    for k in keys:
        if 'SNOMEDCT_US' in k:
            return k
        
def get_id_alternate(dicts, id_type, act_id):
    alternate_dict = dicts[1]
    if id_type == 'SNOMEDCT_US' or id_type == 'SNOMEDCT':
        old_id_type = id_type + ":"
        id_type = get_snomed(alternate_dict.keys())
        act_id = act_id.replace(old_id_type, '')
    if not id_type in alternate_dict.keys():
        print "Specified Id Type does not exist in Disease Ontology"
        return None
    else:
        original_id = act_id
        if not id_type in original_id:
            original_id = id_type + ":" + act_id
        if not original_id in alternate_dict[id_type].keys():
            print "Id not found within Disease Ontology"
            return None
        else:
            return alternate_dict[id_type][original_id]

def get_all_alternate_ids(dicts, doid):
    all_alternate_ids = dicts[0]
    original_id = doid
    if not 'DOID:' in doid and not doid.isdigit():
        print "Not a valid DOID"
        return None
    else:
        if not 'DOID:' in doid:
            original_id = "DOID:" + doid
        if not original_id in all_alternate_ids.keys():
            print "DOID does not exist"
            return None
        else:
            return all_alternate_ids[original_id]

def auto_get_doid(id_type, act_id):
    dicts = create_do_ontology(do_link)
    return get_id_alternate(dicts, id_type, act_id)

def auto_get_alternate_ids(doid):
    dicts = create_do_ontology(do_link)
    return get_all_alternate_ids(dicts, doid)
