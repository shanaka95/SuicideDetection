# -*- coding: utf-8 -*-
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "PATH_TO_YOUR_GOOGLEAPI_JSON_FILE"
def get_values(text):
    client = language.LanguageServiceClient()
    text = u'''%s'''%(text)
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    sentiment = client.analyze_sentiment(document=document).document_sentiment

    return sentiment.score, sentiment.magnitude
