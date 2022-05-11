
# https://github.com/etola710/filters/blob/master/alpha-beta-filter/alpha-beta-filter.py

import math


class AlphaBetaFilter:

    # Think of alpha as like filter bandwidth. If alpha = 1 then the bandwidth
    # of the filter is the same as the bandwidth of the data and there is no
    # filtering. Normally alpha is less than 1 so that the filter bandwidth is
    # less than the data bandwidth. Many time 0.1 is a happy number.
    #
    # Think of beta as like dampening. An optimum beta value is calculated based
    # on the value of alpha. For more dampening then pass in beta scale factor > 1.0.
    # For less dampening and more overshoot then beta scale factor < 1.0.

    def __init__(self, sample_period=1, alpha=None, beta_scale=None, init_sample=0):

        # Alpha
        if alpha == None:
            self.alpha = 0.1
        elif alpha > 1.0:
            self.alpha = 1.0
        else:
            self.alpha = alpha

        # Beta, optimum value
        self.beta = 2 * (2 - self.alpha) - 4 * math.sqrt(1-self.alpha)
        if beta_scale != None:
            self.beta /= beta_scale

        # Sample period
        self.dt = sample_period

        # Initial values
        self.xk_1 = init_sample
        self.vk_1 = 0


    def update(self, sample):

        # xk    Value estimate
        # vk    Velocity estimate
        # ak    Acceleration estimate
        # rk    Value estimate error

        xk = self.xk_1 + (self.vk_1 * self.dt)  # New sample value estimate
        vk = self.vk_1                          # New sample velocity estimate
  
        rk = sample - xk                        # Sample value estimate error

        self.xk_1 = xk + (rk * self.alpha)      # Corrected estimate
        self.vk_1 = vk + (rk * self.beta / self.dt)

        return self.xk_1
