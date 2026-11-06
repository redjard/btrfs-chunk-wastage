# Btrfs Chunk Wastage Histogram

### Usage
`btrfs-chunk-wastage.py [path]`
- `[path]` Defaults to `/`

Note there is currently no support for plotting metadata or system chunks (would be easy to add).

### Dependencies
python3, python btrfs module

### Explanation
Btrfs allocates itself (usually) 1 GiB sized chunks of storage space to store files on disk. As files are created, resized, and deleted, those chunks may not get filled one after another, Btrfs may accumulate partially filled chunks.
This can cause some problems, so there are commands to "balance" partially filled chunks, forcing their data to get moved into other, usually partially filled chunks.
For example `btrfs balance start -dusage=30 /` will move all chunks with less than 30% space utilization, ideally leaving few or no blocks under 30% usage afterwards.

But when typing out such a command, it's hard to know how many chunks will be moved, and how much space will be saved. Will usage=30 be enough or should you do usage=60? When do diminishing returns kick in? How many chunks will need to be rewritten? And what *is* the current state of the file system?

This script will generate a histogram that can answer all those questions.

![rm3](https://github.com/user-attachments/assets/04b1c325-5a25-415e-ba54-370f9c8217f4)

![rh](https://github.com/user-attachments/assets/b6a98dec-3a8b-4e7b-b2ce-0e69d9be4c72)

The histogram will attempt to match your terminal's width.

### Update notes
The first version of this script gave some estimates. All numbers in the current script are exact.