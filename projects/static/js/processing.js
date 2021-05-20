
// This function is to set the focus when the page loads for CTL, NCTL and Reshearing operations
function setFocusToTextBox(operation){
    if(operation == "Narrow_CTL"){
        document.getElementById("actual_no_of_pieces").focus();
    }
    if(operation == "Reshearing"){
        document.getElementById("output_width").focus();
    }
    if(operation == "CTL"){
        document.getElementById("output_length").focus();
    }
}


// This function is to set the focus when the page loads for slitting operation
function setFocusToTextBox_Slit(operation){

        document.getElementById("output_width").focus();
        if(operation == "Mini_Slitting"){
            add_row_for_length();
        }


}


// This function calculates the weight for CTL, NCTL and Reshearing functions
function for_packets_and_weight(table_id,table_row,operation){

   // Get the row where the change was made and calculate the weight of the processed material
	var rowCount = table_row.offsetParent.parentElement.rowIndex;
	var last_row = document.getElementById(table_id).rows[rowCount];
	//var numbers = Number(last_row.cells[3].lastChild.value);
	var thk = Number(document.getElementById('thickness').value);
	//var weight_pos = 5;
    var width =  Number(last_row.cells[0].lastChild.value);


    var length =  Number(last_row.cells[1].lastChild.value);

    var numbers =  Number(last_row.cells[4].lastChild.value);
    weight_pos = 5;

    var weight = (thk * width * length * numbers * 0.00000785)/1000;
    last_row.cells[weight_pos].lastChild.value = weight.toFixed(3);
    var rm_weight = Number(document.getElementById("weight").value);

    calculate_wt_and_cuts(table_id);
}

// To calculate processed weight and no of cuts every time numbers are changed
function calculate_wt_and_cuts(table_id){
    var table = document.getElementById(table_id);
    var total_processed_wt =0;
    var total_cuts = 0;
    var total_pkts;
    for (var i = 1, row; row = table.rows[i]; i++) {
        total_processed_wt += Number(row.cells[5].lastChild.value);
        total_cuts += Number(row.cells[4].lastChild.value);

    }
    //var total_order_wt = Number(document.getElementById("order_wt").value);
    //var completed_proc_wt = Number(document.getElementById("tot_proc_wt").value);
    //var scrap_wt = total_order_wt - total_processed_wt - completed_proc_wt ;


    document.getElementById("total_processed_wt").value = Number(total_processed_wt.toFixed(3));
    document.getElementById("total_cuts").value = total_cuts;
    document.getElementById("total_packets").value = table.rows.length - 1;

    validate();

    //document.getElementById("balance_wt").value = scrap_wt.toFixed(3);
    //document.getElementById("scrap_wt").value = Number(scrap_wt.toFixed(3));
}

function time_taken(){
   var t1 = document.getElementById("start_time").value;
   var t2 = document.getElementById("end_time").value;

   var parts = t1.split(':');
   var d1 = Number(parts[0])*60 + Number(parts[1]);
   parts = t2.split(':');
   var d2 = Number(parts[0])*60 + Number(parts[1]);
   // this would also work
   // d2.toTimeString().substr(0, d2.toTimeString().indexOf(' '));
   if(d2>d1){
    var diff =  d2 - d1;
    document.getElementById("processing_time").value = diff;
   }
   else{
    document.getElementById("end_time").value = "";
    alert("Please re-enter the time. End time must be greater than start time");
    document.getElementById("start_time").focus();
   }
    validate();
}

function time_taken_setting(){
   var t1 = document.getElementById("setting_start_time").value;
   var t2 = document.getElementById("setting_end_time").value;
   var parts = t1.split(':');
   var d1 = Number(parts[0])*60 + Number(parts[1]);
   parts = t2.split(':');
   var d2 = Number(parts[0])*60 + Number(parts[1]);
   // this would also work
   // d2.toTimeString().substr(0, d2.toTimeString().indexOf(' '));
   if(d2>=d1){
    var diff =  d2 - d1;
    document.getElementById("setting_time").value = diff;
   }
   else{
    document.getElementById("setting_end_time").value = "";
    alert("Please re-enter the time. End time must be greater than start time");
    document.getElementById("setting_start_time").focus();
   }
}
function change_part_length(table_id){
    var table = document.getElementById(table_id);
    var total_processed_wt =0;
    var total_length = 0;
    var total_parts = 0;
    for (var i = 1, row; row = table.rows[i]; i++) {
        total_length += Number(row.cells[0].lastChild.value);
    }
    document.getElementById("total_length").value = total_length;
    document.getElementById("total_parts").value = table.rows.length-1;
    if(document.getElementById("total_width").value){
    get_part_weight();
   }

}

function change_width(table_id){
    var table = document.getElementById(table_id);
    var total_width =0;

    for (var i = 1, row; row = table.rows[i]; i++) {
        total_width += Number(row.cells[0].lastChild.value);
    }
    document.getElementById("total_width").value = total_width;
   if(document.getElementById("total_length").value){
    get_part_weight();
   }

}

//Calculates processed weight for slitting
function get_part_weight(){
    var total_length = Number(document.getElementById("total_length").value);

    var thickness = Number(document.getElementById("thickness").value);
    var input_material = (document.getElementById("input_material").value);
    input_material = input_material.split("x");

    var width = Number(input_material[0]);
    rm_wt = Number(document.getElementById("input_weight").value);

    var total_processed_wt = thickness * width * total_length * 0.00000785;
    var coil_length = rm_wt/thickness/width/0.00000785;
    document.getElementById("total_processed_wt").value = total_processed_wt.toFixed(3);

    //var total_order_wt = Number(document.getElementById("order_wt").value);
    //var completed_proc_wt = Number(document.getElementById("tot_proc_wt").value);
    //var scrap_wt = total_order_wt - total_processed_wt - completed_proc_wt ;


    //document.getElementById("balance_wt").value = scrap_wt.toFixed(3);

    //validate();
}

function add_row_for_length(){
    var input_size_tbl = document.getElementById('numbers_pkts1');
    var input_material, newHTML;
    var input_mtrl_array = [];
    var html = '<tr><td><input type = "text" id="ip_sz_for_length" value = "%input_sz%" readonly></td><td><input type="number" id="length_run_for_sz" value = ""></td><td><input type="number" id="no_of_parts_for_sz" value = "" readonly><td><input type="number" id="wt_run_for_sz" value = "" readonly></td></tr>'
    for(i=1;i<input_size_tbl.rows.length;i++){
        if (input_mtrl_array.includes(input_size_tbl.rows[i].cells[0].childNodes[0].value)== false){
            input_mtrl_array.push(input_size_tbl.rows[i].cells[0].childNodes[0].value);
        }
    }
    for(i=0;i<input_mtrl_array.length;i++){
        newHTML = html.replace('%input_sz%', input_mtrl_array[i]);
        document.getElementById('length_processed').insertAdjacentHTML('beforeend', newHTML);
    }

}

function addRow(tableID)
	 {

			var table = document.getElementById(tableID);

			var rowCount = table.rows.length;
			var row = table.insertRow(rowCount);

			var last_row = document.getElementById(tableID).rows[rowCount-1];

			var colCount = table.rows[1].cells.length;

			for(var i=0; i<colCount; i++) {

				var newcell	= row.insertCell(i);

				newcell.innerHTML = table.rows[1].cells[i].innerHTML;
				//alert(newcell.childNodes);
				switch(newcell.childNodes[0].type) {
					case "text":
							newcell.childNodes[0].value = "";
							break;
					case "checkbox":
							newcell.childNodes[0].checked = false;
							break;
					case "select-one":
							newcell.childNodes[0].selectedIndex = 0;
							break;
				}
			}
    }

function validate(){
    var total_processed_wt, total_order_wt, completed_proc_wt, order_completed_chk;
    total_processed_wt = Number(document.getElementById("total_processed_wt").value);
    //total_order_wt = Number(document.getElementById("order_wt").value);
    completed_proc_wt = Number(document.getElementById("tot_proc_wt").value);
    rm_wt = Number(document.getElementById("weight").value);
    order_completed_chk = true;

    //if (total_order_wt*0.98 > (total_processed_wt + completed_proc_wt)){
    //    order_completed_chk = confirm("Order weight is greater than Processing Weight. Should the order be marked complete? /nPress OK to mark order complete");
    //    }
    //if(order_completed_chk == false){
    //    document.getElementById("balance_wt").value = 0;
    //}
    if((total_processed_wt + completed_proc_wt) > 1.05*rm_wt){
        alert('Processed wt is greater than Input material weight. Please check');
        document.getElementById('submit').disabled = true;
    }
    else{
        document.getElementById('submit').disabled = false;
    }


 }

function print_label(){
   var rowId = parseInt(event.target.parentNode.parentNode.id);
              //this gives id of tr whose button was clicked
    var data = "";
    var fg_table = document.getElementById('fg_table');
    for(i=0;i<fg_table.rows[rowId].cells.length-1;i++){
        data = data + fg_table.rows[rowId].cells[i].lastChild.data + '&';
    }
    var new_page = window.open('print_label?' + data);
    //new_page.document.write("output");
}

function make_label_slit(){
    var width_table = document.getElementById('numbers_pkts1');
    var parts_table = document.getElementById('part_tbl');
    var newHTML = '';
    var newNEWHTML = '';
    var id =1;
    var part_length,part_name, width, width_name, width_part_name, size;
    var html = '<tr id= %id%><td>%smpl_no%</td><td>%customer%</td><td>%machine%</td><td>%size%</td><td>%coil_length%</td><td>%coil_name%</td><td>%mill_id%</td><td>%grade%</td><td><input type = "button" class="btn btn-default" value="Print" onclick="print_label()"></td></tr>'
    var thickness = document.getElementById("thickness").value;
    var mill_id = document.getElementById("mill_id").value;
    var grade_field = document.getElementById("grade").value;
    var smpl_no = document.getElementById("smpl_no").value;
    var customer = document.getElementById("customer").value;
    grade = grade_field.split("GRADE").pop();
    grade = grade.slice(1);
    for(i=1;i<parts_table.rows.length;i++){
        part_length = parts_table.rows[i].cells[0].lastChild.value;
        part_name = parts_table.rows[i].cells[1].lastChild.value;
        newHTML = html.replace('%coil_length%', part_length);
        newHTML = newHTML.replace('%grade%', grade);
        newHTML = newHTML.replace('%smpl_no%', smpl_no);
        newHTML = newHTML.replace('%customer%', customer);
        newHTML = newHTML.replace('%machine%', "Slitting");
        newHTML = newHTML.replace('%mill_id%', mill_id);

        for(j=1;j<width_table.rows.length;j++){
            width = width_table.rows[j].cells[0].lastChild.value;
            width_name = width_table.rows[j].cells[1].lastChild.value;
            size = thickness + " x " + width + " x Coil";
            width_part_name = width_name + part_name;
            newNEWHTML = newHTML.replace('%coil_name%', width_part_name);
            newNEWHTML = newNEWHTML.replace('%size%', size);
            newNEWHTML = newNEWHTML.replace('%coil_name%', width_part_name);
            newNEWHTML = newNEWHTML.replace('%id%', id);
            document.getElementById('fg_table').insertAdjacentHTML('beforeend', newNEWHTML);
            id = id +1;
        }

    }

}

function setting_done_change(){
    var setting_done_yes = document.getElementById("setting_done_yes").checked;
    var setting_done_no = document.getElementById("setting_done_no").checked;

    console.log(setting_done_yes);
    console.log(setting_done_no);

    if(setting_done_yes == true){
        document.getElementById("setting_date").value = "";
        document.getElementById("setting_date").readOnly = false;
        document.getElementById("setting_start_time").value = "";
        document.getElementById("setting_start_time").readOnly = false;
        document.getElementById("setting_end_time").value = "";
        document.getElementById("setting_end_time").readOnly = false;
        document.getElementById("setting_time").value = "";

    }
    if(setting_done_no == true){
        document.getElementById("setting_date").value = "2001-01-01";
        document.getElementById("setting_date").readOnly = true;
        document.getElementById("setting_start_time").value = "00:00";
        document.getElementById("setting_start_time").readOnly = true;
        document.getElementById("setting_end_time").value = "00:01";
        document.getElementById("setting_end_time").readOnly = true;
        document.getElementById("setting_time").value = "1";

    }

}

function check_slitter_numbers(tableID){
    var table = document.getElementById(tableID);
    var i, slitter_lst, slitter_lst_array, row, flag;
    var rowCount = table.rows.length;
    flag = 0;

    for (i=1; i< rowCount; i++){
        row = table.rows[i];
        slitter_lst = row.cells[1].lastElementChild.value;
        slitter_lst_array = slitter_lst.split(' ');
        for(j=0;j<slitter_lst_array.length;j++){
            if(Number(slitter_lst_array[j]) > 50){
                alert('Please check slitter numbers');
                //document.getElementById('slitter_number').focus();
                flag = 1;
            }
        }
    }
    if(flag == 1){ return false;}
    else {return true;}
}

function validateForm(){
// 1. If slitting check if all slitter numbers < 50
// 2. Processed weight cannot be empty


// First step check for all the nulls and empty fields

    var total_processed_wt = document.getElementById('total_processed_wt').value;
    if (total_processed_wt == ""){
        alert('Processed weight is empty. Please check!');
        return false;
    }
    var check_slitters = check_slitter_numbers('slitting_cutters');
    if(check_slitters == false){
        return false;
    }

}

