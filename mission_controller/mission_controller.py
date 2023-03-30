
import numpy as np
import time
from threading import Thread,Lock

from mission_controller.simulated_robot import SimulatedRobotWithCommunicationDelay,SimulatedRobot

class MissionController:
    """
    A class that manages a robot's mission by sending navigation commands to the robot based on a given trajectory.
    """
    def __init__(self, robot):
        """
        Initializes a MissionController object.

        Args:
        - robot: An object of a robot class (SimulatedRobot or SimulatedRobotWithCommunicationDelay).
        """


        if not isinstance(robot, (SimulatedRobot, SimulatedRobotWithCommunicationDelay)):
            raise TypeError("robot must be an instance of SimulatedRobot or SimulatedRobotWithCommunicationDelay")    

        print("Creating MissionController!")
        
        self.lock = Lock()
        self.robot = robot
        self.current_waypoint_idx = 0
        self.trajectory = None

        self._start_polling_position()

    def set_trajectory(self, trajectory):
        """
        Sets the trajectory for the robot to follow.

        Args:
        - trajectory: A numpy array containing a series of waypoints for the robot to follow.
        """

        if not isinstance(trajectory, np.ndarray):
            raise ValueError("trajectory must be a numpy array")

        self.trajectory = trajectory
        self.current_waypoint_idx = 0

    """
        1. Avoid stack overflow by first checking if the mission is complete.
        2. To add a check for mission completion, 
        modify the MissionController class to keep track of the number of waypoints and the current waypoint index, 
        and then add a check to see if the current waypoint index has reached the last waypoint in the trajectory. 
    """
    def is_mission_completed(self):
        """
        Checks whether the robot has completed its mission.

        Returns:
        - A boolean value indicating whether the robot has completed its mission.
        """
        if self.trajectory is None:
            return False
        return self.current_waypoint_idx >= len(self.trajectory[0])

    def _start_polling_position(self):
        """
        Starts polling the robot's position.
        """
        Thread(target=self._poll_position, daemon=True).start()

    def _poll_position(self):
        """
        Polls the robot's position and sends navigation commands based on the current waypoint in the trajectory.
        """
        time.sleep(1)
        position = self.robot.get_position()

        """
        Avoid race condition of more than one threads updating current_waypoint_idx at the same time
        """
        with self.lock:
            if self.current_waypoint_idx == 0:
                self._send_navigation_command()
                self.current_waypoint_idx += 1

            elif np.all(position == self.trajectory[:, self.current_waypoint_idx]):
                self._send_navigation_command()
                self.current_waypoint_idx += 1
        """
            1. Avoid stack overflow by first checking if the mission is complete.
            2. To add a check for mission completion, 
            modify the MissionController class to keep track of the number of waypoints and the current waypoint index, 
            and then add a check to see if the current waypoint index has reached the last waypoint in the trajectory.
        """
        if self.trajectory is not None and not self.is_mission_completed():
            self._poll_position()

    def _send_navigation_command(self):
        """
        Sends a navigation command to the robot based on the current waypoint in the trajectory.
        """
        print(f"Sending waypoint {self.current_waypoint_idx}")
        self.robot.set_navigation_command(self.trajectory[self.current_waypoint_idx])

