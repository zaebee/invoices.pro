<?php

require_once("pdf/dompdf/dompdf_config.inc.php");
$hellosign_presign_dir = dirname(__DIR__) . '/invoicetome/hellosign_presign/';


// We check wether the user is accessing the demo locally
$local = array("::1", "127.0.0.1");
$is_local = true;

if ( isset( $_POST["html"] ) && $is_local ) {

  if ( get_magic_quotes_gpc() )
    //$_POST["html"] = utf8_decode(stripslashes($_POST["html"]));
    $_POST["html"] = utf8_encode(stripslashes($_POST["html"]));
//    $_POST["html"] = str_replace(array('7','&euro;'),array('&0128;','&0128;'), $_POST["html"]);
  
  $dompdf = new DOMPDF();
  $dompdf->load_html("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\" \"http://www.w3.org/TR/html4/loose.dtd\">
<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"en\" lang=\"en\">
<head>
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">
<style>


@page {
	margin:0;padding:0;	
	}
	
body, div, h1, h2, h3, p {
	margin:0;padding:0;
	}

body {
	margin:50px 57px !important;
	font-family: times;
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

  if ( isset( $_POST["file"] ) ) {
    $date = new DateTime();
    $stamp = $date->getTimestamp();
    $filename = $stamp . '_invioceto.me.pdf';
    $output = $dompdf->output();
    file_put_contents($hellosign_presign_dir . $filename, $output);
    $result = array('created' => true, 'filename' => $filename);
    echo json_encode($result);
    exit(0);
  } else {
    $dompdf->stream("invoices.pro.pdf", array("Attachment" => true));
  }

  $result = array('created' => true);
  echo json_encode($result);
  exit(0);
}

?>
