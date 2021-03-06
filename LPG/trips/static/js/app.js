const metas = document.getElementsByTagName('meta');
 for (let i = 0; i < metas.length; i++) {
    if (metas[i].getAttribute('property') === "og:url") {
        metas[i].setAttribute('content', window.location.href);
    }
}

function getRandom(min,max){
    return Math.floor(Math.random()*(max-min+1))+min;
};

Array.prototype.nthIndexOf = function(e, n) {
    var index = -1;
    for (var i = 0, len = this.length; i < len; i++) {
        if (i in this && e === this[i] && !--n) {
            index = i;
            break;
        }
    }
    return index;
};

//title author publisher callnumber ISBN picturename
function addElement (newContent) {
  // create a new div element
  // and give it some content
  var newDiv = document.createElement("div");
  newDiv.appendChild(newContent); //add the text node to the newly created div.
}

function start() {
    document.getElementById("start_page").style.display = "none";
    document.getElementById("test_page").style.display = "grid";
};

function submit() {
    var result;
    var i = getScore();
    if (i.nthIndexOf(Math.max(...i),2) === -1){
        result = i.indexOf(Math.max(...i))+1
    } else {
        console.log("同類");
        bool = getRandom(0,1);
        if (bool === 0){
            result = i.indexOf(Math.max(...i))+1;
        } else {
            result = (i.nthIndexOf(Math.max(...i),2))+1;
        }
    }
    const csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();

    document.getElementById("test_page").style.display = "none";
    document.getElementById("result_page").style.display = "block";

    const url = window.location.href.replace("app/","process_result_from_client/")
    $.ajax({
        type: 'POST',
        url: url,
        dataType: "html",
        data: {
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
            'result': result
            },
        success: function(res) {
            console.log("Successfully sent the URL to Django");
            $('#result_page').html(res);
                (function(d, s, id) {
                        var js, fjs = d.getElementsByTagName(s)[0];
                        if (d.getElementById(id)) return;
                        js = d.createElement(s); js.id = id;
                        js.src = "https://connect.facebook.net/zh_TW/sdk.js#xfbml=1&version=v3.0";
                        fjs.parentNode.insertBefore(js, fjs);
                    }(document, 'script', 'facebook-jssdk'));

                
        },
        error: function(xhr,errmsg,err){
            console.log("Could not send URL to Django. Error: " + xhr.status + ": " + xhr.responseText);
            console.log('error', err);
        }
    })
};

var test_index = 0;

function getScore(){
    if (document.getElementsByClassName("quiestion")[test_index].hidden == false) {
        var name = document.getElementsByClassName("quiestion")[test_index].children[2].children[0].name;
    }

    var i1 = 0;
    var i2 = 0;
    var i3 = 0;
    var i4 = 0;
    var choice_num = document.querySelectorAll('#test').length;
    var v = $("input[name="+name+"]").is(":checked");
    if (v) {
        for (var i = 0; i < choice_num; i++) {
            obj = document.querySelectorAll('#test')[i];
            if (obj.checked == true){
                res = [obj.value];
                if (obj.value.length > 1){
                    var res = res[0].split(", ");
                }
                if (res.includes("1")){
                    i1+=1;
                } 
                if (res.includes("2")){
                    i2+=1;
                }
                if (res.includes("3")){
                    i3+=1;
                }
                if (res.includes("4")){
                    i4+=1;
                }
            }
        }
        return [i1,i2,i3,i4];
    }
};