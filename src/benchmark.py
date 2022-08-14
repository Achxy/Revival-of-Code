from simplebenchmark import sync_benchmark


def advent_problem(func):
    return sync_benchmark()(func)
