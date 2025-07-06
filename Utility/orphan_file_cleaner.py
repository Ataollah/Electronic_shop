import os

def update_file_field(model_class, pk, file_field_name, new_file):
    if pk:
        try:
            instance = model_class.objects.get(pk=pk)
            old_file = getattr(instance, file_field_name)
            if old_file and old_file != new_file:
                delete_file_field(old_file)
            setattr(instance, file_field_name, new_file)
        except model_class.DoesNotExist:
            print(f"Instance with primary key {pk} does not exist.")


def delete_file_field(file):
    if file and 'default_images' not in file.path:
        if os.path.isfile(file.path):
            os.remove(file.path)
