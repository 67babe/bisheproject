function keepDouble(x) {
    return(x<10)?"0"+x:x;
}
function showDate() {
    var xDate = new Date();
    var xYear = keepDouble(xDate.getFullYear());
    var xMonth = keepDouble(xDate.getMonth()+1);
    var xDay = keepDouble(xDate.getDate());
    var xWeek = xDate.getDay();
    var week = ["日","一","二","三","四","五","六"];
    var xHour = keepDouble(xDate.getHours());
    var xMinute = keepDouble(xDate.getMinutes());
    var xSecond = keepDouble(xDate.getSeconds());
    var string = "";
    string = "📅"+xYear+"/"+xMonth+"/"+xDay+"&nbsp;&nbsp;"+"🕘"+xHour+":"+xMinute+":"+xSecond+"";
    document.getElementById("showtime").innerHTML = string;
}
// window.onload=function(){
//
// }
window.onload=function(){
    window.setInterval(showDate,500);
    var wrap=document.getElementById("wrap");//getElementById() 方法可返回对拥有指定 ID 的第一个对象的引用。
    var pic =document.getElementById("pic").getElementsByTagName("li");
    var list=document.getElementById("list").getElementsByTagName("li");
    var index=0;
    var timer=null;
    timer=setInterval(autoPlay,2000);//计时器= set 时间间隔 (播放,2000);

    wrap.onmouseover=function(){
        clearInterval(timer);	//鼠标被移到元素之上 ；clearInterval() 方法可取消由 setInterval() 设置的 timeout。


    }
    wrap.onmouseout=function(){
        timer=setInterval(autoPlay,2000);//移走
    }

    for(var i=0;i<list.length;i++){
        list[i].onclick=function(){ //鼠标单击某个对象
            clearInterval(timer);
            index=this.innerText-1;

//							this是当前对象
            showPic(index);

        }
    }

    function autoPlay(){
        if(++index>=list.length)   index=0;
        showPic(index);
    }



    function showPic(curIndex){
        for(var i=0;i<list.length;i++){
            pic[i].style.display="none";//获取当前页面里面id为i的标签，改变该标签的样式，使其不显示。
            list[i].className="";
        }
        pic[curIndex].style.display="block"; //获取当前页面里面id为i的标签，改变该标签的样式，使其满眶显示。
        list[curIndex].className="on";
    }
}