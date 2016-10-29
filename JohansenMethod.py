# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import statsmodels.api as sm

from statsmodels.tsa.vector_ar.var_model import VAR

class JohansenMethod(object):
    """
    Class of Johansen's method (Johansen[1988, 1991])

    input:
        data: datapath for analysis (string)
        col: name of columns used for analysis (list)
    """

    def __init__(self, datapath, col):
        self.df = pd.read_csv(datapath)
        self.col = col

        self.df_diff = self.df.diff()
        self.df_t_minus_1 = self.df.shift(periods=1, freq=1, axis=0)

    def u_t(self):
        # estimate residual of delta y with VAR(p-1) model
        model = VAR(self.df_diff)
        result = model.fit()
        return result.resid

    def v_t(self):
        # estimate residual of regression y_t-1 with dlta y_t-1, dlta y_t-2...
        df_y = self.df_t_minus_1[self.col[0]]
        df_x = self.df_t_minus_1.diff()
        df_x = sm.add_constant(df_x)

        model = OLS(df_y, df_x)
        results = model.fit()
        return results.resid

    def A(self):
        # estimate eigenvector from u_t and v_t
        Sigma_vv = np.dot(self.v_t, self.v_t)
        Sigma_uu = np.dot(self.u_t, self.u_t)
        Sigma_uv = np.dot(self.u_t, self.v_t)
        Sigma_vu = np.dot(self.v_t, self.u_t)

    def main(self):
        return self

if __name__ == '__main__':
    # test
    datapath = 'xxx.csv'
    col = ['Y1', 'Y2', 'Y3']

    jm = JohansenMethod(datapath, col)
    result = jm.main()
