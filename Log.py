import datetime

# Leo Neat
# WFIRST-CGI
# Jet Propulsion Laboratory
#
# Log.py
# This class is made to assist in error trapping of the RemoteScreen Class
# It essentially just stores all of the changes that are made to the android screen.
# This can also be used to record and store data.


class Log:

    temp_store_name = ''

    # This creates the log file and detrmines begins storing the information
    def __init__(self, name):
        self.temp_store_name = name + '.txt'
        self.clear_file()



    def clear_file(self):
        with open(self.temp_store_name, "w+") as f:
            f.write("")
            f.close()

    def append_line(self, tag, text):
        with open(self.temp_store_name, "a") as f:
            i = datetime.datetime.now()
            f.write(i.isoformat() + ":" + tag +': ' + text + '\n')
            f.close

    def append_bold_line(self, tag, text):
        with open(self.temp_store_name, "a") as f:
            i = datetime.datetime.now()
            f.write(i.isoformat() + ":" + tag + ': ' + text.upper() + '\n')
            f.close

    def save_log(self, location, config):
        with open(self.temp_store_name, "r") as f:
            temp_str = f.read()
            f.close
        i = datetime.datetime.now()
        if config == True:
            fname = location +'\\' + i.isoformat().replace(':','_') +'CONFIG.txt'
        else:
            fname = location + '\\' + i.isoformat().replace(':', '_') + '.txt'
        print(fname)
        with open(fname,'w') as f:
            f.write(temp_str)
