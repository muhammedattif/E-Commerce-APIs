# First Party Imports
from base.utility.choices import Languages


class Requests:
    @staticmethod
    def get_language_from_header(request):
        """parses header language"""
        header_lang = request.META.get("HTTP_CONTENT_LANGUAGE")
        if header_lang in Languages.values:
            return header_lang

        return None

    @classmethod
    def get_language(cls, request):
        """get language for account"""
        default_language = Languages.EN
        header_language = cls.get_language_from_header(request)
        if header_language:
            return header_language

        return default_language
