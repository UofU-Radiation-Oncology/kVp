import platform
assert platform.python_implementation() == "CPython"

from datetime import datetime

import os   
from connect import *
from System.Windows import *
from System.Windows.Controls import *
from pathlib import Path

class MyWindow(RayWindow):
    def __init__(self, patient, exam):
        # Load xaml component.
        xaml_file = Path('//hci-ro-rsrh/C$/Program Files/HCH_RS_Scripting/kVp/kVp.xaml')
        xaml = xaml_file.read_text()
        self.LoadComponent(xaml)
        self.kVpLabel.Content = GetkVp(exam)
        self.ExamLabel.Content = exam.Name
        self.PatientLabel.Content = patient.Name

    def CloseClicked(self, sender, event):
        # Close window.
        self.DialogResult = True

def GetkVp(examination):
    # Export DICOM data to tmp text file
    tmp_file_name = '//hci-ro-rsrh/C$/tmp/kVpDICOMtmp_{}.txt'.format(datetime.now().strftime("%Y%m%d%H%M%S"))
    examination.WriteStoredDicomDataSetToFileForVerification(FileName=tmp_file_name)
    
    # Get KVP from DICOM data
    tmp_file = open(tmp_file_name, "r")
    KVP = ''
    for line in tmp_file.readlines():
        if 'KVP' in line:
            KVP = line.replace('(0018,0060)','').replace('KVP','').strip()
    tmp_file.close()

    # Delete temp file
    os.remove(tmp_file_name)    

    return KVP


# Run in RayStation.
exam = get_current('Examination')
patient = get_current('Patient')
# Create window, arguments specified by __init__ method.
window = MyWindow(patient,exam)
# Show window.
window.ShowDialog()