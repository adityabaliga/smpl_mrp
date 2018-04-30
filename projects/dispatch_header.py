from database import CursorFromConnectionFromPool
from decimal import *
import time

class DispatchHeader:
    def __init__(self, vehicle_no, customer, dispatch_date, dispatch_time, remarks):
        self.vehicle_no = vehicle_no
        self.customer = customer
        self.dispatch_date = dispatch_date
        self.dispatch_time = dispatch_time
        self.remarks = remarks

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("insert into dispatch_header (vehicle_no, dispatch_date, dispatch_time, customer) values"
                           "(%s, %s, %s, %s)",(self.vehicle_no, self.dispatch_date, self.dispatch_time, self.customer))

            cursor.execute("select dispatch_id from dispatch_header where oid= %s", (cursor.lastrowid,))
            data = cursor.fetchone()
            return data[0]


    @classmethod
    def get_dispatch_lst_by_date(cls, date):
        dispatch_lst = []
        dispatch_hdr_id_lst = []
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("select * from dispatch_header where dispatch_date = %s order by dispatch_time asc",(date,))
            user_data = cursor.fetchall()
        for lst in user_data:
            dispatch_lst.append(DispatchHeader(lst[1], lst[6], lst[2], lst[3], lst[5]))
            dispatch_hdr_id_lst.append(lst[0])
        return zip(dispatch_hdr_id_lst,dispatch_lst)


    @classmethod
    def get_hdr_by_id(cls, select_dispatch_hdr_id):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('select * from dispatch_header where dispatch_id = %s',(select_dispatch_hdr_id,))
            user_data = cursor.fetchone()
        dispatch_hdr = DispatchHeader(user_data[1], user_data[6], user_data[2], user_data[3], user_data[5])
        return dispatch_hdr

    @classmethod
    def load_from_db(cls, dispatch_id):
        dispatch_lst = []
        dispatch_hdr_id_lst = []
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("select * from dispatch_header where dispatch_id = %s order by dispatch_time asc", (dispatch_id,))
            user_data = cursor.fetchall()
        for lst in user_data:
            dispatch_lst.append(DispatchHeader(lst[1], lst[6], lst[2], lst[3], lst[5]))

        return dispatch_lst


