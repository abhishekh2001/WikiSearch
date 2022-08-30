from collections import defaultdict
import time
import config
import heapq
import os


def combine(write_loc):
    if not os.path.exists(write_loc):
        os.mkdir(write_loc)

    inv_files = [os.path.join(config.INTER, x) for x in os.listdir(config.INTER)
                    if 'idx' in x]
    dict_fp = [open(fname) for fname in inv_files]
    open_status = [True for _ in range(len(inv_files))]

    inv_dict = defaultdict()
    tot_tokens = 0  # number of tokens encountered
    fnum = 0  # number of files

    print("Found", len(inv_files), "files")
    heap = []  #  [word, filepointer, value/string]
    for i in range(len(dict_fp)):
        l = dict_fp[i].readline().strip().strip('\n')
        w, v = l.split(':')
        val = [w, i, v]
        heapq.heappush(heap, val)

    st = time.time()
    # print("init heap:", heap)
    while len(heap) and any(open_status):
        target_w = heap[0][0]
        target_v = ''

        # print("target word: ", target_w)

        while len(heap) and heap[0][0] == target_w:
            top = heapq.heappop(heap)
            target_v += top[2]

            # print("Top of heap: ", top)
            # print("\theap: ", heap)

            i = top[1]
            
            if open_status[i]:
                l = dict_fp[i].readline()
                # print("Found in file ", i, " line: ", l)
                if l == '':
                    open_status[i] = False
                else:
                    l = l.strip().strip('\n')
                    w, v = l.split(':')
                    val = [w, i, v]
                    heapq.heappush(heap, val)

        inv_dict[target_w] = target_v
        tot_tokens += 1
        if len(inv_dict) >= config.NUM_FINAL_TOKENS_PF:
            dest = os.path.join(write_loc, f"final{fnum}.txt")
            print(f"Writing to file {dest}")

            with open(dest, "r") as f:
                for w, v in inv_dict.items():
                    f.write(f"{w}:{v}\n")
            fnum += 1
            inv_dict = defaultdict()

    if len(inv_dict):
        dest = os.path.join(write_loc, f"final{fnum}.txt")
        print(f"Writing to file {dest}")

        with open(dest, 'r') as f:
            for w, v in inv_dict.items():
                f.write(f"{w}:{v}\n")
        fnum += 1
        inv_dict = defaultdict()

    print("Merged in", time.time() - st)

    return tot_tokens, fnum
