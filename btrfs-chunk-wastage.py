#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser(description='Print a Histogram of how much space is wasted in total per Btrfs chunk utilization')
parser.add_argument('path', metavar='path', type=str, default="/", nargs='?', help='Pth to the filesystem (defaults to /)')
path = parser.parse_args().path

# # ensure root
# import os
# if os.getuid() != 0:
#     from elevate import elevate
#     elevate(graphical=False)

from bisect import bisect_right
import btrfs
import shutil

fs = btrfs.FileSystem(path)

try:
    blocks = ( fs.block_group(block.vaddr, block.length) for block in fs.chunks() )
    blocks = [ block for block in blocks if block.flags & btrfs.BLOCK_GROUP_TYPE_MASK == btrfs.BLOCK_GROUP_DATA ]
except PermissionError:
    print("Permission denied, can't load chunks data. Please run as root.")
    exit(1)

resolution = 20
extra_edges = (0.00001, 0.99999)
left_edges = sorted((*extra_edges, *( i/resolution for i in range(0,resolution+1)) ))

bins_saveable = [0]*len(left_edges)
bins_count    = [0]*len(left_edges)
for block in blocks:
    bin = bisect_right(left_edges, block.used/block.length) - 1
    bins_saveable[bin] += block.length-block.used
    bins_count[bin]    += 1

max_saveable = max(bins_saveable)
maxwidth = shutil.get_terminal_size((80, 0)).columns  # get term width, default to width 80

print(" Usage  | savable space (number of chunks)")
started = 0
for le, saveable, count in zip(left_edges,bins_saveable,bins_count):
    if not saveable and not started:
        continue
    started = 1
    
    bar = saveable/max_saveable * (maxwidth - 40) * 2  # 40 chars space for other stuff left and right. *2 cause we use half-width rendering
    bar = round(bar)
    
    if le < 1:
        print(f"{le*100:6.3f}% | {'█'*(bar//2)}{'▌'*(bar%2)}\t {btrfs.utils.pretty_size(saveable)} ({count})")
    else:
        print(f"100.00% | {'█'*(bar//2)}{'▌'*(bar%2)}\t {btrfs.utils.pretty_size(saveable)} ({count})")

print(f"Total savable {btrfs.utils.pretty_size(sum(bins_saveable))}")
