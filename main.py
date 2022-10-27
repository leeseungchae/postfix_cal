from typing import List
import re
from token_base import Operand, Operator


class LexemeAnalyzer:
    def __init__(self):
        pass

    @staticmethod
    def brac_check(expression: str):
        """
        barc 개수를 판단하는 함수

        :param expression:
        :return: True or raise Exception
        """

        if expression.count("(") != expression.count(")"):
            raise Exception("Parentheses error")

        elif expression.count("(") == 0 or expression.count(")") == 0:
            return True

        else:
            stack = []
            for i in expression:
                if i == '(':  # '('는 stack에 추가
                    stack.append(i)
                elif i == ')':  # i == ')'인 경우
                    if stack == []:  # 괄호 짝이 ')'로 시작하면 False 반환
                        raise Exception("value error")
                    else:
                        stack.pop()

            return True

    def check_expreesion(self, expression: str):

        """
        정규표현식을 이용하여 정해진 규칙인지 아닌지 판단하는 함수

        :param expression:
        :return:True or raise Exception
        """

        expression = expression.replace(" ", "")
        pattern = re.compile("[^\d.\/\+\*\-\(\)]")
        pattern2 = re.compile(r"([\+\-\*\/])\1+")

        if pattern.search(expression):
            raise Exception("Unexpected character")
        elif pattern2.search(expression):
            raise Exception("Overlap operator")
        elif not self.brac_check(expression):
            raise Exception("Parentheses error")
        elif not check_num(expression):
            raise Exception("value error")
        else:
            return True

    def lex(self, expression: str) -> List[str]:
        """
             infix equation 을 postfix 로 변경하는 함수

             :param expression
             :return: postix
             """

        self.check_expreesion(expression)
        expression = re.findall(r'[\d.]+|[*/+\-()]', expression)

        postfix = []
        stack = []

        for idx, token in enumerate(expression):

            if Operand.is_valid(token):
                try:
                    if stack and stack[-1].value == '-' and not expression[idx-2].isdigit():
                        stack = stack[:-1]
                        postfix.append(Operand("-"+ token))
                    else:
                        postfix.append(Operand(token))
                except:
                    postfix.append(Operand(token))

            elif token == '(':
                stack.append(token)
            elif token == ')':  # )가 나오면 stack에서 (가 나올때까지 pop처리 및 lst에 추가.
                while stack[-1] != '(':
                    postfix.append(stack.pop())
                stack.pop()  # (가 나타나면 pop처리
            else:
                while stack and stack[-1] != '(' and Operator.priority(token) <= Operator.priority(stack[-1]):
                    postfix.append(stack.pop())  # pop한것들은 lst에 추가 시켜줌
                stack.append(Operator(token))  # 위의 조건이 완료 되면 stack에 추가
        while stack:  # 스택에 남은 연산자 postfix에 모두 추가
            postfix.append(stack.pop())
        return postfix


def check_num(num: str):

    """
    맨 앞과 마지막의 input 형태가 맞는지
    판한하는 함수


    :param num
    :return: True or raise Exception
    """
    all_number = re.compile("[^[\d.]")
    if all_number.search(num):
        pass
    else:
        return False


    num_list = re.findall(r'[\d.]+|[*/+\-()]', num)


    for idx,token in enumerate(num_list):
        try:
            token = isinstance(float(token), float)
            if num_list[idx-1] == '(' and num_list[idx+1] == ')':
                return False
            elif num_list[idx-1] == '-' and num_list[idx-2] == '(' and num_list[idx+1] == ')':
                return False
        except:
            pass


    try:
        first_check = isinstance(float(num_list[0]), float)
        second_check = isinstance(float(num_list[-1]), float)

        if first_check is True and second_check is True :
            return True
        else:
            raise Exception("value error")
    except:

        if num_list[0] == '(' or num_list[-1] == ')':
            return True
        else:
            raise Exception("value error")


class PostfixCalculator:
    """postfix 기반 Calculator"""

    def __init__(self):
        self.lexeme_analyzer = LexemeAnalyzer()

    def _validate_equation(self, equation: str) -> bool:
        try:
            eval(equation)

        except (SyntaxError, NameError, ZeroDivisionError):
            return False

        return True

    def calculate(self, equation: str) -> float:
        """
        input equation 이 들어왔을 때 계산하는 함수
        Args:
            equation(str): infix equation

        Returns:
            float: calculation result value

        Raises:
            SyntaxError : 수식이 유효하지 않을 때

        """
        # if not self._validate_equation(equation):  # 수식 유효성 검정
        #     raise SyntaxError("This equation is not valid.")

        postfix = self.lexeme_analyzer.lex(equation)
        return self.calculate_postfix(postfix)

    def calculate_postfix(self, postfix: List[str]) -> float:
        """
        postfix 배열을 받아 계산하는 함수
        Args:
            postfix(List[str]): postfix로 표현된 equation

        Returns:
            float: calculation result value

        """

        stack = []
        for char in postfix:

            if type(char) == Operator:

                b = stack.pop()
                a = stack.pop()

                if char.value == "+":
                    stack.append(a + b)

                elif char.value == "-":
                    stack.append(a - b)

                elif char.value == "*":
                    stack.append(a * b)

                elif char.value == "/":
                    stack.append(a / b)
            else:
                stack.append(float(char.value))

        return float(stack[0])


""" input spec
    연산자 정의 ['*', '/' , '+','-', '(',')']

    1. 입력은 실수 혹은 연산자만 입력 가능하다.
    2. 맨앞은 양수인 실수만 입력 가능하고, 맨마지막은 ')' 혹은 실수만 입력가능 하다.   
    3. 연산자는 정해진 연산자만 사용 가능하다.
    4. 연산결과는 소수 둘째짜리 까지  표현한다.
    5. 괄호 안에 피연산자 한개만 오지 못한다.
    6. 연산자는 연속해서 올 수 없다."""

if __name__ == '__main__':
    calculator = PostfixCalculator()
    analyzer = LexemeAnalyzer()

    input_txt = "* * "
    print(f"equation : {input_txt}")
    print(f"postfix : {analyzer.lex(input_txt)}")
    print(f"result :{calculator.calculate(input_txt):.2f}")
