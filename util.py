def get_dict_from_request(form_data):
    output = dict()
    for field in form_data:
        output[field] = form_data[field].strip()
    return output
