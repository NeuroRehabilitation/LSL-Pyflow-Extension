from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class DDA1(NodeBase):
    def __init__(self, name):
        super(DDA1, self).__init__(name)
        self.Nvalues = self.createInputPin('NValues', 'IntPin')
        self.Focus = self.createInputPin('Focus', 'IntPin')

        self.Data = self.createInputPin('Data', 'AnyPin', structure=StructureType.Multi)
        self.Data.enableOptions(PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.Data.disableOptions(PinOptions.SupportsOnlyArrays)

        self.Send = self.createOutputPin('Data', 'AnyPin', structure=StructureType.Multi)
        self.Send.enableOptions(PinOptions.AllowAny)


    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('BoolPin')
        helper.addOutputDataType('BoolPin')
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return 'Generated from wizard'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def compute(self, *args, **kwargs):

        Player_Skills = self.Data.getData()

        # Usage example:
        player_score = Player_Skills[0]
        remaining_lives = Player_Skills[1]
        time_left = Player_Skills[2]

        skill_level = self.calculate_skill_level(player_score, remaining_lives, time_left)
        ball_speed, ball_spawn_rate, life_spawn_rate = self.set_difficulty(skill_level)

        Dificulty_Skill=[]
        Dificulty_Skill.append(ball_speed)
        Dificulty_Skill.append(ball_spawn_rate)
        Dificulty_Skill.append(life_spawn_rate)

        ball_speed, ball_spawn_rate, life_spawn_rate = self.set_difficulty_focus(skill_level)

        Dificulty_Focus = []
        Dificulty_Focus.append(ball_speed)
        Dificulty_Focus.append(ball_spawn_rate)
        Dificulty_Focus.append(life_spawn_rate)

        Dificulty = []
        Dificulty.append((Dificulty_Skill[0]+Dificulty_Focus[0])/2)
        Dificulty.append((Dificulty_Skill[1]+Dificulty_Focus[1])/2)
        Dificulty.append((Dificulty_Skill[2]+Dificulty_Focus[2])/2)

        self.Send.setData(Dificulty)

    def calculate_skill_level(self,score, lifes, time_left):
        # You can define your own formula to calculate the skill level
        # based on the player's score, remaining lives, and time left.
        # For example:
        skill_level = (score + lifes * 10) / (time_left + 1)
        return skill_level

    # Define the function to determine difficulty settings based on Skill Level (SL)
    def set_difficulty(self, skill_level):
        # You can define your own mapping of skill levels to difficulty settings
        # Here's a simple example:
        if skill_level <= 50:
            ball_speed = 10
            ball_spawn_rate = 5
            life_spawn_rate = 3
        elif skill_level <= 100:
            ball_speed = 20
            ball_spawn_rate = 4
            life_spawn_rate = 2
        elif skill_level <= 150:
            ball_speed = 30
            ball_spawn_rate = 3
            life_spawn_rate = 1
        else:
            ball_speed = 60
            ball_spawn_rate = 2
            life_spawn_rate = 1

        return ball_speed, ball_spawn_rate, life_spawn_rate

    def set_difficulty_focus(self, focus):
        # You can define your own mapping of skill levels to difficulty settings
        # Here's a simple example:
        if focus <= -1:
            ball_speed = 10
            ball_spawn_rate = 5
            life_spawn_rate = 3
        elif focus <= 0:
            ball_speed = 20
            ball_spawn_rate = 4
            life_spawn_rate = 2
        elif focus <= 1:
            ball_speed = 30
            ball_spawn_rate = 3
            life_spawn_rate = 1
        else:
            ball_speed = 60
            ball_spawn_rate = 2
            life_spawn_rate = 1

        return ball_speed, ball_spawn_rate, life_spawn_rate
