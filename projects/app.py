from flask import Flask, render_template, request
from incoming import Incoming
from current_stock import CurrentStock
from decimal import Decimal
from user import User
from flask_login import LoginManager, login_user, current_user, logout_user
from file_uploader import FileUploader
from processing import Processing
from processing_detail import ProcessingDetail
from slitter_usage import SlitterUsage
from dispatch_header import DispatchHeader
from dispatch_detail import DispatchDetail
from slitter_batch import SlitterBatch
import time


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


# Clicking on http://127.0.0.1:5000/ (the home page), this will redirect you to login page
@app.route('/')
def home(message=""):
    return render_template('/home.html', message=message)


@login_manager.user_loader
def user_loader(username):
    return User.get(username)


# Login page. Authenticates user and then proceeds
# Sources for login and logout functions
# http://gouthamanbalaraman.com/blog/minimal-flask-login-example.html
# https://realpython.com/blog/python/using-flask-login-for-user-management-with-flask/
# https://flask-login.readthedocs.io/en/latest/#flask_login.LoginManager
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
    else:
        username = request.args.get('username')
        pwd = request.args.get('password')
    user = User.get(username)
    if pwd == user.password:
        login_user(user, remember=True)
        return render_template('/main_menu.html')
    else:
        return render_template('/unsuccessful_login.html')


# This is for the user to logout. Redirects back to the login page
@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return render_template('/home.html')


# Main Menu page. Once logged in, the user will always come back to this after his operations done
@app.route('/main_menu')
def main_menu(message=""):
    user = current_user
    try:
        if user.username is not None:
            return render_template('/main_menu.html', current_user=user, message=message)
    # In case the user is not logged in => no username is detected, the user cannot reach the main menu page and is
    # redirected to the login page
    except AttributeError:
        return render_template('/home.html', message="Please login first")


# If login fail, will be redirected to login page with message
@app.route('/unsuccessful_login')
def unsuccessful_login():
    return render_template('/home.html', message="Wrong details! Please retry!")


# This is to load the change password page. The message returned if old password is incorrect
@app.route('/change_password_form')
def change_password_form(message=""):
    return render_template('/change_password.html', message=message)


# Change password on submit. Checks if old password is correct and then updates user with new password
@app.route('/change_pwd', methods=['POST', 'GET'])
def change_pwd():
    if request.method == 'POST':
        old_pwd = request.form['old_password']
        new_pwd = request.form['new_password']

    else:
        old_pwd = request.args.get('username')
        new_pwd = request.args.get('new_password')

    user = current_user
    user = User.get(user.username)
    if old_pwd == user.password:
        user.update_pwd(new_pwd)
    else:
        return render_template('/change_password.html', message="Password is incorrect. Please re-enter details")
    logout_user()
    return render_template('/home.html', message="Please login again")

@app.route('/change_unit', methods=['GET', 'POST'])
def change_unit():
    unit = ""
    if request.method == 'POST':
        unit = request.form['unit']

    if request.method == 'GET':
        unit = request.args.get('unit')

    user = current_user
    if unit == '1':
        current_user.unit = 1
    if user == '2':
        current_user.unit = 2

    return render_template('/main_menu.html')


# This is for incoming of smpl coil. The details are got from the xml file generated from Tally.
# The filename is to be entered here
@app.route('/incoming_input_smpl', methods=['GET', 'POST'])
def incoming_input_smpl():
    return render_template('/incoming_enter_xml.html')


# This is for incoming of TR coil.
@app.route('/incoming_input_tr', methods=['GET', 'POST'])
def incoming_input_tr():
    return render_template('/incoming_for_tr.html')


# XML filename to be entered. After filename given, a table is generated with all the details populated in
#  incoming_review_after_upload_form.html. The user gets a chance to review the details and enter remarks, if any.
@app.route('/smpl_incoming', methods=['GET', 'POST'])
def smpl_incoming():

    if request.method == 'POST':
        
        xml_filename = request.files['xml_filename']

    else:
        xml_filename = request.args.get('xml_filename')

    incoming_lst = Incoming.fromfile(xml_filename)
    # The details got from the XML file are updated to the database. The details are displayed for review and if any
    # remarks are to be entered
    for incoming_coil in incoming_lst:
        incoming_coil.savetodb()
    return render_template('incoming_review_after_upload_form.html', incoming_lst=incoming_lst)


# The remarks are recovered. SMPL No is made a hidden field in the HTML to map the remarks and the SMPL
# This is then updated to the DB and then redirects to the main menu
@app.route('/submit_smpl_incoming', methods=['GET', 'POST'])
def submit_smpl_incoming():
    incoming_remarks = []
    smpl_nos = []
    if request.method == 'POST':
        incoming_remarks = request.form.getlist('remarks')
        smpl_nos = request.form.getlist('smpl_nos')
    for remark, smpl_no in zip(incoming_remarks, smpl_nos):
        Incoming.update_remarks_by_smpl_no(remark, smpl_no)

    if request.method == 'GET':
        pass
    return render_template('/main_menu.html', message="Incoming details updated")


# This will take details for TR coils that are entered manually and then commits to DB
@app.route('/tr_incoming_commit', methods=['GET', 'POST'])
def tr_incoming_commit():
    smpl_no = ""
    if request.method == 'POST':
        smpl_no = "TR" + request.form['smpl_no']
        smpl_no = smpl_no.replace(" ", "")
        customer = request.form['customer']
        incoming_date = request.form['incoming_date']
        thickness = Decimal(request.form['thickness'])
        width = Decimal(request.form['width'])
        length = (request.form['length'])
        grade = request.form['grade']
        weight = Decimal(request.form['weight'])
        numbers = int((request.form['numbers']))
        mill = request.form['mill']
        mill_id = request.form['mill_id']
        incoming_remarks = request.form['remarks']
        unit = request.form['unit']
        _incoming = Incoming(smpl_no, customer, incoming_date, thickness, width, length, grade, weight, numbers, mill,
                             mill_id, incoming_remarks, unit)
        _incoming.savetodb()

    return render_template('/main_menu.html', message="Incoming details for " + smpl_no + " entered.")


# This function is to place raw material on hold. A list is obtained from current_stock table and displayed.
# The user has to pick from this list
@app.route('/rm_onhold', methods=['GET', 'POST'])
def rm_onhold():
    cs_return_lst = CurrentStock.rm_list_for_hold()
    cs_obj_lst = []
    cs_id_lst = []

    for cs_id, cs in cs_return_lst:
        cs_id_lst.append(cs_id)
        cs_obj_lst.append(cs)

    if cs_obj_lst:
        return render_template('rm_on_hold_pick_smpl.html', cs_lst=zip(cs_id_lst, cs_obj_lst))
    else:
        return render_template('/main_menu.html', message="No raw material available to put on hold")


# Once the RM to be placed on hold is selected. The status in current_stock is updated to RM - On Hold. With remarks
#  updated in Incoming
@app.route('/put_on_hold', methods=['GET', 'POST'])
def put_on_hold():
    hold_remarks = ""
    smpl = ""
    if request.method == 'POST':
        smpl = request.form['select_smpl']
        hold_remarks = request.form['remarks']

    if request.method == 'GET':
        smpl = request.args.get('select_smpl')
        hold_remarks = request.args.get('remarks')

    smpl_details = smpl.split(',')
    smpl_no = smpl_details[1]
    cs_id = smpl_details[0]
    CurrentStock.update_status_cls(cs_id, "RM - On Hold")
    hold_remarks = " Put hold because " + hold_remarks + " on " + time.strftime("%d/%m/%Y")
    Incoming.update_remarks(hold_remarks, smpl_no)
    return render_template('/main_menu.html', message=smpl_no + " placed on hold")


# This function is to unhold the raw material. The list of rm which is currently on hold is displayed
@app.route('/rm_unhold', methods=['GET', 'POST'])
def rm_unhold():
    cs_return_lst = CurrentStock.rm_list_for_unhold()
    cs_obj_lst = []
    cs_id_lst = []

    for cs_id, cs in cs_return_lst:
        cs_id_lst.append(cs_id)
        cs_obj_lst.append(cs)
    if cs_obj_lst:
        return render_template('rm_undo_hold.html', cs_lst=zip(cs_id_lst, cs_obj_lst))
    else:
        return render_template('/main_menu.html', message="No raw material is currently on hold")


# The selected SMPL in removed from hold. The remarks are updated in incoming table.
@app.route('/put_on_unhold', methods=['GET', 'POST'])
def put_on_unhold():
    unhold_remarks = ""
    smpl = ""
    if request.method == 'POST':
        smpl = request.form['select_smpl']
        unhold_remarks = request.form['remarks']

    if request.method == 'GET':
        smpl = request.args.get('select_smpl')
        unhold_remarks = request.args.get('remarks')

    smpl_details = smpl.split(',')
    smpl_no = smpl_details[1]
    cs_id = smpl_details[0]
    CurrentStock.update_status_cls(cs_id, "RM")
    unhold_remarks = " Removed from hold because " + unhold_remarks + " on " + time.strftime("%d/%m/%Y")
    Incoming.update_remarks(unhold_remarks, smpl_no)
    return render_template('/main_menu.html')


# In this function, the user can select the smpl to be transferred to the other unit.

@app.route('/transfer_material', methods=['GET', 'POST'])
def transfer_material():
    cs_return_lst = CurrentStock.get_stock('All')
    cs_obj_lst = []
    cs_id_lst = []

    for cs_id, cs in cs_return_lst:
        cs_id_lst.append(cs_id)
        cs_obj_lst.append(cs)

    if cs_obj_lst:
        return render_template('transfer_material.html', cs_lst=zip(cs_id_lst, cs_obj_lst))
    else:
        return render_template('/main_menu.html', message="No Raw material to transfer")


# On selection and submit, the unit is changed in current_stock and remarks are updated in incoming about the transfer
# and when it was transferred
@app.route('/transfer_submit', methods=['GET', 'POST'])
def transfer_submit():
    smpl = ""
    unit = ""
    transfer_remarks = ""
    if request.method == 'POST':
        smpl = request.form['select_smpl']
        unit = request.form['unit']
        transfer_remarks = request.form['remarks']

    if request.method == 'GET':
        smpl = request.args.get('select_smpl')
        unit = request.args.get('unit')
        transfer_remarks = request.args.get('remarks')

    smpl_details = smpl.split(',')
    smpl_no = smpl_details[1]
    cs_id = smpl_details[0]
    CurrentStock.transfer_material_cls(cs_id, unit)
    transfer_remarks = " Transferred to Unit " + unit + " for " + transfer_remarks + " on " + time.strftime("%d/%m/%Y")
    Incoming.update_remarks(transfer_remarks, smpl_no)
    return render_template('/main_menu.html')


# pick smpl for uploading documents
@app.route('/upload_pick_smpl', methods=['GET', 'POST'])
def upload_pick_smpl(message=""):
    return render_template('/upload_pick_smpl.html', message=message)


# Check if entered SMPL for uploading documents exist and then forward to uploading page
@app.route('/upload_pick_smpl_submit', methods=['GET', 'POST'])
def upload_smpl_submit():
    smpl_no = ""
    if request.method == 'POST':
        smpl_no = request.form['smpl_no']
    if request.method == 'GET':
        smpl_no = request.args.get('smpl_no')

    smpl_no = smpl_no.replace(" ", "")
    incoming = Incoming.load_smpl_by_smpl_no(smpl_no)

    if incoming:
        return render_template('/upload_documents.html', incoming=incoming)

    else:
        return render_template('/upload_pick_smpl.html', message="SMPL no. does not exist. Please re-check")


@app.route('/upload_docs_submit', methods=['GET', 'POST'])
def upload_docs_submit():
    return_file_list = ""
    if request.method == 'POST':
        smpl_no = request.form['smpl_no']
        if 'cust_order_files[]' in request.files:
            files = request.files.getlist("cust_order_files[]")
            file_type = "cust_order"
            return_file_list += FileUploader.upload_files(smpl_no, file_type, files)
        if 'smpl_order_files[]' in request.files:
            files = request.files.getlist("smpl_order_files[]")
            file_type = "smpl_order"
            return_file_list += FileUploader.upload_files(smpl_no, file_type, files)
        if 'prod_rprt_files[]' in request.files:
            files = request.files.getlist("prod_rprt_files[]")
            file_type = "prod_rprt"
            return_file_list += FileUploader.upload_files(smpl_no, file_type, files)

    if len(return_file_list) > 1:
        return render_template('/upload_pick_smpl.html', message="These files were not uploaded. Please check the file "
                                                                 "extension and retry" + return_file_list)
    else:
        return render_template('/main_menu.html', message='Files uploaded successfully')


# To load orders by machine to chose for processing
@app.route('/orders_by_machine', methods=['GET', 'POST'])
def orders_by_machine():
    operation = ""
    if request.method == 'POST':
        operation = request.form['select_operation']

    if request.method == 'GET':
        operation = request.args.get('select_operation')

    if current_user.unit == 1 or current_user.unit == 2:
        cs_lst = CurrentStock.smpl_list_for_place_order(operation, current_user.unit)

    if cs_lst:
        return render_template('/processing_pick_smpl.html', operation=operation, cs_lst=cs_lst)
    else:
        return render_template('/main_menu.html', message="No raw material or WIP available!")


# Function to load details of raw material and order for the smpl selected
@app.route('/processing_load', methods=['GET', 'POST'])
def processing_load():
    operation = ""
    cs_rm_id = ""
    if request.method == 'POST':
        cs_rm_id = request.form['select_smpl']
        operation = request.form['operation']
    if request.method == 'GET':
        cs_rm_id = request.args.get('select_smpl')
        operation = request.args.get('operation')

    cs_rm = CurrentStock.load_smpl_by_id(cs_rm_id)
    incoming = Incoming.load_smpl_by_smpl_no(cs_rm.smpl_no)

    processing_detail_lst = ProcessingDetail.load_from_db(cs_rm.smpl_no, operation)

    if operation == "CTL":
        return render_template('processing_ctl.html', incoming=incoming, operation=operation,
                               processing_details_lst=processing_detail_lst, cs_rm=cs_rm, cs_rm_id=cs_rm_id)

    if operation == "Narrow CTL":
        return render_template('processing_nctl.html', incoming=incoming, operation=operation,
                               processing_details_lst=processing_detail_lst, cs_rm=cs_rm, cs_rm_id=cs_rm_id)

    if operation == 'Slitting' or operation == 'Mini Slitting':
        # if operation == 'Slitting':
        #    _operation = 'Slitting'
        # if operation == 'Mini Slitting':
        #    _operation = 'Mini Slitting'
        return render_template('processing_slit.html', incoming=incoming, operation=operation,
                               processing_details_lst=processing_detail_lst, cs_rm=cs_rm, cs_rm_id=cs_rm_id)

    if operation == 'Reshearing':
        return render_template('processing_reshearing.html', incoming=incoming, operation=operation,
                               processing_details_lst=processing_detail_lst, cs_rm=cs_rm, cs_rm_id=cs_rm_id)


# 1. Get processing and processing details from the screen
# 2. Reduce the qty from mother material and update/insert cut material in current_stock
# 3. Check if stage is complete. If yes, change status of next stage in order detail to ready and current stage to
# completed
# 4. If all stages complete, the mark order closed
@app.route("/submit_processing", methods=['GET', 'POST'])
def submit_processing():
    if request.method == 'POST':
        smpl_no = request.form['smpl_no']
        operation = request.form['operation']

        input_size = request.form['input_material']
        output_width_lst = request.form.getlist('output_width')
        output_length_lst = request.form.getlist('output_length')

        fg_yes_no_lst = request.form.getlist('fg_yes_no')
        actual_no_of_pieces_lst = request.form.getlist('actual_no_of_pieces')
        actual_no_of_packets_lst = request.form.getlist('actual_no_of_packets')
        processed_wt_lst = request.form.getlist('processed_wt')
        remarks_lst = request.form.getlist('remarks')

        machine = request.form['machine']
        processing_date = request.form['processing_date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        processing_time = request.form['processing_time']
        customer = request.form['customer']
        thickness = float(request.form['thickness'])
        grade = request.form['grade']

        no_of_qc = request.form['no_of_qc']
        no_of_helpers = request.form['no_of_helpers']
        names_of_qc = request.form['names_of_qc']
        names_of_helpers = request.form['names_of_helpers']
        name_of_packer = request.form['name_of_packer']

        setting_date = request.form['setting_date']
        setting_start_time = request.form['setting_start_time']
        setting_end_time = request.form['setting_end_time']
        setting_time = request.form['setting_time']

        # Processing object created and saved to db
        processing = Processing(smpl_no, operation, processing_date, start_time, end_time, setting_start_time,
                                setting_end_time, processing_time, setting_time, no_of_qc, no_of_helpers, names_of_qc, 
                                names_of_helpers, name_of_packer, setting_date)
        processing_id = processing.save_to_db()

        # Slitting/Mini Slitting and CTL/Reshearing/NCTL are managed differently
        if operation == "CTL" or operation == "Reshearing" or operation == "Narrow CTL":
            lamination_lst = request.form.getlist('lamination')
            for output_width, output_length, actual_no_of_pieces, actual_no_of_packets, processed_wt, \
                remarks, fg_yes_no, lamination in zip(output_width_lst, output_length_lst, actual_no_of_pieces_lst,
                                                      actual_no_of_packets_lst, processed_wt_lst, remarks_lst,
                                                      fg_yes_no_lst, lamination_lst):
                ip_size = input_size.split('x')
                ms_width = ip_size[0]
                ms_length = ip_size[1]

                if lamination == "single-side" or lamination == "double-side":
                    machine += " " + lamination

                if processed_wt != '':
                    # Get mother size and cut size from the screen. Create processing detail and then update to db
                    processing_detail = ProcessingDetail(smpl_no, operation, machine, processing_id, ms_width,
                                                         ms_length, output_width, output_length, actual_no_of_pieces,
                                                         actual_no_of_packets, processed_wt, remarks)
                    processing_detail.save_to_db()

                    # Reduce weight of mother material by the processed weight of cut material
                    CurrentStock.change_wt(smpl_no, ms_width, ms_length, processed_wt, actual_no_of_pieces, "minus")

                    # Increase weight of cut material by processed weight. If cut material, doesn't already exist, the
                    # function returns insert => a new record has to be inserted
                    cc_insert = CurrentStock.change_wt(smpl_no, output_width, output_length, processed_wt,
                                                       actual_no_of_pieces, "plus")

                    # Unit of the material is decided based on the machine used to process the material.
                    # WARNING: This is bad programming
                    if machine == "CTL 2" or machine == "Slitting" or machine == "Mini Slitting" or \
                            machine == "Reshearing 5" or machine == "Reshearing 6" or machine == "Reshearing 7" or \
                            machine == "NCTL 2" or machine == "NCTL 3":
                        unit = '2'
                    else:
                        unit = '1'

                    # The new material is inserted in to current stock
                    if cc_insert == "insert":
                        cs_cc = CurrentStock(smpl_no, customer, processed_wt, actual_no_of_pieces, thickness,
                                             output_width, output_length, fg_yes_no, grade, unit)
                        cs_cc.save_to_db()

                    # This checks if detail is complete by comparing the processed weight and order detail weight.
                    # If the order detail is complete, it checks if all the order details in that stage are complete 
                    # (check_stage_complete)
                    # If all the order details in that stage are complete, it makes the order details of the next stage 
                    # ready for production
                    # If this is the last stage of the order, it marks the order as closed
                    # OrderDetail.detail_complete(order_detail_id)

        if operation == "Slitting" or operation == "Mini Slitting":
            ip_size = input_size.split('x')
            ms_width = ip_size[0]
            ms_length = ip_size[1]

            # actual_no_of_pieces = length processed per part
            # actual_no_of_packets = no of parts
            # numbers = no of slits
            total_length = float(request.form['total_length'])

            no_of_parts = int(actual_no_of_packets_lst[0])
            length_per_part = float(total_length/no_of_parts)
            no_of_slits_lst = request.form.getlist('no_of_slits')
            # processed_wt = processed_wt_lst[0]
            remarks = remarks_lst[0]
            output_length = 0
            for output_width, fg_yes_no, no_of_slits in zip(
                    output_width_lst, fg_yes_no_lst, no_of_slits_lst):

                # Get number of coils produced for size = no of slits x no of parts
                no_of_coils = int(no_of_slits) * no_of_parts
                # This is processed weight for that size
                processed_wt = Decimal(thickness * float(output_width) * length_per_part * 0.00000785 * no_of_coils)
                processed_wt = round(processed_wt, 3)

                # Processing details updated to db
                if processed_wt > 0:
                    processing_detail = ProcessingDetail(smpl_no, operation, machine, processing_id, ms_width,
                                                         ms_length, output_width, output_length, length_per_part,
                                                         no_of_coils, processed_wt, remarks)

                    processing_detail.save_to_db()

                    # Reduce weight of mother material by the processed weight of cut material
                    CurrentStock.change_wt(smpl_no, ms_width, ms_length, processed_wt, length_per_part, "minus")

                    # Increase weight of cut material by processed weight. If cut material, doesn't already exist, the
                    # function returns insert => a new record has to be inserted
                    cc_insert = CurrentStock.change_wt(smpl_no, output_width, output_length, processed_wt,
                                                       length_per_part, "plus")

                    # Unit of the material is decided based on the machine used to process the material.
                    # WARNING: This is bad programming
                    if machine == "CTL 2" or machine == "Slitting" or machine == "Mini Slitting" \
                            or machine == "Reshearing 5" or machine == "Reshearing 6" \
                            or machine == "Reshearing 7" or machine == "NCTL 1" or machine == "NCTL 2":
                        unit = '2'
                    else:
                        unit = '1'

                    # The new material is added to current stock
                    if cc_insert == "insert":
                        cs_cc = CurrentStock(smpl_no, customer, processed_wt, no_of_coils, thickness,
                                             output_width, output_length, fg_yes_no, grade, unit)
                        cs_cc.save_to_db()

                    # This checks if detail is complete by comparing the processed weight and order detail weight.
                    # If the order detail is complete, it checks if all the order details in that stage are complete 
                    # (check_stage_complete)
                    # If all the order details in that stage are complete, it makes the order details of the next stage 
                    # ready for production
                    # If this is the last stage of the order, it marks the order as closed
                    # OrderDetail.detail_complete(order_detail_id)

            # This is for the slitter maintenance
            # Get the slitter batches and numbers used in slitting
            slitter_batch_lst = request.form.getlist('slitter_batch')
            slitter_number_lst = request.form.getlist('slitter_number')

            # The meterage is updated to the slitter usage  and slitter grinding table
            for slitter_batch, slitter_numbers in zip(slitter_batch_lst, slitter_number_lst):
                slitter_numbers = slitter_numbers.split(' ')
                for slitter_number in slitter_numbers:
                    slitter_usage = SlitterUsage(processing_id, smpl_no, slitter_batch, slitter_number, total_length,
                                                 thickness)
                    slitter_usage.save_to_db()

        return render_template('/main_menu.html', message="Processing for " + smpl_no + " entered.")


@app.route('/check_stock', methods=['GET', 'POST'])
def check_stock():
    return render_template('check_stock.html')


# Function displays stock based on stock type selected
@app.route('/stock', methods=['GET', 'POST'])
def stock():
    stock_type = ""
    if request.method == 'POST':
        stock_type = request.form['stock_type']

    if request.method == 'GET':
        stock_type = request.args.get('stock_type')

    cs_lst = CurrentStock.get_stock(stock_type)

    return render_template('stock_display.html', cs_lst=cs_lst)


# Choose from list of customer for whose FG/RM is present for dispatch
@app.route('/dispatch_pick_customer', methods=['GET', 'POST'])
def dispatch_pick_customer():
    customer_lst = CurrentStock.customer_list_for_dispatch()
    return render_template('dispatch_pick_customer.html', customer_lst=customer_lst)


# Display list of FG/RM of selected customer to choose for dispatch
@app.route('/dispatch_list', methods=['GET', 'POST'])
def dispatch_list():
    customer = ""
    display_type = ""
    if request.method == 'POST':
        customer = request.form['select_customer']
        display_type = request.form['FG/RM']
    if request.method == 'GET':
        customer = request.args.get('select_customer')
        display_type = request.args.get('FG/RM')

    cs_lst = CurrentStock.get_stock_by_customer(customer, display_type)

    return render_template('dispatch_list.html', cs_lst=cs_lst, customer=customer)


@app.route('/dispatch', methods=['GET', 'POST'])
def dispatch():
    if request.method == 'POST':
        dispatch_lst = request.form.getlist['select_smpl']
        dispatch_nos = request.form.getlist['dispatch_numbers']
        dispatch_quantity = request.form.getlist['dispatch_quantity']
        vehicle_no = request.form['vehicle_no']
        customer = request.form['customer']
        dispatch_date = request.form['dispatch_date']
        dispatch_time = request.form['dispatch_time']
        dispatch_pkts = request.form.getlist['dispatch_packets']
        remarks = request.form['remarks']

    if request.method == 'GET':
        dispatch_lst = request.args.getlist('select_smpl')
        dispatch_nos = request.args.getlist('dispatch_numbers')
        dispatch_quantity = request.args.getlist('dispatch_quantity')
        dispatch_pkts = request.args.getlist('dispatch_packets')
        defectives = request.args.getlist('defective')
        vehicle_no = request.args.get('vehicle_no')
        customer = request.args.get('customer')
        dispatch_date = request.args.get('dispatch_date')
        dispatch_time = request.args.get('dispatch_time')
        remarks = request.args.get('remarks')

    # This fetches the list and removes the elements that are not selected
    # The ones that are not selected are returned as None. The below list filters out the Nones
    dispatch_nos_lst = list(filter(None, dispatch_nos))
    dispatch_quantity_lst = list(filter(None, dispatch_quantity))
    defectives_lst = list(filter(None, defectives))
    dispatch_pkts_lst = list(filter(None,dispatch_pkts))

    dispatch_header = DispatchHeader(vehicle_no, customer, dispatch_date, dispatch_time, remarks)
    dispatch_id = dispatch_header.save_to_db()

    # For the items to be dispatched, dispatch detail is created and the current stock quantity is deleted or reduced
    for smpl, dispatch_nos, dispatch_qty, defective, no_of_packets in zip(dispatch_lst, dispatch_nos_lst, 
        dispatch_quantity_lst, defectives_lst, dispatch_pkts_lst):
        smpl_details = smpl.split(',')
        smpl_no = smpl_details[1]
        cs_id = smpl_details[0]
        cs = CurrentStock.load_smpl_by_id(cs_id)
        dispatch_detail = DispatchDetail(dispatch_id, cs.smpl_no, cs.thickness, cs.width, cs.length, int(dispatch_nos),
                                         Decimal(dispatch_qty), defective, int(no_of_packets))
        dispatch_detail.save_to_db()
        if dispatch_nos == cs.numbers:
            CurrentStock.delete_record(cs_id)
        else:
            cs.change_wt(smpl_no, cs.width, cs.length, dispatch_qty, dispatch_nos,'minus')

    return render_template('/main_menu.html')


@app.route('/display_dispatch_pick_day', methods=['GET', 'POST'])
def display_dispatch_pick_day():
    return render_template('dispatch_pick_date.html')


@app.route('/dispatch_list_hdr_by_date', methods=['GET', 'POST'])
def dispatch_list_hdr_by_date():
    if request.method == 'POST':
        dispatch_date = request.form['dispatch_date']
    if request.method == 'GET':
        dispatch_date = request.args.get('dispatch_date')

    dispatch_hdr_lst = DispatchHeader.get_dispatch_lst_by_date(dispatch_date)
    return render_template('pick_dispatch_hdr.html', dispatch_hdr_lst=dispatch_hdr_lst)


@app.route('/dispatch_view_detail', methods=['GET', 'POST'])
def dispatch_view_detail():
    if request.method == 'POST':
        select_dispatch_hdr_id = request.form['select_dispatch_hdr']
    if request.method == 'GET':
        select_dispatch_hdr_id = request.args.get('select_dispatch_hdr')

    dispatch_detail_lst = DispatchDetail.get_details_by_id(select_dispatch_hdr_id)
    dispatch_hdr = DispatchHeader.get_hdr_by_id(select_dispatch_hdr_id)

    return render_template('dispatch_view.html', dispatch_hdr=dispatch_hdr, dispatch_detail_lst=dispatch_detail_lst)


@app.route('/pick_slitting_batch', methods=['GET', 'POST'])
def pick_slitting_batch():
    slitter_lst = SlitterBatch.getSlitterLst()
    return render_template('slitter_pick_batch.html', slitter_lst=slitter_lst)


@app.route('/slitter_grinding_entry', methods=['GET', 'POST'])
def slitter_griding_entry():
    if request.method == 'POST':
        slitter_batch_no = request.form['select_slitter']
        submit_type = request.form['submit']
    if request.method == 'GET':
        slitter_batch_no = request.args.get('select_slitter')
        submit_type = request.args.get('submit')

    slitter_batch = SlitterBatch.load_slitter(slitter_batch_no)

    if submit_type == 'Enter Grinding Details':
        return render_template('slitter_grinding.html', slitter_batch=slitter_batch)

    if submit_type == 'View Slitter Details':
        slitter_grinding_lst = slitter_batch.get_slitter_grinding()
        return render_template('slitter_batch_view.html', slitter_batch=slitter_batch, 
                                slitter_grinding_lst=slitter_grinding_lst)


@app.route('/slitter_grinding_submit', methods=['GET','POST'])
def slitter_grinding_submit():
    if request.method == 'POST':
        slitter_batch_no = request.form['slitter_batch']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        return_date = request.form['return_date']
        new_od = request.form['new_od']
    if request.method == 'GET':
        slitter_batch_no = request.args.get('slitter_batch')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        return_date = request.args.get('return_date')
        new_od = request.args.get('new_od')

    SlitterBatch.after_return_from_grinding(slitter_batch_no, end_date, return_date, float(new_od))
    return render_template('/main_menu.html')



@app.route('/enter_smpl_no', methods=['GET', 'POST'])
def enter_smpl_no():
    return render_template('/history_enter_smpl_no.html')


@app.route('/history_show_details', methods=['GET', 'POST'])
def history_show_details():
    smpl_no = ""
    if request.method == 'POST':
        smpl_no = request.form['smpl_no']
    if request.method == 'GET':
        smpl_no = request.args.get('smpl_no')

    smpl_no_lst = Incoming.smpl_no_list_for_history(smpl_no)
    if smpl_no_lst:
        incoming = Incoming.load_smpl_by_smpl_no(smpl_no)

        processing_hdr_lst = []
        processing_dtl_lst = []
        dispatch_hdr_lst = []
        dispatch_dtl_lst = []
        dispatch_id_lst = []
        for smpl_no in smpl_no_lst:
            processing_hdr_lst.append(Processing.load_history(smpl_no))
            processing_dtl_lst.append(ProcessingDetail.load_history(smpl_no))

            dispatch_dtl_lst.append(DispatchDetail.load_from_db(smpl_no))
            for dispatch_dtl_sublst in dispatch_dtl_lst:
                for dispatch_dtl in dispatch_dtl_sublst:
                    dispatch_id_lst.append(dispatch_dtl.dispatch_id)

            dispatch_id_lst = list(set(dispatch_id_lst))
            for dispatch_id in dispatch_id_lst:
                dispatch_hdr_lst.append(DispatchHeader.load_from_db(dispatch_id))

        file_list = FileUploader.get_files_for_smpl_no(smpl_no)

        return render_template('/history_view.html', incoming=incoming, file_list=file_list)
    else:
        return render_template('/main_menu.html')


if __name__ == '__main__':
    app.config["SECRET_KEY"] = "SMPLMRP"
    # app.run(debug=True)
    SERVER_NAME = 'UNIT2-OFFICE2'
    SERVER_PORT = 5001
    app.run(SERVER_NAME, SERVER_PORT, threaded=True)
