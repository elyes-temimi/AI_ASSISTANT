from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0  # stability

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except:
        return "en"
