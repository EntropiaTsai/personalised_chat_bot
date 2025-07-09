import langid 
from langid.langid import LanguageIdentifier, model
identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)

language_mapping = {
    "af": "Afrikaans",
    "am": "Amharic",
    "an": "Aragonese",
    "ar": "Arabic",
    "as": "Assamese",
    "az": "Azerbaijani",
    "be": "Belarusian",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "br": "Breton",
    "bs": "Bosnian",
    "ca": "Catalan",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "dz": "Dzongkha",
    "el": "Greek",
    "en": "English",
    "eo": "Esperanto",
    "es": "Spanish",
    "et": "Estonian",
    "eu": "Basque",
    "fa": "Persian",
    "fi": "Finnish",
    "fo": "Faroese",
    "fr": "French",
    "ga": "Irish",
    "gl": "Galician",
    "gu": "Gujarati",
    "he": "Hebrew",
    "hi": "Hindi",
    "hr": "Croatian",
    "ht": "Haitian Creole",
    "hu": "Hungarian",
    "hy": "Armenian",
    "id": "Indonesian",
    "is": "Icelandic",
    "it": "Italian",
    "ja": "Japanese",
    "jv": "Javanese",
    "ka": "Georgian",
    "kk": "Kazakh",
    "km": "Khmer",
    "kn": "Kannada",
    "ko": "Korean",
    "ku": "Kurdish",
    "ky": "Kyrgyz",
    "la": "Latin",
    "lb": "Luxembourgish",
    "lo": "Lao",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mg": "Malagasy",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mn": "Mongolian",
    "mr": "Marathi",
    "ms": "Malay",
    "mt": "Maltese",
    "nb": "Norwegian Bokmål",
    "ne": "Nepali",
    "nl": "Dutch",
    "nn": "Norwegian Nynorsk",
    "no": "Norwegian",
    "oc": "Occitan",
    "or": "Oriya",
    "pa": "Punjabi",
    "pl": "Polish",
    "ps": "Pashto",
    "pt": "Portuguese",
    "qu": "Quechua",
    "ro": "Romanian",
    "ru": "Russian",
    "sa": "Sanskrit",
    "sd": "Sindhi",
    "sh": "Serbo-Croatian",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovenian",
    "so": "Somali",
    "sq": "Albanian",
    "sr": "Serbian",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tl": "Tagalog",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "wa": "Walloon",
    "xh": "Xhosa",
    "zh": "Chinese",
    "zu": "Zulu"
}



def lang_detect(string):
    language_code, prob= identifier.classify(string)
    language = language_mapping[language_code]
    if language == "Chinese":
            language = determine_chinese_variant(string)
    return language

# 讀取 Unihan_Variants.txt 並建立簡繁對照表
simplified_set = set()
traditional_set = set()

with open("./Unihan_Variants.txt", encoding="utf-8") as f:
    for line in f:
        if line.startswith("U+") and "kSimplifiedVariant" in line:
            trad_code, _, simp_info = line.strip().partition("kSimplifiedVariant")
            trad_char = chr(int(trad_code.strip()[2:], 16))
            simplified_set.add(simp_info.split()[0].strip())  # 有些值可能有多個簡體，用第一個
            traditional_set.add(trad_char)
        elif line.startswith("U+") and "kTraditionalVariant" in line:
            simp_code, _, trad_info = line.strip().partition("kTraditionalVariant")
            simp_char = chr(int(simp_code.strip()[2:], 16))
            traditional_set.update(trad_info.strip().split())
            simplified_set.add(simp_char)

def determine_chinese_variant(text):
    simp_count = sum(1 for ch in text if ch in simplified_set)
    trad_count = sum(1 for ch in text if ch in traditional_set)
    
    if simp_count > trad_count:
        return "Simplified Chinese"
    else:
        return "Traditional Chinese"