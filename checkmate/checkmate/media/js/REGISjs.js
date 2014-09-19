function f1(){
 
var u=document.form1.n.value;
var k=document.form1.nam.value;
var m=document.form1.mail.value;
var l=document.form1.no.value;
var k1=document.form1.n1.value;
var m1=document.form1.mail1.value;
var l1=document.form1.no1.value;
var pw=document.form1.pwd.value;
// var cpw=document.form1.cpwd.value;
//checking for empty space
if(u==null || u=="")
{
alert("Username must be filled out!");
return 0;
}
if(pw==null || pw==""){
alert("Password must be filled out!");
return 0;
}
if(k==null || k==""){
alert("Name of participant 1 mandatory!");
return 0;
}
if(m==null || m==""){
alert("Email of participant 1 mandatory!");
return 0;
}
if(l==null || l==""){
alert("Phone No. of participant 1 mandatory!");
return 0;
}
//NAME VALIDATION
var letter = /^[A-Za-z ]+$/;
if(!letter.test(k))
{
alert("Name must have alphabet characters only");
}
if(k1!=""){

	
	if(!letter.test(k1))
	{
		alert("Name must have assslphabet characters only");
	}  
}
  // if(pw!=cpw){
  // 	alert("password enetered in both the fields must be same");
  // }

//email validation
   
var mailvalidate=/^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})+$/;
if(!mailvalidate.test(m))
{
alert("invalid email");
}
if(m1!=""){
	if(!mailvalidate.test(m1))
	{
		alert("invalid email");
	}
}

//number validation
if(isNaN(document.form1.no.value)==true)
{
alert("Enter a valid number");
}
if(isNaN(document.form1.no1.value)==true)
{
alert("Enter a valid number");
}

}