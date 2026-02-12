import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.backtest_strategy import backtest_strategy
from code.combine_trending_coins import combine_trending_coins
from code.develop_trading_strategy import develop_trading_strategy
from code.download_historical_prices import download_historical_prices
from code.download_historical_volumes import download_historical_volumes
from code.gather_data import gather_data
from code.hedge_strategy import hedge_strategy
from code.identify_price_trends import identify_price_trends
from code.identify_volume_trends import identify_volume_trends
from code.launch_strategy import launch_strategy
from code.perform_statistical_analysis import perform_statistical_analysis
from code.preprocess_price_data import preprocess_price_data
from code.preprocess_volume_data import preprocess_volume_data
from code.validate_strategy import validate_strategy

# Get async mode from environment variable or default to False
ASYNC_MODE = os.environ.get('ASYNC_MODE', '').lower() in ('true', '1', 'yes', 'y')

def make_async(func):
    """Convert a synchronous function to an asynchronous function.

    If the function is already asynchronous, return it unchanged.
    If the function is synchronous, wrap it in an async function.
    """
    # If it's already a coroutine function, return it as is
    if inspect.iscoroutinefunction(func):
        return func

    # Otherwise, wrap it as an async function
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return async_wrapper

backtest_strategy_async = make_async(backtest_strategy)
combine_trending_coins_async = make_async(combine_trending_coins)
develop_trading_strategy_async = make_async(develop_trading_strategy)
download_historical_prices_async = make_async(download_historical_prices)
download_historical_volumes_async = make_async(download_historical_volumes)
gather_data_async = make_async(gather_data)
hedge_strategy_async = make_async(hedge_strategy)
identify_price_trends_async = make_async(identify_price_trends)
identify_volume_trends_async = make_async(identify_volume_trends)
launch_strategy_async = make_async(launch_strategy)
perform_statistical_analysis_async = make_async(perform_statistical_analysis)
preprocess_price_data_async = make_async(preprocess_price_data)
preprocess_volume_data_async = make_async(preprocess_volume_data)
validate_strategy_async = make_async(validate_strategy)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: gather_data
    async def run_gather_data():
        # Call the async version of gather_data with results from dependencies
        return await gather_data_async(user_input)

    # Run level 0 nodes in parallel
    results['gather_data'] = await run_gather_data()

    # Level 1: download_historical_prices, download_historical_volumes
    async def run_download_historical_prices():
        # Call the async version of download_historical_prices with results from dependencies
        return await download_historical_prices_async(results['gather_data'])

    async def run_download_historical_volumes():
        # Call the async version of download_historical_volumes with results from dependencies
        return await download_historical_volumes_async(results['gather_data'])

    # Run level 1 nodes in parallel
    level_1_results = await asyncio.gather(run_download_historical_prices(), run_download_historical_volumes())
    results['download_historical_prices'] = level_1_results[0]
    results['download_historical_volumes'] = level_1_results[1]

    # Level 2: preprocess_volume_data, preprocess_price_data
    async def run_preprocess_volume_data():
        # Call the async version of preprocess_volume_data with results from dependencies
        return await preprocess_volume_data_async(results['download_historical_volumes'])

    async def run_preprocess_price_data():
        # Call the async version of preprocess_price_data with results from dependencies
        return await preprocess_price_data_async(results['download_historical_prices'])

    # Run level 2 nodes in parallel
    level_2_results = await asyncio.gather(run_preprocess_volume_data(), run_preprocess_price_data())
    results['preprocess_volume_data'] = level_2_results[0]
    results['preprocess_price_data'] = level_2_results[1]

    # Level 3: perform_statistical_analysis
    async def run_perform_statistical_analysis():
        # Call the async version of perform_statistical_analysis with results from dependencies
        return await perform_statistical_analysis_async(results['preprocess_price_data'], results['preprocess_volume_data'])

    # Run level 3 nodes in parallel
    results['perform_statistical_analysis'] = await run_perform_statistical_analysis()

    # Level 4: identify_volume_trends, identify_price_trends
    async def run_identify_volume_trends():
        # Call the async version of identify_volume_trends with results from dependencies
        return await identify_volume_trends_async(results['preprocess_volume_data'], results['perform_statistical_analysis'])

    async def run_identify_price_trends():
        # Call the async version of identify_price_trends with results from dependencies
        return await identify_price_trends_async(results['preprocess_price_data'], results['perform_statistical_analysis'])

    # Run level 4 nodes in parallel
    level_4_results = await asyncio.gather(run_identify_volume_trends(), run_identify_price_trends())
    results['identify_volume_trends'] = level_4_results[0]
    results['identify_price_trends'] = level_4_results[1]

    # Level 5: combine_trending_coins
    async def run_combine_trending_coins():
        # Call the async version of combine_trending_coins with results from dependencies
        return await combine_trending_coins_async(results['identify_price_trends'], results['identify_volume_trends'])

    # Run level 5 nodes in parallel
    results['combine_trending_coins'] = await run_combine_trending_coins()

    # Level 6: develop_trading_strategy
    async def run_develop_trading_strategy():
        # Call the async version of develop_trading_strategy with results from dependencies
        return await develop_trading_strategy_async(results['combine_trending_coins'])

    # Run level 6 nodes in parallel
    results['develop_trading_strategy'] = await run_develop_trading_strategy()

    # Level 7: backtest_strategy, hedge_strategy
    async def run_backtest_strategy():
        # Call the async version of backtest_strategy with results from dependencies
        return await backtest_strategy_async(results['develop_trading_strategy'])

    async def run_hedge_strategy():
        # Call the async version of hedge_strategy with results from dependencies
        return await hedge_strategy_async(results['develop_trading_strategy'])

    # Run level 7 nodes in parallel
    level_7_results = await asyncio.gather(run_backtest_strategy(), run_hedge_strategy())
    results['backtest_strategy'] = level_7_results[0]
    results['hedge_strategy'] = level_7_results[1]

    # Level 8: validate_strategy
    async def run_validate_strategy():
        # Call the async version of validate_strategy with results from dependencies
        return await validate_strategy_async(results['backtest_strategy'], results['hedge_strategy'])

    # Run level 8 nodes in parallel
    results['validate_strategy'] = await run_validate_strategy()

    # Level 9: launch_strategy
    async def run_launch_strategy():
        # Call the async version of launch_strategy with results from dependencies
        return await launch_strategy_async(results['validate_strategy'], results['hedge_strategy'])

    # Run level 9 nodes in parallel
    results['launch_strategy'] = await run_launch_strategy()

    # Return all results
    return results

def run_workflow_sync(user_input: str) -> Dict[str, Any]:
    """Synchronous wrapper around the async workflow execution."""
    return asyncio.run(run_workflow(user_input))

def main():
    """Main entry point.

    Handles arguments in the following priority:
    1. Command-line argument (sys.argv[1])
    2. If no argument, uses empty string as input but displays a warning.
    """
    # Get user input from command line or use empty string
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        # No input provided - display help message but continue with empty string
        print('Warning: No input provided. Using empty string as input.')
        print('For better results, provide an input argument:')
        print(f'  python {os.path.basename(__file__)} "your input text here"')
        print('Or use a file as input:')
        print(f'  python {os.path.basename(__file__)} "$(cat input.txt)"')
        user_input = ""

    print(f'Running workflow with input: {user_input}')

    # Run the workflow
    results = run_workflow_sync(user_input)

    # Print results
    try:
        # Convert results to JSON
        json_results = json.dumps(results, indent=2, default=str)
        print(json_results)
    except (TypeError, ValueError) as e:
        print(f'Results could not be converted to JSON: {e}')
        print(f'Raw results: {results}')

    return results

if __name__ == '__main__':
    main()
