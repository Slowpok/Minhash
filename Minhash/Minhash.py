from random import shuffle
import torch
import env
import dao
import pickle
from tqdm import tqdm
import global_variable
import processing_levels
import Ext_func

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def shingling(text: str, k: int):
    shingle_set = []
    if len(text) == 0:
        return shingle_set
    elif len(text) == 1:
        shingle_set.append(text)
    else:
        for i in range(len(text) - k + 1):
            shingle_set.append(text[i:i+k])

    return set(shingle_set)


def shingling_list(k: int):
    # shingle_list = []
    # all_shingle_list = []
    list_of_text = []
    if not global_variable.reanimate:
        global_variable.shingle_list = []
        global_variable.all_shingles = []
        processing_levels.levels["shingling_list"] = 0
        list_of_text = global_variable.list_in_ordnund

    elif not processing_levels.steps['shingling_list'] and global_variable.reanimate:
        lev = processing_levels.levels["shingling_list"]
        list_of_text = global_variable.list_in_ordnund[lev::]

    for value in tqdm(list_of_text):
        list_shin = shingling(value, k)
        global_variable.shingle_list.append(list(list_shin))
        global_variable.all_shingles.extend(list_shin)
        processing_levels.levels["shingling_list"] += 1

    processing_levels.steps['shingling_list'] = True

    # return all_shingle_list, shingle_list


def onehot(vocab: list, shingle_text: list):
    return [1 if x in shingle_text else 0 for x in vocab]


def list_of_onehot_from_list_of_shingles():
    # list_of_one_hot = []
    shingle_list = []
    if not global_variable.reanimate:
        global_variable.list_of_onehot = []
        shingle_list = global_variable.shingle_list
        processing_levels.levels['list_of_onehot'] = 0
    elif not processing_levels.steps['list_of_onehot'] and global_variable.reanimate:
        lev = processing_levels.levels['list_of_onehot']
        shingle_list = global_variable.shingle_list[lev::]

    for value in tqdm(shingle_list):
        global_variable.list_of_onehot.append([1 if x in value else 0 for x in global_variable.vocab])
        processing_levels.levels['list_of_onehot'] += 1

    processing_levels.steps['list_of_onehot'] = True
    # return list_of_one_hot


def create_hash_queue(num: int):
    assert env.count_shuffle != 0
    assert num != 0
    c_shuffle = 0

    if not global_variable.reanimate:
        global_variable.hash_func = []
        c_shuffle = env.count_shuffle
        processing_levels.levels['create_hash_queue'] = 0
    elif not processing_levels.steps['create_hash_queue'] and global_variable.reanimate:
        c_shuffle = env.count_shuffle - processing_levels.levels["create_hash_queue"]

    for i in range(c_shuffle):
        queue = list(range(1, num + 1))
        shuffle(queue)
        global_variable.hash_func.append(queue)
        processing_levels.levels["create_hash_queue"] += 1

    with open("hash_queue", "wb") as file:
        pickle.dump(global_variable.hash_func, file)

    processing_levels.steps['create_hash_queue'] = True


def create_hash(vector: list, hash_func: list):
    signature = []
    for func in hash_func:
        for i in range(1, len(func) + 1):
            idx = func.index(i)
            signature_val = vector[idx]
            if signature_val == 1:
                signature.append(idx)
                break
    return signature


def list_of_hashes():
    # list_of_sign = []
    list_of_onehot = []
    if not global_variable.reanimate:
        global_variable.list_of_hash = []
        processing_levels.levels['list_of_hashes'] = 0
        list_of_onehot = global_variable.list_of_onehot
    elif not processing_levels.steps['list_of_hashes'] and global_variable.reanimate:
        lev = processing_levels.levels['list_of_hashes']
        list_of_onehot = global_variable.list_of_onehot[lev::]

    for item in tqdm(list_of_onehot):
        global_variable.list_of_hash.append(create_hash(item, global_variable.hash_func))
        processing_levels.levels['list_of_hashes'] += 1

    processing_levels.steps['list_of_hashes'] = True
    # return list_of_sign



def jaccard_distance(x, y):
    x = set(x)
    y = set(y)
    return len(x.intersection(y)) / len(x.union(y))


def split_vector(signature, b):
    assert len(signature) % b == 0
    r = int(len(signature)/b)

    subvecs = []
    for i in range(0, len(signature), r):
        subvecs.append(signature[i:i+r])

    return subvecs


def split_list_of_vectors():
    # split_list_one_hot = []
    list_of_hash = []
    if not global_variable.reanimate:
        global_variable.split_list_hashes = []
        processing_levels.levels['split_list_of_hashes'] = 0
        list_of_hash = global_variable.list_of_hash
    elif not processing_levels.steps['split_list_of_vectors'] and global_variable.reanimate:
        lev = processing_levels.levels['split_list_of_hashes']
        list_of_hash = global_variable.list_of_hash[lev::]

    for i in tqdm(list_of_hash):
        global_variable.split_list_hashes.append(split_vector(i, env.len_of_buck))
        processing_levels.levels['split_list_of_hashes'] += 1

    processing_levels.steps['split_list_of_vectors'] = True
    # return split_list_one_hot


def catch_coincidences_idx(split_list_one_hot, idx=0):
    list_idxs = []
    req = split_list_one_hot[idx]
    for i in range(0, len(split_list_one_hot)):
        if i == idx:
            continue
        for a, b in zip(req, split_list_one_hot[i]):
            if a == b:
                list_idxs.append(i)
    return list_idxs


def catch_coincidences_element_id(split_list_one_hot, id_list, idx=0):
    list_id = []
    req = split_list_one_hot[idx]
    for i in range(0, len(split_list_one_hot)):
        # if i == idx:
        #     continue
        for a, b in zip(req, split_list_one_hot[i]):
            if a == b and id_list[i] not in list_id:
                list_id.append(id_list[i])
    return list_id


def strings_comparison(string1: str, string2: str):
    shin_str1 = shingling(string1, 2)
    shin_str2 = shingling(string2, 2)
    shin_list1 = list(shin_str1)
    shin_list2 = list(shin_str2)

    vocab = list(shin_str1.union(shin_str2))

    onehot_str1 = onehot(vocab, shin_list1)
    onehot_str2 = onehot(vocab, shin_list2)

    hash_func = create_hash_queue(len(vocab))
    hash_str1 = create_hash(onehot_str1, hash_func)
    hash_str2 = create_hash(onehot_str2, hash_func)

    print(jaccard_distance(hash_str1, hash_str2))


def collect_all_buckets():
    # bucket_list = []
    len_split_list_hashes = 0
    if not global_variable.reanimate:
        global_variable.buckets = []
        processing_levels.levels['collect_all_buckets'] = 0
        len_split_list_hashes = len(global_variable.split_list_hashes)
    elif not processing_levels.steps['collect_all_buckets'] and global_variable.reanimate:
        lev = processing_levels.levels['collect_all_buckets']
        len_split_list_hashes = len(global_variable.split_list_hashes[lev::])

    for i in tqdm(range(len_split_list_hashes)):
        global_variable.buckets.append(catch_coincidences_element_id(global_variable.split_list_hashes, global_variable.id_list, i))
        processing_levels.levels['collect_all_buckets'] += 1
        processing_levels.steps['collect_all_buckets'] = True
    # return bucket_list


def mass_string_comparison(list_of_strings: list):
    all_shingles, list_of_shingles = shingling_list(list_of_strings, 2)
    vocab = list(set(all_shingles))

    list_of_onehot = list_of_onehot_from_list_of_shingles(list_of_shingles, vocab)
    hash_func = create_hash_queue(len(vocab))
    list_of_hash = list_of_hashes(list_of_onehot, hash_func)

    split_list_hashes = split_list_of_vectors(list_of_hash)
    idxs = catch_coincidences_idx(split_list_hashes)

    return ranging_coincidences(list_of_hash, idxs)


def get_past_data(cursor):
    past_data = dao.select_all_entry(cursor)
    all_id = [y[0] for y in past_data]
    all_hash = [y[1] for y in past_data]
    all_split_hash = [y[2] for y in past_data]
    return all_id, all_hash, all_split_hash


def hashing_and_bucking(update=False, cursor=None):

    print("shingling in process")
    # all_shingles, list_of_shingles = shingling_list(list_of_strings, 2)
    if not global_variable.reanimate or (not processing_levels.steps['shingling_list'] and global_variable.reanimate):
        shingling_list(2)
        global_variable.reanimate = False

    print("shingling done")

    print("create_hash_queue in process")

    if not update:
        global_variable.vocab = list(set(global_variable.all_shingles))
        if not global_variable.reanimate or (not processing_levels.steps['create_hash_queue'] and global_variable.reanimate):
            create_hash_queue(len(global_variable.vocab))
            global_variable.reanimate = False
            with open("vocab", "wb") as file:
                pickle.dump(global_variable.vocab, file)
    else:
        with open("vocab", "rb") as file:
            global_variable.vocab = pickle.load(file)
        with open("hash_queue", "rb") as file:
            global_variable.hash_func = pickle.load(file)

    print("create_hash_queue done")

    print("list of one_hot in process")

    if not global_variable.reanimate or (not processing_levels.steps['list_of_onehot'] and global_variable.reanimate):
        list_of_onehot_from_list_of_shingles()
        global_variable.reanimate = False

    print("list_of_onehot done")

    print("list_of_hashes in process")

    if not global_variable.reanimate or (not processing_levels.steps['list_of_hashes'] and global_variable.reanimate):
        list_of_hashes()
        global_variable.reanimate = False

    print("list_of_hashes done")
    print("split_list_of_vectors in process")

    if not global_variable.reanimate or (not processing_levels.steps['split_list_of_vectors']
                                         and global_variable.reanimate):
        split_list_of_vectors()
        global_variable.reanimate = False

    print("split_list_of_vectors done")

    if update:
        print("prepare updating data")
        past_id_list, past_list_hashes, past_split_list_hashes = get_past_data(cursor)
        global_variable.split_list_hashes.extend(past_split_list_hashes)
        global_variable.id_list.extend(past_id_list)
        global_variable.list_of_hash.extend(past_list_hashes)
        print("prepare done")

    print("collect buckets in process")
    if not global_variable.reanimate or (not processing_levels.steps['collect_all_buckets']
                                         and global_variable.reanimate):
        collect_all_buckets()
        global_variable.reanimate = False
        print("buckets done")


    # return global_variable.id_list, list_of_hash, split_list_hashes, buckets


def ranging_coincidences(list_of_hash, idxs):
    req = list_of_hash[0]
    res_dict = dict()

    for i in idxs:
        res_dict[i] = jaccard_distance(req, list_of_hash[i])

    return res_dict


def strings_comparison_with_numbers(string1: str, string2: str, numbers1: str, numbers2: str):
    shin_str1 = shingling(string1, 2)
    shin_str2 = shingling(string2, 2)
    shin_num1 = shingling(numbers1, 2)
    shin_num2 = shingling(numbers2, 2)

    shin_list_str1 = list(shin_str1)
    shin_list_str2 = list(shin_str2)

    shin_list_num1 = list(shin_num1)
    shin_list_num2 = list(shin_num2)

    vocab = list(shin_str1.union(shin_str2).union(shin_num1).union(shin_num2))

    onehot_str1 = onehot(vocab, shin_list_str1)
    onehot_str2 = onehot(vocab, shin_list_str2)
    onehot_num1 = onehot(vocab, shin_list_num1)
    onehot_num2 = onehot(vocab, shin_list_num2)

    create_hash_queue(len(vocab))

    hash_str1 = create_hash(onehot_str1, global_variable.hash_func)
    hash_str2 = create_hash(onehot_str2, global_variable.hash_func)
    hash_num1 = create_hash(onehot_num1, global_variable.hash_func)
    hash_num2 = create_hash(onehot_num2, global_variable.hash_func)

    jac_str = jaccard_distance(hash_str1, hash_str2)
    jac_num = jaccard_distance(hash_num1, hash_num2)

    print(jaccard_distance(hash_str1, hash_str2))









