#
# Copyright 2017 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import division
from unittest import TestCase
from nose_parameterized import parameterized
from numpy import nan
from pandas import (DataFrame, date_range)

from .. tears import (create_returns_tear_sheet,
                      create_information_tear_sheet,
                      create_turnover_tear_sheet,
                      create_summary_tear_sheet,
                      create_full_tear_sheet,
                      create_event_returns_tear_sheet,
                      create_event_study_tear_sheet)

from .. utils import get_clean_factor_and_forward_returns


class PerformanceTestCase(TestCase):
    dr = date_range(start='2015-1-10', end='2015-2-28')
    dr.name = 'date'
    tickers = ['A', 'B', 'C', 'D', 'E', 'F']
    data = [[1.25**i, 1.50**i, 1.00**i, 0.50**i, 1.50**i, 1.00**i]
            for i in range(1, 51)]
    prices = DataFrame(index=dr, columns=tickers, data=data)
    dr2 = date_range(start='2015-1-15', end='2015-2-13')
    dr2.name = 'date'
    factor = DataFrame(index=dr2, columns=tickers,
                       data=[[3, 4, 2, 1, nan, nan], [3, 4, 2, 1, nan, nan],
                             [3, 4, 2, 1, nan, nan], [3, 4, 2, 1, nan, nan],
                             [3, 4, 2, 1, nan, nan], [3, 4, 2, 1, nan, nan],
                             [3, nan, nan, 1, 4, 2], [3, nan, nan, 1, 4, 2],
                             [3, 4, 2, 1, nan, nan], [3, 4, 2, 1, nan, nan],
                             [3, nan, nan, 1, 4, 2], [3, nan, nan, 1, 4, 2],
                             [3, nan, nan, 1, 4, 2], [3, nan, nan, 1, 4, 2],
                             [3, nan, nan, 1, 4, 2], [3, nan, nan, 1, 4, 2],
                             [3, nan, nan, 1, 4, 2], [3, nan, nan, 1, 4, 2],
                             [3, nan, nan, 1, 4, 2], [3, nan, nan, 1, 4, 2],
                             [3, 4, 2, 1, nan, nan], [3, 4, 2, 1, nan, nan],
                             [3, 4, 2, 1, nan, nan], [3, 4, 2, 1, nan, nan],
                             [3, 4, 2, 1, nan, nan], [3, 4, 2, 1, nan, nan],
                             [3, 4, 2, 1, nan, nan], [3, 4, 2, 1, nan, nan],
                             [3, nan, nan, 1, 4, 2], [3, nan, nan, 1, 4, 2]]) \
        .stack()
    factor_groups = {'A': 1, 'B': 2, 'C': 1, 'D': 2, 'E': 1, 'F': 2}

    @parameterized.expand([(2, (1, 5, 10), False),
                           (3, (2, 4, 6), True)])
    def test_create_returns_tear_sheet(
            self,
            quantiles,
            periods,
            filter_zscore):
        """
        Test no exceptions are thrown
        """
        factor_data = get_clean_factor_and_forward_returns(
            self.factor,
            self.prices,
            quantiles=quantiles,
            periods=periods,
            filter_zscore=filter_zscore)

        create_returns_tear_sheet(
            factor_data, long_short=False, group_neutral=False, by_group=False)

    @parameterized.expand([(1, (1, 5, 10), False),
                           (4, (1, 2, 3, 7), True)])
    def test_create_information_tear_sheet(
            self, quantiles, periods, filter_zscore):
        """
        Test no exceptions are thrown
        """
        factor_data = get_clean_factor_and_forward_returns(
            self.factor,
            self.prices,
            quantiles=quantiles,
            periods=periods,
            filter_zscore=filter_zscore)

        create_information_tear_sheet(factor_data, by_group=False)

    @parameterized.expand([(2, (2, 3, 6), True),
                           (4, (1, 2, 3, 7), False)])
    def test_create_turnover_tear_sheet(
            self,
            quantiles,
            periods,
            filter_zscore):
        """
        Test no exceptions are thrown
        """
        factor_data = get_clean_factor_and_forward_returns(
            self.factor,
            self.prices,
            quantiles=quantiles,
            periods=periods,
            filter_zscore=filter_zscore)

        create_turnover_tear_sheet(factor_data)

    @parameterized.expand([(2, (1, 5, 10), False),
                           (3, (1, 2, 3, 7), True)])
    def test_create_summary_tear_sheet(
            self,
            quantiles,
            periods,
            filter_zscore):
        """
        Test no exceptions are thrown
        """
        factor_data = get_clean_factor_and_forward_returns(
            self.factor,
            self.prices,
            quantiles=quantiles,
            periods=periods,
            filter_zscore=filter_zscore)

        create_summary_tear_sheet(
            factor_data, long_short=True, group_neutral=False)
        create_summary_tear_sheet(
            factor_data, long_short=False, group_neutral=False)

    @parameterized.expand([(2, (1, 5, 10), False),
                           (3, (2, 4, 6), True),
                           (4, (1, 8), False),
                           (4, (1, 2, 3, 7), True)])
    def test_create_full_tear_sheet(
            self,
            quantiles,
            periods,
            filter_zscore):
        """
        Test no exceptions are thrown
        """
        factor_data = get_clean_factor_and_forward_returns(
            self.factor,
            self.prices,
            groupby=self.factor_groups,
            quantiles=quantiles,
            periods=periods,
            filter_zscore=filter_zscore)

        create_full_tear_sheet(factor_data, long_short=False,
                               group_neutral=False, by_group=False)
        create_full_tear_sheet(factor_data, long_short=True,
                               group_neutral=False, by_group=True)
        create_full_tear_sheet(factor_data, long_short=True,
                               group_neutral=True, by_group=True)

    @parameterized.expand([(2, (1, 5, 10), False),
                           (3, (2, 4, 6), True),
                           (4, (3, 4), False),
                           (1, (2, 3, 6, 9), True)])
    def test_create_event_returns_tear_sheet(
            self, quantiles, periods, filter_zscore):
        """
        Test no exceptions are thrown
        """
        factor_data = get_clean_factor_and_forward_returns(
            self.factor,
            self.prices,
            groupby=self.factor_groups,
            quantiles=quantiles,
            periods=periods,
            filter_zscore=filter_zscore)

        create_event_returns_tear_sheet(factor_data, self.prices, avgretplot=(
            5, 11), long_short=False, group_neutral=False, by_group=False)
        create_event_returns_tear_sheet(factor_data, self.prices, avgretplot=(
            5, 11), long_short=True, group_neutral=False, by_group=False)
        create_event_returns_tear_sheet(factor_data, self.prices, avgretplot=(
            5, 11), long_short=False, group_neutral=True, by_group=False)
        create_event_returns_tear_sheet(factor_data, self.prices, avgretplot=(
            5, 11), long_short=False, group_neutral=False, by_group=True)
        create_event_returns_tear_sheet(factor_data, self.prices, avgretplot=(
            5, 11), long_short=True, group_neutral=False, by_group=True)
        create_event_returns_tear_sheet(factor_data, self.prices, avgretplot=(
            5, 11), long_short=False, group_neutral=True, by_group=True)

    @parameterized.expand([((6, 8), False),
                           ((6, 8), False),
                           ((6, 3), True),
                           ((6, 3), True),
                           ((0, 3), False),
                           ((3, 0), True)])
    def test_create_event_study_tear_sheet(
            self, avgretplot, filter_zscore):
        """
        Test no exceptions are thrown
        """
        factor = DataFrame(index=self.dr2, columns=self.tickers,
                           data=[[1, nan, nan, nan, nan, nan],
                                 [4, nan, nan, 7, nan, nan],
                                 [nan, nan, nan, nan, nan, nan],
                                 [nan, 3, nan, 2, nan, nan],
                                 [1, nan, nan, nan, nan, nan],
                                 [nan, nan, 2, nan, nan, nan],
                                 [nan, nan, nan, 2, nan, nan],
                                 [nan, nan, nan, 1, nan, nan],
                                 [2, nan, nan, nan, nan, nan],
                                 [nan, nan, nan, nan, 5, nan],
                                 [nan, nan, nan, 2, nan, nan],
                                 [nan, nan, nan, nan, nan, nan],
                                 [2, nan, nan, nan, nan, nan],
                                 [nan, nan, nan, nan, nan, 5],
                                 [nan, nan, nan, 1, nan, nan],
                                 [nan, nan, nan, nan, 4, nan],
                                 [5, nan, nan, 4, nan, nan],
                                 [nan, nan, nan, 3, nan, nan],
                                 [nan, nan, nan, 4, nan, nan],
                                 [nan, nan, 2, nan, nan, nan],
                                 [5, nan, nan, nan, nan, nan],
                                 [nan, 1, nan, nan, nan, nan],
                                 [nan, nan, nan, nan, 4, nan],
                                 [0, nan, nan, nan, nan, nan],
                                 [nan, 5, nan, nan, nan, 4],
                                 [nan, nan, nan, nan, nan, nan],
                                 [nan, nan, 5, nan, nan, 3],
                                 [nan, nan, 1, 2, 3, nan],
                                 [nan, nan, nan, 5, nan, nan],
                                 [nan, nan, 1, nan, 3, nan]]).stack()

        factor_data = get_clean_factor_and_forward_returns(
            factor, self.prices, bins=1, quantiles=None, periods=(
                1, 2), filter_zscore=filter_zscore)

        create_event_study_tear_sheet(
            factor_data, self.prices, avgretplot=avgretplot)
