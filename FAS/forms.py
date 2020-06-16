from django import forms

class emp_reg(forms.Form):
    emp_code=forms.CharField(label="Employee Code", max_length=8)
    emp_name=forms.CharField(label="Employee Name", max_length=100)
    