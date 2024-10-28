import pandas as pd
import String_methods
import Minhash
import env
import initialisation
import dao


def processing_file(filename, update=False, connection=None, cursor=None):
    df = pd.read_csv(filepath_or_buffer=filename,
                     names=['element_id', 'request'], encoding='Windows-1251', delimiter=';')
    yyy = 0
    list_in_ordnund = []
    id_list = []
    for index, next_str in df.iterrows():
        if yyy == 1000:
            break
        ind = next_str.element_id
        id_list.append(ind)
        list_in_ordnund.append(String_methods.string_in_ordnung(next_str.request))
        yyy += 1

    if update:
        dao.delete_updating_note(connection, cursor, [(y,) for y in id_list])

    list_of_id, list_of_hash, split_list_hashes, buckets = Minhash.hashing_and_bucking(list_in_ordnund, id_list, update, cursor)

    str_list_of_hash = []
    String_methods.list_to_string(list_of_hash, str_list_of_hash)
    str_split_list_hashes = []
    String_methods.list_to_string(split_list_hashes, str_split_list_hashes)
    str_buckets = []
    String_methods.list_to_string(buckets, str_buckets)
    res = [(list_of_id[i], str_list_of_hash[i], str_split_list_hashes[i], str_buckets[i]) for i in range(len(list_of_id))]

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

    dao.clear_minhash_table(connection, cursor)
    dao.mass_insert_to_db(connection, cursor, data)


def search_similarity(element_id, connenction=None, cursor=None):
    result = []
    if connenction is None or cursor is None:
        conn = initialisation.connection_db()
        if conn is None:
            return result
        connection = conn['connection']
        cursor = conn['cursor']

    res_req = dao.execute_read_query(cursor, element_id)
    if len(res_req) == 0:
        return result

    idx = max(enumerate(1 if y[0] == element_id else 0 for y in res_req), key=lambda x: x[1])[0]
    element_hash = res_req[idx][1]
    for res in res_req:
        if res[0] == element_id:
            continue
        result.append((res[0], Minhash.jaccard_distance(element_hash, res[1])))

    return result


def update_base():
    conn = initialisation.connection_db()
    if conn == None:
        return None

    connection = conn['connection']
    cursor = conn['cursor']

    data = processing_file(env.filename_update, True, connection, cursor)
    # dao.clear_minhash_table(connection, cursor)
    dao.mass_insert_to_db(connection, cursor, data)




