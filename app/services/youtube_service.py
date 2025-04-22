import re
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
from youtube_transcript_api.formatters import TextFormatter
from pyfreeproxies import proxies

class YouTubeService:
    YOUTUBE_URL_PATTERN = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'

    @staticmethod
    def extract_video_id(url):
        match = re.search(YouTubeService.YOUTUBE_URL_PATTERN, url, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def get_transcript(video_id, progress=None, lang=None):
        """
        Try to fetch transcript without proxy first, then with proxies if needed.
        Optionally update progress tracker if provided.
        """
        # Try without proxy
        try:
            if progress and lang:
                progress.update(
                    45,
                    lang.get("fetching_transcript", "Fetching transcript...")
                    + lang.get("no_proxy", "")
                )
            session = requests.Session()
            ytt_api = YouTubeTranscriptApi(http_client=session)
            transcript_list = ytt_api.list(video_id)
            transcript = transcript_list._generated_transcripts[list(transcript_list._generated_transcripts.keys())[0]].fetch()
            text_formatted = TextFormatter().format_transcript(transcript)
            return text_formatted, False  # False: no proxy used
        except Exception as first_exc:
            pass  # Will try proxies

        # Try with proxies
        proxy_list = list(proxies().get_confirmed_working_proxies())
        for idx, proxy in enumerate(proxy_list):
            try:
                if progress and lang:
                    progress.update(
                        45,
                        lang.get("fetching_transcript", "Fetching transcript...")
                        + lang.get("using_proxy", "").format(number=idx + 1)
                    )
                session = requests.Session()
                session.proxies = {
                    'http': proxy,
                    'https': proxy,
                }
                ytt_api = YouTubeTranscriptApi(http_client=session)
                transcript_list = ytt_api.list(video_id)
                transcript = transcript_list._generated_transcripts[list(transcript_list._generated_transcripts.keys())[0]].fetch()
                text_formatted = TextFormatter().format_transcript(transcript)
                return text_formatted, True  # True: proxy used
            except Exception:
                continue
        # If all proxies fail, raise the first error
        raise Exception(f"Transcript error: {str(first_exc)}")