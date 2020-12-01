# 3D Soil Mask

## Inputs
A point cloud (x,y,z) ply file.

## Outputs
The portion above a large consistent surface in the cloud.

## Arguments and Flags
* **Positional Arguments:** 
    * **Path to a ply file of a full 3D Scanner pass:** 'full_pass_ply'
* **Optional Arguments:**
    * **Output Directory:** '-o', '--outdir', default = '3d_soil_mask'
    * **Output Filename:** 'f', '--filename', default = 'plants_no_soil'
    * **Slice size to take when clustering:** '-sl', '--slice_size', default = 0.02
    * **Estimated distance between points in a cluster:** '-eps', '--eps_num', default = 6
    * **Minimum points to make a cluster:** '-min_points, '--min_points', default = 200
    * **Percentage of the upper portion of the soil that is shown:** '-cutoff_percent', '--cutoff', default = 0.97

       
## Adapting the Script

This script could be used in any setting where the object you are interested in has a separation from a consistent and much larger surface under it in the point cloud.
                                        
## Example Deployment
```
./3d_soil_mask.py path_to_cloud.ply
```
