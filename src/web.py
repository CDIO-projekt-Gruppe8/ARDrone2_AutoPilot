from interfaces import AnalyzedCamObserver
# TODO: Implement start(), stop(), receive_analyzed_video()


class WebInterface(AnalyzedCamObserver):
    def start(self):
        # Initiates the drone and starts the video display
        pass

    def stop(self):
        # Stops the drone and stops the video display
        pass

    def receive_analyzed_video(self, video):
        # Interface methods for Observer pattern
        # Updates the display with the newly received video
        pass
