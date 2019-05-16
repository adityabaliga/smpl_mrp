from database import CursorFromConnectionFromPool
from decimal import Decimal


class Processing:
    def __init__(self, smpl_no, operation, processing_date, start_time, end_time, setting_start_time,
                 setting_end_time, processing_time, setting_time, no_of_qc, no_of_helpers, names_of_qc,
                 names_of_helpers, name_of_packer, setting_date, total_processed_wt, total_cuts):
        self.smpl_no = smpl_no
        self.operation = operation
        self.processing_date = processing_date
        self.start_time = start_time
        self.end_time = end_time
        self.setting_start_time = setting_start_time
        self.setting_end_time = setting_end_time
        self.processing_time = processing_time
        self.setting_time = setting_time
        self.no_of_qc = no_of_qc
        self.no_of_helpers = no_of_helpers
        self.names_of_qc = names_of_qc
        self.names_of_helpers = names_of_helpers
        self.name_of_packer = name_of_packer
        self.setting_date = setting_date
        self.total_processed_wt = total_processed_wt
        self.total_cuts = total_cuts

    @classmethod
    def load_from_db(cls, smpl_no, operation):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('select * from processing where smpl_no = %s and operation = %s', (smpl_no, operation))
            user_data = cursor.fetchall()
            processing_lst = []
            for lst in user_data:
                processing = Processing(smpl_no=lst[2], operation=lst[2], processing_date=lst[3], start_time=lst[4],
                                        end_time=lst[5], processing_time=int(lst[6]), setting_start_time=lst[7],
                                        setting_end_time=lst[8], setting_time=int(lst[9]), no_of_qc=lst[10],
                                        no_of_helpers=lst[11], names_of_qc=lst[12], names_of_helpers=lst[13],
                                        name_of_packer=lst[14], setting_date=lst[15], total_processed_wt = Decimal(lst[16]),
                                        total_cuts=int(lst[17]))
                processing_lst.append(processing)
        return processing_lst

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("insert into processing (smpl_no, operation, processing_date, start_time, "
                           "end_time, setting_start_time, setting_end_time, production_time, setting_time, no_of_qc, "
                           "no_of_helpers, names_of_qc, names_of_helpers,name_of_packer,setting_date, total_processed_wt,"
                           "total_cuts) values (%s, %s,%s, %s, "
                           "%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)",
                           (self.smpl_no, self.operation, self.processing_date,
                            self.start_time, self.end_time, self.setting_start_time,
                            self.setting_end_time, self.processing_time, self.setting_time,
                            self.no_of_qc, self.no_of_helpers, self.names_of_qc,
                            self.names_of_helpers, self.name_of_packer, self.setting_date, self.total_processed_wt,
                            self.total_cuts))

            cursor.execute("select processing_id from processing where oid= %s", (cursor.lastrowid,))
            data = cursor.fetchone()
            return data[0]

    @classmethod
    def load_history(cls, smpl_no):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('select * from processing where smpl_no = %s', (smpl_no, ))
            user_data = cursor.fetchall()

        return user_data

    @classmethod
    def get_daily_report(cls, report_date):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('select * from processing where processing_date = %s', (report_date, ))
            user_data = cursor.fetchall()
        return user_data