import zipfile
import sys
import os
import compileall
import shutil
from optparse import OptionParser

from bzrlib.branch import Branch
from bzrlib.log import show_log, ShortLogFormatter
from bzrlib.export import export

from utils import clean_path

class ZipUtils(object):
    """Utility class for all 'zipfile' module related work.

    Part of implementation is from the snippet at
    http://stackoverflow.com/questions/458436/adding-folders-to-a-zip-file-using-python
    """
    def toZip(self, file, zip_location):
        """Adds a given file (or directory for that matter) to a zip file.
        
        file - File or Directory that to be zipped.
        zip_location - Location where the resultant .zip file would be created.
        """
        zip_file = zipfile.ZipFile(zip_location, 'w')
        if os.path.isfile(file):
            zip_file.write(file)
        else:
            self.__addFolderToZip(zip_file, file)
        print "Wrote %s to %s"%(file,zip_location)
        zip_file.close()

    def fromZip(self, zip_location,extract_location):
        """Extracts the .zip file to a given location

        zip_location - Location of the .zip file which needs to the extracted.
        extract_location - Path on the file system where the .zip file will be extracted. 
        """
        zip_file = zipfile.ZipFile(zip_location,'r')
        zip_file.extractall(extract_location)

    def __addFolderToZip(self, zip_file, folder): 
        for file in os.listdir(folder):
            full_path = os.path.join(folder, file)
            if os.path.isfile(full_path):
                print 'File added: %s'%(full_path)
                zip_file.write(full_path)
            elif os.path.isdir(full_path):
                print 'Entering folder: %s'%(full_path)
                self.__addFolderToZip(zip_file, full_path)

z = ZipUtils()

def parseOptions():
    """Adds different commandline options for mDataRecovery. 
    """
    parser = OptionParser()
    parser.add_option('-s',
                      '--source_location',
                      dest='source_location',
                      help="Location of source directory of the bundle.\n\n")

    (params, args) = parser.parse_args()
    if not params.source_location:
        print "--source_location must be secified. Execute 'python create_bundle.py -h' for options."
        sys.exit(0)
    return params


def bundle(dir):
    branch = Branch.open(dir)
    output_zip = '%s_%d.zip'%(dir, branch.revno())
    temp_dir = '/tmp/output_%d'%(branch.revno())

    #Empty the temp_dir
    shutil.rmtree(temp_dir, True)

    #export the bzr repository to temp_dir
    export(branch.basis_tree(), temp_dir)

    #Compile the source code in templocation
    compileall.compile_dir(temp_dir)

    #Remove the .py files from the exported directory.
    clean_path(temp_dir, [".py"])
    
    #create a HISTORY file in the temp_dir
    show_log(branch, ShortLogFormatter(open(temp_dir+os.sep+'HISTORY', 'w')))

    #create a VERSION file in temp_dir
    f = open(temp_dir+os.sep+'VERSION', 'w')
    f.write(str(branch.revno()))
    f.close()

    #write to zip
    z.toZip(temp_dir, output_zip)

if __name__ == '__main__':
    parser = parseOptions()
    bundle(parser.source_location)
