from translate import Translator
translator= Translator(from_lang="english",to_lang="russian")
translation = translator.translate("apple")
print(translation)