import sys
sys.path.append('O:\\code\\')  # 手动更改成代码存储路径

import utils_project_factor_test as utils_test
import pandas as pd
import numpy as np


if __name__ == '__main__':
    basic_path = 'O:\\data1\\hf_data_project\\'       # 基础数据存储路径
    factor_path = 'P:\\shentl\\project_code\\'      # 原始因子存储路径，手动更改
    sample_path = 'O:\\data1\\hf_data_project\\'
    start_date = 'date0000'
    end_date = 'date1258'

    pool_type = 'all_stk'                             # 指定股票池，默认all_stk
    ticker_set = pd.read_hdf(basic_path + 'ticker_set.h5')
    used_ticker = ticker_set[pool_type]

    industry = pd.read_hdf(basic_path + 'industry.h5').reindex(index=used_ticker)  # 行业信息
    # 市值因子
    size = pd.read_hdf(basic_path + 'size.h5').reindex(columns=used_ticker).truncate(start_date, end_date)
    # 5日收益标签
    ret_label = pd.read_hdf(basic_path + 'ret_label.h5').reindex(columns=used_ticker).truncate(start_date, end_date)
    # 每日收益
    daily_ret = pd.read_hdf(basic_path + 'daily_ret.h5').reindex(columns=used_ticker).truncate(start_date, end_date)
    # 剔除部分股票
    valid_pool = pd.read_hdf(basic_path + 'valid_pool.h5').reindex(columns=used_ticker).truncate(
        start_date, end_date)

    long_ret_ori_pool = pd.read_hdf(basic_path + 'long_ret(%s).h5' % pool_type)      # 原有因子库的pnl日收益

    ##################
    # 测试因子
    ##################
    raw_factor = pd.read_hdf(sample_path+'sample_factor1.h5').reindex(columns=used_ticker).truncate(
        start_date, end_date)

    # 确保时间戳和股票池一致
    assert tuple(industry.index) == tuple(raw_factor.columns)
    assert (tuple(size.index) == tuple(raw_factor.index)) and \
           (tuple(size.columns) == tuple(raw_factor.columns))
    assert (tuple(ret_label.index) == tuple(raw_factor.index)) and \
           (tuple(ret_label.columns) == tuple(raw_factor.columns))
    assert (tuple(daily_ret.index) == tuple(raw_factor.index)) and \
           (tuple(daily_ret.columns) == tuple(raw_factor.columns))
    assert (tuple(valid_pool.index) == tuple(raw_factor.index)) and \
           (tuple(valid_pool.columns) == tuple(raw_factor.columns))

    # 因子预处理
    test_factor = utils_test.preproc_raw_factor(raw_factor, valid_pool, industry, size)

    # 因子测试
    ic_series = utils_test.factor_ic_test(test_factor, ret_label)
    factor_pnl = utils_test.factor_pnl_test(test_factor, daily_ret, ic_series.mean())
    test_summary = utils_test.get_factor_test_summary(ic_series, factor_pnl, long_ret_ori_pool)
    test_summary['coverage'] = (~ test_factor.isna()).mean(axis=1).mean()        # assert coverage > 0.7
    print(test_summary)