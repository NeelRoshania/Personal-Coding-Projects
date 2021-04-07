from google.cloud import language_v1
from google.cloud.language_v1 import enums
import os


################################################################################################################################
# Description
################################################################################################################################

# documentSentiment contains the overall sentiment of the document, which consists of the following fields:
# score of the sentiment ranges between -1.0 (negative) and 1.0 (positive) and corresponds to the overall emotional leaning of the text.
# magnitude indicates the overall strength of emotion (both positive and negative) within the given text, between 0.0 and +inf. Unlike score, magnitude is not normalized; each expression of emotion within the text (both positive and negative) contributes to the text's magnitude (so longer text blocks may have greater magnitudes).

# magnitude describes the degree to which the sentiment score expressed i.e the emotional weight of the sentiment score

# Sentiment	            Sample Values
# Clearly Positive*	    "score":    0.8, "magnitude":   3.0
# Clearly Negative*	    "score":   -0.6, "magnitude":   4.0
# Neutral	            "score":    0.1, "magnitude":   0.0
# Mixed	                "score":    0.0, "magnitude":   4.0

# Source: https://cloud.google.com/natural-language/docs/basics#interpreting_sentiment_analysis_values

################################################################################################################################
# Functions
################################################################################################################################

def sample_analyze_sentiment(text_content):
    """
    Analyzing Sentiment in a String

    Args:
      text_content The text content to analyze
    """

    # installtion
    #   - pip3 install google-cloud-language
    #   - Enable Google Cloud Natural Language API

    # credential_path = "/home/nroshania/Personal-Coding-Projects/COVID19/private/covid19-2020-0fb8513fcbd8.json"
    # credential_path = "C:\\Users\\nrosh\\Desktop\\Personal Coding Projects\\COVID19\\private\\covid19-2020-0fb8513fcbd8.json"
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    client = language_v1.LanguageServiceClient()

    # text_content = 'I am so happy and joyful.'

    # Available types: PLAIN_TEXT, HTML
    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages

    document = {
        "content": text_content,
        "type": type_,
        "language": language
    }

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = enums.EncodingType.UTF8

    return client.analyze_sentiment(document, encoding_type=encoding_type)


################################################################################################################################
# Usage
################################################################################################################################

# response = sample_analyze_sentiment("As Match Breaks Away, Investors Shouldn’t Break Up")

# # Get overall sentiment of the input document
# print(u"Document sentiment score: {}".format(response.document_sentiment.score))
# print(
#     u"Document sentiment magnitude: {}".format(
#         response.document_sentiment.magnitude
#     )
# )

# # Get sentiment for all sentences in the document
# for sentence in response.sentences:
#     print(u"Sentence text: {}".format(sentence.text.content))
#     print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
#     print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))

# # Get the language of the text, which will be the same as
# # the language specified in the request or, if not specified,
# # the automatically-detected language.
# print(u"Language of the text: {}".format(response.language))
