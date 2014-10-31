<?php

require_once("pdf/dompdf/dompdf_config.inc.php");

// We check wether the user is accessing the demo locally
$local = array("::1", "127.0.0.1");
$is_local = true;

if ( isset( $_POST["html"] ) && $is_local ) {

  if ( get_magic_quotes_gpc() )
    $_POST["html"] = utf8_decode(stripslashes($_POST["html"]));
//    $_POST["html"] = str_replace(array('7','&euro;'),array('&0128;','&0128;'), $_POST["html"]);

  
  $dompdf = new DOMPDF();
  $dompdf->load_html("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\" \"http://www.w3.org/TR/html4/loose.dtd\">
<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"en\" lang=\"en\">
<head>

<style>


@page {
	margin:0;padding:0;	
	}
	
body, div, h1, h2, h3, p {
	margin:0;padding:0;
	}

body {
	margin:50px 57px !important;
	font-family: Helvetica;
	}

.left {text-align:left;}
.right {text-align:right;}

#title {
	font-size: 33px;
	}

#company {
	font-size: 23px;
	padding-top:14px;
	line-height:42px;
	padding-top:9px;	
	}

p {
	line-height:20px;
	font-size:14px;
	}

#client {
	font-size: 17px;
	font-weight:bold;
	
	}	
	
#line2 p {
	margin-top:-14px;
	}

#header {
	padding-bottom:23px;
	border-bottom: 1px solid #ccc;
	width: 100%;	
	}

#text1 {
	width:100%;
	margin:30px 66px 0 66px;	
	}

#text2 {
	width:100%;
	margin:0 66px;	
	}

table {
	width: 100%;
	}

#data {
	border:1px solid #ccc;
	border-right:0;
	border-bottom:0;
	margin:30px 0;
	}
	
table {border-collapse:separate;border-spacing:0;}
	

#data td, th {
	border-right:1px solid #bbb;
	height:18px;
	text-align: left;
	font-size: 12px;
	text-indent: 10px;
	}

th {
	background: #ececec;
	border-bottom:1px solid #ccc;
	}

#total th {
	background: #ddd;
	}

.tint td {background-color: #f5f5f5;}

div p {
	font-size:13px;
	line-height:19px;
	}

</style>  

</head>

<body> " . $_POST["html"] . "</body></html>");
  $dompdf->set_paper("a4", "portrait");
  $dompdf->render();

  $dompdf->stream("invoiceto.me.pdf", array("Attachment" => true));

  exit(0);
}

?>


<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8" />
	<title>invoiceto.me &middot; Make a free invoice PDF online</title>
	<meta name="description" content="Quickly edit and publish a PDF invoice" >	
	<link rel="shortcut icon" href="icon.png" type="image/x-icon" />
	<link rel="apple-touch-icon" href="/apple-touch-icon.png"/>	
	<link rel="stylesheet" href="design/blueprint/screen.css" type="text/css" media="screen, projection">
	<link rel="stylesheet" href="design/main.css" type="text/css" />
	<script src="jq.js" type="text/javascript" charset="utf-8"></script>
	<script src="page.js" type="text/javascript" charset="utf-8"></script>
	<script src="autogrow.js" type="text/javascript" charset="utf-8"></script>
	<script src="textsaver.js" type="text/javascript" charset="utf-8"></script>
	<!--[if IE]><style type="text/css">body {zoom: 0.75;margin-top:150px !important;margin-right:-300px;} #company {width:415px !important;}</style><![endif]-->
<script type="text/javascript">  var _gaq = _gaq || [];  _gaq.push(['_setAccount', 'UA-23071661-1']);  _gaq.push(['_trackPageview']);  (function() {    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);  })();</script>
</head>
 
<body>

<form action="/index.php" method="post"> 
 
<p id="ad" class="tools" onClick="_gaq.push(['_trackEvent', 'Ad', 'Intercom']);"><span>Ad
</span> <a href="http://intercom.io/">Intercom – communicate personally with every single customer</a></p>

 
<div class="tools" id="one">
	<h5>invoiceto.me</h5>
	<p>Edit the fields to make an invoice &rarr;</p>
</div>
<div class="tools" id="two">
	<h5>Finished editing?</h5>
	<ul>
		<li><a class="button" href="#">Get PDF</a></li>
	</ul>
</div>
<div class="tools" id="three">
	<h5>Resize table</h5>
	<ul>	
		<li><a id="addRow" href="#" title="test"><span style="padding-right:5px;">+</span> Add row</a></li>
		<li><a id="delRow" href="#"><span style="padding-right:5px;padding-left:1px;">&ndash;</span> Delete row</a></li>
	</ul>
</div>
 
	<input id="rowCounter" type="hidden" value="8" />
 
<div id="invoice" class="container">
 
	<div id="header">
		<input id="company" class="span-12 ll" value="Your Company Name" />
		<input id="title" class="span-12 last rr" value="INVOICE" />
		<div id="address" class="span-12">
			<input class="ll" value="123 Your Street" />
			<input class="ll" value="Your Town" />
			<input class="ll" value="Address Line 3" />	
			<input style="margin-top:20px;" class="ll" value="(123) 456 789" />
			<input style="margin-bottom:30px;" class="ll" value="email@yourcompany.com" />
		</div>
		<div id="meta" class="span-12 last">
			<input id="date" class="rr" value="12/11/2010" />
			<input class="rr" value="Invoice #2334889" />
			<input class="rr" value="PO 456001200" />
			<input style="margin-top:20px;" class="client rr" value="Att: Ms. Jane Doe" />
			<input style="margin-bottom:30px;" class="client rr" value="Client Company Name" />
		</div>
	</div>
	
	<hr>
	
	
<textarea class="notes" id="textone" cols="95" rows="1">Dear Ms. Jane Doe,
		
Please find below a cost-breakdown for the recent work completed. Please make payment at your earliest convenience, and do not hesitate to contact me with any questions.
		
Many thanks,
Your Name</textarea>
	
	
	<table class="span-24 last">
	<thead>
	<tr>
		<th class="span-2" ><input value="#" /></th>
    	<th class="span-10"><input value="Item Description" /></th>
    	<th class="span-4"><input value="Quantity" /></th>
    	<th class="span-4"><input value="Unit price (€)" /></th>
    	<th class="span-4"><input value="Total (€)" /></th>
	</tr>
	</thead>
	<tbody>
	<tr>
		<td class="noteditable" title="This field is done automatically">1</td>	
    	<td><input value="Supporting of in-house project (hours worked)" /></td>
    	<td><input value="40" /></td>
    	<td><input value="125" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">2</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">3</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">4</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">5</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">6</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">7</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">8</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">9</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">10</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>	
	<tr>
		<td class="noteditable" title="This field is done automatically">11</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">12</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">13</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">14</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">15</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">16</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>	
	<tr>
		<td class="noteditable" title="This field is done automatically">17</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">18</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">19</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">20</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">21</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">22</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">23</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">24</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>
	<tr>
		<td class="noteditable" title="This field is done automatically">25</td>	
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td><input value="" /></td>
    	<td class="noteditable" title="This field is done automatically"></td>            
	</tr>			
	</tbody>	
	<tfoot>
	<tr>
		<th id="subtotallabel" colspan="4" class="span-20"><input value="Subtotal" /></th>
    	<th id="formsubtotal" class="span-4 noteditable">0</th>
	</tr>
	<tr>
		<th id="taxrate" colspan="4" class="span-20"><input value="Sales Tax (20%)" /></th>
    	<th id="formtax" class="span-4 noteditable">0</th>
	</tr>
	<tr id="total">
		<th id="totallabel" colspan="4" class="span-20"><input value="Total" /></th>
    	<th id="formtotal" class="span-4 noteditable">0</th>
	</tr>	
	</tfoot>												
	</table>
	
<textarea class="notes" id="texttwo" cols="95">Many thanks for your custom! I look forward to doing business with you again in due course.
 
Payment terms: to be received within 60 days.</textarea>
		
 
</div>
 
<textarea name="html" id="markup" cols="60" rows="20" style="display:none;">
</textarea>
 
</form>
</body>
</html>