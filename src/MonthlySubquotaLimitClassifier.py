from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin

class MonthlySubquotaLimitClassifier(TransformerMixin):
    KEYS = ['applicant_id', 'month', 'year']

    def fit(self, X):
        self.X = X
        self._X = self.X.copy()
        self.__create_columns()
        return self

    def transform(self, X):
        self.limits = [
            {
                'subquota': 'Automotive vehicle renting or watercraft charter',
                'data': self._X.query('(subquota_number == "120") & (reimbursement_month >= datetime(2015, 4, 1))'),
                'monthly_limit': 1090000,
            },
            {
                'subquota': 'Taxi, toll and parking',
                'data': self._X.query('(subquota_number == "122") & (reimbursement_month >= datetime(2015, 4, 1))'),
                'monthly_limit': 270000,
            },
            {
                'subquota': 'Fuels and lubricants',
                'data': self._X.query('(subquota_number == "3") & (reimbursement_month >= datetime(2015, 10, 1))'),
                'monthly_limit': 600000,
            },
            {
                'subquota': 'Security service provided by specialized company',
                'data': self._X.query('(subquota_number == "8") & (reimbursement_month >= datetime(2015, 4, 1))'),
                'monthly_limit': 870000,
            },
            {
                'subquota': 'Participation in course, talk or similar event',
                'data': self._X.query('(subquota_number == "137") & (reimbursement_month >= datetime(2015, 11, 1))'),
                'monthly_limit': 769716,
            },
        ]
        return self


    def predict(self, X):
        self._X['is_over_monthly_subquota_limit'] = False
        for metadata in self.limits:
            data, monthly_limit = metadata['data'], metadata['monthly_limit']
            surplus_reimbursements = self.__find_surplus_reimbursements(data, monthly_limit)
            self._X.loc[surplus_reimbursements.index,
                        'is_over_monthly_subquota_limit'] = True
        results = self._X.loc[self.X.index, 'is_over_monthly_subquota_limit']
        return np.r_[results]


    def predict_proba(self, X):
        return 1.


    def __create_columns(self):
        self._X['net_value_int'] = (self._X['total_net_value'] * 100).apply(int)

        self._X['coerced_issue_date'] = \
            pd.to_datetime(self._X['issue_date'], errors='coerce')
        self._X.sort_values('coerced_issue_date', inplace=True)

        reimbursement_month = self._X[['year', 'month']].copy()
        reimbursement_month['day'] = 1
        self._X['reimbursement_month'] = pd.to_datetime(reimbursement_month)


    def __find_surplus_reimbursements(self, data, monthly_limit):
        grouped = data.groupby(self.KEYS).apply(self.__create_cumsum_cols)
        return grouped[grouped['cumsum_net_value'] > monthly_limit]


    def __create_cumsum_cols(self, subset):
        subset['cumsum_net_value'] = subset['net_value_int'].cumsum()
        return subset





if __name__ == '__main__':
    dataset = pd.read_csv('/tmp/serenata-data/reimbursements.xz',
                          dtype={'applicant_id': np.str,
                                'subquota_number': np.str},
                          low_memory=False)
    model = MonthlySubquotaLimitClassifier()
    model.fit_transform(dataset)
    y = model.predict(dataset)
    print(y)
    print(model.predict_proba(dataset))
