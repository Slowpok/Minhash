from random import shuffle
import torch
import env
import dao
import pickle
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


def shingling_list(list_of_text: list, k: int):
    shingle_list = []
    all_shingle_list = []
    for value in list_of_text:
        list_shin = shingling(value, k)
        shingle_list.append(list(list_shin))
        all_shingle_list.extend(list_shin)

    return all_shingle_list, shingle_list


def onehot(vocab: list, shingle_text: list):
    return [1 if x in shingle_text else 0 for x in vocab]


def list_of_onehot_from_list_of_shingles(list_of_shingles, vocab):
    list_of_one_hot = []
    for value in list_of_shingles:
        list_of_one_hot.append([1 if x in value else 0 for x in vocab])

    return list_of_one_hot


def create_hash_queue(num: int):
    assert env.count_shuffle != 0
    assert num != 0
    res_queue = []

    for i in range(env.count_shuffle):
        queue = list(range(1, num + 1))
        shuffle(queue)
        res_queue.append(queue)

    with open("hash_queue", "wb") as file:
        pickle.dump(res_queue, file)

    return res_queue


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


def list_of_hashes(list_of_onehot, hash_func):
    list_of_sign = []
    for item in list_of_onehot:
        list_of_sign.append(create_hash(item, hash_func))

    return list_of_sign



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


def split_list_of_vectors(list_of_onehot):
    split_list_one_hot = []
    for i in list_of_onehot:
        split_list_one_hot.append(split_vector(i, env.len_of_buck))

    return split_list_one_hot


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


def collect_all_buckets(splt_hash, id_list):

    bucket_list = []
    for i in range(len(splt_hash)):
        bucket_list.append(catch_coincidences_element_id(splt_hash, id_list, i))

    return bucket_list



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


def hashing_and_bucking(list_of_strings, id_list, update=False, cursor=None):
    all_shingles, list_of_shingles = shingling_list(list_of_strings, 2)
    if not update:
        vocab = list(set(all_shingles))
        hash_func = create_hash_queue(len(vocab))
        with open("vocab", "wb") as file:
            pickle.dump(vocab, file)
    else:
        with open("vocab", "rb") as file:
            vocab = pickle.load(file)
        with open("hash_queue", "rb") as file:
            hash_func = pickle.load(file)

    list_of_onehot = list_of_onehot_from_list_of_shingles(list_of_shingles, vocab)
    print("list_of_onehot done")

    # if not update:
    #     hash_func = create_hash_queue(len(vocab))
    # else:
    #     with open("hash_queue", "rb") as file:
    #         hash_func = pickle.load(file)

    print("create_hash_queue done")
    list_of_hash = list_of_hashes(list_of_onehot, hash_func)
    print("list_of_hashes done")
    split_list_hashes = split_list_of_vectors(list_of_hash)
    print("split_list_of_vectors done")
    if update:
        past_id_list, past_list_hashes, past_split_list_hashes = get_past_data(cursor)
        split_list_hashes.extend(past_split_list_hashes)
        id_list.extend(past_id_list)
        list_of_hash.extend(past_list_hashes)

    buckets = collect_all_buckets(split_list_hashes, id_list)

    print("buckets done")

    return id_list, list_of_hash, split_list_hashes, buckets



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

    hash_func = create_hash_queue(len(vocab))

    hash_str1 = create_hash(onehot_str1, hash_func)
    hash_str2 = create_hash(onehot_str2, hash_func)
    hash_num1 = create_hash(onehot_num1, hash_func)
    hash_num2 = create_hash(onehot_num2, hash_func)

    jac_str = jaccard_distance(hash_str1, hash_str2)
    jac_num = jaccard_distance(hash_num1, hash_num2)

    print(jaccard_distance(hash_str1, hash_str2))









