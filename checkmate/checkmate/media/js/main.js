var teamName = $('.fn').html();
var score = parseInt($('.topContainer1').html());
var level = parseInt(($('#levelBox').html()).substring(6));
var canUpgradeLevel = 0;
var questionsAttempted;
var flip = parseInt($('#numflip').html());
dipp=$('#numDoubleDip').html();
if(level>1)
{
	var doubleDip = parseInt(dipp.substring(dipp.indexOf(':')+1));
}
var presentQuestion;
var canUseDoubleDip = 0;
var canUseFlip = 0;
var flipUsed = 0;
var doubleDipUsed = 0;
var ddques=[];
var ddques2=[];


function changeLevel(level) {
	if(level == 1) {
		$('#levelBox').html('LEVEL 1');
		$('#levelBox').css({'background-color': '#e54444'});
	}
	if(level == 2) {
		$('#levelBox').html('LEVEL 2');
		$('#levelBox').css({'background-color': '#0e97a7'});
	}
}

function changeQuestion(num) {
	$('#numQuestion').html('Question '+num);
} 

function updateScore(current) {
    $scoreBox = $("#topContainer1");
    var onBoard = $scoreBox.text();
    if (onBoard > current) {
        var i = setInterval(function()
        {
            if (onBoard === current) {
                clearInterval(i);
                $scoreBox.css("color", "white");
            }
            else
            {
                onBoard--;
                $scoreBox.text(onBoard);
                if ($scoreBox.css("color") === "rgb(255, 255, 255)")
                    $scoreBox.css("color", "rgb(220, 22, 24)");
                else
                    $scoreBox.css("color", "white");
            }
        }, 10);
    }
    else if (onBoard < current) {
        console.log("green path");
        var i = setInterval(function()
        {
            if (onBoard === current) {
                clearInterval(i);
                $scoreBox.css("color", "white");
            }
            else
            {
                onBoard++;
                $scoreBox.text(onBoard);
                if ($scoreBox.css("color") === "rgb(255, 255, 255)")
                    $scoreBox.css("color", "rgb(135, 189, 0)");
                else
                    $scoreBox.css("color", "white");
            }
        }, 10);
    }
    if(onBoard<200){
    	$('#levelbtn').css('background', '#6e7a75');


    }
    else
    {
    	$('#levelbtn').css('background', 'rgb(55,123,205)');	
    }

}

function addflip() {
	if(flip > 0 && flipUsed == 0 && doubleDipUsed == 0
		) {
		flip -= 1;
		flipUsed = 1;
		$('#numflip').html(flip);
		$('#flipCheck').html('Using flip !')
	}
	else
		console.log('fail')
}

function addDoubleDip() {
	dds=$('#numDoubleDip').html();
	noofdoubledips=dds.substring(dds.indexOf(':')+1);
	//alert(noofdoubledips);
	if(noofdoubledips > 0 ) {
		noofdoubledips -= 1;
		doubleDipUsed = 1;
		// if(ddques.indexOf(presentQuestion)>-1){
			
		// }
		$('#useDoubleDip').prop('disabled',true);
		$('#useDoubleDip').css("background-color","#6e7a75");
		$('#doubleDipCheck').html('Using Double Dip !');
		ddques.push(presentQuestion);
		// else{
		// }
		
		$('#numDoubleDip').html("Available:"+noofdoubledips);
		
	}
	else
		//$("#useDoubleDip").css("background-color","#6e7a75");
		alert('Please buy power before using');
}

function buyLaterflip() {
	// if (score > 15) {
	// 	score -= 15;
	// 	flip++;
	// 	updateScore(score);
	// 	$('#numflip').html(flip);
	// }
	$.ajax({
			url : '/market/',
			type : "POST",
			data : $.param({ dd : 0, flip : 1, buy : 1 }),
			success : function(data) {
				if(data.status==0)
					alert("You don't have enough points!!");
				else {
					updateScore(data.score);
					$('#numflip').html("Available:"+data.flip);
					$('#numDoubleDip').html("Available:"+data.dd);
					flip=data.flip;
				}
				
			}
	});
}

function buyLaterDoubleDip() {
	// if (score > 15) {
	// 	score -= 15;
	// 	doubleDip++;
	// 	updateScore(score);
	// 	$('#numDoubleDip').html(doubleDip);
	// }
	dds=$('#numDoubleDip').html();
	noofdoubledips=parseInt(dds.substring(dds.indexOf(':')+1));
	noofdoubledips+=1;
	$.ajax({
			url : '/market/',
			type : "POST",
			data : $.param({ dd : 1, flip : 0, buy : 1 }),
			success : function(data) {
				if(data.status==0)
					alert("You don't have enough points!!");
				else {
					updateScore(data.score);
					$('#numflip').html("Available:"+data.flip);
					$('#numDoubleDip').html("Available:"+noofdoubledips);
					doubleDip=data.dd;
				}
				
			}
	});
}
function useFlip(){
	flp=$('#numflip').html();
	cqno=flp.substring(flp.indexOf(':')+1);
	// alert(cqno);
	if (cqno < 1)
	{
		alert('Please buy power before using');
	}
	else{
	$.ajax({
			url : '/question/',
			type : "POST",
			data : $.param({ flip : 1 , no : presentQuestion }),
			success : function(data) {
				if(data.status==1){
					var qno=data.qno;
					//Salert("sd");
					$('#ques'+qno).trigger("click");
				}
				cqno--;
				$("#numflip").html("Available:"+cqno);
				
				$('#useflip').prop('disabled', true);
				$("#useflip").css("background-color","#6e7a75");
			}

		});
	

}
}


$('#useflip').click(function() {

	//ajax request !
	// if(parseInt($("numflip").html())>0){
		if(confirm("Do you really want to flip this ques???")){
				useFlip();
			}
	// }
});

$('#useDoubleDip').click(function() {
	//ajax request !
	// if(ddques.indexOf(presentQuestion)>-1)
	// 	alert("u can't");
	// else
		addDoubleDip();
});

$('#buyflip').click(function() {
	//ajax request !
	buyLaterflip();
});

$('#buyDoubleDip').click(function() {
	//ajax request !
	buyLaterDoubleDip();
});


$('.qButton').click(function() {
	var attempted = $(this).hasClass('nonClickableQuestion');
	var queriedFor = parseInt($(this).html().substring(1));
	if(!attempted) {
		$.ajax({
			url : '/question/',
			type : "GET",
			data : $.param({ no : queriedFor }),
			success : function(data) {
				if(data.status == 1)
					$('#numQuestion').html('Question '+queriedFor);
					$('#IOContent').html(data.content);
					presentQuestion = queriedFor;
					canUseDoubleDip = data.cdd;
					if(data.cflip == 0){
						$("#useflip").css("background-color","#6e7a75");
						$('#useflip').prop('disabled', true);
					}
					if (data.cflip == 1){
						$("#useflip").css("background-color","#238dd0");
						$('#useflip').prop('disabled',false);	
					}
					if(data.cdd == 0 && level == 2 && ddques2.indexOf(queriedFor) == -1 ){
						ddques2.push(queriedFor);
					}
					if(ddques.indexOf(queriedFor)>-1){
						$("#useDoubleDip").css("background-color","#6e7a75");
						$('#useDoubleDip').prop('disabled',true);
						$('#doubleDipCheck').html('Using Double Dip !');
					}
					if(ddques2.indexOf(queriedFor)>-1)

					{
						$("#useDoubleDip").css("background-color","#6e7a75");
						$('#useDoubleDip').prop('disabled',true);
						$('#doubleDipCheck').html('Second Attempt !!');
					}
					else{
						$("#useDoubleDip").css("background-color","#238dd0");
						$('#useDoubleDip').prop('disabled',false);
						$('#doubleDipCheck').html('');
					}
				


			}

		});
	}
});

$('#answerSubmit').click(function() {
	
	var ans = $('#answerBox').val();
	// var ddu = (doubleDipUsed==0)?false:true;
	var ddu='False';
	$('#answerBox').val("");
	if(ddques.indexOf(presentQuestion)>-1)
	{
		ddques.splice(ddques.indexOf(presentQuestion),1);
		ddu='True';
	}
	if(ddques2.indexOf(presentQuestion)>-1)
	{
		ddques2.splice(ddques2.indexOf(presentQuestion),1);
		
	}
	
	
	$.ajax({
		url : '/question/',
		type : "POST",
		data : $.param({ answer : ans, no : presentQuestion, dd : ddu }),
		success : function(data) {
				$("#answerBox").focus(function() {
    				$(this).attr("placeholder","Your answer here");
				});
			if(data.status==1||data.status==0){
				var quesno=data.qno;
				updateScore(data.score);
				$('#ques'+quesno).addClass('nonClickableQuestion');
			}


			if(data.status==1 && data.score>=200){
				$('#levelbtn').attr('disabled',false);
			}

			if(data.score<200){
				$('#levelbtn').attr('disabled',true);
			}
			
			$("#numQuestion").html("Select another question");
			// document.getElementById("answerBox").defaultValue="ur answer here";
			$("answerBox").text("");
			$('#IOContent').html('');
			$('#doubleDipCheck').html('');
		
			if(data.status==2){
				// document.getElementById("answerBox").defaultValue="ur answer here";
				updateScore(data.score);
				$('#ques'+presentQuestion).trigger("click");
			}
		}
	
	});	
	
});
$('#answerBox').bind("enterKey",function(e){
   //do stuff here
   var ans = $('#answerBox').val();
   $('#answerBox').val("");

	// var ddu = (doubleDipUsed==0)?false:true;
	var ddu='False';
	if(ddques.indexOf(presentQuestion)>-1)
	{
		ddques.splice(ddques.indexOf(presentQuestion),1);
		ddu='True';
	}
	if(ddques2.indexOf(presentQuestion)>-1)
	{
		ddques2.splice(ddques2.indexOf(presentQuestion),1);
		
	}
	$.ajax({
		url : '/question/',
		type : "POST",
		data : $.param({ answer : ans, no : presentQuestion, dd : ddu }),
		success : function(data) {
			if(data.status==1||data.status==0){
				var quesno=data.qno;
				updateScore(data.score);
				$('#ques'+quesno).addClass('nonClickableQuestion');
			


			if(data.status==1 && data.score>=200){
				$('#levelbtn').css('background', 'rgb(55,123,205)');
				$('#levelbtn').attr('disabled',false);
			}

			if(data.score<200){
				$('#levelbtn').attr('disabled',true);
			}
			
			$("#numQuestion").html("Select another ques");
			document.getElementById("answerBox").defaultValue="ur answer here";
			$("answerBox").text("");
			$('#IOContent').html('');
			$('#doubleDipCheck').html('');
		}
		if(data.status==2){
			document.getElementById("answerBox").defaultValue="ur answer here";
			updateScore(data.score);
			$('#ques'+presentQuestion).trigger("click");
		}
		}
	
	});	



    });
	$('#answerBox').keyup(function(e){
    if(e.keyCode == 13)
    {
        $(this).trigger("enterKey");
    }
	});
$('#levelbtn').click(function(){
	if(confirm("Do you really want to go to the next level??")){
	$.ajax({
		url : '/transition/',
		type : "POST",
		success : function(data) {
			if(data.status==1){
				$('.blackout').css('display','block');
				$('.blackoutContent').css('display','block');
			}
		}
	});
}
});
$('#marketSubmit').click(function(){
	var ddr=$('#doubledip').val();
	var flipr=$('#flip').val();
	$.ajax({
			url : '/market/',
			type : "POST",
			data : $.param({ dd : ddr, flip : flipr, buy : 1 }),
			success : function(data) {
				if(data.status==0)
					alert("You don't have enough points!!");
				else {
						//empty the array again
					window.location.href = "/";
				}
				
			}
	});
});
