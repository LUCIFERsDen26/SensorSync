import mysql.connector
import datetime

class StateData:
    def __init__(self):
        
        self.cnx = mysql.connector.connect(user='outlaw', password='mysql',
                                      host='192.168.43.177',port=6678, database='Mqtt')
        self.cursor = self.cnx.cursor()

    def raw_data(self,state):
        query = f"SELECT QIndex FROM MQTable WHERE random_state = '{state}' limit 12;"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def get_QIndex(self,state):
        qindex = self.raw_data(state)
        qindex = [x[0] for x in qindex]
        month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December']
        
        data = [{"month_name": month_names[i], "Qindex": qindex[i]} for i in range(len(qindex))]
        return data

    def state_count(self):
        query = f"select random_state, count(random_state) from MQTable group by random_state;"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data
    
    def get_graph(self):
        query = f"SELECT Time,GraphYval FROM MQTable ORDER BY Time DESC LIMIT 10;"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        sampData = []
        for duration, value in data:
            duration_in_seconds = duration.total_seconds()
            hours, remainder = divmod(duration_in_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            am_pm = 'AM' if hours < 12 else 'PM'
            formatted_time = f"{int(hours % 12):02d}:{int(minutes):02d} {am_pm}"
            sampData.append((formatted_time, value))
        data=sampData
        return data

    def get_wave(self):
        query = f"SELECT Time,WaveYval FROM MQTable ORDER BY Time DESC LIMIT 10;"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        sampData = []
        for duration, value in data:
            duration_in_seconds = duration.total_seconds()
            hours, remainder = divmod(duration_in_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            am_pm = 'AM' if hours < 12 else 'PM'
            formatted_time = f"{int(hours % 12):02d}:{int(minutes):02d} {am_pm}"
            sampData.append((formatted_time, value))
        data=sampData
        return data

    def __del__(self):
        #self.cursor.close()
        self.cnx.close()

state_data = StateData()
data = state_data.get_graph()

print(data)
