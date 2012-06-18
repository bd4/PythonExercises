import find
import io
import unittest
import os
import os.path


tmp_dir_previously_existed = False
a_dir_p_e = False
b_dir_p_e = False
abc_dir_p_e = False
abc123_file_p_e = False
a_1_file_p_e = False
b_2_file_p_e = False
b_3_file_p_e = False

tmp_dir = os.path.join('/', 'tmp')


class FindTestCase(unittest.TestCase):

    def setUp(self):
        global tmp_dir_previously_existed
        global a_dir_p_e
        global b_dir_p_e
        global abc_dir_p_e
        global abc123_file_p_e
        global a_1_file_p_e
        global b_2_file_p_e
        global b_3_file_p_e
        
        #create a /tmp file structure so you can have something to work with
        if os.path.isdir('/tmp'):
            tmp_dir_previously_existed = True
            
            if os.path.isdir('/tmp/a'):
                a_dir_p_e = True
            else:
                os.mkdir('/tmp/a')
            
            if os.path.isdir('/tmp/b'):
                b_dir_p_e = True
            else:
                os.mkdir('/tmp/b')
            
            if os.path.isdir('/tmp/abc'):
                abc_dir_p_e = True
            else:
                os.mkdir('/tmp/abc')
            
            if os.path.isfile('/tmp/abc123.txt'):
                abc123_file_p_e = True
            else:
                tmp_file_abc123 = open('/tmp/abc123.txt','w')
                tmp_file_abc123.close()
            
            if os.path.isfile('/tmp/a/1.txt'):
                a_1_file_p_e = True
            else:
                tmp_file_a_1 = open('/tmp/a/1.txt','w')
                tmp_file_a_1.close()
            
            if os.path.isfile('/tmp/b/2.txt'):
                b_2_file_p_e = True
            else:
                tmp_file_b_2 = open('/tmp/b/2.txt','w')
                tmp_file_b_2.close()
            
            if os.path.isfile('/tmp/b/3.txt'):
                b_3_file_p_e = True
            else:
                tmp_file_b_3 = open('/tmp/b/3.txt','w')
                tmp_file_b_3.close()
            
        else:
            os.mkdir('/tmp')
            os.mkdir('/tmp/a')
            os.mkdir('/tmp/b')
            os.mkdir('/tmp/abc')
            
            tmp_file_abc123 = open('/tmp/abc123.txt','w')
            tmp_file_abc123.close()
            
            tmp_file_a_1 = open('/tmp/a/1.txt','w')
            tmp_file_a_1.close()
            
            tmp_file_b_2 = open('/tmp/b/2.txt','w')
            tmp_file_b_2.close()
                
            tmp_file_b_3 = open('/tmp/b/3.txt','w')
            tmp_file_b_3.close()
    
    
    def test_find_dirs_files_with_exact_name(self):
        global tmp_dir
        actual_output = find.do_search(tmp_dir, None, 'a', None)
        
        theoretical_output = io.StringIO()
        print(os.path.join('/tmp', 'a'), file=theoretical_output)
        
        self.assertEqual(actual_output.getvalue(), theoretical_output.getvalue())
    
    def test_find_dirs_file_with_globbing(self):
        global tmp_dir
        actual_output = find.do_search(tmp_dir, None, 'a*c*', None)
        
        theoretical_output = io.StringIO()
        print(os.path.join('/tmp', 'abc123.txt'), file=theoretical_output)
        print(os.path.join('/tmp', 'abc'), file=theoretical_output)
        
        self.assertEqual(actual_output.getvalue(), theoretical_output.getvalue())
    
    def test_find_dirs_files_with_regex(self):
        global tmp_dir
        actual_output = find.do_search(tmp_dir, '1', None, None)
        
        theoretical_output = io.StringIO()
        print(os.path.join(tmp_dir, 'abc123.txt'), file=theoretical_output)
        print(os.path.join(os.path.join(tmp_dir, 'a'), '1.txt'), file=theoretical_output)
        
        self.assertEqual(actual_output.getvalue(), theoretical_output.getvalue())
    
    def test_type_works_with_name_specified(self):
        global tmp_dir
        actual_output = find.do_search(tmp_dir, 'a', None, 'f')
        
        theorectical_output = io.StringIO()
        print(os.path.join(tmp_dir, 'abc123.txt'), file=theoretical_output)
        
        self.assertEqual(actual_output.getvalue(), theoretical_output.getvalue())
    
    
    def tearDown(self):
        global tmp_dir_previously_existed
        global a_dir_p_e
        global b_dir_p_e
        global abc123_file_p_e
        global a_1_file_p_e
        global b_2_file_p_e
        global b_3_file_p_e
        
        if not abc123_file_p_e:
            os.remove('/tmp/abc123.txt')
        if not a_1_file_p_e:
            os.remove('/tmp/a/1.txt')
        if not b_2_file_p_e:
            os.remove('/tmp/b/2.txt')
        if not b_3_file_p_e:
            os.remove('/tmp/b/3.txt')
        
        if not a_dir_p_e:
            os.rmdir('/tmp/a')
        if not b_dir_p_e:
            os.rmdir('/tmp/b')
        if not abc_dir_p_e:
            os.rmdir('/tmp/abc')
        if not tmp_dir_previously_existed:
            os.rmdir('/tmp')  #Note: the dir must be empty before it can be del
            
if __name__ == '__main__':
    unittest.main()