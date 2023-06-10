# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 11:29:31 2021
@author: Jinjin

@fun: calc_pv
BOND VALUATION: AN EXAMPLE
Let's take an imaginary bond: It has a face value of $1,000, an annual coupon of three percent, and a maturity date in 30 years. What does that all mean?

It means that the company or country that owes the bond will pay the bondholder three percent of the face value of $1,000 ($30) every year for 30 years, at which point they will pay the bondholder the full $1,000 face value.

That leads to cash flows. You would have a series of 30 cash flows—one each year of $30—and then one cash flow, 30 years from now, of $1,000.

You would then apply a discounting formula:

    Cash Flow / (1+r)^t

Represented in the formula are the cash flow and number of years for each of them (called "t" in the above equation). You would then need to calculate the "r," which is the interest rate. Which should you use? You could use the current interest rate for similar 30-year bonds today, but for the sake of this example, plug in five percent.

Now you can value the various cash flows. First, you have the coupon payments:

    30 / (1+.05)^1 + 30 / (1+.05)^2... + 30 / (1+.05)^30

And then you have the final face value payment, in 30 years:

    1000 / (1+.05)^30

Together, these total the price at $692.55. This price will ensure that the bondholder receives an annual return of five percent over the life of the bond.

"""

def calc_pv(fv, coupon, T, r):
    '''
    This function is used to compute the current price of a bond
    param:
        fv: face value
        coupon: payment at each period
        T: remaining years
        r: discounting rate
    '''
    return coupon / r * ( 1 - 1 / ( (1 + 0.5 * r) ** (2 * T)) ) + fv / ( (1 + 0.5 * r) ** (2 * T) )

def func(pv, fv, coupon, T, r):
    # func = theorical value of pv - real pv
    return calc_pv(fv, coupon, T, r) - pv

def Dfunc(pv, fv, coupon, T, r):
    # derivative of func
    return -coupon / (r ** 2) + coupon * (1 / (r**2) ) / ( ( 1 + 0.5*r) ** (2*T) ) + T *coupon * ( 1 / r) /( ( 1 + 0.5 * r) **((2*T + 1))) \
        -fv * T / ( (1 + 0.5 * r) ** ( (2* T + 1)) )

def calc_r(pv, fv, coupon, T, r0, min_err, max_iter):
    # calculate yeild to maturity using newton method
    r1 = r0 - func(pv, fv, coupon, T, r0) / Dfunc(pv, fv, coupon, T, r0)
    iter = 1
    while abs (r1 - r0) > min_err and iter <= max_iter:
        r0 = r1
        r1 = r0 - func(pv, fv, coupon, T, r0) / Dfunc(pv, fv, coupon, T, r0)
        iter += 1
    return r1