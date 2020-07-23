# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 23:30:18 2020

@author: buruzaemon
"""
import os
import spacy

from os import path
from spacy.lang.char_classes import ALPHA, \
                                    ALPHA_LOWER, \
                                    ALPHA_UPPER, \
                                    CONCAT_QUOTES, \
                                    HYPHENS, \
                                    LIST_ELLIPSES, \
                                    LIST_ICONS
from spacy.util import compile_infix_regex


def main(new_model_names, orig_model_names):

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

    for new_model,orig_model in zip(new_model_names, orig_model_names):
        nlp = spacy.load(orig_model)
        nlp.tokenizer.infix_finditer = infix_re.finditer

        outdir = path.join(os.getcwd(), new_model)
        nlp.to_disk(outdir)


if __name__ == "__main__":
    new_model_names = ['en_foobar_sm_base']
    orig_model_names = ['en_core_web_sm']
    main(new_model_names, orig_model_names)
