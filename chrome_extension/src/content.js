
import Vue from 'vue'
import App from './App.vue'

// console.log("Extension loaded!");
var color = ["red", "orange", "yellow", "olive", "green"];


function get_set_score(n){
	// console.log("Get score");
	var url = "https://meichu2017-determinatioanima.c9users.io/";

	/* Get score */

	$.get(url, function(res, status){
		//console.log(JSON.parse(res));
		var parsed_res  = JSON.parse(res);
		$.get(url + "gmail_score/" + parsed_res["messages"][n]["id"], function(data1, status){
			// console.log("N: " + n + "\nData: " + data + "\nStatus: " + status);
			/* Set score */
			var elements = $(".zA");
			var score = data1["score"];
			var score_div = $("<td></td>").addClass("SCORE").append(
				$("<div></div>").addClass("ui tiny statistics label").append(
					$("<div></div>").addClass(color[Math.floor((score -1 )/ 2) ] + " statistic").append(
						$("<div></div>").addClass("value").text(score.toString())
					)
				)
			);
			score_div.appendTo(elements[n]);
		});
	});
}

/* Score */
var checkExist = setInterval(function() {
	var elements = $(".zA");
	if (elements.length) {
		// console.log("Exists!");
		clearInterval(checkExist);
		for (var i = 0;i < elements.length; i++)
			get_set_score(i);
	}
}, 100);

/* ON/OF button */
var checkExist2 = setInterval(function() {
	var head = $(".gb_zc.gb_yg.gb_R");
	if(head.length){
		// console.log("Exists2!");
		clearInterval(checkExist2);
		var side_bar_div = $("<div></div>").addClass("ui toggle checkbox");
		var side_bar = $("<input>").attr("type", "checkbox").attr("id","SIDE_BAR").attr("checked",true);
		side_bar.change(function() {
			if(this.checked) {
					$(".SCORE").show();
			}
			else {
					$(".SCORE").hide()
			}
		});
		side_bar_div.append(side_bar);
		side_bar_div.append($("<label></label>").text("On/Off"));
		head.prepend(side_bar_div);
	}
}, 100);


/* Report Button*/
var checkExist3 = setInterval(function(){
	var element = $(".ha");
	var report = $(".ha > .REPORT_BUTTON");
	// console.log(report.length);
	if(element.length && report.length == 0){
		var report = $("<button></button>").addClass("ui red button").addClass("REPORT_BUTTON").text("Report");
		report.click(function() {
			$('.first.modal').modal('show');
		});
		$(".SEND").click(function(){
			$('.first.modal').modal('hide');
			$('.second.modal').modal('show');
			var url = "https://meichu2017-determinatioanima.c9users.io/payback/junk";
			$.post(url, { level: "High", often: "Once a week",category:"Normal" })
			.done(function(res, status){
				console.log("payback success");
			});
		});
		$(".CANCEL").click(function(){
			$('.first.modal').modal('hide');
		});
		$(".OK").click(function(){
			$('.second.modal').modal('hide');
		});

		element.append(report);
	}
	if($("#SIDE_BAR").is(":checked"))
		$(".REPORT_BUTTON").show();
	else
		$(".REPORT_BUTTON").hide();
}, 100);

function set_info(res){

	// console.log("here");
	var element = $(".ha");
	if($(".INFO_BUTTON").length == 0){
		var info = $("<button></button>").addClass("INFO_BUTTON").addClass("ui primary basic button").text("More Info").click(function(){
				$('#INFO').modal('show');
		});
		$("#PSCORE").text(res["score"]);
		if(res["spf_score"] == 1)
			$("#PSPF").text("YES");
		else
			$("#PSPF").text("NO");

		if(res["dkim_score"] == 1)
			$("#PDKIM").text("YES");
		else
			$("#PDKIM").text("NO");

		if (res["dmarc_score"] == 1)
			$("#PDMARC").text("YES");
		else
			$("#PDMARC").text("NO");

		if(res["file_exist"] == 1)
			$("#PATTACHED").text("YES");
		else
			$("#PATTACHED").text("NO");

		if(res["result_NB"] == "ham")
			$("#PCONTENT").text("安全");
		else
			$("#PCONTENT").text("可疑");

		element.append(info);
	}
}

var checkExist5 = setInterval(function(){
	if($("#SIDE_BAR").is(":checked")){
		var elements = $(".gs a");
		var info_btn = $(".INFO_BUTTON");
		if(elements.length){
			if($(".INFO_BUTTON").length == 0){
				var href = location.href.split('/');
				var last = href[href.length-1];
				var url = "https://meichu2017-determinatioanima.c9users.io/";
				$.get(url+"gmail_score/"+last,function(res,code){
					console.log(res);
						set_info(res);
				});
			}
		}
	}
}, 500);

/* Sean */
var loadUrl = true;
var turnOn = false;
var checkExist6 = setInterval(function() {
	if($("#SIDE_BAR").is(":checked")){
		var elements = $(".gs a");
		if (elements.length  ) {
			// console.log('#C');
			if(loadUrl === true) {
				// console.log('#D');
				var href = location.href.split('/');
				var last = href[href.length-1];
				if(last.length == 16 ){
					// console.log('pass');
				}
				else {
					// console.log('fail');
					return;
				}

				// console.log(/^https:\/\/maisl.google.com\/mail\/u\/[0-9]\/#inbox/.test(location.href));
				loadUrl = false;
				// console.log("Exists!");
				var i;
				var oriText=[];
				var covText=[];
				// console.log(elements);
				for (i = 0;i < elements.length; i++) {
					$(elements[i]).addClass(`url_${i}`);
					$(`.url_${i}`).css('border','3px solid red');
					$(`.url_${i}`).attr('oriText',`${$(`.url_${i}`).text()}`);
					$(`.url_${i}`).attr('covText',`${$(`.url_${i}`).attr('href')}`);
					$(`.url_${i}`).hover(function(){
						$(this).text($(this).attr('covtext'));
					}, function(){
						$(this).text($(this).attr('oriText'));
					});
				}
			//   console.log(covText);
			}
		}
		$('.INFO_BUTTON').show();
	}
	else {
		loadUrl = true;
		$('a').css('border','3px none red');
		$('a').unbind('mouseenter mouseleave');
		$('.INFO_BUTTON').hide();
	}
}, 200);

$(window).on('hashchange', function(e){
	if ($("#SIDE_BAR").is(":checked")){
		loadUrl = true;
	}
});

var initDom = document.createElement("div");
initDom.id = "extensionUIwrap";

document.getElementsByTagName("body")[0].appendChild(initDom);

new Vue({
  el: '#extensionUIwrap',
  render: h => h(App)
})
