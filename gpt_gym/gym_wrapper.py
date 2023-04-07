from server import GymServer
import socket
import numpy as np

# Constants
HOST = '127.0.0.1'
PORT = 65432

class GymWrapper:
    def __init__(self, env_id, host, port):
        self.connect_server(host, port)

    #
    def connect_server(self, host, port):
        self.client_socket = socket.socket()  # instantiate
        self.client_socket.connect((host, port))  # connect to the server

    def send(self, message):
        self.client_socket.send(message.encode())

    def get_initial_state(self):
        pass 

    def random_straegy(self):
        pass 

    def set_state(self, state):
        pass

    def get_state(self):
        pass

    def apply_action(self, action):
        # send action to server
        self.send(action)

        # get response from server
        response = self.client_socket.recv(1024).decode()

        return response 
    
"""
    def takeoff(self):
        self.client.takeoffAsync().join()

    def land(self):
        self.client.landAsync().join()

    def get_drone_position(self):
        pose = self.client.simGetVehiclePose()
        return [pose.position.x_val, pose.position.y_val, pose.position.z_val]

    def fly_to(self, point):
        if point[2] > 0:
            self.client.moveToPositionAsync(
                point[0], point[1], -point[2], 5).join()
        else:
            self.client.moveToPositionAsync(
                point[0], point[1], point[2], 5).join()

    def fly_path(self, points):
        airsim_points = []
        for point in points:
            if point[2] > 0:
                airsim_points.append(airsim.Vector3r(
                    point[0], point[1], -point[2]))
            else:
                airsim_points.append(airsim.Vector3r(
                    point[0], point[1], point[2]))
        self.client.moveOnPathAsync(
            airsim_points, 5, 120, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False, 0), 20, 1).join()

    def set_yaw(self, yaw):
        self.client.rotateToYawAsync(yaw, 5).join()

    def get_yaw(self):
        orientation_quat = self.client.simGetVehiclePose().orientation
        yaw = airsim.to_eularian_angles(orientation_quat)[2]
        return yaw

    def get_position(self, object_name):
        query_string = objects_dict[object_name] + ".*"
        object_names_ue = []
        while len(object_names_ue) == 0:
            object_names_ue = self.client.simListSceneObjects(query_string)
        pose = self.client.simGetObjectPose(object_names_ue[0])
        return [pose.position.x_val, pose.position.y_val, pose.position.z_val]
"""