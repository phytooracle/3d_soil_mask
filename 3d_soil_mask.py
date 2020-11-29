#!/usr/bin/env python3
"""
Author : Travis Simmons
Date   : 11/28/2020
Purpose: Segment out soil from pointclouds.
"""

import argparse
import os
import numpy as np
import open3d as o3d
import os.path
import statistics as stats


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description = '3d soil masking',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Positional Args
    parser.add_argument('full_pass_ply',
                        metavar='full_pass_ply',
                        type = str,
                        help='path to a ply file of a full 3d scanner pass')

    # Optional Args
    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory',
                        metavar='outdir',
                        type=str,
                        default='3d_soil_mask')

    parser.add_argument('-f',
                        '--filename',
                        help='Output filename',
                        metavar='filename',
                        type=str,
                        default='plants_no_soil')
    
    parser.add_argument('-sl',
                        '--slice_size',
                        help='Slice size to take when doing clustering',
                        metavar='slice_size',
                        type=float,
                        default= 0.02)

    parser.add_argument('-eps',
                        '--eps_num',
                        help='Estimated distance between points, smaller number makes it more restrictive',
                        metavar='eps_num',
                        type=int,
                        default= 6)

    parser.add_argument('-min_points',
                        '--min_points',
                        help='Minimum points to make a cluster',
                        metavar='min_points',
                        type=int,
                        default= 200)

    parser.add_argument('-cutoff_percent',
                        '--cutoff',
                        help='Controlls the percentage of the top of the soil and above that is shown',
                        metavar='cutoff',
                        type=float,
                        default= 0.97)

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Find just the plants, leave out the soil"""

    args = get_args()

    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)

    # Full Pass
    plant = args.full_pass_ply

    # ------------------------------------------------------
    # Slicing out a portion

    # Read .ply file
    pcd_whole = o3d.io.read_point_cloud(plant)
    # Convert open3d format to numpy array
    # Here, you have the point cloud in numpy format. 
    ar_whole_field = np.asarray(pcd_whole.points)

    # Slicing
    max_1 = max(ar_whole_field[:,1])
    min_1 = min(ar_whole_field[:,1])

    length = [max_1,min_1]
    yrange = (abs(max_1)-abs(min_1))*(args.slice_size)
    middle = stats.median(length)
    bound_1 = middle + yrange
    bound_2 = middle - yrange

    print(f'Max Y Value of Full PCD = {max_1}\nMin Y Value of Full PCD = {min_1}\nMiddle Y Value of Full PCD = {middle}')
    slice_of_whole = []

    for index, row in enumerate(ar_whole_field):
        if bound_1 > bound_2:
            if bound_1 > row[1] >  bound_2:
                slice_of_whole.append(row)

        if bound_2 > bound_1:
            if bound_2 > row[1] >  bound_1:
                slice_of_whole.append(row)
                
                
    pcd_slice = o3d.geometry.PointCloud()
    pcd_slice.points = o3d.utility.Vector3dVector(slice_of_whole)

    ar_slice = np.asarray(pcd_slice.points)


    # Writes out the slice for validation
    # o3d.io.write_point_cloud(NEED ARGUMENT FOR OPTIONAL WRITING, pcd_slice)

    #------------------------------------------------
    # Sending the slice to be clustered

    # Clustering
    labels = np.array(pcd_slice.cluster_dbscan(eps=args.eps_num, min_points=args.min_points, print_progress=True))

    max_label = labels.max()
    print(f"point cloud has {max_label + 1} clusters")

    l0 = []

    # Separating out the labels
    for index, row in enumerate(ar_slice):
        lab = labels[index]
        if lab == 0:
            l0.append(row)

    #---------------------------------
    # Getting the extent of the ground to crop out the plants

    pcd_ground = o3d.geometry.PointCloud()
    pcd_ground.points = o3d.utility.Vector3dVector(l0)
    ar_ground = np.asarray(pcd_ground.points) 
    # Extents for cropping
    max_0 = max(ar_ground[:,0])
    max_2 = max(ar_ground[:,2])
    min_0 = min(ar_ground[:,0])

    # Writes out the identified ground for validation
    # o3d.io.write_point_cloud(NEED ARGUMENT FOR OPTIONAL WRITING, pcd_ground)


    #-----------------------------------------------------
    # Cropping out the plants
    plant = []
    for i in ar_whole_field:
        if (min_0 < i[0] < max_0) and (i[2] > (max_2*args.cutoff)):
            plant.append(i)
    pcd_plant = o3d.geometry.PointCloud()
    pcd_plant.points = o3d.utility.Vector3dVector(plant)

    # Writes out just the plants for downstream analysis
    out_path = os.path.join(args.outdir, args.filename + '.ply')
    o3d.io.write_point_cloud(out_path, pcd_plant)




# --------------------------------------------------
if __name__ == '__main__':
    main()
