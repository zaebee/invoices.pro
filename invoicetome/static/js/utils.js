$(document).ready(function(){
  // Function to insert <br>s for newlines
  function nl2br (str, is_xhtml) {
    var breakTag = (is_xhtml || typeof is_xhtml === 'undefined') ? '<br />' : '<br>';
    return (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1'+ breakTag +'$2');
  };

  // (Evil) function to prepare markup for PDF export
  app.makeMarkup  = function() {

    $("#markup").val("");
    $("#markup").val($("#markup").val()+"<table id=\"header\"><tr><td><h1 id=\"company\" class=\"left\">"+$("#company").val()+"</h1></td><td><h1 id=\"title\" class=\"right\">"+$("#title").val()+"</tr><tr id=\"line1\"><td><p class=\"left\">"+$("#address input:nth-child(1)").val()+"<br>"+$("#address input:nth-child(2)").val()+"<br>"+$("#address input:nth-child(3)").val()+"</p><p style=\"margin-top:15px;\" class=\"left\">"+$("#address input:nth-child(4)").val()+"<br>"+$("#address input:nth-child(5)").val()+"</p></td><td><p class=\"right\">"+$("#meta input:nth-child(1)").val()+"<br>"+$("#meta input:nth-child(2)").val()+"<br>"+$("#meta input:nth-child(3)").val()+"</p></p><p id=\"client\" class=\"right\" style=\"margin-top:12px;\"><b>"+$("#meta input:nth-child(4)").val()+"<br>"+$("#meta input:nth-child(5)").val()+"</b></p></td></tr></table></div><div id=\"text1\"><p>"+nl2br($("#textone:not(.growfieldDummy)").val())+"</p></div><table id=\"data\"><tr><th style=\"width:50px\">"+$("thead th:nth-child(1) input").val()+"</th><th style=\"width:313px;\">"+$("thead th:nth-child(2) input").val()+"</th><th style=\"width:100px;\">"+$("thead th:nth-child(3) input").val()+"</th><th style=\"width:100px;\">"+$("thead th:nth-child(4) input").val()+"</th><th style=\"width:100px;\">"+$("thead th:nth-child(5) input").val()+"</th></tr>");

    var i = 0;
    $("#task-list tr").each(function() {
      var s = "";
      if (i % 2 === 0 ){
        s = "tint";
      };
      if (i>$('#task-list tr').length){
        return;
      } else if (i>=0) {
        $("#markup").val($("#markup").val()+"<tr class=\"" + s + "\"><td>"+$(this).find("td:nth-child(1)").text()+"</td><td>"+$(this).find("td:nth-child(2) input").val()+"</td><td>"+$(this).find("td:nth-child(3) input").val()+"</td><td>"+$(this).find("td:nth-child(4) input").val()+"</td><td>"+$(this).find("td:nth-child(5)").text()+"</td></tr>");
      };
      i = i + 1;
    });

    $("#markup").val($("#markup").val()+"<tr><th style=\"border-top: 1px solid #bbb;\" colspan=\"4\">"+$("#subtotallabel input").val()+"</th><th style=\"border-top: 1px solid #bbb;\" id=\"formsubtotal\">"+$("#formsubtotal").text()+"</th></tr><tr><th id=\"taxrate\" colspan=\"4\">"+$("#taxrate input").val()+"</th><th id=\"formtax\">"+$("#formtax").text()+"</th></tr><tr id=\"total\"><th colspan=\"4\">"+$("#totallabel input").val()+"</th><th id=\"formtotal\">"+$("#formtotal").text()+"</th></tr></table><div id=\"text2\"><p>"+nl2br($("#texttwo:not(.growfieldDummy)").val())+"</p></div>");


    $("#markup").val($("#markup").val().replace(/€/g, "&euro;"));

  }

});
