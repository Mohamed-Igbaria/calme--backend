import nltk
import re
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt_tab')

from nltk import word_tokenize, pos_tag


#function 1 to check tense

def is_modal_future(tagged_tokens):
    """Check for modal + base verb combo"""
    for i, (word, tag) in enumerate(tagged_tokens[:-1]):
        if tag == 'MD' and tagged_tokens[i + 1][1] == 'VB':
            return True
    return False

#function 2 to check tense

def contains_future_time_expression(sentence):
    FUTURE_PHRASES = [
    r'\btomorrow\b',
    r'\bsoon\b',
    r'\blater\b',
    r'\bin the future\b',
    r'\bnext\s+(week|month|year|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
    r'\bby (tomorrow|[a-z]+day)\b'
    ]
    """Regex match future-related time expressions"""
    lowered = sentence.lower()
    return any(re.search(pattern, lowered) for pattern in FUTURE_PHRASES)

#function 3 to check tense
def tense_detect(tagged_sentence):

    verb_tags = ['MD','MDF',
                 'BE','BEG','BEN','BED','BEDZ','BEZ','BEM','BER',
                 'DO','DOD','DOZ',
                 'HV','HVG','HVN','HVD','HVZ',
                 'VB','VBG','VBN','VBD','VBZ',
                 'SH',
                 'TO',

                 'JJ' # maybe?
                 ]

    verb_phrase = []

    for item in tagged_sentence:
        if item[1] in verb_tags:
            verb_phrase.append(item)
    
    if not verb_phrase:
        return False
    
    # print("verb Phrases => " ,verb_phrase)

    grammar = r'''
            future perfect continuous passive:     {<MDF><HV><BEN><BEG><VBN|VBD>+}
            conditional perfect continuous passive:{<MD><HV><BEN><BEG><VBN|VBD>+}
            future continuous passive:             {<MDF><BE><BEG><VBN|VBD>+}   
            conditional continuous passive:        {<MD><BE><BEG><VBN|VBD>+}    
            future perfect continuous:             {<MDF><HV><BEN><VBG|HVG|BEG>+}   
            conditional perfect continuous:        {<MD><HV><BEN><VBG|HVG|BEG>+}
            past perfect continuous passive:       {<HVD><BEN><BEG><VBN|VBD>+}
            present perfect continuous passive:    {<HV|HVZ><BEN><BEG><VBN|VBD>+}
            future perfect passive:                {<MDF><HV><BEN><VBN|VBD>+}   
            conditional perfect passive:           {<MD><HV><BEN><VBN|VBD>+}    
            future continuous:                     {<MDF><BE><VBG|HVG|BEG>+ }   
            conditional continuous:                {<MD><BE><VBG|HVG|BEG>+  }   
            future indefinite passive:             {<MDF><BE><VBN|VBD>+ }
            conditional indefinite passive:        {<MD><BE><VBN|VBD>+  }
            future perfect:                        {<MDF><HV><HVN|BEN|VBN|VBD>+ }   
            conditional perfect:                   {<MD><HV><HVN|BEN|VBN|VBD>+  }   
            past continuous passive:               {<BED|BEDZ><BEG><VBN|VBD>+}  
            past perfect continuous:               {<HVD><BEN><HVG|BEG|VBG>+}   
            past perfect passive:                  {<HVD><BEN><VBN|VBD>+}
            present continuous passive:            {<BEM|BER|BEZ><BEG><VBN|VBD>+}   
            present perfect continuous:            {<HV|HVZ><BEN><VBG|BEG|HVG>+}    
            present perfect passive:               {<HV|HVZ><BEN><VBN|VBD>+}
            future indefinite:                     {<MDF><BE|DO|VB|HV>+ }       
            conditional indefinite:                {<MD><BE|DO|VB|HV>+  }   
            past continuous:                       {<BED|BEDZ><VBG|HVG|BEG>+}           
            past perfect:                          {<HVD><BEN|VBN|HVD|HVN>+}
            past indefinite passive:               {<BED|BEDZ><VBN|VBD>+}   
            present indefinite passive:            {<BEM|BER|BEZ><VBN|VBD>+}            
            present continuous:                    {<BEM|BER|BEZ><BEG|VBG|HVG>+}            
            present perfect:                       {<HV|HVZ><BEN|HVD|VBN|VBD>+  }       
            past indefinite:                       {<DOD><VB|HV|DO>|<BEDZ|BED|HVD|VBN|VBD>+}        
            infinitive:                            {<TO><BE|HV|VB>+}
            present indefinite:                    {<DO|DOZ><DO|HV|VB>+|<DO|HV|VB|BEZ|DOZ|BER|HVZ|BEM|VBZ>+}    
            '''

    cp = nltk.RegexpParser(grammar)
    result = cp.parse(verb_phrase)
    # print("RESULTS ==> ",result)    

    tenses_set = set()
    for node in result:
        if type(node) is nltk.tree.Tree:
            tenses_set.add(node.label())
    # print("tenses_set ====>   ", tenses_set)
    for future_tense_type in {"future","conditional","infinitive"}:
        for tense in tenses_set:
           if future_tense_type in tense:
                return True
            
    return False


def detect_futureAux(sentence):
    """Combine modal check + time phrase check"""
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)

    has_modal = is_modal_future(tagged)
    has_time = contains_future_time_expression(sentence)
    tense_detect_result = tense_detect(tagged)

    return {
        'modal_future': has_modal,
        'time_phrase': has_time,
        'tense_detect' : tense_detect_result,
        'is_future': has_modal or has_time or tense_detect_result
    }

def detect_future(sentence):
    return detect_futureAux(sentence)["is_future"]
