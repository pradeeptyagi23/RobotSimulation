
import time

from threading import Thread,Lock

import random

class SimulatedRobot:
    """
    A class that simulates a robot with an initial position and the ability to move to waypoints.
    """
    def __init__(self, initial_position, update_position_callback=None):
        """
        Initializes a SimulatedRobot object.

        Args:
        - initial_position: A numpy array representing the robot's initial position.
        - update_position_callback: A function that will be called when the robot's position is updated.
        """
        print("Creating SimulatedRobot!")
        self.position = initial_position
        self.update_position_callback = update_position_callback

    def get_position(self):
        """
        Gets the robot's current position.

        Returns:
        - A numpy array representing the robot's current position.
        """
        return self.position

    def set_navigation_command(self, waypoint):
        """
        Sends a navigation command to the robot to move to a specified waypoint.

        Args:
        - waypoint: A numpy array representing the waypoint to which the robot should move.
        """
        print(f"Commanding robot to move to {waypoint}")
        Thread(target=self._update_position, args=(waypoint,)).start()

    def _update_position(self, waypoint):
        """
        Updates the robot's position and calls the update_position_callback function (if defined).

        Args:
        - waypoint: A numpy array representing the new position of the robot.
        """
        time.sleep(random.uniform(1.0, 2.0))
        print(f"Robot is now at {waypoint}")
        self.position = waypoint
        if self.update_position_callback:
            self.update_position_callback(waypoint)


class SimulatedRobotWithCommunicationDelay:
    """
    A class that simulates a robot with an initial position and the ability to move to waypoints with added communication delay.
    """
    def __init__(self, initial_position):
        """
        Initializes a SimulatedRobotWithCommunicationDelay object.

        Args:
        - initial_position: A numpy array representing the robot's initial position.
        """
        self.lock = Lock()
        self._robot = SimulatedRobot(initial_position, self.set_position)
        self.position = initial_position

    def get_position(self):
        """
        Gets the robot's current position.

        Returns:
        - A numpy array representing the robot's current position.
        """
        return self.position

    def set_navigation_command(self, waypoint):
        """
        Sends a navigation command to the robot to move to a specified waypoint with added communication delay.

        Args:
        - waypoint: A numpy array representing the waypoint to which the robot should move.
        """
        print(f"Commanding robot to move to {waypoint}")
        Thread(target=self._update_position_with_delay, args=(waypoint,)).start()

    def _update_position_with_delay(self, waypoint):
        """
        Updates the robot's position with added communication delay.

        Args:
        - waypoint: A numpy array representing the waypoint to which the robot should move.
        """
        time.sleep(random.uniform(0.0, 2.0))
        with self.lock:
            self._robot.set_navigation_command(waypoint)
    
    def set_position(self, position):
        """
        Sets the robot's position.

        Args:
        - position: A numpy array representing the new position of the robot.
        """
        Thread(target=self._update_position, args=(position,)).start()

    def _update_position(self, position):
        """
        Updates the robot's position.

        Args:
        - position: A numpy array representing the new position of the robot.
        """
        time.sleep(random.uniform(0.0, 2.0))
        self.position = position
