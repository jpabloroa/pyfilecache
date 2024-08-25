import unittest
import os
import tempfile
import hashlib
from datetime import datetime, timedelta
from ..pyfilecache import FileCacheManager

class TestFileCacheManager(unittest.TestCase):
    
    def setUp(self):
        """Set up a temporary directory and file for testing."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test_file.txt')
        with open(self.test_file, 'wb') as f:
            f.write(b'Test data')
        
        self.cache_manager = FileCacheManager(
            file_path=self.test_file,
            signature_algo='sha256',
            log_mode='print',
            interval=timedelta(minutes=1),
            remove_old_cache=True
        )

    def tearDown(self):
        """Clean up the temporary directory and files after tests."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.cache_manager._FileCacheManager__directory):
            for file in os.listdir(self.cache_manager._FileCacheManager__directory):
                os.remove(os.path.join(self.cache_manager._FileCacheManager__directory, file))
            os.rmdir(self.cache_manager._FileCacheManager__directory)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def test_write_read_cache(self):
        """Test writing and reading cache."""
        test_data = b'New test data'
        self.cache_manager.write(test_data, force=True)
        cache_files = os.listdir(self.cache_manager._FileCacheManager__directory)
        self.assertGreater(len(cache_files), 0, "No cache files found.")
        
        cache_file = os.path.join(self.cache_manager._FileCacheManager__directory, cache_files[0])
        read_data = self.cache_manager.read(cache_file)
        self.assertEqual(test_data, read_data, "Read data does not match written data.")
    
    def test_delete_cache(self):
        """Test deleting cache files."""
        self.cache_manager.write(b'Some data', force=True)
        cache_files = os.listdir(self.cache_manager._FileCacheManager__directory)
        self.assertGreater(len(cache_files), 0, "No cache files found before deletion.")
        
        cache_file = os.path.join(self.cache_manager._FileCacheManager__directory, cache_files[0])
        self.cache_manager.delete_cache()
        self.assertFalse(os.path.exists(cache_file), "Cache file was not deleted.")
    
    def test_get_cache_size(self):
        """Test getting the size of cache files."""
        self.cache_manager.write(b'Some data', force=True)
        cache_files = os.listdir(self.cache_manager._FileCacheManager__directory)
        self.assertGreater(len(cache_files), 0, "No cache files found for size check.")
        
        cache_size_kb = self.cache_manager.get_cache_size()
        self.assertGreater(cache_size_kb, 0, "Cache size should be greater than 0.")

    def test_set_interval(self):
        """Test setting different intervals."""
        self.cache_manager.set_interval_5_minutes()
        self.assertTrue(callable(self.cache_manager._FileCacheManager__interval))
        
        self.cache_manager.set_interval_next_day_at_8am()
        self.assertTrue(callable(self.cache_manager._FileCacheManager__interval))
        
        self.cache_manager.set_interval_first_day_of_year()
        self.assertTrue(callable(self.cache_manager._FileCacheManager__interval))

    def test_signature_generation(self):
        """Test signature generation."""
        data = b'Test data'
        signature = self.cache_manager._FileCacheManager__generate_signature(data)
        expected_signature = hashlib.sha256(data).hexdigest()
        self.assertEqual(signature, expected_signature, "Generated signature does not match expected signature.")

    def test_file_creation_date(self):
        """Test getting the creation date of a file."""
        self.cache_manager.write(b'Some data', force=True)
        cache_files = os.listdir(self.cache_manager._FileCacheManager__directory)
        self.assertGreater(len(cache_files), 0, "No cache files found for date check.")
        
        cache_file = os.path.join(self.cache_manager._FileCacheManager__directory, cache_files[0])
        creation_date = self.cache_manager.get_file_creation_date(cache_file)
        self.assertIsInstance(creation_date, float, "File creation date should be a float.")

if __name__ == '__main__':
    unittest.main()
