import uuid


def search_dict_by_key(data_set, some_key, value_name):
    try:
        return data_set[some_key]
    except KeyError:
        return '{0} with ID {1} doesnot exist'.format(value_name, str(some_key))


def return_all_dict_values(data_set, value_name):
    if len(data_set) > 0:
        return [value for value in data_set.values()]
    return 'No {} available'.format(value_name)


def parse_product_dict(data_set):
    total = 0
    for item in data_set:
        total += item['price']
    return total


def generate_id():
    return uuid.uuid4().int >> 64
