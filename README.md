# Hyde
Process selected data from the [HYDE](https://themasites.pbl.nl/tridion/en/themasites/hyde/) model and store in easy to use file formats.

## What is Hyde?
HYDE presents (gridded) time series of population and land use for the last 12,000 years ! It also presents various other indicators such as GDP, value added, livestock, agricultural areas and yields, private consumption, greenhouse gas emissions and industrial production data, but only for the last century.

## Why this repo?
Hyde is available for download as zipped ascii files from an FTP server. For easy analysis, other file formats are preferred. This repository contains a few scripts to convert the files to geotiffs on Amazon S3 and ImageCollections on Google Earthengine. 


## Disclaimer and credit
The author of this repo is not associated with the HYDE project team. Scripts might contain errors and none of this work is reviewed. Please use with caution. See the Hyde [website](https://themasites.pbl.nl/tridion/en/themasites/hyde/) to provide appropriate credit

## Data download

Accessed on 2019 07 22 10:47 CEST  
FTP: `ftp.pbl.nl/hyde/`

Only the following data was downloaded:
`/hyde/hyde3.2/*/zip/*`

this first version includes baseline only.

Upzipped to `unzipped` folder and uploaded to S3.

Release [file](https://raw.githubusercontent.com/rutgerhofste/hyde/master/readme_release_HYDE3.2.1.txt)

Files stored on `s3://wri-projects/Aqueduct30/rawData/Hyde/`

## Data structure

### Population (pop)

| short      | description                                                                             |
|------------------|--------------------------------------------------------------------------------------|
|opc|population counts, in inhabitants/gridcell |
|opd|population density, in inhabitants/km2 per gridcell |
|urc|rural population counts, in inh/gridcell |
|rbc|urban population counts, in inh/gridcell |
|opp|total built-up area, such as towns, cities, etc, in km2 per grid cell |

###  Land use (lu)




## EarthEngine


var icUniques = ic.distinct(["property"]).aggregate_array("property")



