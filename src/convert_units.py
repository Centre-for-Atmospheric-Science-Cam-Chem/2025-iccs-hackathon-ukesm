#!/bin/env python

"""Utility to convert units in NetCDF file to allow comparison with another
file. E.g. from mass mixing ratio to Dobson Units"""

import argparse
import iris


def main(args):
    """Main entry point"""

    print(f"Attempting to load file: {args.input_file}")
    dataset = iris.load(args.input_file)

    # TODO useful work!
    
    print("All done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog="convert_units.py",
                    description="Changes units of model data to facilitate comparisons")
    
    parser.add_argument("-i", "--input-file",
                        required=True,
                        help="Input file to process")
    parser.add_argument("-o", "--output-file",
                        required=True,
                        help="Transformed output file")
    parser.add_argument("-f", "--format",
                        default="DU",
                        help="Units to convert to")
    
    args = parser.parse_args()

    main(args)
