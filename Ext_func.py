import pandas as pd
import String_methods
import Minhash
import env
import initialisation
import dao


def processing_file(filename):
    df = pd.read_csv(filepath_or_buffer=filename,
                     names=['element_id', 'request'], encoding='Windows-1251', delimiter=';')
    yyy = 0
    list_in_ordnund = []
    id_list = []
    for index, next_str in df.iterrows():
        if yyy == 5000:
            break
        ind = next_str.element_id
        id_list.append(ind)
        list_in_ordnund.append(String_methods.string_in_ordnung(next_str.request))
        yyy += 1

    list_of_hash, split_list_hashes, buckets = Minhash.hashing_and_bucking(list_in_ordnund, id_list)
    str_list_of_hash = []
    String_methods.list_to_string(list_of_hash, str_list_of_hash)
    str_split_list_hashes = []
    String_methods.list_to_string(split_list_hashes, str_split_list_hashes)
    str_buckets = []
    String_methods.list_to_string(buckets, str_buckets)
    res = [(id_list[i], str_list_of_hash[i], str_split_list_hashes[i], str_buckets[i]) for i in range(len(id_list))]
    return res


def download_to_db_file(create=False):
    if create:
        initialisation.create_new_db()

    initialisation.create_table()

    conn = initialisation.connection_db()
    if conn == None:
        return None

    connection = conn['connection']
    cursor = conn['cursor']
    data = processing_file(env.filename)

    dao.mass_insert_to_db(connection, cursor, data)


def search_similarity(element_id, connenction=None, cursor=None):
    if connenction is None or cursor is None:
        conn = initialisation.connection_db()
        if conn is None:
            return None
        connection = conn['connection']
        cursor = conn['cursor']

    res_req = dao.execute_read_query(connection, cursor, element_id)
    idx = max(enumerate(1 if y[0] == element_id else 0 for y in res_req), key=lambda x: x[1])[0]
    element_hash = res_req[idx][1]
    result = []
    for res in res_req:
        if res[0] == element_id:
            continue
        result.append((res[0], Minhash.jaccard_distance(element_hash, res[1])))
    print()
    return result


