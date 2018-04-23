from src.drone import Drone
from src.web import WebInterface
# TODO: Implement main() as a CLI which could call drone.run()


def main():
    drone = Drone()
    web = WebInterface()
    drone.run()
    pass

if __name__ == "__main__":
    # Being executed as a standalone project
    # Execute the main method
    main()
