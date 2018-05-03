from interfaces import Commander, Priority
# TODO: Sanity and type check on all add/delete methods
# TODO: Implement analyze_video()
# TODO: analyze_video() should run in a separate thread [this also affects start() and stop()]


class Analyzer(Commander):
    _ring_observers = set()
    _analyzed_video_observers = set()
    _analyzing = False

    def analyze_video(self, video_URL, rings):
        priority = Priority.Analyzing
        video = None  # TODO: cv2.VideoCapture(video_URL)
        # Analyzes the video and searches for rings
        # video is the resulting object of cv2.VideoCapture(video_URL)
        # Rings contains all previously found rings
        # If a new ring is found, call _ring_observer_callback()
        # Always call _analyzed_video_observer_callback()
        ret, frame = video.read()
        while self._analyzing and ret:
            # TODO: Analyze the video
            if False:
                # If specific drone movement is needed for analysis, call send_command()
                command = None  # TODO
                self.send_command(command, priority)
            ring = None  # TODO: Any ring found in the analysis - loop if multiple
            if not rings.contains(ring):
                self._ring_observer_callback(ring)
            analyzed_video = None  # TODO: A single, analyzed/augmented frame
            self._analyzed_video_observer_callback(analyzed_video)
            pass

    def start(self):
        # TODO: Check if analyzer-thread is running, create it if not
        self._analyzing = True

    def pause(self):
        self._analyzing = False

    def stop(self):
        # TODO: Check if analyzer-thread is running, close if it is
        self._analyzing = False

    def _analyzed_video_observer_callback(self, analyzed_video):
        for obs in self._analyzed_video_observers:
            obs.receive_analyzed_video(analyzed_video)

    def _ring_observer_callback(self, ring):
        for obs in self._ring_observers:
            obs.add_ring(ring)

    def add_ring_observer(self, obs):
        self._ring_observers.add(obs)

    def del_ring_observer(self, obs):
        try:
            self._ring_observers.remove(obs)
        except KeyError:
            pass  # TODO

    def add_analyzed_video_observer(self, obs):
        self._analyzed_video_observers.add(obs)

    def del_analyzed_video_observer(self, obs):
        try:
            self._analyzed_video_observers.remove(obs)
        except KeyError:
            pass  # TODO
