from drone import Drone
import thread

if __name__ == "__main__":
    drone = Drone()
    thread.start_new_thread(drone._send_command, ())
    print 'Command >>'
    while True:
        key = raw_input()
        if key == 't':
            thread.start_new_thread(drone.run, ())
        if key == 'q':
            drone._shutdown()
            thread.start_new_thread(drone._send_command, ())
        else:
            try:
                command = int(key)
                drone.receive_command(command)
            except ValueError:
                pass
