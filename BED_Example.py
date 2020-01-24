from __future__ import division

import wpf
import os
import math

from System.Windows import *
from System.Windows.Controls import *

from connect import *

patient = get_current('Patient')
plan = get_current("Plan")
beam_set = get_current("BeamSet")
case = get_current("Case")

patient_name = patient.Name
dob = patient.DateOfBirth
id = patient.PatientID
current_case = case.CaseName
current_beam_set = beam_set.DicomPlanLabel
prescription = beam_set.Prescription.PrimaryDosePrescription.DoseValue
fractions = beam_set.FractionationPattern.NumberOfFractions
pres_label = str(prescription) + " cGy @ " + str(float(prescription)/float(fractions)) + " cGy/fx in " + str(fractions) + " fractions"


class MyWindow(Window):
    def __init__(self):
        # Load xaml component.
        xaml_file = os.path.join(os.path.dirname(__file__), 'BED_Example.xaml')
        wpf.LoadComponent(self, xaml_file)

        # xaml unique identification
        self.patient_label.Text = patient_name
        self.mrn_label.Text = id
        self.dob_label.Text = str(dob)
        self.case_label.Text = current_case
        self.beamset_label.Text = current_beam_set
        self.prescription_label.Text = pres_label

     
    #event handling
    def OnClick(self, sender, e):
        d_original = 200
        fx_original = 30
        a_b_r = int(self.alpha_beta_ratio.Text)
        BED = fx_original * (d_original/100) * (1 + ((d_original/100) / a_b_r))
        self.BED_label.Content = str(BED) + ' Gy!'

        try:
            fraction_TB = float(self.fraction_TB.Text)
        except:
            fraction_TB = self.fraction_TB.Text

        try:
            dose_per_fx_TB = float(self.dose_per_fx_TB.Text)
        except:
            dose_per_fx_TB = self.dose_per_fx_TB.Text

        if type(fraction_TB) == float and type(dose_per_fx_TB) == float:
            print("error")
            MessageBox.Show("Error: Leave one of the fields empty")
        elif type(fraction_TB) == float:
            result = ((-1+(math.sqrt(1**2-4*(1/a_b_r)*(-BED/float(self.fraction_TB.Text)))))/(2*(1/a_b_r)))*BED
            self.dose_per_fx_TB.Text = str(result)
            print(result)
        elif type(dose_per_fx_TB) == float:
            result = BED / ((float(self.dose_per_fx_TB.Text)/100) * (1 + ((float(self.dose_per_fx_TB.Text)/100)/a_b_r)))
            self.fraction_TB.Text = str(result)
            print(result)
        else:
            MessageBox.Show("Error")

# Run in RayStation.
# Create window, arguments specified by __init__ method.
window = MyWindow()
# Show window.
window.ShowDialog()






















