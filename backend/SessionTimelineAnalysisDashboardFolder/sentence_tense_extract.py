import nltk
import re
# nltk.download('averaged_perceptron_tagger_eng')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt_tab')
# nltk.help.upenn_tagset()  # shows all tags

from nltk import word_tokenize, pos_tag


# Set of future-related time keywords


def is_modal_future(tagged_tokens):
    """Check for modal + base verb combo"""
    for i, (word, tag) in enumerate(tagged_tokens[:-1]):
        if tag == 'MD' and tagged_tokens[i + 1][1] == 'VB':
            return True
    return False

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
        # print("non-verb-sentence")
        return
    
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
    # return result, tenses_set

def detect_futureAux(sentence):
    """Combine modal check + time phrase check"""
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)

    has_modal = is_modal_future(tagged)
    has_time = contains_future_time_expression(sentence)
    tense_detect_result = tense_detect(tagged)

    # has_modal = True
    # has_time = True
    # tense_detect_result = True

    return {
        'modal_future': has_modal,
        'time_phrase': has_time,
        'tense_detect' : tense_detect_result,
        'is_future': has_modal or has_time or tense_detect_result
    }

def detect_future(sentence):
    return detect_futureAux(sentence)["is_future"]

def testInput(sentence):
    tags = pos_tag(word_tokenize(sentence))
    result= tense_detect(tags)
    result2 = contains_future_time_expression(sentence)
    result3 = is_modal_future(tags)
    result4 = detect_future(sentence)
    # print("-------------------------------------tense_detect---------------------------------------------")
    # print(result)
    # print("-------------------------------------contains_future_time_expression---------------------------------------------")
    # print(result2)
    # print("-------------------------------------is_modal_future---------------------------------------------")
    # print(result3)
    print("-------------------------------------detect_future---------------------------------------------")
    print(result4)
    print()
    print()



sentence1 = "I am going to do that tomorrow"
sentence2 = "I might do it"
sentence3 = "I will do that"
sentence4 = "I am thinking of trying a new thing next week"
sentence5 = "ok, next week"

# testInput(sentence1)
# testInput(sentence2)
# testInput(sentence3)
# testInput(sentence4)
# testInput(sentence5)