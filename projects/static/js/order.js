function setFocusToTextBox(){
    document.getElementById("processing_wt").focus();
}




//http://jsfiddle.net/7AeDQ/ - source of code
//http://viralpatel.net/blogs/dynamically-add-remove-rows-in-html-table-using-javascript/
// This function is to add a row. mm_list is an array of input material possible based on the order.
// It is populated if a row is entered as WIP, in the format of 'width x length"
// http://jsfiddle.net/jackwanders/kGgkE/ source for dynamically populating input material drop down
	var mm_list = [];


	function addRow(tableID)
	 {

			var table = document.getElementById(tableID);

			var rowCount = table.rows.length;
			var row = table.insertRow(rowCount);

			var last_row = document.getElementById(tableID).rows[rowCount-1];
			/*last_row.cells[5].lastChild.value;

			var cut_length = document.getElementById("cut_length").value;
			var cut_width = document.getElementById("cut_width").value;
			var size_no = document.getElementById("stage_no").value;*/
			var new_input_material = ""

			if(last_row.cells[10].lastElementChild.value == "WIP"){
			    new_input_material = last_row.cells[4].lastChild.value + " x " + last_row.cells[5].lastChild.value;
			    mm_list.push(new_input_material);
    		    var sel = document.getElementById('input_material');
                i = mm_list.length-1;
                var opt = document.createElement('option');
                opt.innerHTML = mm_list[i];
                opt.value = mm_list[i];
                sel.appendChild(opt);
            }




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

    function addRowModifyOrder(tableID)
	 {

			var table = document.getElementById(tableID);

			var rowCount = table.rows.length;
			var row = table.insertRow(rowCount);
			var colCount = table.rows[2].cells.length;

			for(var i=0; i<colCount; i++) {

				var newcell	= row.insertCell(i);

				newcell.innerHTML = table.rows[2].cells[i].innerHTML;
				//alert(newcell.childNodes);
				switch(newcell.lastElementChild.type) {
					case "text":
							newcell.lastElementChild.value = "";
							break;
					case "checkbox":
							newcell.childNodes[0].checked = false;
							break;
					case "select-one":
							newcell.childNodes[0].selectedIndex = 0;
							break;
                    case "number":
                            newcell.childNodes[0].value = 0;
							break;

				}
			}
		}

    function deleteRow(tableID)
    {
			try {
			var table = document.getElementById(tableID);
			var rowCount = table.rows.length;


			for(var i=1; i<rowCount; i++) {
				var row = table.rows[i];
				var chkbox = row.cells[0].childNodes[0];
				if(null != chkbox && true == chkbox.checked) {
					if(rowCount <= 1) {
						alert("Cannot delete all the rows.");
						break;
					}
					table.deleteRow(i);
					rowCount--;
					i--;
				}
			}
			}catch(e) {
				alert(e);
			}
	}

    // Function to delete row. No change taken straight from source
    function deleteRowModifyOrder(tableID)
    {
			try {
			var table = document.getElementById(tableID);
			var rowCount = table.rows.length;


			for(var i=1; i<rowCount; i++) {
				var row = table.rows[i];
				var chkbox = row.cells[0].childNodes[0];
				//var chkbox = row.childNodes[0];
				if(null != chkbox && true == chkbox.checked) {
					if(rowCount <= 1) {
						alert("Cannot delete all the rows.");
						break;
					}
					table.deleteRow(i);
					rowCount--;
					i--;
				}
			}
			}catch(e) {
				alert(e);
			}
	}

// After input material is selected from drop down. The cut length and cut width set based on CTL or slitting operations selected.
    function  after_input_material(th, tableID){
        var table = document.getElementById(tableID);

		var rowCount = th.parentNode.parentNode.rowIndex;
		var last_row = document.getElementById(tableID).rows[rowCount];
        var answer = last_row.cells[1].lastElementChild.value;

        var input_material = (last_row.cells[3].lastElementChild.value).split(" x ");
        ms_width = input_material[0];
        ms_length = input_material[1];

         if(answer == "Slitting" || answer == "Mini Slitting")
            {
                if(ms_length != 0){
                //alert("The input material is not a coil. Please re-enter input material");
                //alert("The input material is not a coil. Please re-enter input material");
                }
                last_row.cells[5].lastChild.value = 0;
            }
         if(answer == "CTL" || answer == "CTL - 1 side lamination" || answer == "CTL - 2 side lamination" || answer == "Narrow CTL")
            {
                    if(ms_length != 0){
                        //alert("The input material is not a coil. Please re-enter input material");
                    }
                    last_row.cells[4].lastChild.value = ms_width;

            }


    }


    //The place holders of some fields are changed based on the operation selected
    function on_select_operation(th, tableID)
    {
            var table = document.getElementById(tableID);

			var rowCount = th.parentNode.parentNode.rowIndex;

			var last_row = document.getElementById(tableID).rows[rowCount];

            var answer = last_row.cells[1].lastElementChild.value;

            var input_material = (last_row.cells[3].lastElementChild.value).split(" x ");
            ms_width = input_material[0];
            ms_length = input_material[1];

            if(answer == "Slitting" || answer == "Mini Slitting")
            {
                last_row.cells[7].lastChild.placeholder="No. of slits";
                last_row.cells[11].lastChild.placeholder="No. of parts";
                last_row.cells[12].lastChild.placeholder="Length/Part";
                last_row.cells[5].lastChild.value = "0";
                last_row.cells[5].lastChild.readOnly = true;
                if(ms_length != 0){
                alert("The input material is not a coil. Please re-enter input material");
                }
                //last_row.cells[6].lastChild.readOnly = true;
            }
            else
            {
                if(answer == "CTL" || answer == "CTL - 1 side lamination" || answer == "CTL - 2 side lamination" || answer == "Narrow CTL")
                {
                    if(ms_length != 0){
                        alert("The input material is not a coil. Please re-enter input material");
                    }
                    last_row.cells[4].lastChild.value = ms_width;
                    last_row.cells[5].lastChild.readOnly = false;

                }
                last_row.cells[11].lastChild.placeholder="No.s/packet";
                last_row.cells[12].lastChild.placeholder="No. of packets";
            }
	}


    // Fields like packing type, no of packets and no.s / packet disabled or enabled based on FG or WIP selected
    function fg_or_no_fg(th,tableID)
    {
		    var table = document.getElementById(tableID);

			var rowCount = th.parentNode.parentNode.rowIndex;

			var last_row = document.getElementById(tableID).rows[rowCount];

            var answer = last_row.cells[10].lastElementChild.value;
            var operation = last_row.cells[1].lastElementChild.value;
            fg_wt = Number(document.getElementById("total_fg").value);
            var process_weight = Number(document.getElementById("processing_wt").value);
            var total_fg = 0;


		    if(answer == "FG" )
		    {

                last_row.cells[11].lastChild.readOnly = false;
                last_row.cells[12].lastChild.readOnly = false;
                last_row.cells[13].lastChild.readOnly = false;
                output_wt = Number(last_row.cells[6].lastElementChild.value);
                total_fg = (fg_wt + output_wt).toFixed(3)
                document.getElementById("total_fg").value = total_fg;
            }
            else
            {
                if(operation != "Slitting" && operation != "Mini Slitting"){
                    last_row.cells[11].lastChild.readOnly = true;
                    last_row.cells[11].lastChild.value = "0"
                    last_row.cells[12].lastChild.readOnly = true;
                    last_row.cells[12].lastChild.value = "0"
                    last_row.cells[13].lastChild.readOnly = true;
                }
                if(operation == "Slitting" || operation == "Mini Slitting"){
                    last_row.cells[11].lastChild.readOnly = false;
                    last_row.cells[12].lastChild.readOnly = false;
                }
		        last_row.cells[13].lastChild.placeholder = "Packing"
		        last_row.cells[13].lastChild.value = " "

            }
    }


    // numbers or length calculated after weight entered
    function calculate_numbers(th, tableID){
           var table = document.getElementById(tableID);

			var rowCount = th.parentNode.parentNode.rowIndex;

			var last_row = document.getElementById(tableID).rows[rowCount];

            var weight = Number(last_row.cells[6].lastChild.value);
            var cut_length = Number(last_row.cells[5].lastChild.value);
            var cut_width = Number(last_row.cells[4].lastChild.value);
            var thickness = Number(document.getElementById("thickness").value);

            var answer = last_row.cells[1].lastElementChild.value;
            var numbers = 0;

            if (answer == "Slitting" || answer == "Mini Slitting"){
                //numbers =  (weight*1000/(cut_width * thickness)/0.00000785)/1000;
            }
            else{
                if (answer == "Reshearing")
                {
                   var input_material = (last_row.cells[3].lastElementChild.value).split(" x ");
                    ms_width = input_material[0];
                    ms_length = input_material[1];
                    if (ms_width==0 || ms_length==0)
                     {
                        alert("Please check input material for reshearing")
                        return false;
                     }
                }
                numbers = weight*1000/(cut_length * cut_width * thickness)/0.00000785;
            }

            last_row.cells[7].lastChild.value = numbers.toFixed(0);
            return true;

    }






    // No of packets calculated based on no.s per packet and total numbers selected
    function calculate_no_of_packets(th, tableID){
            var table = document.getElementById(tableID);

		    var rowCount = th.parentNode.parentNode.rowIndex;
		    var last_row = document.getElementById(tableID).rows[rowCount];
            var answer = last_row.cells[1].lastElementChild.value;

            var weight = Number(last_row.cells[6].lastChild.value);
            var cut_length = Number(last_row.cells[5].lastChild.value);
            var cut_width = Number(last_row.cells[4].lastChild.value);
            var thickness = Number(document.getElementById("thickness").value);
            var input_material = (last_row.cells[3].lastElementChild.value).split(" x ");
            ms_width = Number(input_material[0]);
            ms_length = input_material[1];

            var coil_length = 0;
            var length_per_part = 0
            var no_of_parts = Number(last_row.cells[11].lastChild.value);



            if (answer == "Slitting" || answer == "Mini Slitting"){
                var no_of_slits = Number(last_row.cells[7].lastChild.value);
                var weight_per_coil = weight/no_of_slits;
                coil_length = (weight_per_coil * 1000)/(thickness * cut_width * 0.00000785)/1000;
                length_per_part = coil_length/no_of_parts;
                last_row.cells[12].lastChild.value = length_per_part.toFixed(2);
            }

            else{
                if (last_row.cells[10].lastElementChild.value == "FG"){
                var numbers = Number(last_row.cells[7].lastChild.value);
                var no_per_packet = Number(last_row.cells[11].lastChild.value);
                var no_of_packets = numbers / no_per_packet;
                last_row.cells[12].lastChild.value = no_of_packets.toFixed(0);
                }
            }
    }

    function check_stage_weight(tableID)
    {
        var table = document.getElementById(tableID);
		var rowCount = table.rows.length;
		var current_row = document.getElementById(tableID).rows[0];
		var stage_weight = [0];
		var stage_number = 0;
		var mother_weight = Number(document.getElementById("processing_wt").value);
		var fg_wt = 0;


		for(i=1;i<rowCount;i++)
		{
		   current_row = document.getElementById(tableID).rows[i];
		   stage_number = parseInt(current_row.cells[2].lastChild.value);
		   if(stage_weight[stage_number])
		    stage_weight[stage_number] += Number(current_row.cells[6].lastChild.value);
           else
            stage_weight[stage_number] = Number(current_row.cells[6].lastChild.value);
           if(current_row.cells[10].lastElementChild.value == "FG")
            fg_wt += Number(current_row.cells[6].lastChild.value);
      	}
        document.getElementById("total_fg").value = fg_wt;

      	for(i=1;i<=stage_weight.length;i++)
      	{
      	    if(stage_weight[i]>mother_weight)
      	    {
      	        alert("The processing weight of stage "+ i + " is greater than processing weight. Please re-check");
      	        return false;
      	    }
      	}

    }

    function validate_form(tableID){
         var fg_return_value = true;
         var stage_wt_return_value =  check_stage_weight(tableID);

         var fg_wt = Number(document.getElementById("total_fg").value);
         var process_weight = Number(document.getElementById("processing_wt").value);
         // This is to check that FG cannot be greater than processing weight entered
         if (fg_wt > process_weight)
         {
              alert("Total FG greater than processing weight. Please check");
              fg_return_value =  false;
         }

         // This is to check that FG and processing weight * 95% match
         if (fg_wt < (0.95*process_weight))
         {
                alert("Total FG is less than processing weight. Please check");
                fg_return_value = false;
         }

         var order_date = new Date(document.getElementById("order_date").value);
         var expected_date = new Date(document.getElementById("expected_date").value);
         var date_check = true;

         if (order_date>expected_date)
         {
            date_check = false;
            alert("Order date cannot be greater than expected date!");
         }

         if (fg_return_value == false || stage_wt_return_value == false || date_check == false)
            return false;
         else
            return true;
    }



    function select_operation(operation){
        switch(operation){
        case "ctl":
            document.getElementById('operation').selectedIndex = "0";
            break;
        case "ctl_single_lami":
            document.getElementById('operation').selectedIndex = "1";
            break;
        case "ctl_double_lami":
            document.getElementById('operation').selectedIndex = "2";
            break;
        case "slitting":
            document.getElementById('operation').selectedIndex = "3";
            break;
        case "mini_slitting":
            document.getElementById('operation').selectedIndex = "4";
            break;
        case "nctl":
            document.getElementById('operation').selectedIndex = "5";
            break;
        case "reshearing":
            document.getElementById('operation').selectedIndex = "6";
        }
    }