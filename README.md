# LanguageDetector
Language detector made without any language detection library (using cosine similarity on N-Grams)

Ldetect is the textual version to be executed on a console

it has 2 possible options:
'-f' : asks for a .txt file name as unique argument in order to evaluate its content
'-d' : Displays the scores of every supported language
Les deux options sont cumulables (-fd ou -df).

Executing Ldetect.py without any argument or with the --help option will display additional instructions

Ldetect_GUIver is a basic GUI version using tkinter

Results for long texts are good (obviously), short sentences can have incorrect evaluations

Training corpus was made with Universal Dependencies.
