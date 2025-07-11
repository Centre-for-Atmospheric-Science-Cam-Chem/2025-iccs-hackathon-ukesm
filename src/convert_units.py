#!/bin/env python

"""Utility to convert units in NetCDF file to allow comparison with another
file. E.g. from mass mixing ratio to Dobson Units"""

import argparse
import iris


def main(args):
    """Main entry point"""

    print(f"Attempting to load file: {args.input_file}")
    cubelist = iris.load(args.input_file)

    air_mass_cube_kg_cell = get_cube_by_longname_fragment(cubelist, "AIR MASS DIAGNOSTIC (WHOLE")

    O3_MMR_cube_proportion = get_cube_by_longname_fragment(cubelist, "O3")

    # Build up version of data in new units. Doesn't seem to work using
    # arithmetic operators directly with cube objects, so going for underlying
    # data arrays instead. Start with copy (or is it a reference?)
    O3_mass_cube_kg_cell = O3_MMR_cube_proportion

    # Convert from mass mixing ratio (unitless) to mass per model cell (kg)
    O3_mass_cube_kg_cell.data *= air_mass_cube_kg_cell.data
    
    # Sum all of the model cells vertically in each longitude/latitude patch
    collapse_coords=['atmosphere_hybrid_height_coordinate']
    O3_mass_cube_kg_column = O3_mass_cube_kg_cell.collapsed(collapse_coords,
                                                            iris.analysis.SUM)
    
    # Convert from total mass in cell (which may be of order 100km * 100km)
    # to mass per unit area
    cell_areas_m2 = iris.analysis.cartography.area_weights(O3_mass_cube_kg_column)
    O3_mass_cube_kg_m2 = O3_mass_cube_kg_column / cell_areas_m2

    # Convert from mass to a volume at standard temperature and pressure
    standard_T_K = (273.15 + 25)
    standard_p_Pa = 101325
    molar_gas_const_J_K_mol = 8.314
    molar_mass_O3_g_mol = 3 * 16.0 # Approx from molecular formula
    molar_mass_O3_kg_mol = molar_mass_O3_g_mol * 1e-3

    # pV = nRT           where n = num mols
    #  n = m / M         where m = atual mass, M = relative molar mass
    # --> V = ((m/M) RT) / p   
    num_mols_column_per_m2 = O3_mass_cube_kg_m2 / molar_mass_O3_kg_mol
    volume_column_m3_per_m2 = ((num_mols_column_per_m2 * molar_gas_const_J_K_mol * standard_T_K)
                                  / standard_p_Pa)
    
    # So we have the 'volume per unit area' which has dimensions of length,
    # i.e. the equivalent thickness of pure O3 in the column compressed to standard T & p
    # Dobson Units are just that expressed in units of 10 um (or 1e5 metres).
    # We should get values of about 300 (i.e. 3 mm or 0.003 m) according to:
    # https://en.wikipedia.org/wiki/Dobson_unit
    volume_column_DU = volume_column_m3_per_m2 * 1e5

    print(f"Writing output to {args.output_file}")
    iris.save(volume_column_DU, args.output_file)

    print("All done")


def get_cube_by_longname_fragment(cubelist, name_fragment):
    """Find the one and only cube in the list whose long name contains the provided
    fragment, else error"""

    matching_cubes = []
    for cube in cubelist:
        if cube.long_name and name_fragment in cube.long_name:
            matching_cubes.append(cube)
    if len(matching_cubes) == 0:
        raise ValueError(f"No cubes match '{name_fragment}'")
    elif len(matching_cubes) > 1:
        matching_names = [cube.long_name for cube in matching_cubes]
        raise ValueError(f"All of these cubes match '{name_fragment}': {matching_names}")
    else:
        return matching_cubes[0]


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
