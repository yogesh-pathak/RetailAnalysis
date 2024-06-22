import pytest

from lib.ConfigReader import get_app_config
from lib.DataManipulation import filter_closed_orders, count_orders_state, filter_orders_generic
from lib.DataReader import read_customers, read_orders


def test_read_customers_df(spark):
    customers_count = read_customers(spark, 'LOCAL').count()
    assert customers_count == 12435


def test_read_orders_df(spark):
    orders_count = read_orders(spark, 'LOCAL').count()
    assert orders_count == 68884


@pytest.mark.transformation
def test_filter_closed_orders(spark):
    filtered_count = filter_closed_orders(read_orders(spark, 'LOCAL')).count()
    assert filtered_count == 7556


@pytest.mark.skip('work in progress')
def test_read_app_config(spark):
    config = get_app_config('LOCAL')
    assert config['orders.file.path'] == 'data/orders.csv'


@pytest.mark.transformation
def test_count_orders_state(spark, expected_results):
    customers_df = read_customers(spark, 'LOCAL')
    actual_results = count_orders_state(customers_df)
    assert actual_results.collect() == expected_results.collect()


@pytest.mark.skip
def test_check_closed_count(spark):
    orders_df = read_orders(spark, 'LOCAL')
    filtered_count = filter_orders_generic(orders_df, 'CLOSED').count()
    assert filtered_count == 7556


@pytest.mark.skip
def test_check_pending_payment_count(spark):
    orders_df = read_orders(spark, 'LOCAL')
    filtered_count = filter_orders_generic(orders_df, 'PENDING_PAYMENT').count()
    assert filtered_count == 15030


@pytest.mark.latest
@pytest.mark.parametrize(
    'status, count',
    [
        ('CLOSED', 7556),
        ('PENDING_PAYMENT', 15030),
        ('COMPLETE', 22900)
    ]
)
def test_check_count(spark, status, count):
    orders_df = read_orders(spark, 'LOCAL')
    filtered_count = filter_orders_generic(orders_df, status).count()
    assert filtered_count == count