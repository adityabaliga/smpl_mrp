from database import CursorFromConnectionFromPool
from decimal import *

class ProcessingDetail:
    def __init__(self, smpl_no, operation, machine, processing_id, cut_width, cut_length,  processed_numbers,
                 processed_packets, remarks, processed_wt, input_width, input_length, order_detail_id):
        self.smpl_no = smpl_no
        self.operation = operation
        self.machine = machine
        self.processing_id = processing_id
        self.cut_width = cut_width
        self.cut_length = cut_length
        self.processed_numbers = processed_numbers
        self.processed_packets = processed_packets
        self.remarks = remarks
        self.processed_wt = processed_wt
        self.input_width = input_width
        self.input_length = input_length
        self.order_detail_id = order_detail_id





    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("insert into processing_detail (smpl_no, operation, machine, processing_id, input_width,"
                           "input_length, cut_width, cut_length, processed_numbers, processed_packets, processed_wt, "
                           "remarks, order_detail_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (self.smpl_no,
                                                                                            self.operation,
                                                                                            self.machine,
                                                                                            self.processing_id,
                                                                                            self.input_width,
                                                                                            self.input_length,
                                                                                            self.cut_width,
                                                                                            self.cut_length,
                                                                                            self.processed_numbers,
                                                                                            self.processed_packets,
                                                                                            self.processed_wt,
                                                                                            self.remarks,
                                                                                            self.order_detail_id))


    @classmethod
    def load_from_db(cls,smpl_no, operation):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("select * from processing_detail where smpl_no = %s and operation = %s ",
                           (smpl_no, operation))
            user_data = cursor.fetchall()
            processing_dtl_lst = []
            for lst in user_data:
                processing_dtl = ProcessingDetail(smpl_no=lst[1], operation=lst[2], machine=lst[3],
                                                  processing_id=int(lst[4]),
                                                  cut_width=Decimal(lst[5]), cut_length=Decimal(lst[6]),
                                                  processed_numbers=int(lst[7]), processed_packets=int(lst[8]),
                                                  remarks=lst[9], processed_wt=Decimal(lst[10]),
                                                  input_width=Decimal(lst[11]), input_length=Decimal(lst[12]),
                                                  order_detail_id=lst[13])
                processing_dtl_lst.append(processing_dtl)
            return processing_dtl_lst

    @classmethod
    def load_history(cls, smpl_no):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("select * from processing_detail where smpl_no = %s ",(smpl_no, ))
            user_data = cursor.fetchall()
            processing_dtl_lst = []
            for lst in user_data:
                processing_dtl = ProcessingDetail(smpl_no=lst[1], operation=lst[2], machine=lst[3],
                                                  processing_id=int(lst[4]),
                                                  cut_width=Decimal(lst[5]), cut_length=Decimal(lst[6])
                                                  , processed_numbers=int(lst[7]), processed_packets=int(lst[8]),
                                                  processed_wt=Decimal(lst[10]), remarks=lst[9],
                                                  input_width=Decimal(lst[11]), input_length=Decimal(lst[12]),
                                                  order_detail_id=lst[13])
                processing_dtl_lst.append(processing_dtl)
            return processing_dtl_lst

    @classmethod
    def load_for_report(cls, processing_id):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("select * from processing_detail where processing_id = %s ", (processing_id,))
            user_data = cursor.fetchall()
            processing_dtl_lst = []
            for lst in user_data:
                processing_dtl = ProcessingDetail(smpl_no=lst[1], operation=lst[2], machine=lst[3],
                                                  processing_id=int(lst[4]),
                                                  cut_width=Decimal(lst[5]), cut_length=Decimal(lst[6])
                                                  , processed_numbers=int(lst[7]), processed_packets=int(lst[8]),
                                                  processed_wt=Decimal(lst[10]), remarks=lst[9],
                                                  input_width=Decimal(lst[11]), input_length=Decimal(lst[12]))
                processing_dtl_lst.append(processing_dtl)
            return processing_dtl_lst