import pytest
from unittest import mock

def test_update_file_field_deletes_old_file_if_changed():
    # Mock model instance and file fields
    mock_instance = mock.Mock()
    mock_old_file = mock.Mock()
    mock_old_file.path = '/tmp/old_file.txt'
    mock_new_file = mock.Mock()
    mock_new_file.path = '/tmp/new_file.txt'

    # Mock model_class.objects.get
    mock_model_class = mock.Mock()
    mock_model_class.objects.get.return_value = mock_instance
    setattr(mock_instance, 'file_field', mock_old_file)

    # Patch delete_file_field
    with mock.patch('Utility.orphan_file_cleaner.delete_file_field') as mock_delete:
        # Call function
        from Utility.orphan_file_cleaner import update_file_field
        update_file_field(mock_model_class, 1, 'file_field', mock_new_file)
        # Should call delete_file_field for old file
        mock_delete.assert_called_once_with(mock_old_file)
        # Should set new file
        assert getattr(mock_instance, 'file_field') == mock_new_file

def test_update_file_field_instance_does_not_exist():
    mock_model_class = mock.Mock()
    class DoesNotExist(Exception):
        pass
    mock_model_class.DoesNotExist = DoesNotExist
    mock_model_class.objects.get.side_effect = DoesNotExist
    from Utility.orphan_file_cleaner import update_file_field
    update_file_field(mock_model_class, 1, 'file_field', mock.Mock())