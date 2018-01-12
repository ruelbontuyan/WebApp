from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators

class Forms(Form):
    idnumNew = StringField('Id Number', [validators.Length(min=1,max=60)])
    fnameNew = StringField('First Name', [validators.Length(min=1,max=60)])
    mnameNew = StringField('Middle Name', [validators.Length(min=1,max=60)])
    lnameNew = StringField('Last Name', [validators.Length(min=1,max=60)])
    sexNew = StringField('Sex (Enter M or F) ', [validators.Length(min=1,max=1)])
    courseidNew = StringField('Course Id', [validators.Length(min=1,max=60)])
    submit = SubmitField('Submit')

class courseForms(Form):
    courseNumNew = StringField('Course Id', [validators.Length(min=1,max=20)])
    coursenameNew = StringField('Course Name', [validators.Length(min=1,max=60)])
    coursecodeNew = StringField('Course Code', [validators.Length(min=1,max=60)])
    submit = SubmitField('Submit')

class iDnumForm(Form):
    idnumNew = StringField('Id Number', [validators.Length(min=1,max=20)])
    submit = SubmitField('Submit')

class UpdateForm(Form):
    fnameNew = StringField('First Name', [validators.Length(min=1,max=60)])
    mnameNew = StringField('Middle Name', [validators.Length(min=1,max=60)])
    lnameNew = StringField('Last Name', [validators.Length(min=1,max=60)])
    sexNew = StringField('Sex', [validators.Length(min=1,max=60)])
    courseidNew = StringField('Course Id', [validators.Length(min=1,max=60)])
    submit = SubmitField('Submit')

class courseNumForm(Form):
    courseNumNew = StringField('Course Id', [validators.Length(min=1,max=20)])
    submit = SubmitField('Submit')

class courseUpdateForm(Form):
    coursenameNew = StringField('Course Name', [validators.Length(min=1,max=60)])
    coursecodeNew = StringField('Course Code', [validators.Length(min=1,max=60)])
    submit = SubmitField('Submit')

