""" class Flight and ManyFlights """

from jdata.utils import load_from_json_file
from config.config import FILE_FLIGHTPLANS
from pprint import pprint


class Flight:
    number: str = ""
    carrier: str = ""
    plane: str = ""
    from_: str = ""
    to: str = ""
    departure_tile: str = ""
    arriving_time: str = ""
    seats: int = 0
    tickets_sold: int = 0

    def __init__(self, **kwargs):
        self.number: str = kwargs['number']
        self.carrier: str = kwargs['carrier']
        self.plane: str = kwargs['plane']
        self.from_: str = kwargs['from']
        self.to: str = kwargs['to']
        self.departure_tile: str = kwargs['departure_time']
        self.arriving_time: str = kwargs['arriving_time']
        self.seats: int = kwargs['seats']
        self.tickets_sold: int = kwargs['tickets_sold']

    def __repr__(self):
        i_will_be_happy_tell_about_me: str = " ".join(["flight", self.number, "'",
                                                       "from", self.from_, "'",
                                                       "to", self.to, ";"])
        return i_will_be_happy_tell_about_me


class ManyFlights():
    big_list_of_flights = []

    def __init__(self):
        self.big_list_of_flights = []

    def load_from_file(self):
        data_ = load_from_json_file("." + FILE_FLIGHTPLANS)
        # pprint(data_)
        for one_item_flight_ in data_:
            tmp_fpl_ = Flight(**one_item_flight_)
            # print(tmp_fpl_)
            self.big_list_of_flights.append(tmp_fpl_)
        # pprint(self.big_list_of_flights)


    def set_real(self, is_real:bool=True):
        """ setter for a flag __is_it_real"""
        self.__is_it_real = is_real

    def  get_real(self):
        """ getter for a flag __is_it_real """
        return self.__is_it_real

    def get_question_hint(self) -> str:
        """ this func return spoiling question """
        # print("I know question:")
        return self.make_magic_spoil(self.question_str)
        # return self.question_str

    def get_answer_hint(self) -> str:
        # print("I know answer to your question:")
        return self.right_answer_str

    @classmethod
    def make_magic_spoil(cls, some_string:str, spoil_number:int=5) ->str:
        """ func for a joke - change some letters in the string to the * """
        # self.question_sting = "".join([x for x in self.question_sting if x == 'a'])
        hard_str: str = ""
        for index in range(0,len(some_string)):
            if index % spoil_number == 0:  # lets spoil each %spoin_number elements :-E~~ (devil face)
                hard_str += '*'
            else:
                hard_str += some_string[index]
        return hard_str

    def get_points(self) -> int:
        """ only for .score_for_right return"""
        return self.score_for_right

    def is_correct(self) ->bool:
        """ compare user_answer with right_answer and return boolean
            if this func started - it means that user has already answered (one or more times)
        """
        self.has_answer_requested = True
        if self.user_answer == self.right_answer_str:
            return True
        return False

    def build_question(self, mode_nightmare:bool=False) ->str:
        """ build string for preparing request the answer"""
        if mode_nightmare:
            tmp_str = self.make_magic_spoil(self.question_str) + " Сложность:" + f"{self.dificulty_num}"
        else:
            tmp_str = self.question_str + " Сложность:" + f"{self.dificulty_num}"
        return tmp_str

    def build_feedback(self):
        """react for answer. it would use is_correct()"""
        if self.is_correct():
            return f"Ответ верный, получено {self.score_for_right} баллов\n"
        else:
            return f"Ответ неверный, правильный ответ {self.right_answer_str}\n"


# self-testing block
if __name__ == '__main__':

    print("Ok")
    # data = load_from_json_file("."+FILE_FLIGHTPLANS)
    # pprint(data)
    # list_of_flights = []
    # for one_item_flight in data:
    #     tmp_fpl = Flight(**one_item_flight)
    #     print(tmp_fpl)
    #     list_of_flights.append(tmp_fpl)
    # pprint(list_of_flights)

    bfp = ManyFlights()
    bfp.load_from_file()
    pprint(bfp.big_list_of_flights)

    # question_4_test: Questions = Questions(right_answer_str="my_Ok", dificulty_str=8, question_str="say just 'Ok'")
    # print(question_4_test)
    # print(question_4_test.get_answer_hint()) # can visible right answer, wait for my_Ok
    # print(question_4_test.get_question_hint())
    # question_4_test.user_answer = "NotOk"
    # print(question_4_test.is_correct()) # wait for False
    # question_4_test.user_answer = "my_Ok"
    # print(question_4_test.is_correct())  # wait for True
    # print(question_4_test.build_question())
