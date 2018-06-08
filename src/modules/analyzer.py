# TODO: Sanity and type check on all add/delete methods
# TODO: Implement analyze_video()
# TODO: analyze_video() should run in a separate thread [this also affects start() and stop()]


class Analyzer(object):
    _ring_observers = set()
    _analyzing = False

    def analyze_video(self, video_url, current_qr_number):
        if video_url is None:
            return
        video = None  # TODO: cv2.VideoCapture(video_URL)
        # Analyzes the video and searches for rings
        # video is the resulting object of cv2.VideoCapture(video_URL)
        # Rings contains all previously found rings
        # If a new ring is found, call _ring_observer_callback()
        ret, frame = video.read()
        while self._analyzing and ret:
            # TODO: Analyze the video
            qr_number = None
            if qr_number is current_qr_number:
                # Found the ring of interest. Stop analyzing.
                self._ring_observer_callback()
                break
            pass

    def get_ring_center(self, qr_number):
        # TODO: Returns the x-y coordinates of the ring
        pass

    def start(self):
        # TODO: Check if analyzer-thread is running, create it if not
        self._analyzing = True

    def pause(self):
        self._analyzing = False

    def stop(self):
        # TODO: Check if analyzer-thread is running, close if it is
        self._analyzing = False

    def _ring_observer_callback(self):
        for obs in self._ring_observers:
            obs.ring_found()

    def add_ring_observer(self, obs):
        self._ring_observers.add(obs)

    def del_ring_observer(self, obs):
        try:
            self._ring_observers.remove(obs)
        except KeyError:
            pass  # TODO
