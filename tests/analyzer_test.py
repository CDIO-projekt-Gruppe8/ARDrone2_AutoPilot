from src.modules.analyzer import Analyzer


def analyze_video_test():
    analyzer = Analyzer()
    analyzer.start()
    print 'Enter QR number:'
    key = raw_input()
    while key is not 'q':
        try:
            qr = int(key)
            analyzer.analyze_video(None, current_qr_number=qr)
        except ValueError:
            print 'QR must be a number!'
        print 'Enter QR number:'
        key = raw_input()


if __name__ == "__main__":
    analyze_video_test()
