"""
    Abrar Mahi
    Python Version 3.11
    
    -Please enter the message as an integer

    -Please enter shares in the format:
        "x0,y0 x1,y1, ... xn,yn"
        where there are: 
        1. spaces between each x,y pair
        2. no spaces between x,y
        3. x,y are comma separated
"""
import random
from decimal import Decimal
from typing import List, Tuple

import numpy as np
import numpy.polynomial.polynomial as poly



def test_everything(obj: "Lagrange"):
    ###########Testing encrypt############
    secret = random.randint(-(10**4), 10**4 + 1)
    minimum_shares = random.randint(2, 6)
    new_number_of_shares = random.randint(minimum_shares, minimum_shares + 5)
    shares = obj.encrypt(
        secret, minimum_shares, new_number_of_shares
    )  # want to generate 3 new shares
    print(f"original secret {secret}")
    print("shares generated:", shares)

    ###########Testing decrypt############
    decrypted_secret = obj.decrypt(minimum_shares, shares)
    if decrypted_secret == secret:
        print(
            f"secret decrypted successfully {decrypted_secret} \N{smiling face with sunglasses}\n"
        )
    else:
        print(f"decryption failed {decrypted_secret} != {secret} \N{angry face}\n")

    ###########Testing generate_new_shares############
    new_share_num = random.randint(
        minimum_shares, minimum_shares + random.randint(1, 5)
    )
    new_shares = obj.generate_new_shares(minimum_shares, shares, new_share_num)
    # print('new shares generated:', new_shares)
    new_decrypted_secret = obj.decrypt(minimum_shares, new_shares)
    if new_decrypted_secret == secret:
        print(
            f"secret decrypted successfully {decrypted_secret} == {secret} \N{smiling face with sunglasses}\n"
        )
    else:
        print(
            f"new shares decryption failed {decrypted_secret} != {secret} \N{angry face}\n"
        )


def interpolate(shares: list, xp=Decimal(0), yp=Decimal(0)):
    """
    Interpolates a polynomial using Lagrange's method
    shares: list of tuples (x,y)
    x: the x value to interpolate at, defaults to 0
    """
    x = np.array([Decimal(i[0]) for i in shares], Decimal)  # x values
    y = np.array([Decimal(i[1]) for i in shares], Decimal)  # y values
    # evaluating the polynomial at x=0
    for xi, yi in zip(x, y):
        yp += yi * np.prod((xp - x[x != xi]) / (xi - x[x != xi]))
    return int(round(yp))


def shares_to_list(shares: str):
    """
    Converts a string of shares to a list of tuples
    e.g.
    "1,2 3,4" -> [(1,2), (3,4)]
    """
    try:
        result = shares.split(" ")
        result = [tuple(map(int, x.split(","))) for x in result]
        return result
    except Exception as e:
        print("Please enter shares in the format: x0,y0 x1,y1, ... xn,yn")
        raise e


class Lagrange:
    def __init__(self):
        pass

    def generate_new_shares(
        self, minimum_shares: int, shares: list, number_of_new_shares: int
    ):
        """
        # Parameters
        minimum_shares: the minimum number of shares (coordinate pairs) required to unlock a secret
        shares: the actual secret shares
        number_of_new_shares: the number of new shares requested (should be consistent with old shares)

        # Function
        this function outputs new keys given the secret shares
        """

        try:
            minimum_shares = int(minimum_shares)
            number_of_new_shares = int(number_of_new_shares)
            # parsing the shares if they are a string
            if type(shares) == str:
                parsed_shares = shares_to_list(shares)
            elif type(shares) == list:
                parsed_shares = shares
            # decrypting the shares
            message = self.decrypt(minimum_shares, parsed_shares)
            # generating {number_of_new_shares}  new shares
            new_shares = self.encrypt(message, minimum_shares, number_of_new_shares)
            return new_shares
        except Exception as e:
            raise e

        # generating new shares

    def encrypt(
        self, message: int, minimum_shares: int, share_number: int
    ) -> List[Tuple]:
        """
        # Parameters
        message: a message you wish to encrypt, you can choose to simply encode numbers or, for extra credit, you can convert plaintext messages to a number representation and encode that
        minimum_shares: the minimum number of shares required to "unlock" the secret
        share_number: the number of shares generated

        # Function
        this function outputs coordinate pairs (the secret shares) that can be handed out to the end user
        """
        try:
            message = int(message)
            minimum_shares = int(minimum_shares)
            share_number = int(share_number)

            # calculating degree of polynomial
            degree_of_poly = minimum_shares - 1

            # generating random coefficients for the polynomial
            coeff = [message]
            for _ in range(degree_of_poly):
                coeff.append(random.randint(1, 50))
            # print('random coeficients generated:', coeff)

            # generating the polynomial from the coefficients
            polynomial = poly.Polynomial(coeff)
            # print('polynomial:',  polynomial)

            # generating {share_number} random x-coordinate values
            x_values = [random.randint(1, 300) for _ in range(1, share_number + 1)]
            # print('random x values generated: ', x_values)

            # generating the y-coordinate values
            y_values = [polynomial(i) for i in x_values]

            # zipping the x and y values together into a list of tuples
            shares = list(zip(x_values, y_values))
            print(shares)
            return shares
        except Exception as e:
            raise e

    def decrypt(self, minimum_shares: int, shares: list):
        """
        30 points
        # Parameters
        minimum_shares: the minimum number of shares (coordinate pairs) required to unlock a secret
        shares: the actual secret shares

        # Function
        this function takes the minimum number of shares to unlock a secret, and the shares you are providing and outputs the decoded secret (if you devise a system for converting messages to a coordinate in the encrypt step, to receive the full extra credit, you need to convert those messages to plaintext at this step
        """
        try:
            if type(shares) == str:
                parsed_shares = shares_to_list(shares)
            elif type(shares) == list:
                parsed_shares = shares
            else:
                raise Exception(
                    "please enter shares as a list of tuples or a string of shares of the form 'x,y x,y'"
                )
            minimum_shares = int(minimum_shares)
            if minimum_shares > len(parsed_shares):
                raise Exception("not enough shares to decrypt")
            # randomly picking {minimum_shares} shares to use
            parsed_shares = random.sample(parsed_shares, minimum_shares)
            return interpolate(parsed_shares)

        except Exception as e:
            raise e


def main():
    interpolation = Lagrange()
    # running 10 tests on all class functions
    for i in range(1, 11):
        print("\ntest", i)
        print("================")
        test_everything(interpolation)
    # choice = input(
    #     "Do you want to encrypt or decrypt a secret or generate new shares (e/d/g)?"
    # )

    # if choice == "e":
    #     message = input("What is the secret you wish to encrypt?: ")
    #     minimum_shares = input(
    #         "What is the minimum number of shares you wish to deploy?: "
    #     )
    #     share_number = input(
    #         "What is the minimum number of shares you wish to generate?: "
    #     )
    #     encryption = interpolation.encrypt(message, minimum_shares, share_number)
    #     print(encryption)

    # elif choice == "d":
    #     minimum_shares = input(
    #         "What is the minimum number of shares you need to decrypt?"
    #     )
    #     shares = input("What shares do you have?")
    #     decryption = interpolation.decrypt(minimum_shares, share_number)
    #     print(decryption)

    # elif choice == "g":
    #     minimum_shares = input(
    #         "What is the minimum number of shares you need to decrypt?"
    #     )
    #     shares = input("What shares do you have?")
    #     share_number = input("What is the number of new shares you want to generate?")
    #     new_shares = interpolation.generate_new_shares(
    #         minimum_shares, shares, share_number
    #     )
    #     print(new_shares)


if __name__ == "__main__":
    main()
