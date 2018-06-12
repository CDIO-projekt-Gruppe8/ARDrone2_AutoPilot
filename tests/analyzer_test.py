from src.modules.analyzer import Analyzer


def analyze_video_test():
    analyzer = Analyzer()
    analyzer.start()
    key = raw_input()
    while key is not 'q':
        qr = key
        analyzer.analyze_video(None, current_qr_number=qr)
        key = raw_input()
