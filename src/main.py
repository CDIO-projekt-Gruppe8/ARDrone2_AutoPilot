from drone import Drone
from web import WebInterface
# TODO: Implement main() as a CLI which could call drone.run()


def main():
    drone = Drone()
    web = WebInterface()
    drone.run()
    drone.add_analyzed_video_observer(web)
    pass


if __name__ == "__main__":
    # Being executed as a standalone project
    # Execute the main method
    main()
