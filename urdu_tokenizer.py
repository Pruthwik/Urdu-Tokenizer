"""Tokenize Urdu at sentence and token level."""
import re
from string import punctuation


# the below code defines different kinds of regular expressions
token_specification = [
    ('datemonth',
     r'^(0?[1-9]|1[012])[-\/\.](0?[1-9]|[12][0-9]|3[01])[-\/\.](1|2)\d\d\d$'),
    ('monthdate',
     r'^(0?[1-9]|[12][0-9]|3[01])[-\/\.](0?[1-9]|1[012])[-\/\.](1|2)\d\d\d$'),
    ('yearmonth',
     r'^((1|2)\d\d\d)[-\/\.](0?[1-9]|1[012])[-\/\.](0?[1-9]|[12][0-9]|3[01])'),
    ('EMAIL1', r'([\w\.])+@(\w)+\.(com|org|co\.in)$'),
    ('url1', r'(www\.)([-a-z0-9]+\.)*([-a-z0-9]+.*)(\/[-a-z0-9]+)*/i'),
    ('url', r'/((?:https?\:\/\/|www\.)(?:[-a-z0-9]+\.)*[-a-z0-9]+.*)/i'),
    ('BRACKET', r'[\(\)\[\]\{\}]'),       # Brackets
    ('urdu_year', r'^(ء)(\d{4,4})'),
    ('NUMBER', r'^(\d+)([,\.٫٬]\d+)*(\w)*'),  # Integer or decimal number
    ('ASSIGN', r'[~:]'),          # Assignment operator
    ('END', r'[;!_]'),           # Statement terminator
    ('EQUAL', r'='),   # Equals
    ('OP', r'[+*\/\-]'),    # Arithmetic operators
    ('QUOTES', r'[\"\'‘’“”]'),          # quotes
    ('Fullstop', r'(\.+)$'),
    ('ellips', r'\.(\.)+'),
    ('HYPHEN', r'[-+\|+]'),
    ('Slashes', r'[\\\/]'),
    ('COMMA12', r'[,%]'),
    ('hin_stop', r'।'),
    ('urdu_stop', r'۔'),
    ('urdu_comma', r'،'),
    ('urdu_semicolon', r'؛'),
    ('urdu_question_mark', r'؟'),
    ('urdu_percent', r'٪'),
    ('quotes_question', r'[”\?]'),
    ('hashtag', r'#'),
    ('join', r'–')
]
# the below code converts the above expression into a python regex
tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
get_token = re.compile(tok_regex, re.U)
punctuations = punctuation + '\"\'‘’“”'


def word_tokenize(list_s):
    """Tokenize a list of tokens."""
    tkns = []
    for wrds in list_s:
        wrds_len = len(wrds)
        initial_pos = 0
        end_pos = 0
        while initial_pos <= (wrds_len - 1):
            mo = get_token.match(wrds, initial_pos)
            if mo is not None and len(mo.group(0)) == wrds_len:
                if mo.lastgroup == 'urdu_year':
                    tkns.append(wrds[: -4])
                    tkns.append(wrds[-4:])
                else:
                    tkns.append(wrds)
                initial_pos = wrds_len
            else:
                match_out = get_token.search(wrds, initial_pos)
                if match_out is not None:
                    end_pos = match_out.end()
                    if match_out.lastgroup == "NUMBER":
                        aa = wrds[initial_pos:(end_pos)]
                    else:
                        aa = wrds[initial_pos:(end_pos - 1)]
                    if aa != '':
                        tkns.append(aa)
                    if match_out.lastgroup != "NUMBER":
                        tkns.append(match_out.group(0))
                    initial_pos = end_pos
                else:
                    tkns.append(wrds[initial_pos:])
                    initial_pos = wrds_len
    return tkns


def sentence_tokenize_text(text):
    """Sentence and word tokenize a piece of text."""
    end_markers = ['؟', '!', '|', '۔']
    proper_sentences = []
    list_tokens = word_tokenize(text.split())
    end_sentence_markers = [index + 1 for index, token in enumerate(list_tokens) if token in end_markers]
    if len(end_sentence_markers) > 0:
        if end_sentence_markers[-1] != len(list_tokens):
            end_sentence_markers += [len(list_tokens)]
        end_sentence_markers_with_sentence_end_positions = [0] + end_sentence_markers
        sentence_boundaries = list(zip(end_sentence_markers_with_sentence_end_positions, end_sentence_markers_with_sentence_end_positions[1:]))
        for start, end in sentence_boundaries:
            individual_sentence = list_tokens[start: end]
            proper_sentences.append(' '.join(individual_sentence))
    else:
        proper_sentences.append(' '.join(list_tokens))
    return proper_sentences


def main():
    """Pass arguments and call functions here."""
    text = """
    نئی دہلی۔24مئی؛ وزیراعظم جناب نریندر مودی کی صدارت میں مرکزی کابینہ کو الیکٹرانکس اور اطلاعاتی ٹیکنالوجی کے شعبے میں دو طرفہ تعاون کو فروغ دینے کے لیے ہندوستان اور انگولا کے درمیان مفاہمت نامے سے مطلع کرایا گیا۔ اس مفاہمت نامے کا مقصد ای -حکمرانی، آئی ٹی تعلیم کے ایچ آر ڈی، اطلاعاتی تحفظ، الیکٹرانکس ہارڈوئیر مینو فیکچرنگ، آئی ٹی سے متعلق سافٹ وئیر صنعت، ٹیلی میڈیسن وغیرہ کے شعبوں میں قریبی تعاون کو فروغ دینا ہے۔ الیکٹرانکس اور اطلاعاتی ٹیکنالوجی کی وزارت کو دو طرفہ اور علاقائی تعاون فریم ورک کے تحت اطلاعاتی اور مواصلاتی ٹیکنالوجی (آئی سی ٹی) کے ابھرتے ہوئے اور آگے کے شعبو میں بین الاقوامی تعاون کو فروغ دینے کی ذمہ داری سونپی گئی ہے۔ اس وزارت نے آئی سی ٹی کے شعبے میں قریبی تعاون اور اطلاعات کے تبادلے کو فروغ دینے کی لیے مختلف ملکوں کی متعلقہ تنظیموں /ایجنسیوں کے ساتھ مفاہمت/ معاہدے کیے گئے۔
    """
    # to use this tokenizer in your program
    # do as per the following
    # from urdu_tokenizer import sentence_tokenize_text
    urdu_sentences = sentence_tokenize_text(text)
    print(urdu_sentences)
    print(len(urdu_sentences))


if __name__ == '__main__':
    main()
