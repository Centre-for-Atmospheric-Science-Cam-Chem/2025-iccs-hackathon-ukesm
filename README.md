# 2025-iccs-hackathon-ukesm
For hackathon effort 11 Jul 2025 ICCS summer school, relevant to UKESM evaluation next week

## Overall aim

The UK Met Office earth system model (UKESM) will be one of many
models used to predict future Earth behaviour for the IPCC
Assessment Report 7.

There is a hackathon at Reading to evaluate the UKESM 1.3 output
to discuss its output quality currently and what variant should
be taken forward for this purpose. To decide that, we need to compare
the model predictions against past observations of the real
atmosphere.

Today we have some model output from UKESM 1.3 (model run
`u-dp226`) in NetCDF format, gridded as a function of
(time, latitude, longitude, model level). This data is supplied
separately as it is too large for GitHub.

We also have some observational datasets which some more detailed
notes about will be added below.



## Observational datasets

### BodekerScientific_Vertical_Ozone

From `ncdump -h` this dataset has:
```
dimensions:
        time = 456 ;
        latitude = 36 ;
        level = 70 ;
...
o3_mean:units = "mole mole^-1" ;
```
The UKESM output is in _mass_ mixing ratio, so a conversion is neeeded to
_molar_ mixing ratio to compare to this.
Also the levels will not be the same -- we could average or sum over levels
initially to get something comparable.
