
properties=['cur_date', 'up_5', 'down_5', 'up_num', 'down_num', 'up_all', 'down_all', 'id', 'up_10_2', 'up_highest']

class Sentiment:
    def __init__(self, cur_date, up_5=0, down_5=0, up_num=0, down_num=0, up_all=0, down_all=0, up_10_2=0, up_highest=0, id=None):
        self.cur_date = cur_date
        self.up_5 = up_5
        self.down_5 = down_5
        self.up_num = up_num
        self.down_num = down_num
        self.up_all = up_all
        self.down_all = down_all
        self.id = id
        self.up_10_2 = up_10_2
        self.up_highest = up_highest

    def __setitem__(self, key: str, value: any) -> None:
        self.key=value

    def __getitem__(self, key) -> any:
        return self.__dict__[key]

if __name__ == '__main__':
    a=Sentiment(cur_date='121', up_5=3)
    print(a['up_5'])