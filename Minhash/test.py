import uuid

import initialisation
import dao

def create_all():
    res2 = initialisation.create_tables()
    if res2 is None:
        print('vse ok, prover v pgadmin')
    else:
        print('truba, nichego ne vishlo')


def test_ins():
    # create
    dao.insert_record_to_queue(uuid.uuid4(), 'training')


def test_get():
    print(dao.get_next_in_queue('training'))


def test_set():

    id_test = uuid.UUID('fa14929e-13a7-4ad6-95e8-c0d303797d95')

    dao.set_status(id_test, 'working', 'blablabla')

def test_getst():
    id_test = uuid.UUID('fa14929e-13a7-4ad6-95e8-c0d303797d95')
    #id_test = uuid.UUID('b83a1c22-73d0-456f-9740-76ef477386f9')

    print(dao.get_status(id_test))

test_get()
test_set()
test_get()
test_getst()

