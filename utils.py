import pandas
from MQTT import MqttSap


class Utils():
    """Utility class that provides some functionalities to be used by other classes, such as the Excel processing
    in the Graphical User Interface"""

    @staticmethod
    def readExcelFile(filePath: str):
        """
        Loads measurement data from Excel file, in the format denoted by the template in file Template_migration_IAM.xlsx in
        the project's repository.

        Parameters:
            filePath: str -> Excel file directory containing the data
        """
        return pandas.read_excel(filePath,header=2)

    @staticmethod
    def loadData(filePath: str):
        """
        Loads measurement data from Excel file, in the format denoted by the template in file Template_migration_IAM.xlsx in
        the project's repository.

        Parameters:
            filePath: str -> Excel file directory containing the data
        """
        try:
            excelData = Utils.readExcelFile(filePath)
            for index, row in excelData.iterrows():
                conn = MqttSap(clientID=row["device_alternate_id"],
                               certificateFile=row["PEM_file_directory"],
                               secret=row["secret"])
                conn.sendSingleData(capAltId=row["capability_alternate_id"],
                                    sensorAltId=row["sensor_alternate_id"],
                                    measure=[[row["measures"]]],
                                    timestamp=row["timestamp"],simulateDelay=False)
                conn.disconnect()
        except (FileNotFoundError):
            return -1
        return 0



