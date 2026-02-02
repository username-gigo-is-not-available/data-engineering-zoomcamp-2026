import click
import typing

def dataset_options(function: typing.Callable) -> typing.Callable:
    options: list[click.FC] = [

    click.option('--dataset_type', type=click.Choice(['green', 'yellow']), required=True,
                  help='Type of taxi dataset (green or yellow)'),
    click.option('--year', type=click.IntRange(2019, 2021), required=True, help='Year of the data'),
    click.option('--month', type=click.IntRange(1, 12), required=True, help='Month of the data'),
    click.option('--chunk_size', type=int, required=True, help='Chunk size for processing'),

    ]
    for option in reversed(options):
        function = option(function)
    return function

