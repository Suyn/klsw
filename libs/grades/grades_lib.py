# -*- coding: utf-8 -*-

# 积分表
grades = [10,50,100,500,1000,2000,5000,10000,20000]

class Grade(object):
    """
    计算积分等级
    """

    def __init__(self, grade):
        # 当前积分-------------------------
        self.grade = grade

        global grades

    def after(self):
        for index, value in enumerate(grades):
            if self.grade < value:
                pre_grade = grades[index - 1]

                # 当前等级-------------------------
                current_grade = index + 1

                # 距离下一等级---------------------
                next_grade = grades[index] - self.grade

                # 当前百分比值---------------------
                percentage = round(float(self.grade - pre_grade) / (value - pre_grade), 3) * 100

                return current_grade, next_grade, percentage

