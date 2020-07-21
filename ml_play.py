"""
The template of the script for the machine learning process in game pingpong
"""


class MLPlay:
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False
        self.side = side
        self.previous_ball = (0, 0)
        self.pred = 100

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            self.previous_ball = scene_info["ball"]
            return "SERVE_TO_LEFT"

        if self.side == "1P":
            self.pred = 100
            if scene_info["ball_speed"][1] > 0:
                self.pred = scene_info["ball"][0]+((scene_info["platform_1P"][1] - scene_info["ball"][1]) //
                                                   scene_info["ball_speed"][1]) * scene_info["ball_speed"][0]
            while (self.pred < 0 or self.pred > 200):
                if (self.pred > 200):
                    self.pred = 200 - (self.pred - 200)
                if (self.pred < 0):
                    self.pred = -self.pred

            if (scene_info["platform_1P"][0]+20) < self.pred-2.5:
                command = "MOVE_RIGHT"
            else:
                command = "MOVE_LEFT"
        elif self.side == "2P":
            self.pred = 100
            if scene_info["ball_speed"][1] < 0:
                self.pred = scene_info["ball"][0]+((scene_info["ball"][1] - scene_info["platform_2P"][1] - 30) //
                                                   (-scene_info["ball_speed"][1])) * scene_info["ball_speed"][0]
            while (self.pred < 0 or self.pred > 200):
                if (self.pred > 200):
                    self.pred = 200 - (self.pred - 200)
                if (self.pred < 0):
                    self.pred = -self.pred

            if (scene_info["platform_2P"][0]+20) < self.pred-2.5:
                command = "MOVE_RIGHT"
            else:
                command = "MOVE_LEFT"
        self.previous_ball = scene_info["ball"]
        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
