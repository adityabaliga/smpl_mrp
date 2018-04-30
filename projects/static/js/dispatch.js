function full_dispatch(th, tableID)
{
    var table = document.getElementById(tableID);

    var rowCount = th.parentNode.parentNode.rowIndex;

	var last_row = document.getElementById(tableID).rows[rowCount];

    var full_disp = last_row.cells[7].lastElementChild.checked;

    if (full_disp == true)
    {
        last_row.cells[8].lastElementChild.value = last_row.cells[3].lastElementChild.value;
        last_row.cells[9].lastElementChild.value = last_row.cells[4].lastElementChild.value;
    }
    else
    {
        last_row.cells[8].lastElementChild.value = '';
        last_row.cells[9].lastElementChild.value = '';
    }
}

function enable_dispatch(th, tableID)
{
    var table = document.getElementById(tableID);

    var rowCount = th.parentNode.parentNode.rowIndex;

	var last_row = document.getElementById(tableID).rows[rowCount];

	var dispatch_on = last_row.cells[0].lastElementChild.checked;

	if(dispatch_on == true)
	{
        last_row.cells[7].lastChild.disabled = false;
        last_row.cells[8].lastChild.readOnly = false;
        last_row.cells[9].lastChild.readOnly = false;
        last_row.cells[10].lastChild.readOnly = false;
        last_row.cells[11].lastChild.readOnly = false;

        last_row.cells[8].lastChild.required = true;
        last_row.cells[9].lastChild.required = true;
        last_row.cells[10].lastChild.required = true;
        last_row.cells[11].lastChild.value = ' ';
	}
	else
	{
	    last_row.cells[7].lastChild.disabled = true;
	    last_row.cells[8].lastChild.readOnly = true;
        last_row.cells[9].lastChild.readOnly = true;
        last_row.cells[10].lastChild.readOnly = true;
        last_row.cells[11].lastChild.readOnly = true;

	}
}

function check_numbers(th, tableID)
{
    var table = document.getElementById(tableID);

    var rowCount = th.parentNode.parentNode.rowIndex;

	var last_row = document.getElementById(tableID).rows[rowCount];

    numbers = last_row.cells[3].lastElementChild.value;
    dispatch_nos = last_row.cells[8].lastElementChild.value;

    if(dispatch_nos > numbers)
    {
        alert('Dispatch numbers cannot be more than available numbers!');
        last_row.cells[3].lastElementChild.value = '';
    }
    else
    {
        qty = last_row.cells[4].lastElementChild.value;
        dispatch_qty = qty/numbers * dispatch_nos;
        last_row.cells[9].lastElementChild.value = dispatch_qty.toFixed(3);
    }
 }
