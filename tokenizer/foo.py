# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 23:30:18 2020

@author: buruzaemon
"""
import spacy
from spacy.lang.char_classes import ALPHA, \
                                    ALPHA_LOWER, \
                                    ALPHA_UPPER, \
                                    CONCAT_QUOTES, \
                                    HYPHENS, \
                                    LIST_ELLIPSES, \
                                    LIST_ICONS
from spacy.util import compile_infix_regex

# default tokenizer
nlp = spacy.load("en_core_web_sm")

#txt = "mother-in-law"
txt = "Foobar Inc. (8895.T)(BUY) is a winner. IOW, (8895 JP)(Buy)!"

doc = nlp(txt)
print([t.text for t in doc]) # ['mother', '-', 'in', '-', 'law']

# modify tokenizer infix patterns
infixes = (
    LIST_ELLIPSES
    + LIST_ICONS
    + [
        r"(?<=[0-9])[+\-\*^](?=[0-9-])",
        r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
            al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
        ),
        r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
        r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
        r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
        # handle infix of )(
        r"(?<=[{a}0-9])(\))".format(a=ALPHA),
        r"(\()(?=[{a}0-9])".format(a=ALPHA),
    ]
)

infix_re = compile_infix_regex(infixes)
nlp.tokenizer.infix_finditer = infix_re.finditer


doc = nlp(txt)
print([t.text for t in doc]) # ['mother-in-law']