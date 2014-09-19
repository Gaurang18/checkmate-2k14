function f1(){
var k=document.js1.n1.value;
var p=document.js1.p1.value;
if((k=="" || k==null) && (p!="" && p!=null))
{
alert("Enter the Username!");
}
if((p=="" || p==null)&& (k!="" && k!=null))
{
alert("Enter the Password!");
}

if((k=="" || k==null)&& (p=="" || p==null))
{
alert("All fields must  be filled out!");
}
}
