import pandas as pd
import String_methods
import Minhash
import env
import initialisation
import dao
import global_variable
import hashlib
import os
import pickle
import processing_levels
# from console_thrift import KeyboardInterruptException as ConsoleKeyboardInterrupt


def is_keyboard_interrupt(exception):
    # The second condition is necessary for it to work with the stop button
    # in PyCharm Python console.
    return (type(exception) is KeyboardInterrupt
            or type(exception).__name__ == 'KeyboardInterruptException')


def delete_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f'Ошибка при удалении файла {file_path}. {e}')


def get_file_hash(file_path: str, algorithm: str = 'sha256'):

    hash_func = hashlib.new(algorithm)
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def update_processing_levels():
    with open("tmp/processing_levels", "rb") as file:
        processing_levels_var = pickle.load(file)
        processing_levels.steps = processing_levels_var.get('steps')
        processing_levels.levels = processing_levels_var.get('levels')


def update_global_variable():
    with open("tmp/global_variable", "rb") as file:
        global_variable_var = pickle.load(file)
        global_variable.update = global_variable_var.get('update')
        global_variable.id_list = global_variable_var.get('id_list')
        global_variable.list_in_ordnund = global_variable_var.get('list_in_ordnund')
        global_variable.shingle_list = global_variable_var.get('shingle_list')
        global_variable.all_shingles = global_variable_var.get('all_shingles')
        global_variable.list_of_onehot = global_variable_var.get('list_of_onehot')
        global_variable.list_of_hash = global_variable_var.get('list_of_hash')
        global_variable.split_list_hashes = global_variable_var.get('split_list_hashes')
        global_variable.buckets = global_variable_var.get('buckets')
        global_variable.hash_func = global_variable_var.get('hash_func')


def update_env_variable():
    with open("tmp/env_variable", "rb") as file:
        env_variable = pickle.load(file)
        env.name_db = env_variable.get('name_db')
        env.user = env_variable.get('user')
        env.password = env_variable.get('password')
        env.host = env_variable.get('host')
        env.port = env_variable.get('port')
        # env.filename = r"minhash_data3.csv"
        # env.filename_update = r"update_minhash.csv"
        env.count_shuffle = env_variable.get('count_shuffle')
        env.len_of_buck = env_variable.get('len_of_buck')


def save_temp_data():

    if not os.path.exists("tmp"):
        os.makedirs("tmp")

    delete_files_in_folder("tmp")
    with open("tmp/env_variable", "wb") as file:
        env_dict = dict()
        env_dict["name_db"] = env.name_db
        env_dict["user"] = env.user
        env_dict["password"] = env.password
        env_dict["host"] = env.host
        env_dict["port"] = env.port
        env_dict["count_shuffle"] = env.count_shuffle
        env_dict["len_of_buck"] = env.len_of_buck
        pickle.dump(env_dict, file)
    with open("tmp/global_variable", "wb") as file:
        global_dict = dict()
        global_dict["update"] = global_variable.update
        global_dict["id_list"] = global_variable.id_list
        global_dict["list_in_ordnund"] = global_variable.list_in_ordnund
        global_dict["shingle_list"] = global_variable.shingle_list
        global_dict["all_shingles"] = global_variable.all_shingles
        global_dict["list_of_onehot"] = global_variable.list_of_onehot
        global_dict["list_of_hash"] = global_variable.list_of_hash
        global_dict["split_list_hashes"] = global_variable.split_list_hashes
        global_dict["buckets"] = global_variable.buckets
        global_dict["hash_func"] = global_variable.hash_func
        pickle.dump(global_dict, file)

    with open("tmp/processing_levels", "wb") as file:
        levels_dict = dict()
        levels_dict["steps"] = processing_levels.steps
        levels_dict["levels"] = processing_levels.levels
        pickle.dump(levels_dict, file)


def processing_file(filename, update=False, connection=None, cursor=None):
    # try:
    global_variable.reanimate = False
    old_hash = '0'

    if os.path.exists("hash"):
        with open("hash", "rb") as file:
            old_hash = pickle.load(file)

    new_hash = get_file_hash(filename)
    with open("hash", "wb") as file:
        pickle.dump(new_hash, file)

    if os.listdir("tmp"):
        if (os.path.exists("tmp/processing_levels") and
                os.path.exists("tmp/global_variable") and os.path.exists("tmp/env_variable")):

            if new_hash == old_hash:
                global_variable.reanimate = True

    if global_variable.reanimate:
        update_processing_levels()
        update_global_variable()
        update_env_variable()
        delete_files_in_folder("tmp")
        # if processing_levels.current_step == '':
        #     global_variable.reanimate = False

    if not global_variable.reanimate or (not processing_levels.steps['strings_in_ordnung'] and global_variable.reanimate):
        if not global_variable.reanimate:
            global_variable.id_list = []
            global_variable.list_in_ordnund = []
            processing_levels.levels["strings_in_ordnung"] = 0
            df = pd.read_csv(filepath_or_buffer=filename,
                             names=['element_id', 'request'], encoding='Windows-1251', delimiter=';')
        else:
            df = pd.read_csv(filepath_or_buffer=filename, skiprows=processing_levels.levels.strings_in_ordnung,
                         names=['element_id', 'request'], encoding='Windows-1251', delimiter=';')

        for index, next_str in df.iterrows():

            # if processing_levels.levels["strings_in_ordnung"] == 1000:
            #     break

            ind = next_str.element_id
            global_variable.id_list.append(ind)
            global_variable.list_in_ordnund.append(String_methods.string_in_ordnung(next_str.request))
            processing_levels.levels["strings_in_ordnung"] +=1

        global_variable.reanimate = False
        processing_levels.steps['strings_in_ordnung'] = True


    if update:
        if not global_variable.reanimate or (not processing_levels.steps['delete_updating_note'] and global_variable.reanimate):
            global_variable.reanimate = False
            dao.delete_updating_note(connection, cursor, [(y,) for y in global_variable.id_list])
            processing_levels.steps['delete_updating_note'] = True

    Minhash.hashing_and_bucking(update, cursor)

    str_list_of_hash = []
    String_methods.list_to_string(global_variable.list_of_hash, str_list_of_hash)
    str_split_list_hashes = []
    String_methods.list_to_string(global_variable.split_list_hashes, str_split_list_hashes)
    str_buckets = []
    String_methods.list_to_string(global_variable.buckets, str_buckets)
    res = [(global_variable.id_list[i], str_list_of_hash[i], str_split_list_hashes[i], str_buckets[i])
           for i in range(len(global_variable.id_list))]

    return res
    # except SystemExit or KeyboardInterrupt:
    #     save_temp_data()
    # except BaseException:
    #     # Catch all exceptions and test if it is KeyboardInterrupt, native or
    #     # PyCharm's.
    #     # if is_keyboard_interrupt(ex):
    #     save_temp_data()



def download_to_db_file(create=False):
    try:
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
    except BaseException or KeyboardInterrupt:
        print("W A S T E D")
        save_temp_data()

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
    try:
        conn = initialisation.connection_db()
        if conn == None:
            return None

        connection = conn['connection']
        cursor = conn['cursor']

        data = processing_file(env.filename_update, True, connection, cursor)
        # dao.clear_minhash_table(connection, cursor)
        dao.mass_insert_to_db(connection, cursor, data)
    except BaseException or KeyboardInterrupt:
        print("W A S T E D")
        save_temp_data()




