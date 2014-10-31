$(document).ready(function(){

//Highlight first input

$("#company").focus();

// Current date in readable format
var m_names = new Array("January", "February", "March", 
"April", "May", "June", "July", "August", "September", 
"October", "November", "December");
var d = new Date();
var curr_date = d.getDate();
var curr_month = d.getMonth();
var curr_year = d.getFullYear();
var date = (curr_date + "-" + m_names[curr_month] 
+ "-" + curr_year);
$("#date").attr("value", date);


// Activate growing textareas
$("textarea.notes").growfield();

// Activate localStorage
$("form").textSaver();

// Function to insert <br>s for newlines
function nl2br (str, is_xhtml) {   
var breakTag = (is_xhtml || typeof is_xhtml === 'undefined') ? '<br />' : '<br>';    
return (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1'+ breakTag +'$2');
}

// Function to recalculate invoice cell values 
var refreshCells  = function() {  
	$("table").find("tr").each(function() {
		if (isNaN($(this).find("td:nth-child(3) input").attr("value"))) {
			$(this).find("td:nth-child(5)").html(($(this).find("td:nth-child(4) input").attr("value")));			
		}
		else {
			$(this).find("td:nth-child(5)").html(($(this).find("td:nth-child(3) input").attr("value")) * ($(this).find("td:nth-child(4) input").attr("value")));			
		}
	});	
	
	var total = 0;
	$("table").find("td:nth-child(5)").each(function() {
		total = total + parseFloat($(this).text());
		$(this).text(parseFloat($(this).text()).toFixed(2));
		if (isNaN($(this).text())) {
				$(this).text("-");
			}
			else if (parseInt($(this).text()) == 0) {
			$(this).text("-");
		}
	});	

	$("table").find("td:nth-child(4) input").each(function() {
		$(this).attr("value", (parseFloat($(this).attr("value")).toFixed(2)));
		if (isNaN($(this).attr("value"))) {
				$(this).attr("value", "");
			}
			else if (parseInt($(this).attr("value")) == 0) {
				$(this).attr("value", "");
			}
		});	

		$("#formsubtotal").html(total.toFixed(2));

		var taxrate = $("#taxrate input").attr("value").replace(/\,/g, '').replace(/,/g,'.').replace(/[^\d\.]/g,'') / 100;
		$("#formtax").html(($("#formsubtotal").text() * taxrate).toFixed(2));
		$("#formtotal").html((parseFloat(($("#formsubtotal").text())) + parseFloat($("#formtax").text())).toFixed(2));
}

// Function to insert new invoice cell row 
var insertRow = function() {

$("table").find('tbody')
    .append($('<tr>')
	.append($('<td>').attr('class', 'noteditable').text(parseInt($("tr:last-child td:first-child").text()) + 1).attr('title','This field is done automatically'))
    .append($('<td>').append($('<input>').attr('value', '')))
    .append($('<td>').append($('<input>').attr('value', '')))
    .append($('<td>').append($('<input>').attr('value', '')))
	.append($('<td>').attr('class', 'noteditable').attr('title','This field is done automatically'))
    );	    
}

// (Evil) function to prepare markup for PDF export
var makeMarkup  = function() {

$("#markup").val("");
$("#markup").val($("#markup").val()+"<table id=\"header\"><tr><td><h1 id=\"company\" class=\"left\">"+$("#company").attr("value")+"</h1></td><td><h1 id=\"title\" class=\"right\">"+$("#title").attr("value")+"</tr><tr id=\"line1\"><td><p class=\"left\">"+$("#address input:nth-child(1)").attr("value")+"<br>"+$("#address input:nth-child(2)").attr("value")+"<br>"+$("#address input:nth-child(3)").attr("value")+"</p><p style=\"margin-top:15px;\" class=\"left\">"+$("#address input:nth-child(4)").attr("value")+"<br>"+$("#address input:nth-child(5)").attr("value")+"</p></td><td><p class=\"right\">"+$("#meta input:nth-child(1)").attr("value")+"<br>"+$("#meta input:nth-child(2)").attr("value")+"<br>"+$("#meta input:nth-child(3)").attr("value")+"</p></p><p id=\"client\" class=\"right\" style=\"margin-top:12px;\"><b>"+$("#meta input:nth-child(4)").attr("value")+"<br>"+$("#meta input:nth-child(5)").attr("value")+"</b></p></td></tr></table></div><div id=\"text1\"><p>"+nl2br($("#textone:not(.growfieldDummy)").val())+"</p></div><table id=\"data\"><tr><th style=\"width:50px\">"+$("thead th:nth-child(1) input").attr("value")+"</th><th style=\"width:313px;\">"+$("thead th:nth-child(2) input").attr("value")+"</th><th style=\"width:100px;\">"+$("thead th:nth-child(3) input").attr("value")+"</th><th style=\"width:100px;\">"+$("thead th:nth-child(4) input").attr("value")+"</th><th style=\"width:100px;\">"+$("thead th:nth-child(5) input").attr("value")+"</th></tr>"); 
var i = 0;$("#invoice table").find("tr").each(function() {s="";if (i % 2 === 0 ){var s="tint"};if (i>parseInt($("#rowCounter").attr("value"))){return}else if (i>0){$("#markup").val($("#markup").val()+"<tr class=\"" + s + "\"><td>"+$(this).find("td:nth-child(1)").text()+"</td><td>"+$(this).find("td:nth-child(2) input").attr("value")+"</td><td>"+$(this).find("td:nth-child(3) input").attr("value")+"</td><td>"+$(this).find("td:nth-child(4) input").attr("value")+"</td><td>"+$(this).find("td:nth-child(5)").text()+"</td></tr>");};i = i + 1;});	
$("#markup").val($("#markup").val()+"<tr><th style=\"border-top: 1px solid #bbb;\" colspan=\"4\">"+$("#subtotallabel input").attr("value")+"</th><th style=\"border-top: 1px solid #bbb;\" id=\"formsubtotal\">"+$("#formsubtotal").text()+"</th></tr><tr><th id=\"taxrate\" colspan=\"4\">"+$("#taxrate input").attr("value")+"</th><th id=\"formtax\">"+$("#formtax").text()+"</th></tr><tr id=\"total\"><th colspan=\"4\">"+$("#totallabel input").attr("value")+"</th><th id=\"formtotal\">"+$("#formtotal").text()+"</th></tr></table><div id=\"text2\"><p>"+nl2br($("#texttwo:not(.growfieldDummy)").val())+"</p></div>");


$("#markup").val($("#markup").val().replace(/€/g, "&euro;"));


}

// Parse existing 
refreshCells()
makeMarkup()

//Update after edits
$("input").focusout(function(){
	refreshCells()
	makeMarkup()		
});	
$("textarea").focusout(function(){
	refreshCells()
	makeMarkup()		
});		


// Add new Row
$("#addRow").click(function() {
	if (isNaN(parseInt($("tr:last-child td:first-child").text())))
	{
		$("tr:last-child td:first-child").text("0");
	}
	else if (parseInt($("tr:last-child td:first-child").text())>24){
		return false;
	}
	insertRow();
	$("#rowCounter").attr("value", $("tr:last-child td:first-child").text());
	$("#rowCounter").trigger('keyup');		
	refreshCells()
	makeMarkup()
    return false;	
})
	

// Display correct number of Rows	
	while (parseInt($("tr:last-child td:first-child").text())<parseInt($("#rowCounter").attr("value"))) {
		insertRow();
	    refreshCells();
		makeMarkup()	    
	}
	while (parseInt($("tr:last-child td:first-child").text())>parseInt($("#rowCounter").attr("value"))) {
		$("tbody tr:last").remove();
	}


// Delete last row
	$("#delRow").click(function() {
		$("tbody tr:last").remove();
		$("#rowCounter").attr("value", $("tr:last-child td:first-child").text());
		$("#rowCounter").trigger('keyup');				
		makeMarkup()
		return false;
	})


// Generate PDF
$(".button").click(function() {
	$("form").submit();
})


})

	