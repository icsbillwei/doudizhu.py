class User:
    def __init__(self,order,points):
        """
        order = 出牌顺序 - int
        win = 获胜次数 - int
        points = 积分？不确定 - int
        """
        self.order = order
        self.win = 0
        self.points = 0
    
    def play_turn(self):
        pass

    def respond_turn(self):
        pass
